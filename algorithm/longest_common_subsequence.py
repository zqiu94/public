# Given two strings text1 and text2, return the length of their longest common subsequence.
# If there is no common subsequence, return 0.

# A subsequence of a string is a new string generated from the original string with some characters (can be none)
# deleted without changing the relative order of the remaining characters.

# For example, "ace" is a subsequence of "abcde".
# A common subsequence of two strings is a subsequence that is common to both strings

def longest_common_subsequence(text1, text2):
    m = len(text1)
    n = len(text2)
    c = []
    for i in range(n + 1):
        col = []
        for j in range(m + 1):
            col.append(0)
        c.append(col)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                c[j][i] = c[j - 1][i - 1] + 1
            elif c[j - 1][i] >= c[j][i - 1]:
                c[j][i] = c[j - 1][i]
            else:
                c[j][i] = c[j][i - 1]
    return c[j][i]


text1 = "abcde"
text2 = "ace"
print(longest_common_subsequence(text1, text2))

text1 = "abc"
text2 = "abc"
print(longest_common_subsequence(text1, text2))

text1 = "abc"
text2 = "def"
print(longest_common_subsequence(text1, text2))
