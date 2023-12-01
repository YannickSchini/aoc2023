from typing import Iterator
import re
import requests

SESSION_ID = "<PUT THE SESSION_ID FROM YOUR BROWSER'S AOC COOKIE>"

def get_input(day: int) -> Iterator[str]:
    uri = f"https://adventofcode.com/2023/day/{day}/input"
    response = requests.get(uri, cookies={"session": SESSION_ID})
    return response.iter_lines(decode_unicode=True)

def get_calibration_value_from_string(pattern: str, string: str, convert: bool = False) -> int:
    digits = re.findall(pattern, string)
    if convert:
        return int(_convert_matches_from_words_to_numbers(digits[0]) + _convert_matches_from_words_to_numbers(digits[-1]))
    else:
        return int(digits[0] + digits[-1])

def _convert_matches_from_words_to_numbers(match: str) -> str:
    if match == "one":
        return "1"
    elif match == "two":
        return "2"
    elif match == "three":
        return "3"
    elif match == "four":
        return "4"
    elif match == "five":
        return "5"
    elif match == "six":
        return "6"
    elif match == "seven":
        return "7"
    elif match == "eight":
        return "8"
    elif match == "nine":
        return "9"
    else:
        return match

if __name__ == "__main__":
    total_for_part_1 = 0
    total_for_part_2 = 0
    for line in get_input(1):
        total_for_part_1 += get_calibration_value_from_string("[1-9]", line)
        total_for_part_2 += get_calibration_value_from_string("(?=([1-9]|one|two|three|four|five|six|seven|eight|nine))", line, convert=True)
    print("Total for part 1: ", total_for_part_1)
    print("Total for part 2: ", total_for_part_2)
