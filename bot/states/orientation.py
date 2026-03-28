from aiogram.fsm.state import State, StatesGroup


class OrientationStates(StatesGroup):
    taking_quiz = State()
