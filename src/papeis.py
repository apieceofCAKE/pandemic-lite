from abc import ABC, abstractmethod

class Papel(ABC):
    """
    Classe Abstrata (Padrão Strategy) para os papéis do jogo.
    Define um comportamento base e um contrato para habilidades especiais.
    """
    def __init__(self, nome, descricao):
        self.nome = nome 
        self.descricao = descricao 

    @abstractmethod
    def obter_habilidades_especiais(self):
        """Método que retorna a descrição detalhada das habilidades."""
        return self.descricao

    # --- MÉTODOS DE HABILIDADE COM IMPLEMENTAÇÃO PADRÃO ---

    def cartas_necessarias_para_cura(self) -> int:
        return 5

    def pode_construir_estacao_sem_carta(self) -> bool:
        return False

    def pode_compartilhar_qualquer_carta(self) -> bool:
        """Habilidade do Pesquisador."""
        return False

    def is_quarentena(self) -> bool:
        """Habilidade passiva do Especialista em Quarentena."""
        return False

    def __repr__(self):
        return self.nome

# --- IMPLEMENTAÇÕES CONCRETAS DOS 4 PAPÉIS ---

class Cientista(Papel): 
    def __init__(self):
        super().__init__("Cientista", "Precisa de apenas 4 cartas da mesma cor para descobrir a cura.") 
    def obter_habilidades_especiais(self): 
        return self.descricao 
    
    def cartas_necessarias_para_cura(self) -> int:
        return 4

class EspecialistaEmOperacoes(Papel): 
    def __init__(self):
        super().__init__("Especialista em Operações", "Pode construir uma estação de pesquisa em sua cidade atual sem descartar uma carta.") 
    def obter_habilidades_especiais(self): 
        return self.descricao 

    def pode_construir_estacao_sem_carta(self) -> bool:
        return True

class Pesquisador(Papel): 
    def __init__(self):
        super().__init__("Pesquisador(a)", "Pode dar qualquer carta de cidade a outro jogador na mesma cidade (a ação de Compartilhar Conhecimento não se limita à carta da cidade em que estão).") 
    def obter_habilidades_especiais(self): 
        return self.descricao 

    def pode_compartilhar_qualquer_carta(self) -> bool:
        return True

class EspecialistaEmQuarentena(Papel): 
    def __init__(self):
        super().__init__("Especialista em Quarentena", "Previne a colocação de cubos de doença na cidade onde está e em todas as cidades vizinhas.") 
    def obter_habilidades_especiais(self): 
        return self.descricao 

    def is_quarentena(self) -> bool:
        return True