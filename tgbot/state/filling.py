from aiogram.fsm.state import StatesGroup, State

class FillingState(StatesGroup):
    phone = State()

class FillingNameState(StatesGroup):
    name = State()

class FillingEmailState(StatesGroup):
    email = State()

class FillingCityState(StatesGroup):
    city = State()

class FillingExperienceState(StatesGroup):
    experience = State()

class FillingExperienceClientState(StatesGroup):
    experience_client = State()

class FillingMoneyState(StatesGroup):
    money = State()