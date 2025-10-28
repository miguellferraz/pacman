from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState
from multiAgents import MultiAgentSearchAgent


class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState: GameState):
        """
        Calcula a melhor ação para o Pac-Man (agente 0) usando o algoritmo Minimax.
        A função retorna a ação, enquanto a função aninhada 'minimax' retorna o valor (score).
        """

        def minimax(state, agentIndex, depth):
            # 1. Condição de Parada (Base Case)
            # O algoritmo para se o jogo terminou (vitória/derrota) ou se a profundidade máxima foi atingida.
            # O valor do estado é retornado usando a função de avaliação.
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state) # [cite: 223, 224, 225]
            
            # Obtém as ações legais para o agente atual
            legalActions = state.getLegalActions(agentIndex)
            
            # Se não houver ações legais disponíveis em um estado não terminal (caso extremo)
            if not legalActions:
                return self.evaluationFunction(state) # [cite: 278]


            # 2. Gerenciamento de Agentes e Profundidade
            numAgents = state.getNumAgents()
            
            # Lógica para o próximo agente e a próxima profundidade
            if agentIndex == (numAgents - 1): # Se for o último fantasma (fim de uma 'ply') [cite: 229, 230, 231, 235]
                nextAgent = self.index # Próximo é o Pac-Man (agente 0) [cite: 231]
                nextDepth = depth + 1  # A profundidade aumenta [cite: 234]
            else: # Se for o Pac-Man ou um fantasma intermediário [cite: 232]
                nextAgent = agentIndex + 1 # Próximo agente na sequência
                nextDepth = depth          # A profundidade se mantém


            # 3. Lógica de Maximização (Pac-Man: agentIndex == 0)
            if agentIndex == self.index: # self.index é sempre 0 (Pac-Man) [cite: 272]
                
                # Inicializa o valor máximo com -infinito [cite: 238]
                max_value = -float('inf') 
                
                # Para o nível mais externo (top-level call), rastreamos a melhor ação
                best_action = Directions.STOP # Inicializa a melhor ação [cite: 239]
                
                # Itera sobre todas as ações possíveis [cite: 240]
                for action in legalActions:
                    # Gera o estado sucessor [cite: 242]
                    successor = state.generateSuccessor(agentIndex, action)
                    
                    # Chamada recursiva para obter o score [cite: 243, 244]
                    score = minimax(successor, nextAgent, nextDepth)
                    
                    # Se o score for melhor, atualiza o valor máximo e a ação [cite: 245]
                    if score > max_value:
                        max_value = score
                        best_action = action 
                
                # Se for a chamada inicial (depth == 0), retorna a melhor AÇÃO
                if depth == 0: # [cite: 246, 247]
                    return best_action
                # Se for uma chamada recursiva, retorna apenas o VALOR
                else: # 
                    return max_value

            # 4. Lógica de Minimização (Fantasmas: agentIndex > 0)
            else: # Fantasma: jogador minimizador [cite: 193, 249]
                
                # Inicializa o valor mínimo com +infinito [cite: 250]
                min_value = float('inf')

                # Itera sobre todas as ações possíveis [cite: 251, 252]
                for action in legalActions:
                    # Gera o estado sucessor [cite: 253]
                    successor = state.generateSuccessor(agentIndex, action)
                    
                    # Chamada recursiva para obter o score [cite: 254, 255]
                    score = minimax(successor, nextAgent, nextDepth)
                    
                    # Se o score for pior para o Pac-Man, atualiza o valor mínimo [cite: 256]
                    if score < min_value:
                        min_value = score
                        
                # Retorna apenas o valor (score) [cite: 257]
                return min_value

        # Chamada inicial: Pac-Man (self.index/0), profundidade 0.
        # A função getAction deve retornar o valor que for a AÇÃO
        # (graças ao "if depth == 0: return best_action" dentro de minimax).
        return minimax(gameState, self.index, 0) # [cite: 246, 272]


def betterEvaluationFunction(currentGameState: GameState):
    # ... (A função betterEvaluationFunction já está implementada no seu arquivo e não precisa ser alterada)
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

    # Aumenta a pontuação se o fantasma estiver assustado, mas penaliza se estiver muito perto
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    if min(scaredTimes) > 0:
        minGhostDistance = 0  # Ignora fantasmas assustados

    return currentGameState.getScore() - (1.5 / (minFoodDistance + 1)) + (2 / (minGhostDistance + 1))

# Abbreviation
better = betterEvaluationFunction
