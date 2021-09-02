import random
import math
class State:
    def __init__(self, pieces=None, enemy_pieces=None, depth=0):
        self.dxy = ((1,0), (1,1), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1))
        self.pass_end = False
        self.pieces = pieces
        self.enemy_pieces = enemy_pieces
        self.depth = depth
        if pieces == None or enemy_pieces == None:
            self.pieces = [0]*64
            self.enemy_pieces = [0]*64
            self.pieces[27] = self.pieces[36] = 1
            self.enemy_pieces = [0]*64
            self.enemy_pieces[28] = self.enemy_pieces[35] = 1
    def piece_count(self, pieces):
        cnt = 0
        for i in pieces:
            cnt+=i
        return cnt
    def is_lose(self):
        return self.is_end() and self.piece_count(self.pieces)<self.piece_count(self.enemy_pieces)
    def is_draw(self):
        return self.is_end() and self.piece_count(self.pieces)==self.piece_count(self.enemy_pieces)
    def is_end(self):
        return self.piece_count(self.pieces)+self.piece_count(self.enemy_pieces)==64 or self.pass_end
    def next(self, action):
        state = State(self.pieces.copy(), self.enemy_pieces.copy(), self.depth+1)
        if action!=64:
            state.is_legal_action_xy(action%8, action//8,True)
        tmp = state.pieces
        state.pieces = state.enemy_pieces
        state.enemy_pieces = tmp
        if action==64 and state.legal_actions()==[64]:
            state.pass_end=True
        return state
    def legal_actions(self):
        actions = []
        for j in range(8):
            for i in range(8):
                if self.is_legal_action_xy(i, j):
                    actions.append(i+j*8)
        if not actions:
            actions.append(64)
        return actions
    def is_legal_action_xy(self, x, y, flip=False):
        def is_legal_action_xy_dxy(x,y,dx,dy):
            x+=dx; y+=dy
            if y<0 or y>7 or x<0 or x>7 or self.enemy_pieces[x+y*8]!=1:
                return False
            for j in range(8):
                if y<0 or y>7 or x<0 or x>7 or \
                    (self.enemy_pieces[x+y*8]==0 and self.pieces[x+y*8]==0):
                    return False
                if self.pieces[x+8*y]==1:
                    if flip:
                        for i in range(8):
                            x-=dx; y-=dy
                            if self.pieces[x+y*8]==1:
                                return True
                            self.pieces[x+y*8]=1
                            self.enemy_pieces[x+y*8]=0
                    return True
                x+=dx; y+=dy
            return False
        if self.enemy_pieces[x+y*8]==1 or self.pieces[x+y*8]==1:
            return False
        if flip:
            self.pieces[x+y*8] = 1
        flg = False
        for dx,dy in self.dxy:
            if is_legal_action_xy_dxy(x, y, dx, dy):
                flg=True
        return flg
    def is_first_player(self):
        return self.depth%2==0
    def __str__(self):
        p = ('o','x') if self.is_first_player() else ('x','o')
        grid = ''
        for i in range(64):
            if self.pieces[i]==1:
                grid += p[0]
            elif self.enemy_pieces[i]==1:
                grid += p[1]
            else:
                grid += '-'
            if i%8==7:
                grid+='\n'
        return grid
##############################################
def random_ac(state):
    can = state.legal_actions()
    return can[random.randint(0,len(can)-1)]
################################################
if __name__=='__main__':
    state = State()
    while True:
        if state.is_end():
            break
        state = state.next(random_ac(state))
        print(state)
        print('-----------------')