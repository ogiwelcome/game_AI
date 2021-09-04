from game import State
def alpha_beta(state,alpha,beta,depth):
    if depth>=5:
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
    best_sc = 0
    for ac in state.legal_actions():
        sc = -alpha_beta(state.next(ac),-beta,-alpha,depth+1)
        if sc>alpha:
            alpha=sc
        if alpha>=beta:
            return alpha
    return alpha
def alpha_beta_ac(state):
    best_ac = 64 # default:pass
    INF = 10**9
    alpha = -INF
    for ac in state.legal_actions():
        sc = -alpha_beta(state, -INF, -alpha, depth=0)
        if sc > alpha:
            best_ac = ac
            alpha = sc
    return best_ac