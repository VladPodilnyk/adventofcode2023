import math

class Solver:
    def __init__(self, time: int, distance: int):
        self.time = time
        self.distance = distance

    def solve(self) -> int:
        x1 = (time - math.sqrt(time * time - 4 * distance)) // 2
        x2 = (time + math.sqrt(time * time - 4 * distance)) // 2
        return int(x2 - x1)

if __name__ == '__main__':
    with open('input.txt', 'r') as reader:
        input = reader.readlines()
        time = int(''.join([v for v in filter(lambda x: len(x) > 0, input[0].split(':')[1].strip().split(' '))]))
        distance = int(''.join([v for v in filter(lambda x: len(x) > 0, input[1].split(':')[1].strip().split(' '))]))
        solver = Solver(time, distance)
        print('Result: {}'.format(solver.solve()))