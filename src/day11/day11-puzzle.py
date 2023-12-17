class Solver:
    def __init__(self, grid):
        self.grid = grid

    def solve(self, expand_coef):
        galaxies = self._find_galaxies(self.grid)
        adjusted_galaxies = self._expand_space(galaxies, expand_coef)

        res = 0
        pairs = 0
        for i in range(len(adjusted_galaxies)):
            paths = []
            for j in range(i + 1, len(adjusted_galaxies)):
                paths.append(abs(adjusted_galaxies[i][0] - adjusted_galaxies[j][0]) + abs(adjusted_galaxies[i][1] - adjusted_galaxies[j][1]))
            res += sum(paths)
            pairs += len(paths)
        print('Pairs: {}'.format(pairs))
        return res

    def _find_galaxies(self, grid):
        galaxies = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '#':
                    galaxies.append((i, j))
        return galaxies

    def _expand_space(self, galaxies, expand_coef):
        # find rows to insert
        coef = expand_coef - 1
        rows_to_insert = self._find_rows_to_insert()
        columns_to_insert = self._find_cols_to_insert()
        adjusted_galaxies = [location for location in galaxies]

        # sort by X-axis
        for row in rows_to_insert:
            i = 0
            while i < len(galaxies):
                if galaxies[i][0] > row:
                    break
                i += 1
            while i < len(galaxies):
                adjusted_galaxies[i] = (adjusted_galaxies[i][0] + coef, adjusted_galaxies[i][1])
                i += 1
        
        # sort by Y-axis
        galaxies.sort(key=lambda x: x[1])
        adjusted_galaxies.sort(key=lambda x: x[1])

        for col in columns_to_insert:
            i = 0
            while i < len(galaxies):
                if galaxies[i][1] > col:
                    break
                i += 1
            while i < len(galaxies):
                adjusted_galaxies[i] = (adjusted_galaxies[i][0], adjusted_galaxies[i][1] + coef)
                i += 1
        return adjusted_galaxies

    def _find_rows_to_insert(self):
        rows_to_insert = []
        for i in range(len(grid)):
            is_blank = True
            for j in range(1, len(grid[i])):
                if grid[i][j] != grid[i][j-1]:
                    is_blank = False
                    break
            if is_blank:
                rows_to_insert.append(i)
        return rows_to_insert

    def _find_cols_to_insert(self):
        cols_to_insert = []
        for j in range(len(grid[0])):
            is_blank = True
            for i in range(1, len(grid)):
                if grid[i][j] != grid[i-1][j]:
                    is_blank = False
                    break
            if is_blank:
                cols_to_insert.append(j)
        return cols_to_insert




if __name__ == '__main__':
    file = 'input.txt'
    with open(file, 'r') as reader:
        grid = [line.strip() for line in reader.readlines()]
        solver = Solver(grid)
        print('Result: {}'.format(solver.solve(1000000)))