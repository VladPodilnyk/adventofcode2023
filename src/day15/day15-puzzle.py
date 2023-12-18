class Lens:
    def __init__(self, label: str, power: int):
        self.label = label
        self.power = power

    def __repr__(self) -> str:
        return '{} {}'.format(self.label, self.power)

def parse_input(data: str) -> list[str]:
    return data.split(',')

def hash(value: str) -> int:
    result = 0
    for char in value:
        ascii_value = ord(char)
        result = 17 * (result + ascii_value) % 256
    return result

def eval_init_sequence(data: list[str]) -> int:
    return sum(hash(value) for value in data)

def install_lenses(boxes: dict[int, list[Lens]], value: str):
    operation_index = value.find('-')
    if operation_index >= 0:
        label = value[:operation_index]
        key = hash(label)
        if key in boxes:
            boxes[key] = list(filter(lambda lens: lens.label != label, boxes[key]))
    else:
        label, power_raw = value.split('=')
        key = hash(label)
        if key not in boxes:
            boxes[key] = []

        new_lens = Lens(label, int(power_raw))
        index = -1
        for i in range(len(boxes[key])):
            if boxes[key][i].label == label:
                index = i
                break
        if index >= 0:
            boxes[key] = boxes[key][:index] + [new_lens] + boxes[key][index + 1:]
        else:
            boxes[key].append(new_lens)


def total_focusing_power(boxes: dict[int, list[Lens]]) -> int:
    result = 0
    for key, lenses in boxes.items():
        result += sum((1 + key) * slot * lens.power for slot, lens in enumerate(lenses, 1))
    return result

def verify_lenses_installation(data: list[str]) -> int:
    boxes = {}
    for value in data:
        install_lenses(boxes, value)
    print(boxes)
    return total_focusing_power(boxes)

if __name__ == '__main__':
    file = 'test-input.txt'
    with open(file, 'r') as reader:
        data = reader.read()
        #print('Result: {}'.format(eval_init_sequence(['rn'])))
        print('Result: {}'.format(verify_lenses_installation(parse_input(data))))