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
                [span_0](start_span)return self.evaluationFunction(state) #[span_0](end_span)
            
            # Obtém as ações legais para o agente atual
            legalActions = state.getLegalActions(agentIndex)
            
            # Se não houver ações legais disponíveis em um estado não terminal (caso extremo)
            if not legalActions:
                [span_1](start_span)return self.evaluationFunction(state) #[span_1](end_span)


            # 2. Gerenciamento de Agentes e Profundidade
            numAgents = state.getNumAgents()
            
            # Lógica para o próximo agente e a próxima profundidade
            [span_2](start_span)[span_3](start_span)if agentIndex == (numAgents - 1): # Se for o último fantasma (fim de uma 'ply')[span_2](end_span)[span_3](end_span)
                [span_4](start_span)nextAgent = self.index # Próximo é o Pac-Man (agente 0)[span_4](end_span)
                [span_5](start_span)nextDepth = depth + 1  # A profundidade aumenta[span_5](end_span)
            [span_6](start_span)else: # Se for o Pac-Man ou um fantasma intermediário[span_6](end_span)
                nextAgent = agentIndex + 1 # Próximo agente na sequência
                nextDepth = depth          # A profundidade se mantém


            # 3. Lógica de Maximização (Pac-Man: agentIndex == 0)
            [span_7](start_span)if agentIndex == self.index: # self.index é sempre 0 (Pac-Man)[span_7](end_span)
                
                # [span_8](start_span)Inicializa o valor máximo com -infinito[span_8](end_span)
                max_value = -float('inf') 
                
                # Para o nível mais externo (top-level call), rastreamos a melhor ação
                [span_9](start_span)best_action = Directions.STOP # Inicializa a melhor ação[span_9](end_span)
                
                # [span_10](start_span)Itera sobre todas as ações possíveis[span_10](end_span)
                for action in legalActions:
                    # [span_11](start_span)Gera o estado sucessor[span_11](end_span)
                    successor = state.generateSuccessor(agentIndex, action)
                    
                    # [span_12](start_span)Chamada recursiva para obter o score[span_12](end_span)
                    score = minimax(successor, nextAgent, nextDepth)
                    
                    # [span_13](start_span)Se o score for melhor, atualiza o valor máximo e a ação[span_13](end_span)
                    if score > max_value:
                        max_value = score
                        best_action = action 
                
                # Se for a chamada inicial (depth == 0), retorna a melhor AÇÃO
                [span_14](start_span)if depth == 0: #[span_14](end_span)
                    return best_action
                # Se for uma chamada recursiva, retorna apenas o VALOR
                [span_15](start_span)else: #[span_15](end_span)
                    return max_value

            # 4. Lógica de Minimização (Fantasmas: agentIndex > 0)
            [span_16](start_span)[span_17](start_span)else: # Fantasma: jogador minimizador[span_16](end_span)[span_17](end_span)
                
                # [span_18](start_span)Inicializa o valor mínimo com +infinito[span_18](end_span)
                min_value = float('inf')

                # [span_19](start_span)Itera sobre todas as ações possíveis[span_19](end_span)
                for action in legalActions:
                    # [span_20](start_span)Gera o estado sucessor[span_20](end_span)
                    successor = state.generateSuccessor(agentIndex, action)
                    
                    # [span_21](start_span)Chamada recursiva para obter o score[span_21](end_span)
                    score = minimax(successor, nextAgent, nextDepth)
                    
                    # [span_22](start_span)Se o score for pior para o Pac-Man, atualiza o valor mínimo[span_22](end_span)
                    if score < min_value:
                        min_value = score
                        
                # [span_23](start_span)Retorna apenas o valor (score)[span_23](end_span)
                return min_value

        # Chamada inicial: Pac-Man (self.index/0), profundidade 0.
        # A função getAction deve retornar o valor que for a AÇÃO
        # (graças ao "if depth == 0: return best_action" dentro de minimax).
        [span_24](start_span)[span_25](start_span)return minimax(gameState, self.index, 0) #[span_24](end_span)[span_25](end_span)


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

