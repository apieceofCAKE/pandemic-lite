import random
from utils import CorDoenca

class Carta:
    def __init__(self, nome):
        self.nome = nome
    def __repr__(self):
        return f"{self.__class__.__name__}({self.nome})"

class CartaJogador(Carta):
    def __init__(self, nome, cor: CorDoenca):
        super().__init__(nome)
        self.cor = cor

class CartaInfeccao(Carta):
    def __init__(self, nome, cor: CorDoenca):
        super().__init__(nome)
        self.cor = cor

class Deck:
    def __init__(self, cartas=None):
        self.cartas = cartas if cartas else []
        self.descarte = []

    def baralhar(self):
        random.shuffle(self.cartas)

    def comprar(self):
        if not self.cartas:
            return None
        return self.cartas.pop(0)

    def adicionar_ao_descarte(self, carta):
        self.descarte.append(carta)

    def __len__(self):
        return len(self.cartas)