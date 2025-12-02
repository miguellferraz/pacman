from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class MinimaxAgent(Agent): 
    
    def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2'):
        self.index = 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


    def getAction(self, gameState: GameState):
        """
        Método principal que inicia a busca Minimax.
        Retorna a melhor AÇÃO do Pac-Man (Agente 0) no estado atual.
        """

        def minimax(state, agentIndex, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state) 
            
            legalActions = state.getLegalActions(agentIndex)
            
            if not legalActions:
                return self.evaluationFunction(state) 

            numAgents = state.getNumAgents()
            
            if agentIndex == (numAgents - 1): 
                nextAgent = self.index       
                nextDepth = depth + 1       
            else: 
                nextAgent = agentIndex + 1   
                nextDepth = depth           

            if agentIndex == self.index: 
                
                max_value = -float('inf') 
                
                is_root = (depth == 0) 
                if is_root:
                    best_action = Directions.STOP 

                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(successor, nextAgent, nextDepth)
                    
                    if score > max_value:
                        max_value = score
                        if is_root:
                            best_action = action 
                
                return best_action if is_root else max_value

            else: 
                
                min_value = float('inf')

                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(successor, nextAgent, nextDepth)
                    
                    if score < min_value:
                        min_value = score
                        
                return min_value

        return minimax(gameState, self.index, 0) 


def betterEvaluationFunction(currentGameState: GameState):
    """
    Função de avaliação heurística corrigida para incentivar o movimento 
    (busca por comida) e evitar o estado de parada.
    """
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()

    foodDistances = [manhattanDistance(pos, f) for f in food]
    minFoodDistance = min(foodDistances) if len(foodDistances) > 0 else 0 
    
    if len(food) > 0:
        food_seeking_term = (1.0 / (minFoodDistance + 1)) * 5.0 
        food_count_penalty = -2.0 * len(food)
    else:
        food_seeking_term = 0
        food_count_penalty = 0

    ghost_interaction_term = 0
    
    for ghostState in ghostStates:
        ghostPos = ghostState.getPosition()
        ghostDistance = manhattanDistance(pos, ghostPos)
        scaredTime = ghostState.scaredTimer
        
        if ghostDistance == 0: 
             ghost_interaction_term += -float('inf') 
             continue

        if scaredTime == 0:
            if ghostDistance <= 5: 
                ghost_interaction_term += -2.5 / (ghostDistance) 
            
        else:
            ghost_interaction_term += 1.5 / (ghostDistance)
            if scaredTime < 5:
                 ghost_interaction_term += scaredTime / (ghostDistance * 2.0)
            
    if len(capsules) > 0:
        capsuleDistances = [manhattanDistance(pos, c) for c in capsules]
        minCapsuleDistance = min(capsuleDistances)
        capsule_bonus = 10.0 / (minCapsuleDistance + 1)
    else:
        capsule_bonus = 0
            
    score_base = currentGameState.getScore()

    return (score_base 
            + food_seeking_term 
            + food_count_penalty 
            + ghost_interaction_term 
            + capsule_bonus)

better = betterEvaluationFunction
