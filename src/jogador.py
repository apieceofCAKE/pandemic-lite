# File: src/jogador.py
from cidade import Cidade
from carta_de_jogador import CartaDeJogador
from cor_da_doenca import CorDaDoenca

class Jogador:
    def __init__(self, nome: str, localizacao_atual: Cidade):
        self.nome = nome
        self.localizacao_atual = localizacao_atual
        self.mao = []  # List of CartaDeJogador objects

    def mover(self, destino: Cidade):
        self.localizacao_atual = destino
        print(f"{self.nome} moveu-se para {destino.nome}.")

    def construir_estacao_de_pesquisa(self):
        self.localizacao_atual.construir_estacao_de_pesquisa()
        print(f"{self.nome} construiu uma estação de pesquisa em {self.localizacao_atual.nome}.")

    def tratar_doenca(self, cor: CorDaDoenca):
        self.localizacao_atual.remover_cubo_de_doenca(cor)
        print(f"{self.nome} tratou a doença {cor.name} em {self.localizacao_atual.nome}.")

    def sacar_carta_de_jogador(self, carta: CartaDeJogador):
        self.mao.append(carta)
        print(f"{self.nome} recebeu a carta: {carta}.")

    def descartar_carta_jogador(self, carta: CartaDeJogador):
        if carta in self.mao:
            self.mao.remove(carta)
            print(f"{self.nome} descartou a carta: {carta}.")
        else:
            print(f"A carta {carta} não está na mão de {self.nome}.")
