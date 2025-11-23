from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):

    waiting_for_file = State()

class AdminStates(StatesGroup):

    waiting_for_broadcast_text = State()
    waiting_for_button_text = State()
    waiting_for_button_url = State()
