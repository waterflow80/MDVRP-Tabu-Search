from typing import Tuple
from random import randint

ID = -1
ID2 = -1
def generate_id()->int:
    global ID
    ID += 1
    return ID

def generate_vehicle_id()->int:
    global ID2
    ID2 += 1
    return ID2
def generate_random_location()->Tuple[int, int]:
    """Generate a random location for a depot"""
    x = randint(0, 70) # This can be better adjusted
    y = randint(0, 70)
    return x, y

if __name__ == "__main__":
    print(generate_random_location())