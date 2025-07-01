from papeis import Papel
from tabuleiro import Cidade
from cartas import CartaJogador
from colorama import Fore, Style

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
        cartas_na_mao_str = []
        for c in self.mao:
            if hasattr(c, 'cor') and c.cor:
                cartas_na_mao_str.append(f"{c.cor.cor_terminal}{c.nome}{Style.RESET_ALL}")
            else:
                cartas_na_mao_str.append(f"{Fore.MAGENTA}{Style.BRIGHT}{c.nome}{Style.RESET_ALL}")
        cartas_str = ", ".join(cartas_na_mao_str)
        
        cidade_atual = self.localizacao

        marcadores_coloridos = []
        marcadores_sem_cor = []
        for cor, quantidade in cidade_atual.cubos.items():
            if quantidade > 0:
                marcadores_coloridos.append(f"{cor.cor_terminal}{'*' * quantidade}{Style.RESET_ALL}")
                marcadores_sem_cor.append('*' * quantidade)
        
        marcador_str_colorido = f" [{''.join(marcadores_coloridos)}]" if marcadores_coloridos else ""
        local_str_colorido = f"{cidade_atual.cor.cor_terminal}{cidade_atual.nome}{Style.RESET_ALL}{marcador_str_colorido}"
        
        return f"-> {self.nome} ({self.papel}) em {local_str_colorido} | Ações: {self.acoes_restantes} | Mão: [{cartas_str or 'Vazia'}]"