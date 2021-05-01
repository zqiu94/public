# Given a string s, find the longest palindromic subsequence's length in s.

# A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without
# changing the order of the remaining elements.


def longest_palindrome_subsequence(s):
    n = len(s)
    c = []
    r = []
    for i in range(n):
        r.append(0)
    for i in range(n):
        # make r a reversed list of s
        r[i - 1] = s[-i]
    for i in range(n + 1):
        col = []
        for j in range(n + 1):
            col.append(0)
        c.append(col)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            # a match is found
            if s[i - 1] == r[j - 1]:
                c[j][i] = c[j - 1][i - 1] + 1
            # take the max from its upper of left neighbor
            elif c[j - 1][i] >= c[j][i - 1]:
                c[j][i] = c[j - 1][i]
            else:
                c[j][i] = c[j][i - 1]
    # return the last cell
    return c[j][i]


s = "bbbab"
print(longest_palindrome_subsequence(s))

s = "cbbd"
print(longest_palindrome_subsequence(s))
