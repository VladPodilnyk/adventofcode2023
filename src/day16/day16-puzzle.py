from typing import Mapping

DIRECTIONS = {
    'right': (0, 1),
    'left': (0, -1),
    'up': (-1, 0),
    'down': (1, 0)
}

class Beam:
    def __init__(self, direction: str, x: int, y: int):
        self.direction = direction
        self.x = x
        self.y = y
        self.distance = 0

    def inc(self):
        self.distance += 1

    def set_coordinates(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, tile: str):
        dx, dy = 0, 0
        if tile == '.':
            dx, dy = DIRECTIONS[self.direction]
        elif tile == '/':
            dx, dy = 0, 0
            if self.direction == 'right':
                dx, dy = DIRECTIONS['up']
                self.direction = 'up'
            elif self.direction == 'left':
                dx, dy = DIRECTIONS['down']
                self.direction = 'down'
            elif self.direction == 'up':
                dx, dy = DIRECTIONS['right']
                self.direction = 'right'
            elif self.direction == 'down':
                dx, dy = DIRECTIONS['left']
                self.direction = 'left'
        elif tile == '\\':
            dx, dy = 0, 0
            if self.direction == 'right':
                dx, dy = DIRECTIONS['down']
                self.direction = 'down'
            elif self.direction == 'left':
                dx, dy = DIRECTIONS['up']
                self.direction = 'up'
            elif self.direction == 'up':
                dx, dy = DIRECTIONS['left']
                self.direction = 'left'
            elif self.direction == 'down':
                dx, dy = DIRECTIONS['right']
                self.direction = 'right'
        elif tile == '|':
            dx, dy = DIRECTIONS[self.direction]
        elif tile == '-':
            dx, dy = DIRECTIONS[self.direction]

        self.x += dx
        self.y += dy

    def is_pass_through(self, tile: str) -> bool:
        if tile == '-' and (self.direction == 'right' or self.direction == 'left'):
            return True

        if tile == '|' and (self.direction == 'up' or self.direction == 'down'):
            return True

        return False

def travel(grid: list[list[chr]], beam: Beam, seen: Mapping[tuple[int, int], set[str]]) -> int:
    while True:
        if is_out_of_bounds(grid, beam.x, beam.y) or ((beam.x, beam.y) in seen and beam.direction in seen[(beam.x, beam.y)]):
            return beam.distance

        tile = grid[beam.x][beam.y]
        if (beam.x, beam.y) not in seen:
            seen[(beam.x, beam.y)] = set()
            beam.inc()
        
        if beam.direction not in seen[(beam.x, beam.y)]:
            seen[(beam.x, beam.y)].add(beam.direction)
 
        if tile in '.\/':
            beam.move(tile)
        elif tile in '-|':
            if beam.is_pass_through(tile):
                beam.move(tile)
            else:
                if tile == '-' and (beam.direction == 'up' or beam.direction == 'down'):
                    beam.distance += travel(grid, Beam('right', beam.x, beam.y + 1), seen)
                    beam.distance += travel(grid, Beam('left', beam.x, beam.y - 1), seen)
                elif tile == '|' and (beam.direction == 'right' or beam.direction == 'left'):
                    beam.distance += travel(grid, Beam('up', beam.x - 1, beam.y), seen)
                    beam.distance += travel(grid, Beam('down', beam.x + 1, beam.y), seen)
                else:
                    print('Error: invalid tile: {}, beam.direction: {}, x: {}, y: {}'.format(tile, beam.direction, beam.x, beam.y))

def count_energized_tiles(grid: list[str]) -> int:
    max_energy = 0

    for i in range(len(grid)):
        res = travel(grid, Beam('right', i, 0), {})
        max_energy = max(max_energy, res)

    for i in range(len(grid)):
        res = travel(grid, Beam('left', i, len(grid) - 1), {})
        max_energy = max(max_energy, res)
    
    for i in range(len(grid[0])):
        res = travel(grid, Beam('down', 0, i), {})
        max_energy = max(max_energy, res)

    for i in range(len(grid[0])):
        res = travel(grid, Beam('up', len(grid[0]) - 1, i), {})
        max_energy = max(max_energy, res)

    return max_energy

def is_out_of_bounds(grid: list[str], x: int, y: int) -> bool:
    return x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0])

if __name__ == '__main__':
    file = 'input.txt'
    with open(file, 'r') as reader:
        grid = reader.read().splitlines()
        grid = [list(row) for row in grid]
        [print(''.join(row)) for row in grid]
        print('Result: {}'.format(count_energized_tiles(grid)))