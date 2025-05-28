class Jogador:
    def __init__(self, nome, papel):
        self.nome = nome
        self.localizacao = "Atlanta"
        self.papel = papel
        self.mao = [] 

    def adicionar_carta(self, carta: str):
        self.mao.append(carta)

    def __str__(self):
        return f"{self.nome} ({self.papel})"