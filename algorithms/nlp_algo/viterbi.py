# learning material:
# http://cecas.clemson.edu/~ahoover/ece854/refs/Gonze-ViterbiAlgorithm.pdf

# sequence
S = "AACGCTTGG"
state = ""
# log probabilities of A, C, G, T in H state
H = {"A": -2.322, "C": -1.737, "G": -1.737, "T": -2.322}
# log probabilities of A, C, G, T in L state
L = {"A": -1.737, "C": -2.322, "G": -2.322, "T": -1.737}
# transition probabilities
TP = {"LL": -0.737, "HH": -1, "LH": -1.322, "HL": -1, "SH": -1, "SL": -1}

# probability of the state of the first character
PH = TP["SH"] + H[S[0]]
PL = TP["SL"] + L[S[0]]

# record the state by selecting the max probability
if PH > PL:
    state += "H"
else:
    state += "L"

for c in S[1:]:
    # make a copy of the last PH and PL
    PH_copy = PH
    PL_copy = PL
    # probability of that character in the state, multiplied by the max of the previous probability and the probability
    # of the transition to the state
    PH = H[c] + max((PH_copy + TP["HH"]), (PL_copy + TP["LH"]))
    PL = L[c] + max((PH_copy + TP["HL"]), (PL_copy + TP["LL"]))
    # record the state by selecting the max probability
    if PH > PL:
        state += "H"
    else:
        state += "L"

print(state)
