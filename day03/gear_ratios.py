from dataclasses import dataclass
import re

###########################################################
#################  GEAR RATIOS  ###########################
###########################################################

def sum_of_part_numbers(filename: str) -> int:
    with open(filename, "r") as f:
        lines = f.readlines()

    total = 0
    schematic = EngineSchematic(lines=[line.strip() for line in lines])
    numbers = get_numbers(schematic)
    for number in numbers:
        if is_part_number(number, schematic):
            total += number.value

    return total

def sum_of_gear_ratios(filename: str) -> int:
    with open(filename, "r") as f:
        lines = f.readlines()

    total = 0
    schematic = EngineSchematic(lines=[line.strip() for line in lines])
    numbers = get_numbers(schematic)
    gears = get_gears(schematic)

    for gear in gears:
        total += find_gear_value(gear, numbers)

    return total


###########################################################
################  INPUT PROCESSING  #######################
###########################################################

@dataclass
class EngineSchematic:
    lines: list[str]

@dataclass
class Coord:
    line_num: int
    col_num: int

@dataclass
class Number:
    value: int
    start: Coord
    end: Coord

@dataclass
class Gear:
    position: Coord

def get_numbers(engine_schematic: EngineSchematic) -> list[Number]:
    numbers = []
    digits = re.compile(r"\d+")
    for idx in range(0, len(engine_schematic.lines)):
        for match in digits.finditer(engine_schematic.lines[idx]):
            numbers.append(
                Number(
                    value=int(match.group(0)),
                    start=Coord(idx, match.start()),
                    end=Coord(idx, match.end())
                )
            )
    return numbers

def get_gears(engine_schematic: EngineSchematic) -> list[Gear]:
    gears = []
    digits = re.compile(r"\*")
    for idx in range(0, len(engine_schematic.lines)):
        for match in digits.finditer(engine_schematic.lines[idx]):
            gears.append(
                Gear(
                    position=Coord(idx, match.start()),
                )
            )
    return gears

###########################################################
#################  BUSINESS LOGIC  ########################
###########################################################

def is_part_number(number: Number, schematic: EngineSchematic) -> bool:
    start_of_string_to_check = max(0, number.start.col_num - 1)
    end_of_string_to_check = min(len(schematic.lines[0]), number.end.col_num) + 1
    # Line above
    if does_string_contain_symbol(schematic.lines[max(0, number.start.line_num - 1)][start_of_string_to_check:end_of_string_to_check]):
        return True
    # Line of the number
    elif does_string_contain_symbol(schematic.lines[number.start.line_num][start_of_string_to_check:end_of_string_to_check]):
        return True
    # Line below
    elif does_string_contain_symbol(schematic.lines[min(len(schematic.lines), number.start.line_num + 1)][start_of_string_to_check:end_of_string_to_check]):
        return True
    else:
        return False

def does_string_contain_symbol(string: str) -> bool:
    symbols = re.compile(r"[^\d\.]")
    return symbols.search(string) is not None

def find_gear_value(gear: Gear, numbers: list[Number]) -> int:
    close_numbers_values = []
    for number in numbers:
        if is_number_far_from_gear(gear, number):
            continue
        else:
            close_numbers_values.append(number.value)

            
    if len(close_numbers_values) == 2:
        return close_numbers_values[0] * close_numbers_values[1]
    else:
        return 0

def is_number_far_from_gear(gear: Gear, number: Number) -> bool:
    # check the lines
    if number.start.line_num >= (gear.position.line_num + 2) or number.start.line_num <= (gear.position.line_num - 2):
        return True
    # check the colums
    elif number.start.col_num >= (gear.position.col_num + 2) or number.end.col_num <= (gear.position.col_num - 1):
        return True
    else:
        return False

if __name__ == "__main__":
    assert sum_of_part_numbers("test.txt") == 4361
    print("Part 1: ", sum_of_part_numbers("input.txt"))
    assert sum_of_gear_ratios("test.txt") == 467835
    print("Part 2: ", sum_of_gear_ratios("input.txt"))
