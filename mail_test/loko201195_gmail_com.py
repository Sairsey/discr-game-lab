#THIS IS TEMPLATE FOR FUNCTION. PLEASE FOLLOW THE RULES:
#1) Do Not print anything!!!
#2) Do not exit(0) or smth
#3) Please do not try to hack us.

def func(state):
    # state is array with length 14. 
    # values with indices 0-5 is yours pits, 6 - yours kalah
    # values with indices 7-12 is opponent`s pits, 13 - oppenent`s kalah
    
    # PLACE YOUR CODE HERE

    # Return result for minimax
    return (state[6] - state[13]) * 100 + 1.34 ** 6 * state[0] + 1.34 ** 5 * state[1] + 1.34 ** 4 * state[2] + 1.34 ** 3 * state[3] + 1.34 ** 2 * state[4] + 1.34 * state[5] - state[7] * 1.34 - state[8] * 1.34 ** 2 - state[9] * 1.34 ** 3 - state[10] * 1.34 ** 4 - state[11] * 1.34 ** 5 - state[12] * 1.34 ** 6