from functools import reduce

class Solver:
    def __init__(self, historical_data: list[list[int]]):
        self.historical_data = historical_data

    def solve(self) -> int:
        sum = 0
        for seq in self.historical_data:
            sum += self.predict(seq)
        return sum
    
    def predict(self, seq: list[int]) -> int:
        is_equal = False
        current_seq = seq
        first_values = []

        while not is_equal:
            first_values.append(current_seq[0])
            next_seq = []
            for i in range(len(current_seq) - 1):
                next_seq.append(current_seq[i + 1] - current_seq[i])

            is_equal = self._is_all_equal(next_seq)
            current_seq = next_seq

        first_values.append(current_seq[0])
        res = first_values[-1]
        for i in range(len(first_values) - 2, -1, -1):
           res = first_values[i] - res

        # print('first values: {}'.format(first_values))
        # print('predicted value: {}'.format(res))
        return res
        
    def _is_all_equal(self, seq: list[int]) -> bool:
        for i in range(1, len(seq)):
            if seq[i] != seq[i - 1]:
                return False
        return True


if __name__ == '__main__':
    file = 'input.txt'
    with open(file, 'r') as reader:
        input = []
        for line in reader.readlines():
            input.append([int(x) for x in line.split(' ')])

        print('Result: {}'.format(Solver(input).solve()))
