MOVE_UP = '|7F'
MOVE_DOWN = '|JL'
MOVE_LEFT = '-LF'
MOVE_RIGHT = '-J7'

class Solver:
    def __init__(self, grid: list[str]):
        self.grid = grid

    def run(self) -> int:
        starting_point = self.find_starting_point()
        print('starting point: {}'.format(starting_point))
        if starting_point is None:
            # the grid is invalid
            return -1

        path = self.walk(starting_point)
        if len(path) == 0:
            return -1

        # shoelace formula 
        area = self.polygon_area(path)
        # Pick's theorem (https://en.wikipedia.org/wiki/Pick%27s_theorem)
        # A = i + b / 2 - 1 (interior points is i, and thats what we need to find)
        res = area - len(path) // 2 + 1
        return res


    def walk(self, possition: tuple[int, int]) -> list[tuple[int, int]]:
        curr_pos = self.find_income_pipe(possition)
        if curr_pos is None:
            return []

        path = [curr_pos]
        while True:
            x, y, direction = curr_pos
            print('last path value: {}, value: {}'.format(path[-1], self.grid[x][y]))

            if self.grid[x][y] == 'S':
                break
            elif self.grid[x][y] == '|':
                if direction == 'up':
                    curr_pos = (x - 1, y, 'up')
                elif direction == 'down':
                    curr_pos = (x + 1, y, 'down')
            elif self.grid[x][y] == '-':
                if direction == 'left':
                    curr_pos = (x, y - 1, 'left')
                elif direction == 'right':
                    curr_pos = (x, y + 1, 'right')
            elif self.grid[x][y] == '7':
                if direction == 'up':
                    curr_pos = (x, y - 1, 'left')
                elif direction == 'right':
                    curr_pos = (x + 1, y, 'down')
            elif self.grid[x][y] == 'F':
                if direction == 'up':
                    curr_pos = (x, y + 1, 'right')
                elif direction == 'left':
                    curr_pos = (x + 1, y, 'down')
            elif self.grid[x][y] == 'J':
                if direction == 'down':
                    curr_pos = (x, y - 1, 'left')
                elif direction == 'right':
                    curr_pos = (x - 1, y, 'up')
            elif self.grid[x][y] == 'L':
                if direction == 'down':
                    curr_pos = (x, y + 1, 'right')
                elif direction == 'left':
                    curr_pos = (x - 1, y, 'up')

            path.append(curr_pos)

        print('path: {}'.format(path))
        return path

    # Shoelace formula for calculating the area of a polygon with n given vertices
    # An algorithm is stolen from here https://www.geeksforgeeks.org/area-of-a-polygon-with-given-n-ordered-vertices/?ref=lbp
    def polygon_area(self, path: list[tuple[int, int]]) -> int:
        area = 0.0
        j = len(path) - 1
        for i in range(len(path)):
            area += (path[j][0] + path[i][0]) * (path[j][1] - path[i][1])
            j = i
        return int(abs(area / 2.0))

    def find_income_pipe(self, possition: tuple[int, int]) -> tuple[int, int]:
        for diff in [(0, -1, MOVE_LEFT, 'left'), (0, 1, MOVE_RIGHT, 'right'), (-1, 0, MOVE_UP, 'up'), (1, 0, MOVE_DOWN, 'down')]:
            dx, dy, moves, direction = diff
            new_x = possition[0] + dx
            new_y = possition[1] + dy
            if self.grid[new_x][new_y] in moves:
                return (new_x, new_y, direction)
        return None


    #since we know that the gird has one starting point, lets find it
    def find_starting_point(self) -> tuple[int, int]:
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 'S':
                    return (i, j)
        return None

if __name__ == '__main__':
    file = 'input.txt'
    with open(file, 'r') as reader:
        grid = reader.readlines()
        steps_to_farthest_point = Solver(grid).run()
        print('Result: {}'.format(steps_to_farthest_point))