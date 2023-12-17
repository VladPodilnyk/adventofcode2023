import re

EXCLUDE = '0123456789.\n'

## Revist this later
## Soltion is based on image processing like approach
def find_parts_sum(input: list[list[chr]]) -> int:
    chars = {(r, c): [] for r in range(len(input)) for c in range(len(input[r])) if input[r][c] not in EXCLUDE}

    for r in range(len(input)):
        line = input[r]
        for number in re.finditer(r'\d+', line):
            edge = {(kernel_row, kernel_col) for kernel_row in (r - 1, r, r + 1)
                            for kernel_col in range(number.start() - 1, number.end() + 1) }

            for value in edge & chars.keys():
                chars[value].append(int(number.group()))

    #return sum(sum(adjecent_num) for adjecent_num in chars.values())
    return sum([adjacents[0] * adjacents[1] for adjacents in chars.values() if len(adjacents) == 2])
    

if __name__ == '__main__':
    with open('input.txt') as reader:
        input = reader.readlines()
        print('Sum: {}'.format(find_parts_sum(input)))