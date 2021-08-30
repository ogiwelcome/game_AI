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
def playout(state):
    if state.is_lose():
        return -1
    if state.is_draw():
        return 0
    return -playout( state.next(random_action(state)) )
def monte_carlo_ac(state):
    can = state.legal_actions()
    values = [0]*len(can)
    for i,ac in enumerate(can):
        for _ in range(10):
            values[i] += -playout(state.next(ac))
    idx=values.index(max(values))
    return can[idx]
######################
def first_player_point(ended_state):
    if ended_state.is_lose():
        if ended_state.is_first():
            return 0
        else:
            return 1
    return 0.5
def play(next_actions):
    state = State()
    while True:
        if state.is_end():
            break
        next_ac = next_actions[0] if state.is_first() else next_actions[1]
        ac = next_ac(state)
        state = state.next(ac)
    return first_player_point(state)
EP_GAME_COUNT = 100
def evaluate_algorithm(next_actions):
    tot = 0
    for rep in range(EP_GAME_COUNT):
        if rep%2==0:
            tot += play(next_actions)
        else:
            tot+=1-play(list(reversed(next_actions)))
    ave = tot/EP_GAME_COUNT
    return ave
########################
ave_sc = evaluate_algorithm((monte_carlo_ac,random_action))
print(ave_sc)