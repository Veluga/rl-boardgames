import pytest

from heckmeck import HeckMeck
from random import seed

def generate_taken(target_sum):
    taken = []
    for i in range(6, 0, -1):
        taken.extend([i] * (target_sum // i))
        target_sum %= i
    return taken

@pytest.fixture
def game():
    yield HeckMeck()

@pytest.fixture
def empty_state():
    yield {
        'taken': [],
        'rolled': []
    }

@pytest.fixture
def seeded_randomizer():
    RANDOM_SEED = 0xDEADBEEF
    seed(RANDOM_SEED)
    yield