# File: src/main.py
from jogo import Jogo
from cidade import Cidade
from jogador import Jogador
from cor_da_doenca import CorDaDoenca
from controlador_turno import ControladorTurno
from carta_de_infeccao import CartaDeInfeccao
from carta_de_jogador import CartaDeJogador

def main():
    # Cria uma instância do jogo
    jogo = Jogo()
    
    # Configura cidades
    nova_york = Cidade("Nova York")
    londres = Cidade("Londres")
    jogo.cidades[nova_york.nome] = nova_york
    jogo.cidades[londres.nome] = londres
    
    # Cria jogadores
    jogador1 = Jogador("Alice", nova_york)
    jogador2 = Jogador("Bob", londres)
    jogo.adicionar_jogador(jogador1)
    jogo.adicionar_jogador(jogador2)
    
    # Exemplo: adicionando cartas de infecção ao baralho
    jogo.baralho_infeccao.append(CartaDeInfeccao(nova_york))
    jogo.baralho_infeccao.append(CartaDeInfeccao(londres))
    
    # Inicia o jogo
    jogo.iniciar_jogo()
    
    # Inicia o controlador do turno
    controlador = ControladorTurno(jogo)
    controlador.iniciar_turno()
    
    # Continue implementando a lógica de jogo conforme necessário
    print("Jogo da Pandemia iniciado com sucesso!")

if __name__ == "__main__":
    main()
