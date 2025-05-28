# main.py
from jogo import PandemicGame

if __name__ == "__main__":
    # O jogo é um Singleton, então sempre pegamos a mesma instância
    jogo = PandemicGame()
    jogo.run()