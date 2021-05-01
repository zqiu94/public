# forward algorithm implementation
# study material:
# https://github.com/rain1024/slp2-pdf/blob/master/chapter-wise-pdf/%5B06%5D%20Hidden%20Markov%20and%20Maximum%20Entropy%20Models.pdf
# page 183

import numpy as np
obs1 = [3, 3, 1, 1, 2, 2, 3, 1, 3]
obs2 = [3, 3, 1, 1, 2, 3, 3, 1, 2]

# state-graft
n = [{"name": "hot",1: 0.2, 2: 0.4, 3: 0.4}, {"name": "cold", 1: 0.5, 2: 0.4, 3: 0.1}]
# hh == hot to hot, cc == cold to cold
transition = {"hh": 0.7, "cc": 0.6, "hc": 0.3, "ch": 0.4, "hot": 0.8, "cold": 0.2}


def forward_algo(obs, n):
    # probability matrix
    forward = np.zeros([len(n), len(obs)])
    # initialization step
    for s in range(len(n)):
        forward[s][0] = transition[n[s]["name"]] * n[s][obs[0]]
    # recursion step
    # each time step
    for t in range(len(obs))[1:]:
        # for each state
        for s in range(len(n)):
            # if s is hot
            if s == 0:
                # p(previous) * p(transition) * p(the number in the state)
                forward[s][t] = forward[0][t - 1] * transition["hh"] * n[s][obs[t]] + forward[1][t - 1] * transition[
                    "ch"] * n[s][obs[t]]
            # else s is cold
            else:
                forward[s][t] = forward[0][t - 1] * transition["hc"] * n[s][obs[t]] + forward[1][t - 1] * transition[
                    "cc"] * n[s][obs[t]]
    np.set_printoptions(formatter={'float': lambda x: "{0:0.5f}".format(x)})
    # since we have no final state, so just add them together
    print(f"The probability of sequence {obs} is {forward[0][-1] + forward[1][-1]} ")


forward_algo(obs1, n)
forward_algo(obs2, n)