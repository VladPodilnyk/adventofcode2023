import sys

#from test_input import SEEDS, SEEDS_TO_SOIL, SOIL_TO_FERTILIZER, FERTILIZER_TO_WATER, WATER_TO_LIGHT, LIGHT_TO_TEMPERATURE, TEMPERATURE_TO_HUMIDITY, HUMIDITY_TO_LOCATION
from input import SEEDS, SEEDS_TO_SOIL, SOIL_TO_FERTILIZER, FERTILIZER_TO_WATER, WATER_TO_LIGHT, LIGHT_TO_TEMPERATURE, TEMPERATURE_TO_HUMIDITY, HUMIDITY_TO_LOCATION

MAPS = [
    SEEDS_TO_SOIL,
    SOIL_TO_FERTILIZER,
    FERTILIZER_TO_WATER,
    WATER_TO_LIGHT,
    LIGHT_TO_TEMPERATURE,
    TEMPERATURE_TO_HUMIDITY,
    HUMIDITY_TO_LOCATION,
]

class Location:
    def __init__(self, source: int, dest: int, length: int):
        self.source = source
        self.dest = dest
        self.length = length

    def get_end(self) -> int:
        return self.source + self.length - 1

    def __repr__(self) -> str:
        return 'Location({}, {}, {})'.format(self.source, self.dest, self.length)

def parse_map(input: str) -> list[Location]:
    rows = list(filter(lambda value: len(value) > 0, input.split('\n')))
    data = []
    for row in rows:
        raw_location = [int(value) for value in row.split(' ')]
        data.append(Location(raw_location[1], raw_location[0], raw_location[2]))
    return data

class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
    
    def __repr__(self) -> str:
        return 'Range({}, {})'.format(self.start, self.end)

class Solution:
    def __init__(self, seeds: list[Range], locations: list[list[Location]]):
        self.seeds = seeds
        self.locations = locations

    def find_min_location(self) -> int:
        min_location = sys.maxsize
        for seed in self.seeds:
            curr_location = self.map_seed_to_location(seed)
            min_location = min(min_location, curr_location)
        return min_location

    def map_seed_to_location(self, seed: Range) -> list[Range]:
        ranges = [seed]
        for location in self.locations:
            result_ranges = []
            for range in ranges:
                result_ranges.extend(self.intersect(location, range))
            result_ranges.sort(key=lambda value: value.start)
            ranges = result_ranges
        return ranges[0].start

    # |---------------------|      |---------------------------------|   |-----|
    #    |-----| |--|     |-----|     |-----|          |-----|
    # |--|+++++|-|++|-----|+|      |--|+++++|----------|+++++|-------|   |-----|
    def intersect(self, locations: list[Location], range: Range) -> list[Range]:
        locations.sort(key=lambda value: value.source)
        startRange = range.start
        i = 0
        result = []
        while startRange < range.end and i < len(locations):
            l = locations[i]
            if range.end < l.source:
                return [range]
            elif range.end < l.get_end():
                if startRange < l.source:
                    result.append(Range(startRange, l.source - 1))
                    startRange = l.source
                else:
                    offset_start = startRange - l.source
                    offset_end = range.end - l.source
                    result.append(Range(l.dest + offset_start, l.dest + offset_end))
                    return result
            else:
                if startRange > l.get_end():
                    i += 1
                elif startRange < l.source:
                    result.append(Range(startRange, l.source - 1))
                    startRange = l.source
                else:
                    offset_start = startRange - l.source
                    offset_end = l.get_end() - l.source
                    result.append(Range(l.dest + offset_start, l.dest + offset_end))
                    startRange = l.get_end() + 1
                    i += 1

        if startRange < range.end:
            result.append(Range(startRange, range.end))
        return result


if __name__ == '__main__':
    seeds_raw = [int(value) for value in SEEDS.split(' ')]
    seed_ranges = [Range(seeds_raw[i], seeds_raw[i] + seeds_raw[i + 1] - 1) for i in range(0, len(seeds_raw) - 1, 2)]
    locations = [parse_map(m) for m in MAPS]
    solver = Solution(seed_ranges, locations)
    print('Min location: {}'.format(solver.find_min_location()))