
class Grid:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.matrix = [[(0 ,0 ,0) for _ in range(10)] for _ in range(20)]

    def update(self, locked_pos={}):  # *
        self.matrix = [[(0 ,0 ,0) for _ in range(10)] for _ in range(20)]

        for i in range(self.row):
            for j in range(self.col):
                if (j, i) in locked_pos:
                    self.matrix[i][j] = locked_pos[(j ,i)]



    def valid_space(self, shape):
        accepted_pos = set()
        for i in range(self.row):
            for j in range(self.col):
                if self.matrix[i][j] == (0, 0, 0):
                    accepted_pos.add((j, i))

        formatted = shape.update_position()

        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def clear_rows(self):
        res = 0
        delete_rows = []
        for i, row in enumerate(self.matrix):
            if (0, 0, 0) not in row:
                res += 1
                delete_rows.append(i)

        while delete_rows:
            row_num = delete_rows.pop()
            del self.matrix[row_num]

        for _ in range(res):
            row = [(0, 0, 0)] * self.col
            self.matrix.insert(0, row)

        locked_positions = {}
        if res > 0:
            for i in range(self.row):
                for j in range(self.col):
                    if self.matrix[i][j] != (0, 0, 0):
                        locked_positions[(j, i)] = self.matrix[i][j]

        return (50 if res == 4 else res * 10, locked_positions)



