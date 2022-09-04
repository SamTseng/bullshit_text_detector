#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Longest Common Subsequence (LCS) by Dynamic Programming  
# This code is contributed by AMAN ASATI
#   from https://www.geeksforgeeks.org/printing-longest-common-subsequence/
# Modified by Yuen-Hsien Tseng on Dec. 07, 2020 in Python

import pprint

def LCS(X, Y):
    m = len(X) # m rows, the assumed longer text to be highlighted
    n = len(Y) # n columns, the text used to match X
    L = [[0 for x in range(n+1)] for x in range(m+1)] 
  
    # Following steps build L[m+1][n+1] in bottom-up fashion. Note 
    # that L[i][j] contains edit distance between X[0..i-1] and Y[0..j-1]  
    for i in range(m+1): 
        for j in range(n+1): 
            if i == 0 or j == 0: 
                L[i][j] = 0
            elif X[i-1] == Y[j-1]: 
                L[i][j] = L[i-1][j-1] + 1
            else: 
                L[i][j] = max(L[i-1][j], L[i][j-1]) 

    Pos = []
    i = m 
    j = n 
    while i > 0 and j > 0: 
        # If current character in X[i-1] and Y[j-1] are the same, then 
        # current character is part of LCS 
        if X[i-1] == Y[j-1]: 
            Pos.append( (i-1, 1) ) #(Xpos, length))
            i -= 1
            j -= 1
        # If not, then find the larger of two and 
        # go in the direction of larger value 
        elif L[i-1][j] > L[i][j-1]: 
            i -= 1
        else: 
            j -= 1

    if len(Pos) == 0:
        return (L, Pos)

    # Merge back Positions:
    # from [(12, 1), (10, 1), (9, 1), (8, 1), (1, 1)]
    # to [(12, 1), (8, 3), (1, 1)]
    Positions = []
    start = Pos[0][0] # or  (start, length) = Pos[0]
    for j in range(1, len(Pos)):
        if Pos[j-1][0] - 1 != Pos[j][0]: # if not a continuous number
            Positions.append( (Pos[j-1][0], start - Pos[j-1][0] + 1) )
            start = Pos[j][0]

    # Process last element
    if start == Pos[-1][0]: # if a new position
        Positions.append(Pos[-1])
    else: # if a continuous position
        Positions.append( (Pos[-1][0], start - Pos[-1][0] + 1) )
    Positions.reverse()
    return (L, Positions)


if (__name__ == '__main__'):
    import sys
    if len(sys.argv) < 3:
        print("Need to specify two arguments: doc and query")
        exit()
    (doc, query) = sys.argv[1:3]

# matchedPos is the desired result to be able to highlight doc
#    (matchedMatrix, matchedPos) = FuzzyMatchPosotions(doc, query)
    (matchedMatrix, matchedPos) = LCS(doc, query)
    #pprint.pprint(matchedMatrix)
    pprint.pprint(matchedPos)
    for pos in matchedPos:
        (p, length) = pos
        print(doc[ p : p + length ])

# python FuzzyHighLight.py 要被highlight的文字 你被light文
#   [(1, 1), (6, 5), (12, 1)]
#   被
#   light
#   文
# python FuzzyHighLight.py 要被highlight的文字 你文light被
#   [(6, 5)]
#   light
# python FuzzyHighLight.py 你文light被 要被highlight的文字
#   [(2, 5)]
#   light
