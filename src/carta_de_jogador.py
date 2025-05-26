# File: src/carta_de_jogador.py

class CartaDeJogador:
    def __init__(self, nome: str):
        self.nome = nome

    def __repr__(self):
        return f"CartaDeJogador({self.nome})"
