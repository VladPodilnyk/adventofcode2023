import re

class Card:
    def __init__(self, card_number: int, input_numbers: list[int], winning_numbers: list[int]) -> None:
        self.card_number = card_number
        self.input_numbers = input_numbers
        self.winning_numbers = set(winning_numbers)
    
    def worth(self) -> int:
        result = 0
        match = False
        for number in self.input_numbers:
            if number in self.winning_numbers:
                if not match:
                    match = True
                    result += 1
                else:
                    result *= 2
        return result

    def count_win_numbers(self) -> int:
        counter = 0
        for number in self.input_numbers:
            if number in self.winning_numbers:
                counter += 1
        return counter
    
class CardCounter:
    def __init__(self, max_value: int) -> None:
        self.max_value = max_value
        self.store = {}

    def add(self, card: Card) -> None:
        win_numbers = card.count_win_numbers()
        if card.card_number not in self.store:
            self.store[card.card_number] = 0
        self.store[card.card_number] += 1

        for number in range(card.card_number + 1, card.card_number + win_numbers + 1):
            if number <= self.max_value:
                if number not in self.store:
                    self.store[number] = 0
                self.store[number] += self.store[card.card_number]

    def get_sum(self) -> int:
        print('store {}'.format(self.store))
        return sum(self.store.values())

class Parser:
    @staticmethod
    def parse(input: list[str]) -> list[Card]:
        for line in input:
            parts = line.split('|')
            winning_numbers = [int(number.group()) for number in re.finditer(r'\d+', parts[1])]

            input_data = parts[0].split(':')
            raw_card_number = list(re.finditer(r'\d+', input_data[0]))[0]
            card_number = int(raw_card_number.group())

            input_numbers = [int(number.group()) for number in re.finditer(r'\d+', input_data[1])]
            yield Card(card_number, input_numbers, winning_numbers)



if __name__ == '__main__':
    with open('input.txt', 'r') as reader:
        input = reader.readlines()
        counter = CardCounter(len(input))
        for card in list(Parser.parse(input)):
            counter.add(card)

        print('Result: ', counter.get_sum())