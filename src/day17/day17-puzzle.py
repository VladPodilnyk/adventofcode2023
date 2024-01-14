from enum import IntEnum
from typing import Literal, NamedTuple
from heapq import heappush, heappop

Point = tuple[int, int]

def parse_grid(raw_data: list[str]) -> dict[Point, str]:
    grid = {}
    for y, line in enumerate(raw_data):
        for x, char in enumerate(line):
            grid[(x, y)] = char
    return grid

# CCW = Counter Clock Wise
# CW = Clock Wise
Rotation = Literal["CCW", "CW"]

# shamelessly stolen from @xavdid (github.com/xavdid)
class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def rotate(facing: "Direction", towards: Rotation) -> "Direction":
        offset = 1 if towards == "CW" else -1
        return Direction((facing.value + offset) % 4)

    @staticmethod
    def offset(facing: "Direction") -> Point:
        return _ROW_COLL_OFFSETS[facing]


_ROW_COLL_OFFSETS: dict[Direction, Point] = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}

class Position(NamedTuple):
    location: Point
    direction: Direction

    def next_location(self) -> Point:
        loc_x, loc_y = self.location
        offset_x, offset_y = Direction.offset(self.direction)
        return loc_x + offset_x, loc_y + offset_y

    def step(self) -> "Position":
        return Position(self.next_location(), self.direction)

    def rotate_and_step(self, towards: Rotation):
        return Position(self.location, Direction.rotate(self.direction, towards)).step()

class Solver:
    def __init__(self, raw_data: list[str]):
        self.input = raw_data

    # This solution is based on Dijkstra’s algorithm shortest path algorithm
    # For more info about the algorithm itself, see a nice explanation here: https://www.youtube.com/watch?v=XEb7_z5dG3c
    def _solve(self, min_steps: int) -> int:
        # target point
        target = len(self.input) - 1, len(self.input[-1]) - 1
        # grid
        grid = {point: int(heat) for point, heat in parse_grid(self.input).items()}

        # start walking in both directions:
        queue = [
            # we keep track of the heat level, position and number of steps in a given direction
            (0, Position((0, 0), Direction.DOWN), 0),
            (0, Position((0, 0), Direction.RIGHT), 0)
        ]
        # visited points
        seen: set[tuple[Position, int]] = set()

        while queue:
            heat_level, position, steps = heappop(queue)

            if position.location == target:
                return heat_level
            
            if (position, steps) in seen:
                continue
            seen.add((position, steps))

            # verify if we can move in the current direction
            if (left := position.rotate_and_step("CCW")).location in grid:
                heappush(queue, (heat_level + grid[left.location], left, 1))

            if (right := position.rotate_and_step("CW")).location in grid:
                heappush(queue, (heat_level + grid[right.location], right, 1))

            if steps < min_steps and (forward := position.step()).location in grid:
                heappush(queue, (heat_level + grid[forward.location], forward, steps + 1))

        # target is unreachable
        return -1

    def solve_part1(self) -> int:
        return self._solve(3)

if __name__ == "__main__":
    filename = "input.txt"
    with open(filename) as file:
        raw_data = file.read().splitlines()
        solver = Solver(raw_data)
        print(f"Part 1: {solver.solve_part1()}")