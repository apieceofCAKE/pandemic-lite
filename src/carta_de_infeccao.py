# File: src/carta_de_infeccao.py
from cidade import Cidade

class CartaDeInfeccao:
    def __init__(self, cidade: Cidade):
        self.cidade = cidade

    def __repr__(self):
        return f"CartaDeInfeccao({self.cidade.nome})"
