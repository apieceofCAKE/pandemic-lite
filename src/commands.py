from abc import ABC, abstractmethod
from cartas import CartaJogador
from jogador import Jogador
from tabuleiro import Cidade
from utils import CorDoenca
from colorama import Style

class Command(ABC):
    """Interface para o Padrão Command."""
    def __init__(self, jogador: Jogador, jogo):
        self.jogador = jogador
        self.jogo = jogo

    @abstractmethod
    def executar(self):
        pass

class MoverCommand(Command):
    def __init__(self, jogador: Jogador, destino: Cidade, jogo):
        super().__init__(jogador, jogo)
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
            cor_destino = self.destino.cor.cor_terminal
            cor_local = self.jogador.localizacao.cor.cor_terminal
            print(f"Movimento inválido: {cor_destino}{self.destino.nome}{Style.RESET_ALL} não é vizinha de {cor_local}{self.jogador.localizacao.nome}{Style.RESET_ALL}.")
            return False

class TratarDoencaCommand(Command):
    def __init__(self, jogador: Jogador, cor: CorDoenca, jogo):
        super().__init__(jogador, jogo)
        self.cor = cor

    def executar(self):
        if self.jogador.acoes_restantes <= 0:
            print("Sem ações restantes.")
            return False
        
        if self.jogador.tratar_doenca(self.cor):
            self.jogador.acoes_restantes -= 1
            if self.jogo.curas_descobertas[self.cor] == True:
                self.jogo.estoque_cubos[self.cor] = self.jogador.localizacao.cubos[self.cor]
                self.jogador.localizacao.cubos[self.cor] = 0
            return True
        else:
            cor_local = self.jogador.localizacao.cor.cor_terminal
            print(f"Não há cubos de {self.cor.name} em {cor_local}{self.jogador.localizacao.nome}{Style.RESET_ALL} para tratar.")
            return False
        
class ConstruirEstacaoCommand(Command):
    def __init__(self, jogador: Jogador, jogo):
        super().__init__(jogador, jogo)

    def executar(self):
        if self.jogador.acoes_restantes <= 0:
            print("Sem ações restantes.")
            return False
        
        cidade_atual = self.jogador.localizacao
        
        if cidade_atual.tem_estacao:
            print(f"{cidade_atual.nome} já possui uma estação de pesquisa.")
            return False

        pode_construir_gratis = self.jogador.papel.pode_construir_estacao_sem_carta()

        if pode_construir_gratis:
            cidade_atual.construir_estacao()
            self.jogador.acoes_restantes -= 1
            return True
        else:
            carta_da_cidade = next((c for c in self.jogador.mao if c.nome == cidade_atual.nome), None)
            if carta_da_cidade:
                cidade_atual.construir_estacao()
                self.jogador.mao.remove(carta_da_cidade)
                print(f"{self.jogador.nome} descartou a carta de {carta_da_cidade.nome} para construir uma estação.")
                self.jogador.acoes_restantes -= 1
                return True
            else:
                print(f"{self.jogador.nome} não tem a carta de {cidade_atual.nome} para construir uma estação.")
                return False

class DescobrirCuraCommand(Command):
    def __init__(self, jogador: Jogador, cor: CorDoenca, jogo):
        super().__init__(jogador, jogo)
        self.cor = cor

    def executar(self):
        if self.jogador.acoes_restantes <= 0:
            return False
        
        if not self.jogador.localizacao.tem_estacao:
            print("É preciso estar em uma cidade com Estação de Pesquisa para descobrir a cura.")
            return False

        cartas_necessarias = self.jogador.papel.cartas_necessarias_para_cura()
        cartas_da_cor = [c for c in self.jogador.mao if c.cor == self.cor]
        
        if len(cartas_da_cor) >= cartas_necessarias:
            print(f"{self.jogador.nome} usou {cartas_necessarias} cartas e descobriu a cura para a doença {self.cor.name}!")
            for i in range(cartas_necessarias):
                self.jogador.mao.remove(cartas_da_cor[i])
            self.jogador.acoes_restantes -= 1
            self.jogo.curas_descobertas[self.cor] = True
            return True
        else:
            print(f"Cartas insuficientes. São necessárias {cartas_necessarias} cartas da cor {self.cor.name}.")
            return False
        
