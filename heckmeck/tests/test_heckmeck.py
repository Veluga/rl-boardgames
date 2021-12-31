import json
import pytest
from conftest import generate_taken
from random import randint, seed

from heckmeck import HeckMeck, IllegalActionException

def test_construction(
    game
):
    assert isinstance(game, HeckMeck)
    assert game.state == {}

def test_update_state_taking_wurm_with_no_taken_succeeds_with_zero_reward(
    game,
    empty_state
):
    game.state = empty_state
    reward = game.updateState(HeckMeck.Action.TAKE_WURM)
    assert reward == 0

@pytest.mark.parametrize(
    "taking_action",
    [
        HeckMeck.Action.TAKE_ONE,
        HeckMeck.Action.TAKE_TWO,
        HeckMeck.Action.TAKE_THREE,
        HeckMeck.Action.TAKE_FOUR,
        HeckMeck.Action.TAKE_FIVE,
        HeckMeck.Action.TAKE_WURM,
    ]
)
def test_update_state_taking_num_with_num_taken_raises(
    game,
    taking_action
):
    state = {
        'taken': [taking_action.value]
    }
    game.state = state
    with pytest.raises(
        IllegalActionException
    ):
        game.updateState(taking_action)

@pytest.mark.parametrize(
    "pot_num",
    [i for i in range(21, 37)]
)
def test_update_state_taking_pot_succeeds_for_sum_equal(
    game,
    pot_num
):
    state = {
        'pot': [pot_num],
        'taken': generate_taken(pot_num)
    }
    game.state = state
    assert game.updateState(HeckMeck.Action.TAKE_POT) == HeckMeck.CARD_VALUES[pot_num]

@pytest.mark.parametrize(
    "pot_num",
    [i for i in range(21, 37)]
)
def test_update_state_taking_pot_succeeds_for_sum_greater_than(
    game,
    pot_num
):
    state = {
        'pot': [pot_num],
        'taken': generate_taken(pot_num+1)
    }
    game.state = state
    assert game.updateState(HeckMeck.Action.TAKE_POT) == HeckMeck.CARD_VALUES[pot_num]

@pytest.mark.parametrize(
    "pot_num",
    [i for i in range(21, 37)]
)
def test_update_state_taking_pot_raises_for_sum_smaller_than_pot(
    game,
    pot_num
):
    state = {
        'pot': [pot_num],
        'taken': generate_taken(pot_num-1)
    }
    game.state = state
    with pytest.raises(
        IllegalActionException
    ):
        game.updateState(HeckMeck.Action.TAKE_POT)

@pytest.mark.parametrize(
    "pot_num",
    [i for i in range(22, 37)]
)
def test_update_state_taking_pot_takes_largest_if_no_matching(
    game,
    pot_num
):
    state = {
        'pot': [pot_num-1, pot_num],
        'taken': generate_taken(pot_num+1)
    }
    game.state = state
    assert game.updateState(HeckMeck.Action.TAKE_POT) == HeckMeck.CARD_VALUES[pot_num]

@pytest.mark.parametrize(
    "pot_num",
    [i for i in range(21, 37)]
)
def test_update_state_taking_visible_succeeds_for_sum_equal(
    game,
    pot_num
):
    state = {
        'visible': [pot_num],
        'taken': generate_taken(pot_num)
    }
    game.state = state
    assert game.updateState(HeckMeck.Action.TAKE_VISIBLE) == HeckMeck.CARD_VALUES[pot_num]
    
@pytest.mark.parametrize(
    "pot_num",
    [i for i in range(21, 37)]
)
def test_update_state_taking_visible_raises_for_sum_greater_than(
    game,
    pot_num
):
    state = {
        'visible': [pot_num],
        'taken': generate_taken(pot_num+1)
    }
    game.state = state
    with pytest.raises(
        IllegalActionException
    ):
        game.updateState(HeckMeck.Action.TAKE_VISIBLE)

