# 🤖 Projeto Pac-Man: Implementação do Algoritmo Minimax

Este projeto consiste na implementação do algoritmo de busca adversária Minimax para controlar o agente Pac-Man em um ambiente de jogo com fantasmas (agentes minimizadores).

O objetivo principal é demonstrar a compreensão dos conceitos de maximização e minimização, permitindo que o Pac-Man tome decisões estratégicas ao antecipar os movimentos ideais dos fantasmas.

---

## 👨‍💻 Participantes

* **Miguel Carneiro Lira Ferraz** | Matrícula: 22401150
* **Rafael Pinatto Lahr** | Matrícula: 22400897
* **Samuel Pereira Lima** | Matrícula: 22402066
* **Lucas Vilas Boas** | Matrícula: 2240

---

## 🚀 Como Rodar o Código

O código principal do algoritmo Minimax está implementado na classe `MinimaxAgent` dentro do arquivo `seuPacManAgents.py`.

Para executar o jogo Pac-Man usando o seu agente Minimax, abra o terminal no diretório raiz do projeto e use o seguinte comando:

### 1. Comando Básico

Este comando roda o jogo com o `MinimaxAgent` usando a profundidade de busca padrão (que é 3, conforme a classe `MultiAgentSearchAgent`).

```bash
python pacman.py --pacman MinimaxAgent