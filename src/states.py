import random
from abc import ABC, abstractmethod
from utils import CARTAS_EPIDEMIA, PAPEIS_JOGO, CorDoenca
import papeis as classes_papeis
from jogador import Jogador
from cartas import CartaEpidemia, CartaJogador, CartaInfeccao, Deck
from commands import CompartilharConhecimentoCommand, ConstruirEstacaoCommand, DescobrirCuraCommand, MoverCommand, PonteAereaCommand, TratarDoencaCommand, VooDiretoCommand, VooFretadoCommand
from colorama import Fore, Style

""""Classes que representam os estados do jogo, seguindo o padrão State."""

class GameState(ABC):
    def __init__(self, jogo):
        self.jogo = jogo
    @abstractmethod
    def manusear(self):
        pass

class SetupState(GameState):
    def manusear(self):
        print("--- Configurando a Partida ---")
        self._configurar_jogadores()
        self._configurar_tabuleiro_e_baralhos()
        self.jogo.infeccao_inicial()
        self.jogo.definir_estado(PlayerTurnState(self.jogo))

    def _configurar_jogadores(self):
        num = 0
        while num not in [2, 3, 4]:
            try:
                num = int(input("Quantos jogadores? (2-4): "))
            except ValueError:
                print("Número inválido.")
        
        nomes_papeis = list(PAPEIS_JOGO.values())
        papeis_sorteados = random.sample(nomes_papeis, num)
        
        for i in range(num):
            while True:
                nome = input(f"Nome do jogador {i+1}: ").strip()
                nome_existente = any(jogador.nome.lower() == nome.lower() for jogador in self.jogo.jogadores)
            
                if not nome:  # Verifica se o nome não está vazio
                    print("O nome não pode ser vazio. Por favor, digite um nome válido.")
                elif nome_existente:
                    print("Já existe um jogador com esse nome. Por favor, escolha outro.")
                else:
                    break  # Sai do loop quando o nome for válido

            nome_classe_papel = papeis_sorteados[i]
            classe_papel = getattr(classes_papeis, nome_classe_papel)
            jogador = Jogador(nome, classe_papel())
            self.jogo.jogadores.append(jogador)
            print(f"Jogador {jogador.nome} é um(a) {jogador.papel.nome}.")

    def _configurar_tabuleiro_e_baralhos(self):
        cidade_inicial = self.jogo.tabuleiro.obter_cidade("Atlanta")
        cidade_inicial.construir_estacao()

        for p in self.jogo.jogadores:
            p.definir_localizacao(cidade_inicial)

        # PASSO 1: Preparar e embaralhar TODAS as cartas de cidade
        cartas_jogador_cidades = [CartaJogador(c.nome, c.cor) for c in self.jogo.tabuleiro.cidades.values()]
        random.shuffle(cartas_jogador_cidades)

        # PASSO 2: Distribuir as mãos iniciais PRIMEIRO, usando apenas as cartas de cidade
        print("\n--- Distribuindo Mãos Iniciais ---")
        cartas_por_jogador = {2: 4, 3: 3, 4: 2}[len(self.jogo.jogadores)]
        for p in self.jogo.jogadores:
            for _ in range(cartas_por_jogador):
                # Pega a carta do topo do monte embaralhado e dá ao jogador
                carta_inicial = cartas_jogador_cidades.pop(0)
                p.adicionar_carta(carta_inicial)
            # Mostra a mão inicial de cada jogador
            # cartas_str = ", ".join([f"{c.cor.cor_terminal}{c.nome}{Style.RESET_ALL}" for c in p.mao])
            # print(f"Mão de {p.nome}: [{cartas_str}]")

        # PASSO 3: Preparar o baralho de jogo com as cartas restantes e as epidemias
        cartas_restantes_para_o_baralho = cartas_jogador_cidades # O que sobrou após distribuir as mãos

        # Pergunta a dificuldade (nº de epidemias)
        num_epidemias = 0
        while num_epidemias not in [4, 5, 6]:
            try:
                num_epidemias = int(input("\nQuantas cartas de Epidemia (dificuldade 4-Fácil, 5-Normal, 6-Difícil)? "))
            except ValueError:
                print("Número inválido.")

        # Divide o baralho RESTANTE, adiciona epidemias, embaralha os montes e junta tudo
        print(f"Preparando o baralho de compras com {num_epidemias} epidemias...")
        baralho_final = []
        
        # Garante que a divisão funcione mesmo que não seja perfeita
        lista_de_montes = []
        temp_cartas = list(cartas_restantes_para_o_baralho)
        for i in range(num_epidemias):
            monte = temp_cartas[i::num_epidemias] # Distribui as cartas entre os montes
            lista_de_montes.append(monte)

        for monte in lista_de_montes:
            monte.append(CartaEpidemia())
            random.shuffle(monte)
            baralho_final.extend(monte)
        
        # Embaralha a ordem dos próprios montes para uma aleatoriedade final
        random.shuffle(baralho_final)

        self.jogo.baralho_jogador = Deck(baralho_final)
        print(f"Baralho de compras pronto com {len(self.jogo.baralho_jogador.cartas)} cartas.")
        
        # PASSO 4: Configura o baralho de infecção (como antes)
        cartas_infeccao = [CartaInfeccao(c.nome, c.cor) for c in self.jogo.tabuleiro.cidades.values()]
        self.jogo.baralho_infeccao = Deck(cartas_infeccao)
        self.jogo.baralho_infeccao.baralhar()



