# forward algorithm implementation
# study material:
# https://github.com/rain1024/slp2-pdf/blob/master/chapter-wise-pdf/%5B06%5D%20Hidden%20Markov%20and%20Maximum%20Entropy%20Models.pdf
# page 186

import numpy as np
obs1 = [3, 3, 1, 1, 2, 2, 3, 1, 3]
obs2 = [3, 3, 1, 1, 2, 3, 3, 1, 2]

# state-graft
n = [{"name": "hot",1: 0.2, 2: 0.4, 3: 0.4}, {"name": "cold", 1: 0.5, 2: 0.4, 3: 0.1}]
# hh == hot to hot, cc == cold to cold
transition = {"hh": 0.7, "cc": 0.6, "hc": 0.3, "ch": 0.4, "hot": 0.8, "cold": 0.2}


def viterbi_algo(obs, n):
    # probability matrix
    viterbi = np.zeros([len(n), len(obs)])
    backpointer = []
    # initialization step
    for s in range(len(n)):
        viterbi[s][0] = transition[n[s]["name"]] * n[s][obs[0]]
    if viterbi[0][0] > viterbi[0][1]:
        backpointer.append("hot")
    else:
        backpointer.append("cold")
    # recursion step
    # each time step
    for t in range(len(obs))[1:]:
        # for each state
        for s in range(len(n)):
            # if s is hot
            if s == 0:
                hh = viterbi[0][t - 1] * transition["hh"] * n[s][obs[t]]
                ch = viterbi[1][t - 1] * transition["ch"] * n[s][obs[t]]
                # p(current) = max(p(previous) * p(transition) * p(the number in the state))
                viterbi[s][t] = max(hh, ch)
            # else s is cold
            else:
                hc = viterbi[0][t - 1] * transition["hc"] * n[s][obs[t]]
                cc = viterbi[1][t - 1] * transition["cc"] * n[s][obs[t]]
                viterbi[s][t] = max(hc, cc)
        # record the state by selecting the max probability
        if viterbi[0][t] > viterbi[1][t]:
            backpointer.append("hot")
        else:
            backpointer.append("cold")
    print(f"The weather sequence for observation {obs} is {backpointer}")


viterbi_algo(obs1, n)
viterbi_algo(obs2, n)
