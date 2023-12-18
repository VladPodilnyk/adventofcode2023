from collections.abc import Callable

def transpose(grid: list[str]) -> list[str]:
    return [''.join(i) for i in zip(*grid)]

def apply_n_times(func: Callable[[str], str], data: str, n: int) -> str:
    seen = {}
    is_cycle = False
    i = 0
    while i < n:
        if data in seen:
            is_cycle = True
            break
        seen[data] = i
        data = func(data)
        i += 1

    if not is_cycle:
        return data

    cycle_start = seen[data]
    cycle_length = i - cycle_start
    left = (n - i) % cycle_length
    return apply_n_times(func, data, left)

def move_line_east(line: str) -> str:
    return '#'.join([''.join(sorted(part)) for part in line.split('#')])

def move_east(grid: list[str]) -> list[str]:
    return [move_line_east(line) for line in grid]

def move_line_west(line: str) -> str:
    return '#'.join([''.join(sorted(part, reverse=True)) for part in line.split('#')])

def move_west(grid: list[str]) -> list[str]:
    return [move_line_west(line) for line in grid]

def move_north(grid: list[str]) -> list[str]:
    return transpose(move_west(transpose(grid)))

def move_south(grid: list[str]) -> list[str]:
    return transpose(move_east(transpose(grid)))

def exec_cycle(grid: list[str]) -> list[str]:
    return move_east(move_south(move_west(move_north(grid))))

def apply_transformation(data: str) -> str:
    return '\n'.join(exec_cycle(data.splitlines()))

def find_weigth(data: str, cycles: int) -> int:
    transormed_data = apply_n_times(apply_transformation, data, cycles)
    return sum(r * row.count('O') for r, row in enumerate(transormed_data.splitlines()[::-1], 1))

if __name__ == '__main__':
    file = 'input.txt'
    with open(file, 'r') as reader:
        data = reader.read()
        print('Result: {}'.format(find_weigth(data, 1_000_000_000))) #1000000000