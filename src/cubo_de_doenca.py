# File: src/cubo_de_doenca.py
from cor_da_doenca import CorDaDoenca

class CuboDeDoenca:
    def __init__(self, cor: CorDaDoenca):
        self.cor = cor

    def __repr__(self):
        return f"CuboDeDoenca({self.cor.name})"
