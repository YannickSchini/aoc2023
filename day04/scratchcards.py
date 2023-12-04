###########################################################
########################  DAY 04  #########################
###########################################################

from dataclasses import dataclass


def get_scratchcards_value(filename: str) -> int:
    with open(filename, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    total = 0
    for line in lines:
        scratchcard = process_raw_scratchcard(line)
        total += scratchcard.value

    return total

def get_amount_of_scratchcards(filename: str) -> int:
    with open(filename, "r") as f:
        lines = f.readlines()
    scratchcards = {(idx + 1): [process_raw_scratchcard(lines[idx].strip())] for idx in range(len(lines))}
    for idx in range(1, len(lines) + 1):
        new_cards = get_amount_of_winning_numbers(scratchcards[idx][0].winning_numbers, scratchcards[idx][0].numbers)
        for new_cards_idx in range(1, new_cards + 1):
            for _ in range(1, len(scratchcards[idx]) + 1):
                scratchcards[idx + new_cards_idx].append(scratchcards[idx + new_cards_idx][0])

    return sum([len(value) for value in scratchcards.values()])

###########################################################
###################  INPUT PROCESSING  ####################
###########################################################

@dataclass
class ScratchCard:
    card_id: int
    value: int
    winning_numbers: list[int]
    numbers: list[int]

def process_raw_scratchcard(raw_scratchcard: str) -> ScratchCard:
    raw_id, raw_all_numbers = raw_scratchcard.split(":")
    card_id = int(raw_id.lstrip("Card "))
    raw_winning_numbers, raw_numbers = raw_all_numbers.strip().split("|")
    winning_numbers = [int(num.strip()) for num in raw_winning_numbers.split()]
    numbers = [int(num.strip()) for num in raw_numbers.split()]
    winning_numbers_the_card_has = get_amount_of_winning_numbers(winning_numbers, numbers)
    value = get_points_from_numbers(winning_numbers_the_card_has)
    return ScratchCard(
        card_id=card_id,
        winning_numbers=winning_numbers,
        numbers=numbers,
        value=value
    )
    

###########################################################
####################  BUSINESS LOGIC  #####################
###########################################################

def get_amount_of_winning_numbers(winning_numbers: list[int], numbers: list[int]) -> int:
    winning_numbers_the_card_has = 0
    for number in numbers:
        if number in winning_numbers:
            winning_numbers_the_card_has += 1
    return winning_numbers_the_card_has

def get_points_from_numbers(winning_numbers_the_card_has: int) -> int:
    if winning_numbers_the_card_has == 0:
        return 0
    else:
        return 2**(winning_numbers_the_card_has - 1)

if __name__ == "__main__":
    assert get_scratchcards_value("test.txt") == 13
    print(get_scratchcards_value("input.txt"))
    assert get_amount_of_scratchcards("test.txt") == 30
    print(get_amount_of_scratchcards("input.txt"))
