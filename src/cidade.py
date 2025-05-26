# File: src/cidade.py
from cor_da_doenca import CorDaDoenca

class Cidade:
    def __init__(self, nome: str):
        self.nome = nome
        self.tem_estacao_de_pesquisa = False
        # Dictionary to store the number of disease cubes per color.
        self.cubos_de_doenca = {}  # dict[CorDaDoenca, int]

    def adicionar_cubo_de_doenca(self, cor: CorDaDoenca):
        if cor in self.cubos_de_doenca:
            self.cubos_de_doenca[cor] += 1
        else:
            self.cubos_de_doenca[cor] = 1
        print(f"Adicionado cubo de {cor.name} na cidade {self.nome}.")

    def remover_cubo_de_doenca(self, cor: CorDaDoenca):
        if cor in self.cubos_de_doenca and self.cubos_de_doenca[cor] > 0:
            self.cubos_de_doenca[cor] -= 1
            print(f"Removido um cubo de {cor.name} da cidade {self.nome}.")
        else:
            print(f"Nenhum cubo de {cor.name} para remover em {self.nome}.")

    def construir_estacao_de_pesquisa(self):
        self.tem_estacao_de_pesquisa = True
        print(f"Estação de pesquisa construída em {self.nome}.")
