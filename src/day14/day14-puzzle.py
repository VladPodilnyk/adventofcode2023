class Solver:
    def __init__(self, input_data, m, n):
        self.input_data = input_data
        self.m = m
        self.n = n

    def debug(self):
        cols = []
        for j in range(len(self.input_data)):
            col = []
            spheres = self.input_data[j][0]
            cubes = self.input_data[j][1]
            for i in range(self.m):
                if (i, j) in spheres:
                    col.append('O')
                elif (i, j) in cubes:
                    col.append('#')
                else:
                    col.append('.')
            cols.append(''.join(col))
        [print(''.join(i)) for i in zip(*cols)]

    def solve(self) -> int:
        # self.debug()

        for col in range(len(self.input_data)):
            self.move_rocks(col)

        # self.debug()
        res = 0
        for col in range(len(self.input_data)):
            res += self.calc_weight(col)
        return res

    def calc_weight(self, col: int) -> int:
        spheres = self.input_data[col][0]
        weight = 0
        for sphere in spheres:
            weight += self.m - sphere[0]
        return weight

    def move_rocks(self, col: int):
        spheres = self.input_data[col][0]
        cubes = self.input_data[col][1]

        i = 0
        j = 0
        curr_row = 0

        while i < len(spheres):
            # move sphere to the north if there is no obstacle (cube)
            if len(cubes) == 0 or j >= len(cubes):
                spheres[i] = (curr_row, spheres[i][1])
            elif spheres[i][0] < cubes[j][0]:
                spheres[i] = (curr_row, spheres[i][1])
            else:
                while j < len(cubes) and spheres[i][0] > cubes[j][0]:
                    j += 1
                curr_row = cubes[j-1][0] + 1
                spheres[i] = (curr_row, spheres[i][1])
            curr_row += 1
            i += 1


if __name__ == '__main__':
    file = 'input.txt'
    with open(file, 'r') as reader:
        grid = [line.strip() for line in reader.readlines()]

        input_data = []
        for j in range(len(grid)):
            spheres = []
            cubes = []
            for i in range(len(grid[j])):
                if grid[i][j] == 'O':
                    spheres.append((i, j))
                elif grid[i][j] == '#':
                    cubes.append((i, j))
            input_data.append([spheres, cubes])

        solver = Solver(input_data, len(grid), len(grid[0]))
        print('Result: {}'.format(solver.solve()))