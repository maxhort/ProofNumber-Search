import numpy as np
from random import getrandbits,seed
from functools import reduce
import operator
seed(0)
fields  = [(x,y) for x in range(6) for y in range(7)]
values = [-1,1]
ranVals = dict(((f,v),getrandbits(64)) for f in fields for v in values)
class Game:

    def __init__(self,hash_size = 64,hash_code = 20):		
        self.board = np.zeros((6,7))
        self.board = self.board.astype(int)
        self.currentPlayer = 1
        self.opponent = - 1
        self.gameState = GameState(self.board, self.currentPlayer)
        self.pieces = {'1':'X', '0': '-', '-1':'O'}
        self.grid_shape = (6,7)
        self.name = 'connect4'
        
    def reset(self):
        self.board = np.zeros((6,7))
        self.board = self.board.astype(int)
        self.currentPlayer = 1
        self.opponent = - 1
        self.gameState = GameState(self.board, self.currentPlayer)
        return self.gameState

    # def step(self, action):
    #     next_state, value, done = self.gameState.takeAction(action)
    #     self.gameState = next_state
    #     self.currentPlayer, self.opponent = self.opponent,self.currentPlayer
    #     info = None
    #     return ((next_state, value, done, info))




class GameState():
    def __init__(self, board, playerTurn,hash_size = 64, hash_code = 20):
        self.pieces = {'1':'X', '0': '-', '-1':'O'}
        self.rows = 6
        self.columns = 7
        self.win_length = 4
        self.board = board
        self.playerTurn = playerTurn
        self.opponent = -1 * playerTurn
        self.id = self._convertStateToId()
        
        self.hash_size = hash_size
        self.hash_code = hash_code
        # self.fields  = [(x,y) for x in range(self.rows) for y in range(self.columns)]
        # self.values = [-1,1]
        # self.ranVals = dict(((f,v),getrandbits(self.hash_size)) for f in self.fields for v in self.values)
        #self.allowedActions = self._allowedActions()

    def allowed_actions(self):
        return np.where(self.board[0]==0)[0]

    def _convertStateToId(self):
        player1_position = np.zeros(self.board.shape, dtype=np.int)
        player1_position[self.board==1] = 1

        other_position = np.zeros(self.board.shape, dtype=np.int)
        other_position[self.board==-1] = 1

        position = np.append(player1_position.flatten(),other_position.flatten())

        id = ''.join(map(str,position))

        return id
        
    def check_for_win(self,piece):
        required = [piece for _ in range(self.win_length)]
        # horizontal
        for r in range(self.rows):
            for c in range(self.columns-self.win_length+1):
                if np.all(self.board[r,c:c+self.win_length] == required): return 1
        # vertical
        for c in range(self.columns):
            for r in range(self.rows-self.win_length+1):
                if np.all(self.board[r:self.win_length+r,c] == required): return 1
        # diagonal
        for c in range(self.columns-self.win_length+1):
            for r in range(self.rows-self.win_length+1):
                if np.all(self.board[[r+x for x in range(self.win_length)],[c+x for x in range(self.win_length)]] == required): return True
                if np.all(self.board[[self.rows-1-r-x for x in range(self.win_length)],
                            [c+x for x in range(self.win_length)]] == required): return 1
        return 0

    def check_draw(self):
        if np.sum(self.board!=0) == (self.rows*self.columns):
            return True
        return False
    def perform_action(self, action):
        #row = 6-1-np.argmin(self.board[:,action][::-1])
        row = np.max(np.where(self.board[:,action]==0))
        newBoard = np.array(self.board)
        newBoard[row][action]=self.playerTurn
        
        #newState = GameState(newBoard, self.opponent)
        return GameState(newBoard, self.opponent)
    def compute_hash(self):
        stones1_r,stones1_c = np.where(self.board == 1)
        stones2_r,stones2_c = np.where(self.board == -1)
        zxor = reduce(operator.xor, [ranVals[((r,c),1)] for r,c in zip(stones1_r,stones1_c)]
                            +[ranVals[((r,c),-1)] for r,c in zip(stones2_r,stones2_c)], 0)
        hashkey = zxor >> self.hash_code
        mask = ((1 << self.hash_code)-1)
        hashcode = zxor & mask
        return hashcode, hashkey
        #binHash = '{1:0{0}b}'.format(self.hash_size,zxor)
        #return binHash[:self.hash_code],binHash[self.hash_code:]