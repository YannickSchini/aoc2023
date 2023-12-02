from collections import defaultdict
from dataclasses import dataclass
from math import prod

# PART 1
def sum_of_ids(file_name: str) -> int:
    with open(file_name, "r") as f:
        raw_games = f.readlines()

    games = [_process_raw_games(raw_game) for raw_game in raw_games]

    total = 0
    content_of_bag = {"red": 12, "green": 13, "blue": 14}
    for game in games:
        if is_game_possible(game, content_of_bag):
            total += game.id
    return total

# PART 2
def sum_of_powers(file_name: str) -> int:
    with open(file_name, "r") as f:
        raw_games = f.readlines()

    games = [_process_raw_games(raw_game) for raw_game in raw_games]

    total = 0
    for game in games:
        total += get_power_of_game(game)
    return total

###############################################
#############  INPUT PROCESSING  ##############
###############################################
@dataclass
class Game:
    id: int
    draws: list[dict[str, int]]


def _process_raw_games(raw_game: str) -> Game:
    id_part, draw_part = raw_game.split(":")
    raw_draws = draw_part.split(";")

    return Game(
        id= int(id_part.lstrip("Game ")),
        draws=[_parse_raw_draw(raw_draw) for raw_draw in raw_draws],
    )

def _parse_raw_draw(raw_draw: str) -> dict[str, int]:
    raw_colors = raw_draw.split(",")
    draw: dict[str, int] = defaultdict(lambda: 0)
    for raw_color in raw_colors:
        amount, color = raw_color.strip().split(" ")
        draw[color] = int(amount)
    return draw

###############################################
#############  "BUSINESS" LOGIC  ##############
###############################################
def is_game_possible(game: Game, content_of_bag: dict[str, int]):
    for draw in game.draws:
        for color in content_of_bag:
            if draw[color] > content_of_bag[color]:
                return False
    return True

def get_power_of_game(game: Game) -> int:
    minimal_bag = defaultdict(lambda: 0)
    for draw in game.draws:
        for color in draw:
            if draw[color] > minimal_bag[color]:
                minimal_bag[color] = draw[color]
    return prod(minimal_bag.values())

if __name__ == "__main__":
    assert sum_of_ids("test.txt") == 8
    print(sum_of_ids("input.txt"))
    assert sum_of_powers("test.txt") == 2286
    print(sum_of_powers("input.txt"))
