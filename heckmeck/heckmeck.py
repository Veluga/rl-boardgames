from enum import Enum, auto
from random import randint

class IllegalActionException(Exception):
    pass

class HeckMeck:
    class Action(Enum):
        TAKE_ONE = 1
        TAKE_TWO = 2
        TAKE_THREE = 3
        TAKE_FOUR = 4
        TAKE_FIVE = 5
        TAKE_WURM = 6
        TAKE_POT = auto()
        TAKE_VISIBLE = auto()
    
    NUM_DICE = 8

    CARD_VALUES = {
        21: 1,
        22: 1,
        23: 1,
        24: 1,
        25: 2,
        26: 2,
        27: 2,
        28: 2,
        29: 3,
        30: 3,
        31: 3,
        32: 3,
        33: 4,
        34: 4,
        35: 4,
        36: 4,
    }

    def __init__(self, state=None):
        self.state = state or {}

    def isTakingAction(self, action):
        return any(
            action == takingAction for takingAction in [
                HeckMeck.Action.TAKE_ONE,
                HeckMeck.Action.TAKE_TWO,
                HeckMeck.Action.TAKE_THREE,
                HeckMeck.Action.TAKE_FOUR,
                HeckMeck.Action.TAKE_FIVE,
                HeckMeck.Action.TAKE_WURM,
            ]
        )

    def getLargestAvailableInSelection(self, taken, selection):
        sumTaken = sum(taken)
        maxAvailable = -1
        for potNum in selection:
            if sumTaken >= potNum:
                maxAvailable = potNum
        if maxAvailable == -1:
            raise IllegalActionException(
                f"Sum of dice must be larger than or equal to at least one number in pot."
            )
        else:
            return HeckMeck.CARD_VALUES[maxAvailable]

    def getMatchingInSelection(self, taken, selection):
        if sum(taken) in selection:
            return HeckMeck.CARD_VALUES[sum(taken)]
        else:
            raise IllegalActionException("Sum of taken dice must match card.")

    def takeDice(self, action):
        if action.value in self.state['taken']:
                raise IllegalActionException(f"Dice with value {action.value} have already been taken.")

        if len(self.state['taken']) == HeckMeck.NUM_DICE:
            raise IllegalActionException(f"Cannot take dice if no dice remain.")

        numMatchingDice = self.state['rolled'].count(action.value)
        self.state['taken'].extend([action.value] * numMatchingDice)
        self.state['rolled'] = [
            randint(1, 6) for _ in range(
                len(self.state['rolled']) - numMatchingDice
            )
        ]
        return 0

    def updateState(self, action):
        if self.isTakingAction(action):
            return self.takeDice(action)
            
        if action == HeckMeck.Action.TAKE_POT:
            return self.getLargestAvailableInSelection(
                self.state['taken'],
                self.state['pot']
            )
            
        if action == HeckMeck.Action.TAKE_VISIBLE:
            return self.getMatchingInSelection(
                self.state['taken'],
                self.state['visible']
            )