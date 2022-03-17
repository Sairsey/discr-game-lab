def func(state):
    D1 = 0.0
    D2 = 0.0
    for i in range(0,6):
        if state[i] > 0:
            if state[i] <= 6 - i:
                div = 0
            else:
                div = state[i] - 6 + i
            D1 += state[i] - div + 6
    for i in range(7,13):
        if state[i] > 0:
            if state[i] <= 13 - i:
                div = 0
            else:
                div = state[i] - 13 + i
            D2 += state[i] - div + 6
    D1 = D1 / 6 + 1
    D2 = D2 / 6 + 1
    res = (state[6]+34/(70-state[6])-40/D1)-(state[13]+34/(70-state[13])-40/D2)
    return res