class CompartilharConhecimentoCommand(Command):
    def __init__(self, jogador: Jogador, receptor: Jogador, carta: str, jogo):
        super().__init__(jogador, jogo)
        self.receptor = receptor
        self.nome_carta = carta

    def executar(self):
        if self.jogador.acoes_restantes <= 0: return False

        if self.jogador.localizacao != self.receptor.localizacao:
            print("Erro: Os jogadores devem estar na mesma cidade.")
            return False

        carta_para_dar = next((c for c in self.jogador.mao if c.nome.lower() == self.nome_carta.lower()), None)
        if not carta_para_dar:
            print(f"{self.jogador.nome} não possui a carta {self.nome_carta}.")
            return False

        if self.jogador.papel.pode_compartilhar_qualquer_carta():
            pass # Habilidade do Pesquisador permite a troca
        elif carta_para_dar.nome != self.jogador.localizacao.nome:
            print(f"Erro: Só é possível compartilhar a carta da cidade atual ({self.jogador.localizacao.nome}).")
            return False

        self.jogador.mao.remove(carta_para_dar)
        self.receptor.adicionar_carta(carta_para_dar)
        print(f"{self.jogador.nome} deu a carta {carta_para_dar.nome} para {self.receptor.nome}.")
        self.jogador.acoes_restantes -= 1
        return True
    
class VooDiretoCommand(Command):
    """Ação: Descarta uma carta de cidade para se mover para a cidade nomeada."""
    def __init__(self, jogador: Jogador, carta_cidade: CartaJogador, jogo):
        super().__init__(jogador, jogo)
        self.carta_cidade = carta_cidade
        self.cidade_destino = self.jogo.tabuleiro.obter_cidade(carta_cidade.nome)

    def executar(self):
        if self.jogador.acoes_restantes <= 0:
            print("Sem ações restantes.")
            return False

        # Remove a carta da mão do jogador
        self.jogador.mao.remove(self.carta_cidade)
        # Adiciona a carta ao monte de descarte
        self.jogo.baralho_jogador.adicionar_ao_descarte(self.carta_cidade)
        
        # Move o jogador
        self.jogador.mover_para(self.cidade_destino)
        self.jogador.acoes_restantes -= 1
        
        print(f"{self.jogador.nome} usou um Voo Direto para {self.cidade_destino.nome}, descartando a carta correspondente.")
        return True

class VooFretadoCommand(Command):
    """Ação: Descarta a carta da cidade atual para se mover para QUALQUER cidade."""
    def __init__(self, jogador: Jogador, cidade_destino: Cidade, jogo):
        super().__init__(jogador, jogo)
        self.cidade_destino = cidade_destino

    def executar(self):
        if self.jogador.acoes_restantes <= 0:
            print("Sem ações restantes.")
            return False
            
        cidade_atual = self.jogador.localizacao
        carta_necessaria = next((c for c in self.jogador.mao if c.nome == cidade_atual.nome), None)

        if not carta_necessaria:
            print(f"Erro: Você precisa da carta de {cidade_atual.nome} para usar um Voo Fretado.")
            return False

        # Remove a carta da mão e a descarta
        self.jogador.mao.remove(carta_necessaria)
        self.jogo.baralho_jogador.adicionar_ao_descarte(carta_necessaria)

        # Move o jogador
        self.jogador.mover_para(self.cidade_destino)
        self.jogador.acoes_restantes -= 1
        
        print(f"{self.jogador.nome} usou um Voo Fretado de {cidade_atual.nome} para {self.cidade_destino.nome}.")
        return True

class PonteAereaCommand(Command):
    """Ação: Move-se de uma cidade com estação para qualquer outra cidade com estação."""
    def __init__(self, jogador: Jogador, cidade_destino: Cidade, jogo):
        super().__init__(jogador, jogo)
        self.cidade_destino = cidade_destino

    def executar(self):
        if self.jogador.acoes_restantes <= 0:
            print("Sem ações restantes.")
            return False

        cidade_atual = self.jogador.localizacao
        
        if not cidade_atual.tem_estacao:
            print("Erro: Você precisa estar em uma cidade com Estação de Pesquisa para usar a Ponte Aérea.")
            return False
            
        if not self.cidade_destino.tem_estacao:
            print(f"Erro: A cidade de destino ({self.cidade_destino.nome}) não possui uma Estação de Pesquisa.")
            return False

        # Move o jogador
        self.jogador.mover_para(self.cidade_destino)
        self.jogador.acoes_restantes -= 1
        
        print(f"{self.jogador.nome} usou a Ponte Aérea de {cidade_atual.nome} para {self.cidade_destino.nome}.")
        return True
