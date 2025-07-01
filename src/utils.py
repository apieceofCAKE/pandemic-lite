from enum import Enum, auto
from colorama import Fore

""""Informações e funções auxiliares do jogo Pandemic."""
class CorDoenca(Enum):
    AZUL = auto()
    AMARELO = auto()
    PRETO = auto()
    VERMELHO = auto()
    
    @property
    def cor_terminal(self):
        """Retorna a cor correspondente do terminal"""
        return {
            CorDoenca.AZUL: Fore.BLUE,
            CorDoenca.AMARELO: Fore.YELLOW,
            CorDoenca.PRETO: Fore.LIGHTBLACK_EX,
            CorDoenca.VERMELHO: Fore.RED
        }.get(self, Fore.RESET)

PAPEIS_JOGO = {
    '1': 'Cientista',
    '2': 'Pesquisador',
    '3': 'EspecialistaEmOperacoes',
    '4': 'EspecialistaEmQuarentena',
}

CARTAS_EPIDEMIA = 5