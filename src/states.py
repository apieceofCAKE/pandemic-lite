# Ficheiro: states.py
import random
from abc import ABC, abstractmethod
from utils import PAPEIS_JOGO, CorDoenca
import papeis as classes_papeis
from jogador import Jogador
from cartas import CartaJogador, CartaInfeccao, Deck
from commands import MoverCommand, TratarDoencaCommand
from colorama import Style

class GameState(ABC):
    def __init__(self, jogo):
        self.jogo = jogo
    @abstractmethod
    def manusear(self):
        pass

class SetupState(GameState):
    def manusear(self):
        print("--- Configurando a Partida ---")
        self._configurar_jogadores()
        self._configurar_tabuleiro_e_baralhos()
        self.jogo.infeccao_inicial()
        self.jogo.definir_estado(PlayerTurnState(self.jogo))

    def _configurar_jogadores(self):
        num = 0
        while num not in [2, 3, 4]:
            try:
                num = int(input("Quantos jogadores? (2-4): "))
            except ValueError:
                print("Número inválido.")
        
        nomes_papeis = list(PAPEIS_JOGO.values())
        papeis_sorteados = random.sample(nomes_papeis, num)
        
        for i in range(num):
            nome = input(f"Nome do jogador {i+1}: ").strip()
            nome_classe_papel = papeis_sorteados[i]
            classe_papel = getattr(classes_papeis, nome_classe_papel)
            jogador = Jogador(nome, classe_papel())
            self.jogo.jogadores.append(jogador)
            print(f"Jogador {jogador.nome} é um(a) {jogador.papel.nome}.")

    def _configurar_tabuleiro_e_baralhos(self):
        cidade_inicial = self.jogo.tabuleiro.obter_cidade("Atlanta")
        cidade_inicial.construir_estacao()

        for p in self.jogo.jogadores:
            p.definir_localizacao(cidade_inicial)

        cartas_jogador = [CartaJogador(c.nome, c.cor) for c in self.jogo.tabuleiro.cidades.values()]
        self.jogo.baralho_jogador = Deck(cartas_jogador)
        self.jogo.baralho_jogador.baralhar()
        
        cartas_infeccao = [CartaInfeccao(c.nome, c.cor) for c in self.jogo.tabuleiro.cidades.values()]
        self.jogo.baralho_infeccao = Deck(cartas_infeccao)
        self.jogo.baralho_infeccao.baralhar()

        cartas_por_jogador = {2: 4, 3: 3, 4: 2}[len(self.jogo.jogadores)]
        for p in self.jogo.jogadores:
            for _ in range(cartas_por_jogador):
                p.adicionar_carta(self.jogo.baralho_jogador.comprar())


class PlayerTurnState(GameState):
    def manusear(self):
        jogador_atual = self.jogo.obter_jogador_atual()
        jogador_atual.acoes_restantes = 4
        
        self.jogo.mostrar_mapa()
        self.jogo.mostrar_estado_jogadores()

        print("\n" + "="*50)
        print(f"TURNO DE: {jogador_atual.nome} ({jogador_atual.papel})")
        print("="*50)

        while jogador_atual.acoes_restantes > 0:
            comando = self._obter_comando_do_jogador(jogador_atual)
            
            if comando:
                comando.executar()
                if jogador_atual.acoes_restantes > 0:
                    self.jogo.mostrar_estado_jogadores()
            elif jogador_atual.acoes_restantes == 0:
                break
        
        print(f"\nFim do turno de {jogador_atual.nome}.")
        self.jogo.proximo_turno()
        if self.jogo.verificar_fim_de_jogo():
            self.jogo.definir_estado(GameOverState(self.jogo))

    def _obter_comando_do_jogador(self, jogador):
        print(f"\nAções restantes: {jogador.acoes_restantes}")
        print("Comandos: [1] Mover | [2] Tratar Doença | [p] Passar")
        escolha = input("Escolha uma ação: ").lower().strip()

        if escolha == '1':
            vizinhos_coloridos = [f"{v.cor.cor_terminal}{v.nome}{Style.RESET_ALL}" for v in jogador.localizacao.vizinhos]
            print(f"Vizinhos: {', '.join(vizinhos_coloridos)}")
            # --- ENTRADA DA CIDADE MODIFICADA ---
            nome_cidade = input("Mover para qual cidade? ").strip().title()
            cidade_destino = self.jogo.tabuleiro.obter_cidade(nome_cidade)
            if cidade_destino:
                return MoverCommand(jogador, cidade_destino)
        elif escolha == '2':
            # --- TEXTO DE AJUDA MODIFICADO ---
            cor_str = input("Tratar qual cor (AZUL, AMARELO, PRETO, VERMELHO)? ").upper().strip()
            try:
                cor = CorDoenca[cor_str]
                return TratarDoencaCommand(jogador, cor)
            except KeyError:
                pass
        elif escolha == 'p':
            jogador.acoes_restantes = 0
            return None
            
        print("Comando inválido. Tente novamente.")
        return None

class GameOverState(GameState):
    def manusear(self):
        print("\n--- FIM DE JOGO ---")
        self.jogo.rodando = False