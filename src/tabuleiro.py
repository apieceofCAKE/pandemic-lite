from utils import CorDoenca

class Cidade:
    """Information Expert: Contém informações sobre si mesma."""
    def __init__(self, nome, cor: CorDoenca):
        self.nome = nome
        self.cor = cor
        self.vizinhos = []
        self.cubos = {c: 0 for c in CorDoenca}
        self.tem_estacao = False

    def adicionar_vizinho(self, cidade):
        if cidade not in self.vizinhos:
            self.vizinhos.append(cidade)

    def adicionar_cubo(self, cor: CorDoenca):
        if self.cubos[cor] < 3:
            self.cubos[cor] += 1
            print(f"Cubo de doença {cor.name.lower()} adicionado a {self.nome}.")
            return True
        print(f"{self.nome} já tem 3 cubos. Um surto ocorreria!")
        return False

    def remover_cubo(self, cor: CorDoenca):
        if self.cubos[cor] > 0:
            self.cubos[cor] -= 1
            return True
        return False

    def construir_estacao(self):
        if not self.tem_estacao:
            self.tem_estacao = True
            return True
        return False

    def __repr__(self):
        estacao_str = "(Estação)" if self.tem_estacao else ""
        cubos_str = ", ".join([f"{c.name}: {q}" for c, q in self.cubos.items() if q > 0])
        return f"{self.nome} {estacao_str} | Cubos: [{cubos_str or 'Nenhum'}]"

class Tabuleiro:
    """Information Expert: Conhece todas as cidades, suas conexões e o estado geral do tabuleiro."""
    
    MAPA_JOGO = {
        "Atlanta": {"cor": CorDoenca.AZUL, "vizinhos": ["Chicago", "Washington", "Miami"]},
        "Chicago": {"cor": CorDoenca.AZUL, "vizinhos": ["Atlanta", "San Francisco", "Montreal"]},
        "San Francisco": {"cor": CorDoenca.AZUL, "vizinhos": ["Chicago", "Los Angeles", "Tokyo"]},
        "Montreal": {"cor": CorDoenca.AZUL, "vizinhos": ["Chicago", "New York", "Washington"]},
        "Washington": {"cor": CorDoenca.AZUL, "vizinhos": ["Montreal", "New York", "Atlanta"]},
        "New York": {"cor": CorDoenca.AZUL, "vizinhos": ["Montreal", "Washington"]},
        "Los Angeles": {"cor": CorDoenca.AMARELO, "vizinhos": ["San Francisco", "Sydney", "Mexico City"]},
        "Mexico City": {"cor": CorDoenca.AMARELO, "vizinhos": ["Los Angeles", "Miami", "Bogota"]},
        "Miami": {"cor": CorDoenca.AMARELO, "vizinhos": ["Atlanta", "Mexico City", "Bogota"]},
        "Bogota": {"cor": CorDoenca.AMARELO, "vizinhos": ["Mexico City", "Miami", "Sao Paulo"]},
        "Sao Paulo": {"cor": CorDoenca.AMARELO, "vizinhos": ["Bogota", "Madrid"]},
        "Madrid": {"cor": CorDoenca.PRETO, "vizinhos": ["Sao Paulo", "London", "Paris", "Algiers"]},
        "London": {"cor": CorDoenca.PRETO, "vizinhos": ["Madrid", "Paris", "Essen"]},
        "Paris": {"cor": CorDoenca.PRETO, "vizinhos": ["London", "Madrid", "Essen", "Milan", "Algiers"]},
        "Essen": {"cor": CorDoenca.PRETO, "vizinhos": ["London", "Paris", "Milan"]},
        "Milan": {"cor": CorDoenca.PRETO, "vizinhos": ["Paris", "Essen"]},
        "Algiers": {"cor": CorDoenca.PRETO, "vizinhos": ["Madrid", "Paris", "Istanbul", "Cairo"]},
        "Istanbul": {"cor": CorDoenca.VERMELHO, "vizinhos": ["Algiers", "Cairo", "Moscow"]},
        "Cairo": {"cor": CorDoenca.VERMELHO, "vizinhos": ["Algiers", "Istanbul", "Riyadh"]},
        "Riyadh": {"cor": CorDoenca.VERMELHO, "vizinhos": ["Cairo", "Karachi"]},
        "Moscow": {"cor": CorDoenca.VERMELHO, "vizinhos": ["Istanbul", "Tehran"]},
        "Tehran": {"cor": CorDoenca.VERMELHO, "vizinhos": ["Moscow", "Karachi"]},
        "Karachi": {"cor": CorDoenca.VERMELHO, "vizinhos": ["Riyadh", "Tehran"]},
        "Tokyo": {"cor": CorDoenca.VERMELHO, "vizinhos": ["San Francisco", "Osaka"]},
        "Osaka": {"cor": CorDoenca.VERMELHO, "vizinhos": ["Tokyo"]},
        "Sydney": {"cor": CorDoenca.VERMELHO, "vizinhos": ["Los Angeles"]}
    }

    def __init__(self):
        self.cidades = {nome: Cidade(nome, dados["cor"]) for nome, dados in self.MAPA_JOGO.items()}
        self._conectar_cidades()

    def _conectar_cidades(self):
        for nome, dados in self.MAPA_JOGO.items():
            cidade_obj = self.cidades[nome]
            for vizinho_nome in dados["vizinhos"]:
                vizinho_obj = self.cidades[vizinho_nome]
                cidade_obj.adicionar_vizinho(vizinho_obj)
    
    def obter_cidade(self, nome):
        return self.cidades.get(nome)