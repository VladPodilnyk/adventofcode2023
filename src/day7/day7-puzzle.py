from __future__ import annotations
from functools import total_ordering

CHARS = 'AKQT98765432J'
CARD_HANDS = ['kind_five', 'kind_four', 'full_house', 'kind_three', 'two_pair', 'one_pair', 'high_card']

CHAR_TO_STRENGTH = {char: i for i, char in enumerate(reversed(CHARS)) }
TYPE_TO_STRENGTH = {hand_type: i for i, hand_type in enumerate(reversed(CARD_HANDS))}

def get_max_value(hash_map: dict[str, int]):
    max_key = max(hash_map, key=hash_map.get)
    max_count = hash_map[max_key]
    return max_key, max_count

# @total_ordering
class CardHand:
    def __init__(self, hand: str, bid: int):
        self.hand = hand
        self.bid = bid
        self.hand_type = self._get_hand_type(hand)

    def __repr__(self) -> str:
        return 'Hand: {} type: {} bid: {}'.format(self.hand, self.hand_type, self.bid)
    
    def __eq__(self, value: CardHand) -> bool:
        return self.hand_type == value.hand_type

    # BE AWARE: shitty code
    def __lt__(self, value: CardHand) -> bool:
        if TYPE_TO_STRENGTH[self.hand_type] < TYPE_TO_STRENGTH[value.hand_type]:
            return True
        elif TYPE_TO_STRENGTH[self.hand_type] > TYPE_TO_STRENGTH[value.hand_type]:
            return False
        
        for i in range(len(self.hand)):
            if CHAR_TO_STRENGTH[self.hand[i]] < CHAR_TO_STRENGTH[value.hand[i]]:
                return True
            elif CHAR_TO_STRENGTH[self.hand[i]] > CHAR_TO_STRENGTH[value.hand[i]]:
                return False
        return False

    def _get_hand_type(self, hand: str) -> str:
        letters = {}
        for char in hand:
            if char not in letters:
                letters[char] = 0
            letters[char] += 1

        self._replace_joker(letters)

        max_key = max(letters, key=letters.get)
        max_count = letters[max_key]
        if len(letters) == 5:
            return 'high_card'
        elif len(letters) == 4:
            return 'one_pair'
        elif len(letters) == 3:
            return 'kind_three' if max_count == 3 else 'two_pair'
        elif len(letters) == 2:
            return 'kind_four' if max_count == 4 else 'full_house'
        else:
            return 'kind_five'

    def _replace_joker(self, letters: dict[str, int]):
        if 'J' not in letters:
            return letters

        max_key = max(letters, key=letters.get)
        max_count = letters[max_key]
        number_of_jokers = letters['J']
        if len(letters) <= 5 and len(letters) > 1:
            letters.pop('J')
            max_key, _ = get_max_value(letters)
            letters[max_key] += number_of_jokers

if __name__ == '__main__':
    with open('input.txt', 'r') as reader:
        input = reader.readlines()
        card_hands = [CardHand(hand, int(rank)) for hand, rank in [line.split(' ') for line in input]]
        card_hands.sort()
        [print(v) for v in card_hands]
        result = 0
        for i in range(len(card_hands)):
            rank = i + 1
            result += rank * card_hands[i].bid
        print('Result: {}'.format(result))