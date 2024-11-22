from aiogram.fsm.state import StatesGroup, State

class FillingState(StatesGroup):
    phone = State()

class FillingNameState(StatesGroup):
    name = State()

class FillingCityState(StatesGroup):
    city = State()

class FillingExperienceState(StatesGroup):
    experience = State()

class FillingExperienceClientState(StatesGroup):
    experience_client = State()

class FillingMoneyState(StatesGroup):
    money = State()