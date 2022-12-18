from collections import defaultdict
import numpy as np
import copy

card_amount=[7, 8, 12, 14, 11, 11]
shopLevel_cost = [5, 7, 8, 9, 11]

class MonteCarloTreeSearchNode():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):      # 안한 행동
        self._untried_actions=self.state.get_legal_actions()
        return self._untried_actions

    def q(self):        # win-loss 리턴
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def number_of_visits(self):
        return self._number_of_visits

    def expand(self):       # generate next node by action
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self): # 마지막 노드인지 확인(마지막 노드면 겜이 끝남)
        return self.state.is_game_over()

    def rollout(self, ran):                      # 모든 액션은 게임 ran까지 확인하기
        current_rollout_state = self.state

        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()

            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action, ran-1)
        return current_rollout_state.game_result()

    def rollout_policy(self, possible_moves):       # 랜덤으로 가능한거 다해보기
        return possible_moves[np.random.randint(len(possible_moves))]

    def backpropagate(self, result):
        self._number_of_visits+=1
        self._results[result]+=1
        if self.parent:     # 부모 노드에 도달할때까지
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions)==0        # 시도 안한 행동이 없다면 true 리턴

    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.number_of_visits()) + c_param * np.sqrt((2 * np.log(self.number_of_visits()) / c.number_of_visits())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def _tree_policy(self):         # rollout을 수행할 노드 결정
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100
        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)

    #1
    def buy(self, state_i, n):
        if state_i[0] >= 3:
            if state_i[4][n] > 0:
                state_i[4][n] -= 1
                state_i[5][n] += 1
                if state_i[5][n] >= 3:
                    state_i[6][n] += 1
                    state_i[5][n] -= 3
                    #GoldenCard
            state_i[0]-=3
        return state_i

    #2
    def levelup(self, state_i):
        if state_i[0] > self.state_i[3]:
            state_i[0]-=state_i[3]
            state_i[3] = shopLevel_cost[state_i[1]]
            state_i[1]+=1

    #3
    def refresh(self):
        tmp_1=


    def get_legal_actions(self):
        '''
        Modify according to your game or
        needs. Constructs a list of all
        possible actions from current state.
        Returns a list.
        '''



    def is_game_over(self):
        '''
        Modify according to your game or
        needs. It is the game over condition
        and depends on your game. Returns
        true or false
        '''

    def game_result(self):
        '''
        Modify according to your game or
        needs. Returns 1 or 0 or -1 depending
        on your state corresponding to win,
        tie or a loss.
        '''

    def move(self, action):
        '''
        Modify according to your game or
        needs. Changes the state of your
        board with a new value. For a normal
        Tic Tac Toe game, it can be a 3 by 3
        array with all the elements of array
        being 0 initially. 0 means the board
        position is empty. If you place x in
        row 2 column 3, then it would be some
        thing like board[2][3] = 1, where 1
        represents that x is placed. Returns
        the new state after making a move.
        '''

if __name__== '__main__':
    f1=open('gamedata.txt', 'r')

    state_t = []
    state_t.append(int(f1.readline().strip()))      # gold
    state_t.append(int(f1.readline().strip()))      # level
    state_t.append(int(f1.readline().strip()))      # player health
    state_t.append(int(f1.readline().strip()))      # levelup gold
    a=list(map(int, f1.readline().strip().split()))
    t=[0]*63
    t[0]=len(a)
    for i in range(0,len(a)):
        t[a[i]]+=1
    state_t.append(t)       # 상점 카드 (원핫인코딩)
    a = list(map(int, f1.readline().strip().split()))
    t = [0] * 63
    t[0] = len(a)
    for i in range(0, len(a)):
        t[a[i]] += 1
    state_t.append(t)   # 전장 일반 카드(원핫인코딩)
    a = list(map(int, f1.readline().strip().split()))
    t = [0] * 63
    t[0] = len(a)
    for i in range(0, len(a)):
        t[a[i]] += 1
    state_t.append(t)  # 전장 골드 카드(원핫인코딩)

    root = MonteCarloTreeSearchNode(state=initial_state)
    selected_node = root.best_action()