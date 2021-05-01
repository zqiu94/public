# Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.

# You have the following three operations permitted on a word:

# Insert a character
# Delete a character
# Replace a character


def min_distance(word1, word2):
    m = len(word1)
    n = len(word2)
    c = []
    for i in range(n + 1):
        col = []
        for j in range(m + 1):
            col.append(0)
        c.append(col)
    for i in range(m + 1):
        c[0][i] = i
    for j in range(n + 1):
        c[j][0] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                diff = 0
            else:
                diff = 1
            # from the lecture slides
            c[j][i] = min(c[j][i - 1] + 1, c[j - 1][i] + 1, c[j - 1][i - 1] + diff)
    return c[j][i]


word1 = "horse"
word2 = "ros"
min_distance(word1, word2)

word1 = "intention"
word2 = "execution"
min_distance(word1, word2)
