# File: src/jogo.py
from carta_de_infeccao import CartaDeInfeccao
from cidade import Cidade
from jogador import Jogador
from cor_da_doenca import CorDaDoenca

class Jogo:
    def __init__(self):
        self.nivel_de_infeccao = 1
        self.surtos = 0
        self.eh_fim_de_jogo = False
        self.baralho_infeccao = []         # List of CartaDeInfeccao objects
        self.descarte_infeccao = []        # List of CartaDeInfeccao objects
        self.cidades = {}                  # Dictionary mapping city name to Cidade
        self.jogadores = []                # List of Jogador objects
        self.jogador_atual = None

    def iniciar_jogo(self):
        # Initialize game state, shuffle decks, distribute cards, etc.
        print("Jogo iniciado.")

    def adicionar_jogador(self, jogador: Jogador):
        self.jogadores.append(jogador)
        print(f"Jogador {jogador.nome} adicionado.")

    def sacar_carta_de_infeccao(self):
        if self.baralho_infeccao:
            carta = self.baralho_infeccao.pop(0)
            self.descarte_infeccao.append(carta)
            print(f"Sacou a carta de infecção: {carta}")
            return carta
        else:
            print("Baralho de infecção vazio!")
            return None

    def infectar_cidade(self, cidade: Cidade, cor: CorDaDoenca):
        cidade.adicionar_cubo_de_doenca(cor)
        print(f"{cidade.nome} foi infectada com a doença {cor.name}.")

    def construir_estacao_de_pesquisa(self, cidade: Cidade):
        cidade.construir_estacao_de_pesquisa()
        print(f"Estação de pesquisa construída em {cidade.nome}.")

    def verificar_fim_de_jogo(self):
        # Lógica para determinar se o jogo acabou
        return self.eh_fim_de_jogo

    def declarar_fim_de_jogo(self):
        self.eh_fim_de_jogo = True
        print("Fim do jogo!")