class PlayerTurnState(GameState):
    def manusear(self):
        jogador_atual = self.jogo.obter_jogador_atual()
        jogador_atual.acoes_restantes = 4
        
        self.jogo.mostrar_mapa()
        self.jogo.mostrar_estado_jogadores()

        print("\n" + "="*50)
        print(f"TURNO DE: {jogador_atual.nome} ({jogador_atual.papel})")
        print("="*50)

        while jogador_atual.acoes_restantes > 0:
            comando = self._obter_comando_do_jogador(jogador_atual)
            
            if comando:
                comando.executar()
                if jogador_atual.acoes_restantes > 0:
                    self.jogo.mostrar_estado_jogadores()
            elif jogador_atual.acoes_restantes == 0:
                break
        
        print(f"\nFim do turno de {jogador_atual.nome}.")
        self.jogo.definir_estado(TurnTransitionState(self.jogo))

    def _obter_comando_do_jogador(self, jogador):
         
        print(f"\nAções restantes: {jogador.acoes_restantes}")
        print("Ações Normais: [1] Mover | [2] Tratar Doença | [3] Construir Estação | [4] Descobrir Cura | [5] Compartilhar Conhecimento")
        print("Ações de Voo:  [6] Voo Direto | [7] Voo Fretado | [8] Ponte Aérea")
        print("Outros:        [p] Passar | [m] Mapa")

        escolha = input("Escolha uma ação: ").lower().strip()

        if escolha == '1': # Mover
            vizinhos_coloridos = [f"{v.cor.cor_terminal}{v.nome}{Style.RESET_ALL}" for v in jogador.localizacao.vizinhos]
            print(f"Vizinhos: {', '.join(vizinhos_coloridos)}")
            nome_cidade = input("Mover para qual cidade? ").strip().title()
            cidade_destino = self.jogo.tabuleiro.obter_cidade(nome_cidade)
            if cidade_destino:
                return MoverCommand(jogador, cidade_destino, self.jogo)
            
        elif escolha == '2': # Tratar Doença
            cor_str = input("Tratar qual cor (AZUL, AMARELO, PRETO, VERMELHO)? ").upper().strip()
            try:
                cor = CorDoenca[cor_str]
                return TratarDoencaCommand(jogador, cor, self.jogo)
            except KeyError:
                pass

        elif escolha == '3': # Construir Estação
            return ConstruirEstacaoCommand(jogador, self.jogo)
            
        elif escolha == '4': # Descobrir cura
            cor_str = input("Descobrir cura de qual cor (AZUL, AMARELO, PRETO, VERMELHO)? ").upper().strip()
            try:
                cor = CorDoenca[cor_str]
                return DescobrirCuraCommand(jogador, cor, self.jogo)
            except KeyError:
                print(f"Cor '{cor_str}' inválida.")
                return None

        elif escolha == '5': # Compartilhar Carta
            nome_receptor = input("Dar carta para qual jogador? ")
            receptor = next((j for j in self.jogo.jogadores if j.nome.lower() == nome_receptor.lower()), None)
            if not receptor:
                print(f"Jogador '{nome_receptor}' não encontrado.")
                return None
            
            nome_carta = input("Qual carta de cidade? ").strip().title()
            return CompartilharConhecimentoCommand(jogador, receptor, nome_carta, self.jogo)
        
        elif escolha == '6': # Voo Direto
            print("Sua mão: " + ", ".join([f"{c.cor.cor_terminal}{c.nome}{Style.RESET_ALL}" for c in jogador.mao]))
            nome_carta = input("Usar qual carta de cidade para o Voo Direto? ").strip().title()
            carta_obj = next((c for c in jogador.mao if c.nome == nome_carta), None)
            if carta_obj:
                return VooDiretoCommand(jogador, carta_obj, self.jogo)
            else:
                print("Carta não encontrada na sua mão.")
                return None

        elif escolha == '7': # Voo Fretado
            nome_destino = input("Voar para qual cidade? ").strip().title()
            cidade_destino = self.jogo.tabuleiro.obter_cidade(nome_destino)
            if cidade_destino:
                return VooFretadoCommand(jogador, cidade_destino, self.jogo)
            else:
                print(f"Cidade '{nome_destino}' não encontrada.")
                return None

        elif escolha == '8': # Ponte Aérea
            nome_destino = input("Voar para qual Estação de Pesquisa? ").strip().title()
            cidade_destino = self.jogo.tabuleiro.obter_cidade(nome_destino)
            if cidade_destino:
                return PonteAereaCommand(jogador, cidade_destino, self.jogo)
            else:
                print(f"Cidade '{nome_destino}' não encontrada.")
                return None
        
        elif escolha == 'p':
            jogador.acoes_restantes = 0
            return None
        elif escolha == 'm':
            self.jogo.mostrar_mapa()
            self.jogo.mostrar_estado_jogadores()
            return None
            
        print("Comando inválido. Tente novamente.")
        return None
    
