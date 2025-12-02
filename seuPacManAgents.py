from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState
# Note: MultiAgentSearchAgent não está definido aqui, mas está no arquivo multiAgents.py.
# Assumimos que você a está importando corretamente no seu ambiente de execução.


class MinimaxAgent(Agent): # Herda de Agent, mas espera que seja um MultiAgentSearchAgent no ambiente de teste
    
    # Construtor simplificado (a classe base MultiAgentSearchAgent trata a inicialização real)
    def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman é sempre o agente 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


    def getAction(self, gameState: GameState):
        """
        Método principal que inicia a busca Minimax.
        Retorna a melhor AÇÃO do Pac-Man (Agente 0) no estado atual.
        """

        def minimax(state, agentIndex, depth):
            # 1. CONDIÇÃO DE PARADA (Nó Terminal/Folha)
            # A recursão para se o jogo acabou (Vitória/Derrota) ou se a profundidade máxima foi alcançada.
            if state.isWin() or state.isLose() or depth == self.depth:
                # Retorna o valor da heurística (função de avaliação)
                return self.evaluationFunction(state) 
            
            # Obtém as ações possíveis para o agente atual
            legalActions = state.getLegalActions(agentIndex)
            
            # Caso extremo: se não houver movimentos legais, retorna a avaliação.
            if not legalActions:
                return self.evaluationFunction(state) 


            # 2. GERENCIAMENTO DE AGENTES E PROFUNDIDADE
            numAgents = state.getNumAgents()
            
            # A profundidade só avança quando todos os agentes (Pac-Man + Fantasmas) tiveram sua vez.
            if agentIndex == (numAgents - 1): # É o último fantasma? (Fim de uma rodada completa)
                nextAgent = self.index       # O próximo a jogar é o Pac-Man (Agente 0).
                nextDepth = depth + 1        # Incrementa o nível de profundidade.
            else: 
                nextAgent = agentIndex + 1   # Passa para o próximo agente (Fantasma seguinte).
                nextDepth = depth            # A profundidade permanece a mesma.


            # 3. LÓGICA DE MAXIMIZAÇÃO (Turno do Pac-Man: agentIndex == 0)
            if agentIndex == self.index: # O Pac-Man (Agente Max) busca a melhor pontuação.
                
                max_value = -float('inf') 
                
                # Apenas o nó raiz (depth=0) precisa armazenar a ação que levou ao melhor score.
                # Se for o nó raiz, inicializa a melhor ação para ser retornada
                is_root = (depth == 0) 
                if is_root:
                    best_action = Directions.STOP # Valor inicial, será substituído

                # Itera sobre as ações e chama a recursão para os sucessores
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(successor, nextAgent, nextDepth)
                    
                    # Atualiza a melhor pontuação e a ação correspondente
                    if score > max_value:
                        max_value = score
                        # Se estiver no nó raiz, guarda a ação
                        if is_root:
                            best_action = action 
                
                # Retorna a AÇÃO (se for o nó raiz) ou o VALOR (para chamadas recursivas internas)
                return best_action if is_root else max_value

            # 4. LÓGICA DE MINIMIZAÇÃO (Turno dos Fantasmas: agentIndex > 0)
            else: # O Fantasma (Agente Min) busca a pior pontuação para o Pac-Man.
                
                min_value = float('inf')

                # Itera sobre todas as ações do fantasma para encontrar o pior cenário
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(successor, nextAgent, nextDepth)
                    
                    # Encontra o score mínimo
                    if score < min_value:
                        min_value = score
                        
                # Retorna o valor mínimo 
                return min_value

        # Inicia a busca Minimax a partir do estado atual (Agente 0, Profundidade 0)
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

    # 1. Componente de Distância à Comida (RECOMPENSA)
    # CORREÇÃO: Termo POSITIVO para recompensar a proximidade.
    foodDistances = [manhattanDistance(pos, f) for f in food]
    # Se não houver comida, a distância é 0, mas usamos um número grande (ex: 1000) 
    # para que a recompensa seja baixa, mas o agente ainda prefira se mover.
    minFoodDistance = min(foodDistances) if len(foodDistances) > 0 else 0 
    
    # A inversão (1/d) garante que o valor seja MAIOR quando a distância é MENOR.
    # Usando len(food) como penalidade para evitar que o agente se concentre apenas no ponto mais próximo
    # e ignore o objetivo de limpar o mapa.
    if len(food) > 0:
        food_seeking_term = (1.0 / (minFoodDistance + 1)) * 5.0 # Multiplica por um peso de 5.0
        food_count_penalty = -2.0 * len(food)
    else:
        food_seeking_term = 0
        food_count_penalty = 0

    # 2. Componente de Fantasmas (CUSTO/BENEFÍCIO)
    ghost_interaction_term = 0
    
    for ghostState in ghostStates:
        ghostPos = ghostState.getPosition()
        ghostDistance = manhattanDistance(pos, ghostPos)
        scaredTime = ghostState.scaredTimer
        
        if ghostDistance == 0: # Pac-Man foi comido (estado quase-terminal)
             ghost_interaction_term += -float('inf') 
             continue

        # Ameaça (Fantasma NÃO Assustado)
        if scaredTime == 0:
            # CORREÇÃO: Termo NEGATIVO para penalizar a aproximação. 
            # Peso -2.5: Alta penalidade para evitar a morte.
            if ghostDistance <= 5: # Só penaliza se estiver perigosamente perto
                ghost_interaction_term += -2.5 / (ghostDistance) 
            
        # Oportunidade (Fantasma Assustado)
        else:
            # Termo POSITIVO para recompensar a aproximação. 
            # Peso +1.5: Incentivo para ir atrás do fantasma.
            ghost_interaction_term += 1.5 / (ghostDistance)
            # Adiciona bônus se o fantasma estiver quase acabando o tempo (para caçar rápido)
            if scaredTime < 5:
                 ghost_interaction_term += scaredTime / (ghostDistance * 2.0)
            
    # 3. Componente de Cápsulas (BÔNUS de Busca)
    # Incentivo para buscar cápsulas, pois elas criam oportunidades.
    if len(capsules) > 0:
        capsuleDistances = [manhattanDistance(pos, c) for c in capsules]
        minCapsuleDistance = min(capsuleDistances)
        # Bônus positivo para buscar a cápsula
        capsule_bonus = 10.0 / (minCapsuleDistance + 1)
    else:
        capsule_bonus = 0
            
    # 4. Pontuação Base
    score_base = currentGameState.getScore()

    # Combinação dos termos (o peso alto da comida e da penalidade do fantasma dominam)
    return (score_base 
            + food_seeking_term 
            + food_count_penalty 
            + ghost_interaction_term 
            + capsule_bonus)

# Abbreviation
better = betterEvaluationFunction