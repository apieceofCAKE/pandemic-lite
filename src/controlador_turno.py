# File: src/controlador_turno.py
from jogo import Jogo
from jogador import Jogador

class ControladorTurno:
    def __init__(self, jogo: Jogo):
        self.jogo = jogo
        self.jogador_atual = None

    def iniciar_turno(self):
        if self.jogo.jogadores:
            # For simplicity, select the first player to start the turn.
            self.jogador_atual = self.jogo.jogadores[0]
            print(f"Iniciando turno para {self.jogador_atual.nome}.")
        else:
            print("Nenhum jogador disponível para iniciar o turno.")

    def validar_comando(self, comando: str):
        # Implement command validation logic here.
        print(f"Validando comando: {comando}")

    def atualizar_status_jogo(self):
        print("Status do jogo atualizado.")

    def verificar_fim_turno(self):
        print("Verificando se o turno deve terminar.")

    def avancar_para_proximo_turno(self):
        if self.jogo.jogadores:
            idx = self.jogo.jogadores.index(self.jogador_atual)
            self.jogador_atual = self.jogo.jogadores[(idx + 1) % len(self.jogo.jogadores)]
            print(f"Avançando para o turno de {self.jogador_atual.nome}.")

    def aumentar_nivel_de_infeccao(self):
        self.jogo.nivel_de_infeccao += 1
        print(f"Nível de infecção aumentado para {self.jogo.nivel_de_infeccao}.")
