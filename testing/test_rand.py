import random
from pitd.rand import Seed

RANDOM_SEED = 69420
RANDOM_SEED_STR = "RyuZMn4QH6lbGW5O"
RANDOM_SEED_HASH = 94685055
SUPPLIED_SEED_STR = "hello world"
SUPPLIED_SEED_HASH = 5751529


def test_seed_random_str():
    random.seed(RANDOM_SEED)
    seed = Seed()
    assert seed.seed == RANDOM_SEED_STR


def test_seed_random_hash():
    random.seed(RANDOM_SEED)
    seed = Seed()
    assert seed.get() == RANDOM_SEED_HASH


def test_seed_supplied_str():
    seed = Seed(SUPPLIED_SEED_STR)
    assert seed.seed == SUPPLIED_SEED_STR


def test_seed_supply_hash():
    random.seed(RANDOM_SEED)
    seed = Seed(SUPPLIED_SEED_STR)
    assert seed.get() == SUPPLIED_SEED_HASH
