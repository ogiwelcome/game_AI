from game import State
from dual_network import dual_network
from math import sqrt
from tensorflow.keras.models import load_model
from pathlib import Path
import numpy as np

PV_EVALUATE_COUNT = 50

def predict(model, state):
    a, b, c = DN_INPUT_SHAPE
    x = np.array([state.pieces,state.enemy_pieces])
    x = reshape(c,a,b).transpose(1,2,0).reshape(1,a,b,c)
    y = model.predict(x,batch_size=1)
    policies = y[0][0][list(state.legal_actions())]
    policies /= sum(policies) if sum(policies) else 1
    val = y[1][0][0]
    return policies,val
def nodes_to_scores(nodes):
    scores = []
    for c in nodes:
        scores.append(c.n)
    return scores
def pv_mcts_scores(model, state, temperature):
    class node:
        