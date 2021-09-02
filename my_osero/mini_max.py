from game import State
def mini_max(state,depth=0):
    if depth>=3:
        gain = [( 30, -12,  0, -1, -1,  0, -12,  30), \
            (-12, -15, -3, -3, -3, -3, -15, -12), \
            (  0,  -3,  0, -1, -1,  0,  -3,   0), \
            ( -1,  -3, -1, -1, -1, -1,  -3,  -1), \
            ( -1,  -3, -1, -1, -1, -1,  -3,  -1), \
            (  0,  -3,  0, -1, -1,  0,  -3,   0), \
            (-12, -15, -3, -3, -3, -3, -15, -12), \
            ( 30, -12,  0, -1, -1,  0, -12,  30)]
        sc=0
        for i in range(64):
            if state.pieces[i]:
                sc+=gain[i//8][i%8]
        return sc
    if state.is_lose():
        return -100
    if state.is_draw():
        return 0
    best_sc = -10**9
    for ac in state.legal_actions():
        sc = -mini_max(state.next(ac),depth+1)
        if sc>best_sc:
            best_sc=sc
    return best_sc
def mini_max_ac(state):
    best_sc=-10**9
    best_ac=0
    for ac in state.legal_actions():
        sc = -mini_max(state.next(ac),0)
        if sc>best_sc:
            best_sc=sc
            best_ac=ac
    return ac