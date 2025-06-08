# Ficheiro: commands.py
from abc import ABC, abstractmethod
from jogador import Jogador
from tabuleiro import Cidade
from utils import CorDoenca
from colorama import Style # Importação adicionada

class Command(ABC):
    """Interface para o Padrão Command."""
    def __init__(self, jogador: Jogador):
        self.jogador = jogador

    @abstractmethod
    def executar(self):
        pass

class MoverCommand(Command):
    def __init__(self, jogador: Jogador, destino: Cidade):
        super().__init__(jogador)
        self.destino = destino

    def executar(self):
        if self.jogador.acoes_restantes <= 0:
            print("Sem ações restantes.")
            return False
            
        if self.destino in self.jogador.localizacao.vizinhos:
            self.jogador.mover_para(self.destino)
            self.jogador.acoes_restantes -= 1
            return True
        else:
            # --- LINHA CORRIGIDA ---
            cor_destino = self.destino.cor.cor_terminal
            cor_local = self.jogador.localizacao.cor.cor_terminal
            print(f"Movimento inválido: {cor_destino}{self.destino.nome}{Style.RESET_ALL} não é vizinha de {cor_local}{self.jogador.localizacao.nome}{Style.RESET_ALL}.")
            return False

class TratarDoencaCommand(Command):
    def __init__(self, jogador: Jogador, cor: CorDoenca):
        super().__init__(jogador)
        self.cor = cor

    def executar(self):
        if self.jogador.acoes_restantes <= 0:
            print("Sem ações restantes.")
            return False
        
        if self.jogador.tratar_doenca(self.cor):
            self.jogador.acoes_restantes -= 1
            return True
        else:
            cor_local = self.jogador.localizacao.cor.cor_terminal
            print(f"Não há cubos de {self.cor.name} em {cor_local}{self.jogador.localizacao.nome}{Style.RESET_ALL} para tratar.")
            return False