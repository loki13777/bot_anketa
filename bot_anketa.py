import aiogram.contrib.fsm_storage.memory
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from keyboards import start_menu,  inline_send_data, inline_send_data1
from state import Test
import config
import json

storage = aiogram.contrib.fsm_storage.memory.MemoryStorage()
token = config.token
BOT = Bot(token=token)
COMMANDS = Dispatcher(BOT, storage=storage)
state_dict = {}
group_info_id = config.group_info_id


def chek_banned(message: types.Message):
    with open("users_id_ban.json", "r") as file:
        a = json.load(file)
    if str(message.from_user.id) in a:
        return True


@COMMANDS.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    if chek_banned(message):
        await message.answer("Вы забанены")
        return
    await message.answer("Привет, заполни анкету", reply_markup=start_menu)


@COMMANDS.message_handler(regexp='💣Заполнить анкету')
async def texts(message: types.Message):
    if chek_banned(message):
        await message.answer("Вы забанены")
        return
    await BOT.delete_message(message.chat.id, message.message_id)
    await message.answer("вопрос 1")
    await Test.state0.set()


@COMMANDS.message_handler(state=Test.state0)
async def write_info(message: types.Message, state: FSMContext):
    await state.update_data(state0=message.text)
    await message.answer("вопрос 2")
    await Test.state1.set()


@COMMANDS.message_handler(state=Test.state1)
async def write_info(message: types.Message, state: FSMContext):
    await state.update_data(state1=message.text)
    await message.answer(f"вопрос 3")
    await Test.state2.set()


@COMMANDS.message_handler(state=Test.state2)
async def write_info(message: types.Message, state: FSMContext):
    await state.update_data(state2=message.text)
    await message.answer("вопрос 4")
    await Test.state3.set()


@COMMANDS.message_handler(state=Test.state3)
async def write_info(message: types.Message, state: FSMContext):
    await state.update_data(state3=message.text)
    await message.answer("вопрос 5")
    await Test.state4.set()


@COMMANDS.message_handler(state=Test.state4)
async def write_info(message: types.Message, state: FSMContext):
    await state.update_data(state4=message.text)
    await message.answer("вопрос 6")
    await Test.state5.set()


@COMMANDS.message_handler(state=[Test.state5])
async def write_info(message: types.Message, state: FSMContext):
    await state.update_data(state5=message.text)
    await message.answer(f"Информация заполнена правильно?", reply_markup=inline_send_data)
    await Test.state6.set()


@COMMANDS.callback_query_handler(text="send_data", state=Test.state6)
async def add_chat(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(f'Ваши данные отправлены дождитесь ответа от бота,'
                              f'если ответа нет заявка не одобрена')
    data = await state.get_data()

    data0 = data.get('state0')
    data1 = data.get('state1')
    data2 = data.get('state2')
    data3 = data.get('state3')
    data4 = data.get('state4')
    data5 = data.get('state5')
    for el in group_info_id:
        await BOT.send_message(el, f'id {call.from_user.id}\nюзернейм {call.from_user.username}'
                                          f'\nполное имя {call.from_user.full_name}\n'
                                          f'вопрос 1\n-{data0}\n'
                                          f'вопрос 2\n-{data1}\n'
                                          f'вопрос 3\n-{data2}\n'
                                          f'вопрос 4\n-{data3}\n'
                                          f'вопрос 5\n-{data4}\n'
                                          f'вопрос 6\n-{data5}\n', reply_markup=inline_send_data1)
    await state.finish()


@COMMANDS.callback_query_handler(text="back_to_menu", state=Test.state6)
async def add_chat(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(f'Заполни заново', reply_markup=start_menu)
    await state.finish()


@COMMANDS.callback_query_handler(text="send_data1")
async def add_chat(call: types.CallbackQuery):
    await call.message.answer(f"Принято")
    call.message.text.split()
    await BOT.send_message(call.message.text.split()[1], 'заявка одобрена')


@COMMANDS.callback_query_handler(text="edit_data1")
async def add_chat(call: types.CallbackQuery):
    await call.message.delete()


@COMMANDS.callback_query_handler(text="ban")
async def add_chat(call: types.CallbackQuery):
    _id = call.message.text.split()[1]
    await call.message.delete()
    with open("users_id_ban.json", "r") as file:
        a = json.load(file)
    with open("users_id_ban.json", "w") as file:
        a.append(_id)
        json.dump(a, file, indent=1)


executor.start_polling(COMMANDS, skip_updates=True)
