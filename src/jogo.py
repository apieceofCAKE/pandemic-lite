from tabuleiro import Tabuleiro
from states import SetupState
from utils import CorDoenca
from colorama import Fore, Back, Style

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
        self.turno_atual = 0
        self.estado = SetupState(self)
        self.rodando = True
        self._inicializado = True

    def definir_estado(self, novo_estado):
        self.estado = novo_estado

    def run(self):
        print(f"\n{Back.WHITE}{Fore.BLACK}=== PANDEMIC ==={Style.RESET_ALL}")
        while self.rodando:
            self.estado.manusear()

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
                    cidade.adicionar_cubo(cidade.cor)
            
            print("\n--- Cidades com 2 cubos ---")
            # 3 cidades com 2 cubos
            for _ in range(3):
                carta = self.baralho_infeccao.comprar()
                cidade = self.tabuleiro.obter_cidade(carta.nome)
                for _ in range(2):
                    cidade.adicionar_cubo(cidade.cor)

            print("\n--- Cidades com 1 cubo ---")
            # 3 cidades com 1 cubo
            for _ in range(3):
                carta = self.baralho_infeccao.comprar()
                cidade = self.tabuleiro.obter_cidade(carta.nome)
                cidade.adicionar_cubo(cidade.cor)
        except AttributeError:
            print("ERRO: Baralho de infecção não foi configurado corretamente.")
        print("------------------------")

    def mostrar_mapa(self):
        """Exibe o mapa com cores e contagem de cubos no terminal."""
        print(f"\n{Back.WHITE}{Fore.BLACK}--- MAPA GLOBAL ---{Style.RESET_ALL}")
        
        legenda_str = "Legenda: "
        for cor in CorDoenca:
            legenda_str += f"{cor.cor_terminal}█ {cor.name}{Style.RESET_ALL}  "
        print(legenda_str)
        print("-" * 70)
        
        cidades_ordenadas = sorted(self.tabuleiro.cidades.values(), key=lambda c: c.nome)
        for cidade in cidades_ordenadas:
            cor_cidade = cidade.cor.cor_terminal
            
            vizinhos_formatados = [f"{v.cor.cor_terminal}{v.nome}{Style.RESET_ALL}" for v in cidade.vizinhos]

            total_cubos = sum(cidade.cubos.values())
            marcador_cubos = '*' * total_cubos
            
            nome_com_cubos = f"{cidade.nome}{marcador_cubos}"
            
            print(f"{cor_cidade}• {nome_com_cubos.ljust(20)}{Style.RESET_ALL} → {', '.join(vizinhos_formatados)}")
        print("-" * 70)

    def mostrar_estado_jogadores(self):
        print(f"\n{Back.WHITE}{Fore.BLACK}--- POSIÇÃO DOS JOGADORES ---{Style.RESET_ALL}")
        for jogador in self.jogadores:
            print(jogador)
        print("----------------------------")
    
    def obter_jogador_atual(self):
        return self.jogadores[self.turno_atual]

    def proximo_turno(self):
        self.turno_atual = (self.turno_atual + 1) % len(self.jogadores)
    
    def verificar_fim_de_jogo(self):
        if self.baralho_jogador and len(self.baralho_jogador.cartas) == 0:
            print("O baralho de jogador acabou! Derrota!")
            return True
        return False