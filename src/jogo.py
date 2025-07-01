from tabuleiro import Tabuleiro, Cidade
from states import GameOverState, SetupState
from utils import CorDoenca
from colorama import Fore, Back, Style
from collections import deque

class PandemicGame:
    """Singleton, Facade e Controller do jogo."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._inicializado = False
        return cls._instance

    def __init__(self):
        if self._inicializado:
            return
        self.tabuleiro = Tabuleiro()
        self.jogadores = []
        self.baralho_jogador = None
        self.baralho_infeccao = None
        self.estoque_cubos = {c: 24 for c in CorDoenca}
        self.curas_descobertas = {c: False for c in CorDoenca}
        self.doencas_erradicadas = {c: False for c in CorDoenca}
        self._trilha_taxa_infeccao = [2, 2, 2, 3, 3, 4, 4]
        self._indice_taxa_infeccao = 0
        self.turno_atual = 0
        self.estado = SetupState(self)
        self.rodando = True
        self.taxa_infeccao = self._trilha_taxa_infeccao[self._indice_taxa_infeccao]
        self.outbreaks = 0

        self._inicializado = True


    def definir_estado(self, novo_estado):
        self.estado = novo_estado

    def run(self):
        print(f"\n{Back.WHITE}{Fore.BLACK}=== PANDEMIC ==={Style.RESET_ALL}")
        while self.rodando:
            self.estado.manusear()

    def resolver_epidemia(self):
        """Orquestra os 3 passos de uma epidemia."""
        print(f"\n{Back.RED}{Fore.WHITE}=== EPIDEMIA! ==={Style.RESET_ALL}")
        
        # Passo 1: Aumentar
        self._aumentar_taxa_infeccao()
        
        # Passo 2: Infectar
        self._fase_infeccao_epidemia()
        
        # Passo 3: Intensificar
        self._intensificar_infeccoes()
        
        print(f"{Back.RED}{Fore.WHITE}=== FIM DA EPIDEMIA ==={Style.RESET_ALL}")

    def _aumentar_taxa_infeccao(self):
        """Avança o marcador da taxa de infecção."""
        print("Passo 1 (Aumentar): A taxa de infecção aumentou!")
        self._indice_taxa_infeccao += 1
        self.taxa_infeccao = self._trilha_taxa_infeccao[self._indice_taxa_infeccao]
        print(f"Nova taxa de infecção: {self.taxa_infeccao}")

    def _fase_infeccao_epidemia(self):
        """Puxa a carta do fundo do baralho de infecção e adiciona 3 cubos."""
        print("Passo 2 (Infectar): Uma cidade será fortemente infectada.")
        carta = self.baralho_infeccao.comprar_do_fundo()
        if not carta: return

        print(f"A cidade sorteada foi: {carta.cor.cor_terminal}{carta.nome}{Style.RESET_ALL}")
        cidade = self.tabuleiro.obter_cidade(carta.nome)

        # Adiciona 3 cubos da cor da carta, a menos que a doença já esteja erradicada
        # (A lógica de erradicação pode ser adicionada depois)
        for _ in range(3):
            cidade.adicionar_cubo(carta.cor, self.jogadores, self)

        self.baralho_infeccao.adicionar_ao_descarte(carta)

    def _intensificar_infeccoes(self):
        """Reembaralha o descarte de infecção e o coloca no topo do baralho."""
        print("Passo 3 (Intensificar): As cidades recém-infectadas voltarão em breve...")
        self.baralho_infeccao.reembaralhar_descarte_no_topo()

    def infeccao_inicial(self):
        """Infecção inicial do tabuleiro."""
        print(f"\n{Back.WHITE}{Fore.BLACK}--- Infecção Inicial ---{Style.RESET_ALL}")
        try:
            print("--- Cidades com 3 cubos ---")
            # 3 cidades com 3 cubos
            for _ in range(3):
                carta = self.baralho_infeccao.comprar()
                cidade = self.tabuleiro.obter_cidade(carta.nome)
                for _ in range(3):
                    cidade.adicionar_cubo(cidade.cor, self.jogadores, self)
            
            print("\n--- Cidades com 2 cubos ---")
            # 3 cidades com 2 cubos
            for _ in range(3):
                carta = self.baralho_infeccao.comprar()
                cidade = self.tabuleiro.obter_cidade(carta.nome)
                for _ in range(2):
                    cidade.adicionar_cubo(cidade.cor, self.jogadores, self)

            print("\n--- Cidades com 1 cubo ---")
            # 3 cidades com 1 cubo
            for _ in range(3):
                carta = self.baralho_infeccao.comprar()
                cidade = self.tabuleiro.obter_cidade(carta.nome)
                cidade.adicionar_cubo(cidade.cor, self.jogadores, self)
        except AttributeError:
            print("ERRO: Baralho de infecção não foi configurado corretamente.")
        print("------------------------")

    def mostrar_mapa(self):
        """Exibe o mapa com cores e contagem de cubos no terminal."""
        print(f"\n{Back.WHITE}{Fore.BLACK}--- MAPA GLOBAL ---{Style.RESET_ALL}")
        
        # ... (legenda)
        print("-" * 70)
        
        cidades_ordenadas = sorted(self.tabuleiro.cidades.values(), key=lambda c: c.nome)
        for cidade in cidades_ordenadas:
            cor_cidade_nativa = cidade.cor.cor_terminal
            
            marcadores_coloridos = []
            marcadores_sem_cor = []
            for cor, quantidade in cidade.cubos.items():
                if quantidade > 0:
                    asteriscos = '*' * quantidade
                    marcadores_coloridos.append(f"{cor.cor_terminal}{asteriscos}{Style.RESET_ALL}")
                    marcadores_sem_cor.append(asteriscos)
            
            marcador_str_colorido = f"{Style.RESET_ALL}[{''.join(marcadores_coloridos)}]" if marcadores_coloridos else ""
            marcador_str_sem_cor = f" [{''.join(marcadores_sem_cor)}]" if marcadores_sem_cor else ""

            nome_com_cubos_colorido = f"{cidade.nome}{marcador_str_colorido}"
            nome_com_cubos_sem_cor = f"{cidade.nome}{marcador_str_sem_cor}"

            largura_desejada = 30
            padding = ' ' * (largura_desejada - len(nome_com_cubos_sem_cor))

            vizinhos_formatados = [f'{v.cor.cor_terminal}{v.nome}{Style.RESET_ALL}' for v in cidade.vizinhos]
            print(f"{cor_cidade_nativa}• {nome_com_cubos_colorido}{padding} → {', '.join(vizinhos_formatados)}")
        
        print("-" * 70)

    def iniciar_surto(self, cidade_origem: Cidade, cor_do_surto):
        """Gerencia a lógica de surto, incluindo reações em cadeia."""
        fila_de_surtos = deque([cidade_origem])
        cidades_ja_surtaram = {cidade_origem}

        print(f"{Fore.RED}ALERTA: Surto iniciado em {Style.RESET_ALL}{cidade_origem.cor.cor_terminal}{cidade_origem.nome}!{Style.RESET_ALL}")

        while fila_de_surtos:
            cidade_atual = fila_de_surtos.popleft()

            self.outbreaks += 1
            if self.outbreaks >= 8:
                print("FIM DE JOGO: O número máximo de surtos foi atingido! Derrota!")
                self.rodando = False
                self.definir_estado(GameOverState(self))
                return
            
            for vizinho in cidade_atual.vizinhos:
                print(f"  -> Surto se espalhando para {vizinho.cor.cor_terminal}{vizinho.nome}{Style.RESET_ALL}...")
                
                # Se o vizinho já surtou NESTA CADEIA, ele não recebe mais cubos.
                if vizinho in cidades_ja_surtaram:
                    continue

                # Se o vizinho já tem 3 cubos, ele também vai surtar.
                # Adicionamos ele na fila para ser processado e no set de controle.
                if vizinho.cubos[cor_do_surto] == 3:
                    cidades_ja_surtaram.add(vizinho)
                    fila_de_surtos.append(vizinho)
                # Caso contrário, ele apenas recebe um cubo.
                else:
                    vizinho.adicionar_cubo(cor_do_surto, self.jogadores, self)

    def verificar_erradicacao(self, cor: CorDoenca):
        """
        Verifica se uma doença pode ser marcada como erradicada.
        Isso deve ser chamado sempre que um cubo é removido do tabuleiro.
        """
        # Condição 1: A cura para esta doença já foi descoberta?
        if not self.curas_descobertas.get(cor):
            return # Se não há cura, não pode haver erradicação.

        # Condição 2: Ainda existe algum cubo desta cor no tabuleiro?
        for cidade in self.tabuleiro.cidades.values():
            if cidade.cubos[cor] > 0:
                return # Encontrou um cubo, então não está erradicada.

        # Se o código chegou até aqui, ambas as condições foram atendidas!
        # Apenas se ainda não foi erradicada, para não exibir a mensagem toda vez.
        if not self.doencas_erradicadas[cor]:
            self.doencas_erradicadas[cor] = True
            cor_str = f"{cor.cor_terminal}{cor.name}{Style.RESET_ALL}"
            print(f"\n{Fore.CYAN}{Style.BRIGHT}DOENÇA {cor_str} FOI ERRADICADA! Cubos desta cor não serão mais colocados no tabuleiro.{Style.RESET_ALL}")

    def mostrar_estado_jogadores(self):
        print(f"\n{Back.WHITE}{Fore.BLACK}--- POSIÇÃO DOS JOGADORES ---{Style.RESET_ALL}")
        for jogador in self.jogadores:
            print(jogador)
        print("----------------------------")
    
    def obter_jogador_atual(self):
        return self.jogadores[self.turno_atual]

    def proximo_turno(self):
        self.turno_atual = (self.turno_atual + 1) % len(self.jogadores)