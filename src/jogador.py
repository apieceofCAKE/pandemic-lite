from papeis import Papel
from tabuleiro import Cidade
from cartas import CartaJogador
from colorama import Style

class Jogador:
    def __init__(self, nome: str, papel: Papel):
        self.nome = nome
        self.papel = papel
        self.mao = []
        self.localizacao: Cidade = None
        self.acoes_restantes = 4

    def definir_localizacao(self, cidade: Cidade):
        self.localizacao = cidade

    def adicionar_carta(self, carta: CartaJogador):
        self.mao.append(carta)

    def mover_para(self, nova_cidade: Cidade):
        cor_destino = nova_cidade.cor.cor_terminal
        print(f"{self.nome} moveu-se para {cor_destino}{nova_cidade.nome}{Style.RESET_ALL}.")
        self.localizacao = nova_cidade

    def tratar_doenca(self, cor):
        if self.localizacao.remover_cubo(cor):
             cor_local = self.localizacao.cor.cor_terminal
             print(f"{self.nome} tratou a doença {cor.name.lower()} em {cor_local}{self.localizacao.nome}{Style.RESET_ALL}.")
             return True
        return False
        
    def __repr__(self):
        # Formata as cartas na mão do jogador com suas respectivas cores
        cartas_str = ", ".join([f"{c.cor.cor_terminal}{c.nome}{Style.RESET_ALL}" for c in self.mao])
        
        # Lógica para adicionar os asteriscos na localização atual
        cidade_atual = self.localizacao
        total_cubos = sum(cidade_atual.cubos.values())
        marcador_cubos = '*' * total_cubos
        
        # Formata a localização do jogador com cor e os marcadores de cubos
        local_str = f"{cidade_atual.cor.cor_terminal}{cidade_atual.nome}{marcador_cubos}{Style.RESET_ALL}"
        
        return f"-> {self.nome} ({self.papel}) em {local_str} | Ações: {self.acoes_restantes} | Mão: [{cartas_str or 'Vazia'}]"