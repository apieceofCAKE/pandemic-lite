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

class CartaEpidemia(Carta):
    def __init__(self):
        super().__init__("Epidemia")

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
    
    def comprar_do_fundo(self):
        """Puxa a última carta do baralho (usado na fase 'Infectar' da Epidemia)."""
        if not self.cartas:
            return None
        return self.cartas.pop()
    
    def reembaralhar_descarte_no_topo(self):
        """Pega a pilha de descarte, embaralha e a coloca no topo do baralho."""
        print("Intensificando infecções: reembaralhando o descarte no topo do baralho de infecção...")
        random.shuffle(self.descarte)
        self.cartas = self.descarte + self.cartas
        self.descarte = []


    def __len__(self):
        return len(self.cartas)