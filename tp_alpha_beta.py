import random
class State:
    def __init__(self, pieces=None, enemy_pieces=None):
        self.pieces = pieces if pieces != None else [0]*9
        self.enemy_pieces = enemy_pieces if enemy_pieces != None else [0]*9
    def piece_count(self,pieces):
        cnt = 0
        for i in pieces:
            if i == 1:
                cnt+=1
        return cnt
    def is_lose(self):
        def comp(x, y, dx, dy):
            for _ in range(3):
                if y<0 or y>2 or x<0 or x>2 or self.enemy_pieces[x+y*3]==0:
                    return False
                x+=dx
                y+=dy
            return True
        if comp(0,0,1,1) or comp(0,2,1,-1):
            return True
        for i in range(3):
            if comp(0,i,1,0) or comp(i,0,0,1):return True
        return False
    def is_draw(self):
        if self.piece_count(self.pieces) + self.piece_count(self.enemy_pieces)==9:
            return True
        else:
            return False
    def is_end(self):
        return self.is_draw() or self.is_lose()
    def next(self, action):
        pieces = self.pieces.copy()
        pieces[action] = 1
        return State(self.enemy_pieces, pieces)
    def legal_actions(self):
        can = []
        for i in range(9):
            if self.pieces[i]==0 and self.enemy_pieces[i]==0:
                can.append(i)
        return can
    def is_first(self):
        return self.piece_count(self.pieces)==self.piece_count(self.enemy_pieces)
    def __str__(self):
        p = ('o','x') if self.is_first() else ('x','o')
        grid=''
        for i in range(9):
            if self.pieces[i]==1:
                grid+=p[0]
            elif self.enemy_pieces[i]==1:
                grid+=p[1]
            else:
                grid+='-'
            if i%3==2:
                grid+='\n'
        return grid
######################
def random_action(state):
    can_ac = state.legal_actions()
    return can_ac[random.randint(0,len(can_ac)-1)]
######################
def alpha_beta(state,alpha,beta):
    if state.is_lose():
        return -1
    if state.is_draw():
        return 0
    for ac in state.legal_actions():
        sc = -alpha_beta(state.next(ac), -beta, -alpha)
        if sc > alpha:
            alpha = sc
        if alpha >= beta:
            return alpha
    return alpha
def alpha_beta_ac(state):
    best_ac = 0
    INF=10**9
    alpha = -INF
    for ac in state.legal_actions():
        sc = -alpha_beta(state.next(ac), -INF, -alpha)
        if sc > alpha:
            best_ac = ac
            alpha = sc
    return best_ac
####################
state = State()
while True:
    if state.is_end():
        break
    if state.is_first():
        ac = alpha_beta_ac(state)
    else:
        ac = random_action(state)
    state = state.next(ac)
    print(state)
    print("--------------")