def read_input(data: str) -> list[list[str]]:
    res = []
    pattern = []
    for row in data.split('\n'):
        if row != '':
            pattern.append(row)
        else:
            res.append(pattern)
            pattern = []
    if pattern != []:
        res.append(pattern)
    return res

class Solver:
    def __init__(self, patterns: list[list[str]]):
        self.patterns = patterns
    
    def solve(self, allowed_distance: int) -> int:
        res = 0
        for index, pattern in enumerate(self.patterns):
            res += self.summarize_notes(pattern, allowed_distance)
        return res

    def summarize_notes(self, pattern: list[str], allowed_distance: int) -> int:
        mirror_idx = -1
        for i in range(len(pattern) - 1):
            if self.is_horizontal_mirror(pattern, i, allowed_distance):
                mirror_idx = i
                break
        
        if mirror_idx != -1:
            return 100 * (mirror_idx + 1)

        # transpose the matrix
        transposed_pattern = [''.join(i) for i in zip(*pattern)]

        [print(line) for line in pattern]
        print('-------------------------')
        [print(line) for line in transposed_pattern]
        print('-------------------------')
        [print(''.join(line)) for line in zip(*transposed_pattern)]

        for i in range(len(transposed_pattern) - 1):
            if self.is_horizontal_mirror(transposed_pattern, i, allowed_distance):
                mirror_idx = i
                break

        if mirror_idx != -1:
            return mirror_idx + 1

        return 0

    def is_horizontal_mirror(self, pattern: list[str], row: int, allowed_distance: int) -> bool:
        m_i = row + 1
        for i in range(row, -1, -1):
            if m_i >= len(pattern):
                break
            dist = self.distance(pattern[m_i], pattern[i])
            if dist == -1 or dist > allowed_distance:
                return False
            m_i += 1
        return True
    
    # expects that left and right have the same length
    def distance(self, left: str, right: str) -> int:
        if len(left) != len(right):
            return -1
        res = 0
        for i in range(len(left)):
            if left[i] != right[i]:
                res += 1
        return res

if __name__ == '__main__':
    file = 'test-input.txt'
    with open(file, 'r') as reader:
        data = read_input(reader.read())
        solver = Solver(data)
        print('Result: {}'.format(solver.solve(0)))