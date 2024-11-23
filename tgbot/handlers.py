import logging
import datetime
from aiogram import types
from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from kb_bot import kb_start, kb_choice_result
from state.filling import FillingCityState, FillingExperienceClientState, FillingExperienceState, FillingMoneyState, FillingNameState, FillingState
from message import send_email
from client  import append_to_google_sheet

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Начальный экран, где мы благодарим пользователя и предлагаем начать
async def cmd_start(message: types.Message):
    await message.answer(
        '😊Спасибо за ваш интерес к вакансии!\n'
        'Пожалуйста, ответьте на несколько\n'
        'вопросов, чтобы мы подобрали для вас\n'
        'подходящие условия.',
        reply_markup=kb_start
    )

# Запрос номера телефона
async def start_filling(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('<b>📞 Отправьте свой номер телефона</b>\nПример: <b>+7ХХХХХХХХХХ</b>', parse_mode='html')
    await state.set_state(FillingState.phone)

# Запрос имени
async def name_filling(message: types.Message, state: FSMContext):
    await message.answer('👤 Введите свою фамилию и имя')
    await state.update_data(phone=message.text)  # Сохраняем номер телефона
    await state.set_state(FillingNameState.name)

# Запрос города
async def city_filling(message: types.Message, state: FSMContext):
    await message.answer('🏙️ Введите свой город')
    await state.update_data(name=message.text)  # Сохраняем имя
    await state.set_state(FillingCityState.city)

# Вопрос о ремонте телефонов
async def experience_filling(message: types.Message, state: FSMContext):
    # Проверяем длину текста, если он слишком длинный
    if len(message.text) > 200:  # Лимит на 200 символов
        await message.answer('❌ Ваш ответ слишком длинный. Пожалуйста, введите менее 200 символов.')
        return

    await state.update_data(city=message.text)  # Сохраняем город
    await message.answer('🛠️ Есть ли у Вас опыт работы в сфере ремонтов телефонов?')
    await state.set_state(FillingExperienceState.experience)

# Вопрос о работе с клиентами
async def experience_client_filling(message: types.Message, state: FSMContext):
    # Проверяем длину текста, если он слишком длинный
    if len(message.text) > 200:  # Лимит на 200 символов
        await message.answer('❌ Ваш ответ слишком длинный. Пожалуйста, введите менее 200 символов.')
        return

    await state.update_data(experience=message.text)  # Сохраняем опыт
    await message.answer('📳 Есть ли у Вас опыт работы с клиентом напрямую?')
    await state.set_state(FillingExperienceClientState.experience_client)

# Вопрос о зарплате
async def money_filling(message: types.Message, state: FSMContext):
    await message.answer('💵 На какой уровень дохода Вы рассчитываете? (напишите сумму в сообщении)')
    await state.update_data(experience_client=message.text) 
    await state.set_state(FillingMoneyState.money)

# Подтверждение данных и вывод результата
async def result_filling(message: types.Message, state: FSMContext):
    await state.update_data(money=message.text)  # Сохраняем ожидаемый доход
    reg_data = await state.get_data()

    name = reg_data.get('name')
    city = reg_data.get('city')
    number = reg_data.get('phone')
    choice1 = reg_data.get('experience')
    choice2 = reg_data.get('experience_client')
    money = reg_data.get('money')  # Получаем ожидаемый доход

    await message.answer(
        f'<b>Итак, проверяем</b>\n\n'
        f'👤 Имя: {name}\n'
        f'🏙️ Город: {city}\n'
        f'📞 Телефон: {number}\n'
        f'🛠️ Опыт ремонта смартфонов: {choice1}\n'
        f'📳 Опыт работы с клиентами: {choice2}\n'
        f'💵 Ожидаемый доход: {money}\n\n'
        f'<b>Все верно?</b>\n\n'
        f'Если допустили ошибку или требуется корректировка,\n'
        f'нажмите на кнопку "Обновить данные📳 и ответьте,\n'
        f'пожалуйста, на вопросы еще раз.',
        parse_mode='html', reply_markup=kb_choice_result
    )

async def handle_confirmation(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message  # Получаем сообщение из колбэка
    if callback.data == "result":
        reg_data = await state.get_data()
        name = reg_data.get('name')
        city = reg_data.get('city')
        number = reg_data.get('phone')
        choice1 = reg_data.get('experience')
        choice2 = reg_data.get('experience_client')
        money = reg_data.get('money')

        # Формируем тело письма
        email_body = (
            f'👤 Имя: {name}\n'
            f'🏙️ Город: {city}\n'
            f'📞 Телефон: {number}\n'
            f'🛠️ Опыт ремонта смартфонов: {choice1}\n'
            f'📳 Опыт работы с клиентами: {choice2}\n'
            f'💵 Ожидаемый доход: {money}\n'
        )

        try:
            # Отправляем электронное письмо
            email = 'testlolohka@gmail.com'  # Замените на нужный адрес
            subject = 'Новая заявка от пользователя'
            send_email(email, subject, email_body)

            # Записываем данные в Google таблицу
            data_to_append = [
                name,
                str(datetime.datetime.now()),  # Дата создания заявки
                city,  # Здесь можно указать почту, если она есть
                email,
                number,
                choice1,
                choice2,
                money,
            ]
            append_to_google_sheet(data_to_append)  # Записываем данные

            await message.answer('✅ Мы начали изучать вашу анкету!\nОбязательно свяжемся с вами\n' +
                                 'в ближайшее время.\nА пока предлагаем посмотреть\n' +
                                 'интереснейшее интервью с основателем Pedant.ru, вот ссылка\n' +
                                 '👉 https://youtu.be/PlAcF_CuWPo?si=_lBWGXwMLDNO3M20\nДо скорого!')

        except Exception as e:
            logger.error(f'Ошибка при отправке письма или записи в таблицу: {e}')  # Логируем ошибку
            await message.answer(f'❌ Ошибка при отправке письма или записи в таблицу!')

    elif callback.data == "edit":
        await message.answer('Хорошо, давайте начнем с начала. \nПожалуйста, отправьте свой номер телефона.')
        await state.set_state(FillingState.phone)  # Возвращаемся к началу заполнения данных

# Регистрация всех обработчиков
def reg_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command(commands=['start']))
    dp.callback_query.register(start_filling, F.data == "start")
    dp.message.register(name_filling, FillingState.phone)
    dp.message.register(city_filling, FillingNameState.name)
    dp.message.register(experience_filling, FillingCityState.city)
    dp.message.register(experience_client_filling, FillingExperienceState.experience)
    dp.message.register(money_filling, FillingExperienceClientState.experience_client)
    dp.message.register(result_filling, FillingMoneyState.money)
    dp.callback_query.register(handle_confirmation, F.data.in_({"result", "edit"}))  # Обработка подтверждения данных