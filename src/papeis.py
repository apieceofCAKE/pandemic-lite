from abc import ABC, abstractmethod

class Papel(ABC):
    """Interface do Padrão Strategy para os papéis."""
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    @abstractmethod
    def obter_habilidades_especiais(self):
        pass

    def __repr__(self):
        return self.nome

class Cientista(Papel):
    def __init__(self):
        super().__init__("Cientista", "Precisa de apenas 4 cartas para descobrir a cura.")
    def obter_habilidades_especiais(self):
        return self.descricao

class Pesquisador(Papel):
    def __init__(self):
        super().__init__("Pesquisador(a)", "Pode dar qualquer carta de cidade a outro jogador na mesma cidade.")
    def obter_habilidades_especiais(self):
        return self.descricao

class EspecialistaEmOperacoes(Papel):
    def __init__(self):
        super().__init__("Especialista em Operações", "Pode construir uma estação de pesquisa em sua cidade atual sem descartar uma carta.")
    def obter_habilidades_especiais(self):
        return self.descricao
        
class EspecialistaEmQuarentena(Papel):
    def __init__(self):
        super().__init__("Especialista em Quarentena", "Previne a colocação de cubos na sua cidade e vizinhança.")
    def obter_habilidades_especiais(self):
        return self.descricao
        
class PlanejadorDeContingencia(Papel):
    def __init__(self):
        super().__init__("Planejador de Contingência", "Pode pegar uma carta de evento do descarte e guardá-la.")
    def obter_habilidades_especiais(self):
        return self.descricao