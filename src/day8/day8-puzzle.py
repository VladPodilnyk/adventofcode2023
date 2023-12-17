import re

class Route:
    def __init__(self, left: str, right: str):
        self.left = left
        self.right = right
    
    def __repr__(self) -> str:
        return '({}, {})'.format(self.left, self.right)


def parse_routes(routes_raw: list[str]) -> dict[str, Route]:
    routes = {}
    for value in routes_raw:
        matches = re.findall(r'(\w+)', value)
        routes[matches[0]] = Route(matches[1], matches[2])
    return routes


class Solver:
    def __init__(self, instructions: str, routes: dict[str, Route]):
        self.instructions = instructions
        self.routes = routes
        self.starting_points = self._find_starting_points(routes)
    
    def solve(self) -> int:
        steps = []
        for starting_point in self.starting_points:
            steps.append(self._find_min_steps(starting_point))

        print('steps {}'.format(steps))
        acc = steps[0]
        for value in steps[1:]:
            acc = self._least_common_multiple(acc, value)

        return acc

    # Copy-pasted this from GeekForGeeks, need to learn more about this!!!
    def _least_common_multiple(self, a: int, b: int) -> int:
        return (a // self._greatest_common_divisor(a, b)) * b

    def _greatest_common_divisor(self, a: int, b: int) -> int:
        if a == 0:
            return b
        return self._greatest_common_divisor(b % a, a)

    def _find_min_steps(self, start_pos: str) -> int:
        steps = 0
        i = 0
        location = start_pos
        while True:
            instruction = self.instructions[i]
            if instruction == 'L':
                location = self.routes[location].left
            else:
                location = self.routes[location].right

            steps += 1
            if location[-1] == 'Z':
                return steps

            i = (i + 1) % len(self.instructions)

    def _find_starting_points(self, routes: dict[str, Route]) -> list[str]:
        return [key for key in routes.keys() if key[-1] == 'A']

if __name__ == '__main__':
    test_file = 'test-input2.txt'
    real_file = 'input.txt'
    with open(real_file, 'r') as reader:
        input = reader.readlines()
        instructions = input[0].strip()
        routes = parse_routes(input[2:])
        solver = Solver(instructions, routes)
        print('Result: {}'.format(solver.solve()))