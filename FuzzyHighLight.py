#!/usr/bin/python
# -*- coding: UTF-8 -*-

# This code is contributed by BHAVYA JAIN 
#   from https://www.geeksforgeeks.org/printing-longest-common-subsequence/
# Dynamic programming implementation of LCS problem 
# Modified by Yuen-Hsien Tseng on Dec. 07, 2020 in Python

import pprint

# Longest Common Subsequence by Dynamic Programming  
def LCS(X, Y):
    m = len(X)
    n = len(Y) 
    L = [[0 for x in range(n+1)] for x in range(m+1)] 
  
    # Following steps build L[m+1][n+1] in bottom up fashion. Note 
    # that L[i][j] contains length of LCS of X[0..i-1] and Y[0..j-1]  
    for i in range(m+1): 
        for j in range(n+1): 
            if i == 0 or j == 0: 
                L[i][j] = 0
            elif X[i-1] == Y[j-1]: 
                L[i][j] = L[i-1][j-1] + 1
            else: 
                L[i][j] = max(L[i-1][j], L[i][j-1]) 

    Pos = []
    # Start from the right-most-bottom-most corner and 
    # one by one store characters in lcs[] 
    i = m 
    j = n 
    while i > 0 and j > 0: 
        # If current character in X[] and Y are same, then 
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
        if Pos[j-1][0] - 1 != Pos[j][0]: # if not continuous number
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
# python FuzzyHighLight.py "2005 Jan-Feb;20(1):21-34" "f 2005 Jan-Feb;20(1):61"
#   [(0, 19), (20, 1)]
#   2005 Jan-Feb;20(1):
#   1
# python FuzzyHighLight.py 這些辯士們巡走各地藉著論辯來尋求真理。且以雅典為中心，周遊希臘各地，對青年進行修辭、論辯和演說等  辯士們以雅典為中心，周遊希臘各地，對青年進行修辭
# [(2, 3), (20, 21)]
# 辯士們
# 以雅典為中心，周遊希臘各地，對青年進行修辭
# python FuzzyHighLight.py "盧梭 在 Môtiers 的住處在 1765 年 9 月 6 日被丟擲石頭，因此盧梭和休謨到英國 避難，在朋友的鄉間別墅史丹佛郡的 Wootton 居住" "在英國時（1765年）.盧梭在莫蒂埃的住處在1765年9月6日被丟擲石頭，因此盧梭和休謨到英國避難，休謨在史丹佛郡的Wootton，朋友的鄉間別墅居住"


# Developed by Yuen-Hsien Tseng on April 4, 2000 in Perl
'''
# This is an old one modified from my Perl program written on April 4, 2000.
# Word Spoting dymamic programming
# Given 2 arrays: rD (document) and rQ (query), return the (fuzzy) 
# match position and the length of (fuzzy) match
import math
def FuzzyMatchArray(rD, rQ):
    F1 = []; Fm = []
    minv = 0; pe = 0; pb = -1
    lend = len(rD)
    lenq = len(rQ)
    CC = (); # current column, LC : last column
    LC = [i for i in range(lenq + 1)]
    for j in range(lend):
        CC = [0]
        for i in range(lenq):
            (cdq, cd, cq) = (1, 1, 1)
            if (rD[j] == rQ[i]): cdq = 0
            lu = LC[i] + cdq
            l = LC[i+1] + cd # note we have a extra element in LC and CC
            u = CC[-1] + cq
            minv = l if (l<lu) else lu
            if minv > u: minv= u
            CC.append(minv)
#            print(CC[-1], end=' ')
#        print()
        lm = CC[-1]; # last element of current column
        F1.append(CC[1]) # record the first row
        Fm.append(lm) # record the last row
        LC = CC[:] # copy the values of CC to LC
        pe = j # ending position of a possible match, 
        if lm == 0: break

# Now trace back the match positions, return the begining and the end
    if (Fm[-1] == 0): # if there is an exact match
        pb = pe + 1 - lenq
#print "Fm=$#Fm, rQ=$lenq\n";
    else: # no exact match
        minv = lenq + 1 # set Maximum value
        for i in range(len(Fm)): # find $pe
            if Fm[i] < minv:
                minv= Fm[i]
                pe = i

# Calculate the normalized distance measure by minv and lenq
    if (minv== lenq):
        dm = 0
    else:
        dm = 1/math.exp(minv/(lenq-minv))
    if ((lenq < 5 and dm < 0.7) or (dm < 0.54)):
        length = 0
    else:
        pb = -1 # now find pb
        for j in range(pe, -1, -1): # range(start,stop,step)
            if (F1[j] == 0):
                pb = j
                break
            if (pb == -1):
                pb = pe + 1 - lenq + minv
        length = pe + 1 - pb
    return (pb, length) # return start position and match length

# Not the desired way to highlight the doc (based on query)
    (pb, length) = FuzzyMatchArray(doc, query)
    print("Start at : %d, length = %d\n%s" %(pb, length, doc[pb:pb+length]))
# python FuzzyHighLight.py 要被hightlight的文字 light文
#   Start at : 7, length = 5
#   light
# python FuzzyHighLight.py 要被hightlight的文字 被light文
#   Start at : 1, length = 6
#   被hight
# $ python FuzzyHighLight.py 要被highlight的文字 被light文
#   Start at : 1, length = 10
#   被highlight
# python FuzzyHighLight.py 要被highlight的文字 你被light文
#   Start at : 6, length = 5
#   light
'''

# Modified the above by Yuen-Hsien Tseng on Nov. 21, 2020 in Python
'''
def FuzzyMatchPosotions(doc, query):
    hasSwapped = False
    if len(doc) < len(query):
        (query, doc) = (doc, query) # swap doc and query
        hasSwapped  = True
    # Initialize a matrix of zeros
    rows = len(doc)+1
    cols = len(query)+1
    mtrx = []
    for i in range(rows):
        mtrx.append([0 for j in range(cols)])
    # Set the value of each element of matrix
    for row in range(1, rows):
        for col in range(1, cols):
            if doc[row-1] == query[col-1]:
                mtrx[row][col] = mtrx[row - 1][col - 1] + 1
    # Now, find the matches in matrix
    matchedPos = matchPositions(mtrx)
    if hasSwapped: # swap back for each position
        matchedPos = [[length, [p[1], p[0]]] for (length, p) in matchedPos]
    return (mtrx, matchedPos)

def matchPositions(M):
    Pos = []
    rowNum = len(M)
    if rowNum == 0:
        return Pos
    colNum = len(M[0])
    j = 0
    step = 1
    while j < colNum:
        i = 0
        while i < rowNum:
            step = 1
            if M[i][j] > 0:
                while (i+step < rowNum and j+step < colNum and M[i+step][j+step] > 0):
                    step += 1
                Pos.append([step, [i, j]]) # would be better using tuple (step, (i, j))
                break
            i += step
        j += step
#   return Pos # Doing so will lead to [1, [13, 2]] in the below example
    pprint.pprint(Pos)
# python FuzzyHighLight.py 要被highlight的文字 你文light被
#   [[1, [13, 2]], [5, [7, 3]]] # need to remove []
    # So, need to remove [1, [13, 2]]
    Positions = []
    for i in range(len(Pos) - 1):
        if Pos[i][1][0] <= Pos[i+1][1][0]:
            Positions.append(Pos[i])
    Positions.append(Pos[-1])
    return Positions
'''
