class Kalah:
    def __init__(self):
        self.current_state = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
        self.player = 1

    def is_end(self):
        if self.current_state[:6].count(0) == 6:
            for i in range (7, 13):
                self.current_state[13] += self.current_state[i]
                self.current_state[i] = 0
            return True
        elif self.current_state[7:13].count(0) == 6:
            for i in range (0, 6):
                self.current_state[6] += self.current_state[i]
                self.current_state[i] = 0
            return True

        return False

    def max_alpha_beta(self, deep, alpha, beta):
        maxv = -1990
        h = None

        if deep == 5 or self.is_end():
            if self.player == 1:
                return (F1(self.current_state.copy()), 0)
            else:
                return (F2(self.current_state.copy()), 0)

        for i in range(0, 6):
            if self.current_state[i] != 0:
                tmp = self.current_state.copy()
                val = self.current_state[i]
                self.current_state[i] = 0
                pos = i + 1
                for j in range(0, val):
                    if pos == 13:
                        pos = 0
                    self.current_state[pos] += 1
                    pos += 1
                m = self.min_alpha_beta(deep + 1, alpha, beta)
                if m > maxv:
                    maxv = m
                    h = i
                self.current_state = tmp

                if maxv >= beta:
                    return (maxv, h)

                if maxv > alpha:
                    alpha = maxv

        return (maxv, h)

    def min_alpha_beta(self, deep, alpha, beta):
        minv = 1990
        h = None

        if deep == 5 or self.is_end():
            if self.player == 1:
                return F1(self.current_state.copy())
            else:
                return F2(self.current_state.copy())

        for i in range(7, 13):
            if self.current_state[i] != 0:
                tmp = self.current_state.copy()
                val = self.current_state[i]
                self.current_state[i] = 0
                pos = i + 1
                for j in range(0, val):
                    if pos == 14:
                        pos = 0
                    elif pos == 6:
                        pos = 7
                    self.current_state[pos] += 1
                    pos += 1
                (m, max_h) = self.max_alpha_beta(deep + 1, alpha, beta)
                if m < minv:
                    minv = m
                    h = i
                self.current_state = tmp

                if minv <= alpha:
                    return minv

                if minv < beta:
                    beta = minv

        return minv

    def play_alpha_beta(self):
        while True:
            if self.is_end():
                if self.current_state[6] - self.current_state[13] > 0:
                    return self.player
                else:
                    return 3 - self.player

            (m, h) = self.max_alpha_beta(0, -2000, 2000)
            val = self.current_state[h]
            self.current_state[h] = 0
            pos = h + 1
            for i in range(0, val):
                if pos == 13:
                    pos = 0
                self.current_state[pos] += 1
                pos += 1

            half = int(len(self.current_state) / 2)
            self.current_state[:half], self.current_state[half:] = self.current_state[half:], self.current_state[:half]
            self.player = 3 - self.player

def main():
    g = Kalah()
    return g.play_alpha_beta()

if __name__ == "__main__":
    print(main())