@pytest.mark.parametrize(
    "pot_num",
    [i for i in range(21, 37)]
)
def test_update_state_taking_visible_raises_for_sum_smaller_than(
    game,
    pot_num
):
    state = {
        'visible': [pot_num],
        'taken': generate_taken(pot_num-1)
    }
    game.state = state
    with pytest.raises(
        IllegalActionException
    ):
        game.updateState(HeckMeck.Action.TAKE_VISIBLE)

@pytest.mark.parametrize(
    "taking_action,taken_eyes",
    [
        (HeckMeck.Action.TAKE_ONE, 2),
        (HeckMeck.Action.TAKE_TWO, 3),
        (HeckMeck.Action.TAKE_THREE, 4),
        (HeckMeck.Action.TAKE_FOUR, 5),
        (HeckMeck.Action.TAKE_FIVE, 6),
        (HeckMeck.Action.TAKE_WURM, 5)
    ]
)
def test_update_state_taking_num_raises_if_no_remaining_dice(
    game,
    taking_action,
    taken_eyes
):
    state = {
        'taken': [taken_eyes] * 8
    }
    game.state = state
    with pytest.raises(
        IllegalActionException
    ):
        game.updateState(taking_action)

@pytest.mark.parametrize(
    "taking_action,other_eyes",
    [
        (HeckMeck.Action.TAKE_ONE, 2),
        (HeckMeck.Action.TAKE_TWO, 3),
        (HeckMeck.Action.TAKE_THREE, 4),
        (HeckMeck.Action.TAKE_FOUR, 5),
        (HeckMeck.Action.TAKE_FIVE, 6),
        (HeckMeck.Action.TAKE_WURM, 5)
    ]
)
def test_update_state_taking_dice_adds_dice_to_taken(
    game,
    taking_action,
    other_eyes
):
    state = {
        'taken': [],
        'rolled': [taking_action.value] * (HeckMeck.NUM_DICE // 2) + [other_eyes] * (HeckMeck.NUM_DICE // 2)
    }
    game.state = state
    game.updateState(taking_action)
    assert game.state['taken'] == [taking_action.value] * (HeckMeck.NUM_DICE // 2)

@pytest.mark.parametrize(
    "taking_action",
    [
        HeckMeck.Action.TAKE_ONE,
        HeckMeck.Action.TAKE_TWO,
        HeckMeck.Action.TAKE_THREE,
        HeckMeck.Action.TAKE_FOUR,
        HeckMeck.Action.TAKE_FIVE,
        HeckMeck.Action.TAKE_WURM,
    ]
)
@pytest.mark.usefixtures("seeded_randomizer")
def test_update_state_taking_dice_causes_reroll(
    game,
    taking_action
):
    rolled_pre = [randint(1, 6) for _ in range(HeckMeck.NUM_DICE)]
    state = {
        'taken': [],
        'rolled': rolled_pre
    }
    game.state = state
    game.updateState(taking_action)
    assert game.state['rolled'] != rolled_pre
    assert len(game.state['rolled']) == HeckMeck.NUM_DICE - rolled_pre.count(taking_action.value)

@pytest.mark.parametrize(
    "pot_nums,taken",
    [
        ([21], [5, 5, 5, 5, 1]),
        ([36], [5, 5, 5, 5, 5, 5, 5, 1]),
    ]
)
def test_taking_pot_with_no_wurm_taken_raises(
    game,
    pot_nums,
    taken
):
    state = {
        'taken': taken,
        'pot': pot_nums
    }
    game.state = state
    with pytest.raises(
        IllegalActionException
    ):
        game.updateState(HeckMeck.Action.TAKE_POT)

@pytest.mark.parametrize(
    "visible_nums,taken",
    [
        ([21], [5, 5, 5, 5, 1]),
        ([36], [5, 5, 5, 5, 5, 5, 5, 1]),
    ]
)
def test_taking_visible_with_no_wurm_taken_raises(
    game,
    visible_nums,
    taken
):
    state = {
        'taken': taken,
        'visible': visible_nums
    }
    game.state = state
    with pytest.raises(
        IllegalActionException
    ):
        game.updateState(HeckMeck.Action.TAKE_VISIBLE)