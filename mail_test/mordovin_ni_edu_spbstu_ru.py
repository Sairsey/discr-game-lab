# THIS IS TEMPLATE FOR FUNCTION. PLEASE FOLLOW THE RULES:
# 1) Do Not print anything!!!
# 2) Do not exit(0) or smth
# 3) Please do not try to hack us.

def func(state):
    # state is array with length 14.
    # values with indices 0-5 is yours pits, 6 - yours kalah
    # values with indices 7-12 is opponent`s pits, 13 - oppenent`s kalah

    # PLACE YOUR CODE HERE

    # Return result for minimax

    score1 = 0
    score2 = 0

    for i in range(0, 6):
        if state[i] > 6 - i:
            tmp = 6 - i
        else:
            tmp = state[i]
        score1 += tmp
        state[i] -= tmp

        if state[i] > 6:
            tmp = 6
        else:
            tmp = state[i]

        score2 += tmp
        state[i] -= tmp
        mult = 0
        if (state[i] > 13):
            mult = state[i] // 13
        score1 += mult * 7
        score2 += mult * 6
        state[i] -= mult * 13

        if (state[i] > 7):
            score1 += 7
            score2 += state[i] - 7
        else:
            score1 += state[i]

    return (state[6] - state[13]) * 14 + score1 - score2
