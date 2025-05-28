# File: src/jogo.py
from random import sample
from random import shuffle
from utils import *
from jogador import Jogador

class PandemicGame:
    _instance = None  # Variável de classe para armazenar a única instância

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # Cria a instância se não existir
            cls._instance.__init_game()  # Chama o inicializador
        return cls._instance  # Sempre retorna a mesma instância
    
    def __init_game(self):
        print("----Bem vindo ao Pandemic----")
        self.jogadores = []
        self.num_jogadores = 0
        self.baralho_jogador = list(MAPA_JOGO.keys())
        self.baralho_infeccao = list(MAPA_JOGO.keys())
        shuffle(self.baralho_jogador)
        shuffle(self.baralho_infeccao)
        self.estado_jogo = "configuracao"

    def run(self):
        if not self.jogadores:
            self.setup_game()
        self.mostrar_mapa_colorido()

    def setup_game(self):
        numero_jogadores = self._get_numero_de_jogadores()
        nome_jogadores = self._get_nome_dos_jogadores(numero_jogadores)
        papeis = sample(PAPEIS_JOGO, numero_jogadores)
        self.jogadores = []
        for nome, papel in zip(nome_jogadores, papeis):
            self.jogadores.append(Jogador(nome,papel))
            print(f"Jogador {nome} é {papel}")
        self.num_jogadores = numero_jogadores
        self._distribuir_cartas_iniciais()

    def _get_numero_de_jogadores(self):
        """Pede um número entre 2 e 4."""
        while True:
            try:
                num = int(input("Quantos jogadores? (2-4): "))
                if 2 <= num <= 4:
                    return num
                print("Número inválido. Digite 2, 3 ou 4.")
            except ValueError:
                print("Digite um número válido.")
    
    def _get_nome_dos_jogadores(self, n):
        """Pede o nome de cada jogador."""
        nomes = []
        for i in range (1,n+1):
            nomes.append(input(f"Nome do jogador {i}: ".strip()))
        return nomes
        
    def _distribuir_cartas_iniciais(self):
        """Distribui cartas iniciais para os jogadores"""
        cartas_por_jogador = 4 if self.num_jogadores == 2 else 3 if self.num_jogadores == 3 else 2
        
        for jogador in self.jogadores:
            for _ in range(cartas_por_jogador):
                if not self.baralho_jogador:
                    raise RuntimeError("Baralho de jogador vazio!")
                carta = self.baralho_jogador.pop()
                jogador.adicionar_carta(carta)
                print(f"{jogador.nome} recebeu a carta: {carta}")

    def _infecao_inicial(self):
        """Realiza a infecção inicial (9 cidades)"""
        # Divide as primeiras 9 cartas em 3 grupos de 3
        grupos = [self.baralho_infeccao[:3], 
                 self.baralho_infeccao[3:6], 
                 self.baralho_infeccao[6:9]]
        
        print("\n=== Infecção Inicial ===")
        for i, grupo in enumerate(grupos, start=1):
            cubos = 4 - i  # 3, 2, 1 cubos respectivamente
            for cidade in grupo:
                cor = MAPA_JOGO[cidade]["cor"]
                
                # Verifica se há cubos disponíveis
                if self.cubos_disponiveis[cor] < cubos:
                    raise RuntimeError(f"Sem cubos suficientes de {cor.name}!")
                
                # Adiciona cubos à cidade
                self.cubos_cidades[cidade].extend([cor] * cubos)
                self.cubos_disponiveis[cor] -= cubos
                
                print(f"Colocados {cubos} cubos {cor.name} em {cidade}")
                
            # Coloca as cartas usadas no descarte de infecção
            self.descarte_infeccao.extend(grupo)
    
    def mostrar_mapa_colorido(self):
        """Exibe o mapa com cores no terminal"""
        print(f"\n{Back.WHITE}{Fore.BLACK}=== MAPA DO PANDEMIC ==={Style.RESET_ALL}")
        print("Legenda:")
        for cor, valor in CORES_TERMINAL.items():
            print(f"{valor}█ {cor.name}{Style.RESET_ALL}")
        print()
        
        for cidade, dados in MAPA_JOGO.items():
            cor = CORES_TERMINAL[dados["cor"]]
            vizinhos = []
            for v in dados["vizinhos"]:
                vizinhos.append(f"{CORES_TERMINAL[MAPA_JOGO[v]['cor']]}{v}{Style.RESET_ALL}")
            
            print(f"{cor}• {cidade.ljust(15)}{Style.RESET_ALL} → {', '.join(vizinhos)}")
        
        # Mostra posição dos jogadores
        print(f"\n{Style.BRIGHT}Jogadores:{Style.RESET_ALL}")
        for jogador in self.jogadores:
            cidade = jogador.localizacao
            cor = CORES_TERMINAL[MAPA_JOGO[cidade]["cor"]]
            print(f"{jogador.nome} ({jogador.papel}): {cor}{cidade}{Style.RESET_ALL}")