# -*- coding: utf-8 -*-
"""
Created on September 8 2021

@author: mrear

    Core damage formula:
    d_a = [d_hit * min(10, (21 + h -a - epsilon)) / 20] + [d_crit * max(1, 11 + h - a) / 20]
    epsilon = 1 if (a - h) > 10, 0 otherwise
"""

# Lists of lowest and highest possible AC for character by level (not including circumstance/status bonus)
AC_min = {1:12, 2:13, 3:14, 4:15, 5:17, 6:18, 7:19, 8:20, 9:21, 10:22, 11:24, 12:25, 13:28, 14:29, 15:30, 16:31, 17:32, 18:34, 19:35, 20:36}
AC_max = {1:19, 2:20, 3:21, 4:22, 5:24, 6:25, 7:28, 8:29, 9:30, 10:31, 11:33, 12:34, 13:37, 14:38, 15:39, 16:40, 17:43, 18:45, 19:46, 20:47}
# Key = level, level[0] = low, [1] = moderate, [2] = high, [3] = extreme
mStrike = {-1: [4,6,8,10], 0: [4,6,8,10], 1: [5,7,9,11], 2: [7,9,11,13], 3: [8,10,12,14], 4: [9,12,14,16], 5: [11,13,15,17],
           6: [12,15,17,19], 7: [13,16,18,20], 8: [15,18,20,22], 9: [16,19,21,23], 10: [17,21,23,25], 11: [19,22,24,27],
           12: [20,24,26,28], 13: [21,25,27,29], 14: [23,27,29,31], 15: [24,28,30,32], 16: [25,30,32,34], 17: [27,31,33,35],
           18: [28,33,35,37], 19: [29,34,36,38], 20: [31,36,38,40], 21: [32,37,39,41], 22: [33,39,41,43], 23: [35,40,42,44],
           24: [36,42,44,46]}
strikeLabel = ["Low", "Moderate", "High", "Extreme"]

# Returns average damage per attack / average damage on hit for AC = a, Strike bonus = h
def avg_dmg(a, h):
    eps = (a - h) > 10          # accounts for nat 20 -> crit
    zeta = (a - h) > 20         # accounts for nat 20 -> hit
    d = min(10, max((21 + h - a - eps), 0)) / 20 + 2 * max(1 - zeta, 11 + h - a) / 20
    return max(d, 0.01)         # ensures that 0 can't be returned, for divide by 0 purposes

data = []
# data will be a matrix (list of lists) where each list is of form [level, AC, creature level, strike label, dEHP]

for cLevel in AC_min:
    label1 = "Level " + str(cLevel) + " character"
    for AC in range(AC_min[cLevel], AC_max[cLevel] + 1):
        label2 = label1 + " with AC " + str(AC)
        for mLevel in range(cLevel - 2, cLevel + 3):
            label3 = label2 + " vs. level " + str(mLevel) + " creature"
            for i in range(4):      # for strike in mStrike[mLevel]:
                label4 = label3 + " with " + strikeLabel[i] + " attack bonus: "
                dEHP = avg_dmg(AC, mStrike[mLevel][i]) / avg_dmg(AC + 1, mStrike[mLevel][i]) - 1
                label4 += "{:.2%}".format(dEHP) + " increase in EHP from +1 AC"
                data.append([cLevel, AC, mLevel, strikeLabel[i], round(dEHP, 4)])
                # print(label4)

# filters data into a single value for each variable. Not very robust. Better filtering is on line 65
def filter_data(level = False, AC = False, mLevel = False, strikeLabel = False, dEHP = False):
    filtered_data = []
    inputs = [level, AC, mLevel, strikeLabel, dEHP]
    for avg in data:
        for i in range(5):
            if inputs[i] != False:
                if avg[i] == inputs[i]:
                    filtered_data.append(avg)
    return filtered_data
                    
# level2 = filter_data(level = 2)
# for i in level2:
#     print(i)

# strikeLow = filter_data(strikeLabel = "Low")
# for i in strikeLow:
#     print(i)
    
for avg in data:
    AC_avg = round((AC_min[avg[0]] + AC_max[avg[0]])/2)
    if avg[1] == AC_max[avg[0]] - 2:
        if avg[3] == "Moderate":
            if avg[2] == avg[0]:
                print(avg)