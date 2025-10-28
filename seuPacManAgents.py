from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState
from multiAgents import MultiAgentSearchAgent


class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState: GameState):
        """
        Método principal que inicia a busca Minimax.
        Retorna a melhor AÇÃO do Pac-Man (Agente 0) no estado atual.
        """

        def minimax(state, agentIndex, depth):
            # 1. CONDIÇÃO DE PARADA (Nó Terminal/Folha)
            # A recursão para se o jogo acabou (Vitória/Derrota) ou se a profundidade máxima foi alcançada.
            # Nesses casos, o valor da heurística (função de avaliação) é retornado.
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state) 
            
            # Obtém as ações possíveis para o agente atual
            legalActions = state.getLegalActions(agentIndex)
            
            # Caso extremo: se não houver movimentos legais (ex: encurralado), retorna a avaliação.
            if not legalActions:
                return self.evaluationFunction(state) 


            # 2. GERENCIAMENTO DE AGENTES E PROFUNDIDADE
            numAgents = state.getNumAgents()
            
            # A profundidade só avança quando todos os agentes tiveram sua vez.
            if agentIndex == (numAgents - 1): # É o último fantasma? (Fim de uma rodada completa)
                nextAgent = self.index       # O próximo a jogar é o Pac-Man (Agente 0).
                nextDepth = depth + 1        # Incrementa o nível de profundidade.
            else: 
                nextAgent = agentIndex + 1   # Passa para o próximo agente (Fantasma seguinte).
                nextDepth = depth            # A profundidade permanece a mesma.


            # 3. LÓGICA DE MAXIMIZAÇÃO (Turno do Pac-Man: agentIndex == 0)
            if agentIndex == self.index: # O Pac-Man (Agente Max) busca a melhor pontuação.
                
                # Inicializa a melhor pontuação encontrada (Max Value) com -infinito
                max_value = -float('inf') 
                
                # Apenas o nó raiz (depth=0) precisa armazenar a ação que levou ao melhor score.
                if depth == 0:
                    best_action = Directions.STOP # Inicializa a melhor ação (pode ser qualquer valor válido)
                
                # Itera sobre as ações e chama a recursão para os sucessores
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(successor, nextAgent, nextDepth)
                    
                    # Atualiza a melhor pontuação e a ação correspondente
                    if score > max_value:
                        max_value = score
                        # Se estiver no nó raiz, guarda a ação
                        if depth == 0:
                            best_action = action 
                
                # Retorna a AÇÃO (se for o nó raiz) ou o VALOR (para chamadas recursivas internas)
                return best_action if depth == 0 else max_value

            # 4. LÓGICA DE MINIMIZAÇÃO (Turno dos Fantasmas: agentIndex > 0)
            else: # O Fantasma (Agente Min) busca a pior pontuação para o Pac-Man.
                
                # Inicializa o pior score para o Pac-Man (Min Value) com +infinito
                min_value = float('inf')

                # Itera sobre todas as ações do fantasma para encontrar o pior cenário
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(successor, nextAgent, nextDepth)
                    
                    # Encontra o score mínimo
                    if score < min_value:
                        min_value = score
                        
                # Retorna o valor mínimo (o pior que o Pac-Man pode esperar deste nó)
                return min_value

        # Inicia a busca Minimax a partir do estado atual (Agente 0, Profundidade 0)
        return minimax(gameState, self.index, 0) 


def betterEvaluationFunction(currentGameState: GameState):
    # Esta é a função de avaliação padrão, que será substituída por sua versão
    # otimizada para melhor desempenho (evitar o Pac-Man de parar).
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()

    # Calcula a distância de Manhattan para a comida mais próxima
    foodDistances = [manhattanDistance(pos, f) for f in food]
    if len(foodDistances) > 0:
        minFoodDistance = min(foodDistances)
    else:
        minFoodDistance = 0

    # Distância para o fantasma mais próximo
    ghostDistances = [manhattanDistance(pos, ghost.getPosition()) for ghost in ghostStates]
    minGhostDistance = min(ghostDistances)

    # Lógica para Fantasmas Assustados: Ignora a distância se o fantasma estiver assustado.
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    if min(scaredTimes) > 0:
        minGhostDistance = 0  # Ignora fantasmas assustados

    return currentGameState.getScore() - (1.5 / (minFoodDistance + 1)) + (2 / (minGhostDistance + 1))

# Abbreviation
better = betterEvaluationFunction