# utils.py
from enum import Enum, auto
from colorama import Fore, Back, Style

class CorDoenca(Enum):
    BLUE = auto()
    YELLOW = auto()
    BLACK = auto()
    RED = auto()
    
    @property
    def cor_terminal(self):
        """Retorna a cor correspondente do terminal"""
        return {
            CorDoenca.BLUE: Fore.BLUE,
            CorDoenca.YELLOW: Fore.YELLOW,
            CorDoenca.BLACK: Fore.LIGHTBLACK_EX,
            CorDoenca.RED: Fore.RED
        }.get(self, Fore.RESET)

MAPA_JOGO = {
    "Atlanta": {"cor": CorDoenca.BLUE, "vizinhos": ["Chicago", "Washington", "Miami"]},
    "Chicago": {"cor": CorDoenca.BLUE, "vizinhos": ["Atlanta", "San Francisco", "Montreal"]},
    "San Francisco": {"cor": CorDoenca.BLUE, "vizinhos": ["Chicago", "Los Angeles", "Tokyo"]},
    "Montreal": {"cor": CorDoenca.BLUE, "vizinhos": ["Chicago", "New York", "Washington"]},
    "Washington": {"cor": CorDoenca.BLUE, "vizinhos": ["Montreal", "New York", "Atlanta"]},
    "New York": {"cor": CorDoenca.BLUE, "vizinhos": ["Montreal", "Washington"]},
    
    "Los Angeles": {"cor": CorDoenca.YELLOW, "vizinhos": ["San Francisco", "Sydney", "Mexico City"]},
    "Mexico City": {"cor": CorDoenca.YELLOW, "vizinhos": ["Los Angeles", "Miami", "Bogota"]},
    "Miami": {"cor": CorDoenca.YELLOW, "vizinhos": ["Atlanta", "Mexico City", "Bogota"]},
    "Bogota": {"cor": CorDoenca.YELLOW, "vizinhos": ["Mexico City", "Miami", "Sao Paulo"]},
    "Sao Paulo": {"cor": CorDoenca.YELLOW, "vizinhos": ["Bogota", "Madrid"]},
    
    "Madrid": {"cor": CorDoenca.BLACK, "vizinhos": ["Sao Paulo", "London", "Paris", "Algiers"]},
    "London": {"cor": CorDoenca.BLACK, "vizinhos": ["Madrid", "Paris", "Essen"]},
    "Paris": {"cor": CorDoenca.BLACK, "vizinhos": ["London", "Madrid", "Essen", "Milan", "Algiers"]},
    "Essen": {"cor": CorDoenca.BLACK, "vizinhos": ["London", "Paris", "Milan"]},
    "Milan": {"cor": CorDoenca.BLACK, "vizinhos": ["Paris", "Essen"]},
    "Algiers": {"cor": CorDoenca.BLACK, "vizinhos": ["Madrid", "Paris", "Istanbul", "Cairo"]},
    
    "Istanbul": {"cor": CorDoenca.RED, "vizinhos": ["Algiers", "Cairo", "Moscow"]},
    "Cairo": {"cor": CorDoenca.RED, "vizinhos": ["Algiers", "Istanbul", "Riyadh"]},
    "Riyadh": {"cor": CorDoenca.RED, "vizinhos": ["Cairo", "Karachi"]},
    "Moscow": {"cor": CorDoenca.RED, "vizinhos": ["Istanbul", "Tehran"]},
    "Tehran": {"cor": CorDoenca.RED, "vizinhos": ["Moscow", "Karachi"]},
    "Karachi": {"cor": CorDoenca.RED, "vizinhos": ["Riyadh", "Tehran"]},
    
    "Tokyo": {"cor": CorDoenca.RED, "vizinhos": ["San Francisco", "Osaka"]},
    "Osaka": {"cor": CorDoenca.RED, "vizinhos": ["Tokyo"]},
    "Sydney": {"cor": CorDoenca.RED, "vizinhos": ["Los Angeles"]}
}

PAPEIS_JOGO = [
    'Scientist',
    'Researcher',
    'OperationsExpert',
    'QuarantineSpecialist',
    'ContingencyPlanner',
]

CARTAS_EPIDEMIA = ["Epidemia"] * 5  # 5 epidemias para dificuldade normal