class Note:
    def __init__(self, record: str, damaged_groups: list[int]):
        self.record = record
        self.damaged_groups = damaged_groups

class Solver:
    @staticmethod
    def solve(notes: list[Note]) -> int:
        res = 0
        for note in notes:
            res += Solver.ways(note)
        return res

    @staticmethod
    def ways(note: Note) -> int:
        cache = []
        for _ in range(len(note.record)):
            cache.append([-1] * (len(note.damaged_groups) + 1))

        return Solver.dp(0, 0, note, cache)

    @staticmethod
    def dp(i: int, j: int, note: Note, cache: list[list[int]]) -> int:
        if i >= len(note.record):
            # combination is invalid
            if j < len(note.damaged_groups):
                return 0
            # found a valid combination
            return 1

        # return memoized value
        if cache[i][j] != -1:
            return cache[i][j]
        
        res = 0
        if note.record[i] == '.':
            res = Solver.dp(i + 1, j, note, cache)
        else:
            if note.record[i] == '?':
                res += Solver.dp(i + 1, j, note, cache)
            if j < len(note.damaged_groups):
                count = 0
                for k in range(i, len(note.record)):
                    if count > note.damaged_groups[j] or note.record[k] == '.' or (count == note.damaged_groups[j] and note.record[k] == '?'):
                        break
                    count += 1
                if count == note.damaged_groups[j]:
                    if i + count < len(note.record) and note.record[i + count] != '#':
                        res += Solver.dp(i + count + 1, j + 1, note, cache)
                    else:
                        res += Solver.dp(i + count, j + 1, note, cache)

        cache[i][j] = res
        return res



if __name__ == '__main__':
    file = 'input.txt'
    with open(file, 'r') as reader:
        lines = reader.readlines()
        lines = [line.strip() for line in lines]
        notes = []
        for line in lines:
            parts = line.split(' ')
            record = parts[0]
            damaged_groups = [int(v) for v in parts[1].split(',')]
            notes.append(Note(record, damaged_groups))
        
        print('Result: {}'.format(Solver.solve(notes)))