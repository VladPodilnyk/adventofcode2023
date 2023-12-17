from collections.abc import Mapping

CUBES = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

class Game:
    def __init__(self, game_index: int, game_data: list[Mapping[str, int]]):
        self.game_index = game_index
        self.game_data = game_data

    def cube_history(self) -> Mapping[str, list[int]]:
        result = {}
        for game_turn in self.game_data:
            for cube_color, cube_count in game_turn.items():
                if cube_color not in result:
                    result[cube_color] = []
                result[cube_color].append(cube_count)
        return result

def parse_game(game_info_raw: str) -> Game:
    data = game_info_raw.split(':')
    game_index = int(data[0].split(' ')[1])

    game_data = []
    for game_turn in data[1].split(';'):
        mapping = {}
        for cube_data_raw in game_turn.split(','):
            values = cube_data_raw.strip().split(' ')
            mapping[values[1]] = int(values[0])
        game_data.append(mapping)

    return Game(game_index, game_data)

# Returns game index and if the game is valid
# Puzzle part 1
def validate_game(game_info: Game) -> tuple[int, bool]:
    for game_turn in game_info.game_data:
        for cube_color, cube_count in game_turn.items():
            if cube_color in CUBES and cube_count > CUBES[cube_color]:
                return game_info.game_index, False

    return game_info.game_index, True

# Return a power of a set for a given game
def find_set_power(game_info: Game) -> int:
    history_per_color = game_info.cube_history()
    set_power = 1
    for _, history in history_per_color.items():
        set_power *= max(history)
    return set_power

if __name__ == '__main__':
    with open('test-input.txt', 'r') as reader:
        input = reader.readlines()
        # result = 0
        # for line in input:
        #     game_data = parse_game(line)
        #     game_index, is_valid = validate_game(game_data)
        #     if is_valid:
        #         result += game_index
        
        # print('Result: ', result)
        result = 0
        for line in input:
            game_data = parse_game(line)
            set_power = find_set_power(game_data)
            result += set_power

        print('Result: ', result)