class TurnTransitionState(GameState):
    def manusear(self):
        print("\n" + "="*50)
        print("TRANSIÇÃO DE TURNO")
        print("="*50)

        self._comprar_cartas_de_jogador()
        if self.jogo.rodando:
            self._infectar_cidades()
            if self.jogo.rodando:
                self.jogo.proximo_turno()
                self.jogo.definir_estado(PlayerTurnState(self.jogo))

    def _comprar_cartas_de_jogador(self):
        jogador_atual = self.jogo.obter_jogador_atual()
        print(f"\n{jogador_atual.nome} está comprando 2 cartas de jogador...")
        
        cartas_compradas = 0
        while cartas_compradas < 2 and self.jogo.rodando:
            carta = self.jogo.baralho_jogador.comprar()
            if not carta:
                self.jogo.rodando = False
                print("FIM DE JOGO: O baralho de jogador acabou!")
                self.jogo.definir_estado(GameOverState(self.jogo))
                return

            # Se for uma Epidemia, resolva!
            if isinstance(carta, CartaEpidemia):
                print(f"{jogador_atual.nome} comprou uma Carta de Epidemia!")
                self.jogo.resolver_epidemia()
                # A carta de epidemia é removida do jogo, não vai para o descarte
            # Se for uma carta normal, adicione à mão do jogador
            else:
                jogador_atual.adicionar_carta(carta)
                cartas_compradas += 1
                print(f"{jogador_atual.nome} comprou a carta {carta.cor.cor_terminal}{carta.nome}{Style.RESET_ALL}.")
        
        # Lógica para limite de mão (geralmente 7 cartas)
        while len(jogador_atual.mao) > 7:
            print(f"\n{Fore.YELLOW}Atenção!{Style.RESET_ALL} {jogador_atual.nome} tem {len(jogador_atual.mao)} cartas e precisa descartar até ter 7.")
            print("Sua mão: " + ", ".join([f"{c.cor.cor_terminal}{c.nome}{Style.RESET_ALL}" for c in jogador_atual.mao]))
            carta_para_descartar = input("Qual carta descartar? ").strip().title()
            carta_obj = next((c for c in jogador_atual.mao if c.nome.title() == carta_para_descartar), None)
            if carta_obj:
                jogador_atual.mao.remove(carta_obj)
                self.jogo.baralho_jogador.adicionar_ao_descarte(carta_obj)
            else:
                print("Carta inválida.")

    def _infectar_cidades(self):
        print(f"\n--- Fase de Infecção (Taxa: {self.jogo.taxa_infeccao}) ---")
        for _ in range(self.jogo.taxa_infeccao):
            carta = self.jogo.baralho_infeccao.comprar()
            if not carta:
                print("Baralho de infecção vazio (isso não deveria acontecer em um jogo normal).")
                continue
            
            cidade = self.jogo.tabuleiro.obter_cidade(carta.nome)
            
            cidade.adicionar_cubo(cidade.cor, self.jogo.jogadores, self.jogo)
            
            self.jogo.baralho_infeccao.adicionar_ao_descarte(carta)

class GameOverState(GameState):
    def manusear(self):
        print("\n--- FIM DE JOGO ---")
        self.jogo.rodando = False