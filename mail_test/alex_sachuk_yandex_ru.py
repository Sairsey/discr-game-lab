#THIS IS TEMPLATE FOR FUNCTION. PLEASE FOLLOW THE RULES:
#1) Do Not print anything!!!
#2) Do not exit(0) or smth
#3) Please do not try to hack us.

def MakeMove(state, pos):
    stones = state[pos]
    emptyField = [0 for i in range(14)]
    while stones > 0:
        stones -= 1
        emptyField[pos % 14] += 1
        pos += 1
    return emptyField

def getFieldActivityFir(state):
    ans = 0
    for i in range(0, 6):
        ans += (state[i] * 1.337 ** (6 - i))
        #emptyField = MakeMove(state, i)
        #for i in range(0, 6):
        #    ans += emptyField[i]
        #for i in range(7, 13):
        #    ans -= emptyField[i]

    return ans

def getFieldActivitySec(state):
    ans = 0
    for i in range(7, 13):
        ans += (state[i] * 1.337 ** (13 - i))
        #emptyField = MakeMove(state, i)
        #for i in range(0, 6):
        #    ans -= emptyField[i]
        #for i in range(7, 13):
        #    ans += emptyField[i]
    return ans


def func(state):
    # state is array with length 14. 
    # values with indices 0-5 is yours pits, 6 - yours kalah
    # values with indices 7-12 is opponent`s pits, 13 - oppenent`s kalah
    
    # PLACE YOUR CODE HERE
    Dfir = getFieldActivityFir(state)
    Dsec = getFieldActivitySec(state)
    res = (state[6] - state[13]) * 100 + getFieldActivityFir(state) - getFieldActivitySec(state)

    # Return result for minimax
    return res
