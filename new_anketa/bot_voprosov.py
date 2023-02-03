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
    await message.answer("Привет, нажми ➕ что бы опрвить предложение или ❓ что бы задать вопрос.\nВ течении 24 часов мы тебе обязательно ответим"
                         , reply_markup=start_menu)



@COMMANDS.message_handler(regexp='➕')
async def texts(message: types.Message):
    if chek_banned(message):
        await message.answer("Вы забанены")
        return
    await BOT.delete_message(message.chat.id, message.message_id)
    await message.answer("Что желаете предложить?")
    await Test.state0.set()

@COMMANDS.message_handler(regexp='❓')
async def texts(message: types.Message):
    if chek_banned(message):
        await message.answer("Вы забанены")
        return
    await BOT.delete_message(message.chat.id, message.message_id)
    await message.answer("Что желаете спросить?")
    await Test.state1.set()

@COMMANDS.message_handler(state=[Test.state0, Test.state1])
async def write_info(message: types.Message, state: FSMContext):
    a = await state.get_state()
    if a == 'Test:state0':
        await state.update_data(state0=message.text)
        await Test.state01.set()
    elif a == 'Test:state1':
        await state.update_data(state1=message.text)
        await Test.state11.set()
    await message.answer(f"Информация заполнена правильно?", reply_markup=inline_send_data)



@COMMANDS.callback_query_handler(text="send_data", state=[Test.state01, Test.state11])
async def add_chat(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    a = await state.get_state()
    if a == 'Test:state01':
        await call.message.answer(f'Ваше предложение отправлено')
        data0 = data.get('state0')
        for el in group_info_id:
            await BOT.send_message(el, f'id {call.from_user.id}\nюзернейм {call.from_user.username}'
                                              f'\nполное имя {call.from_user.full_name}\n'
                                              f'предложение\n{data0}\n', reply_markup=inline_send_data1)
    elif a == 'Test:state11':
        await call.message.answer(f'Ваш вопрос отправлен')
        data1 = data.get('state1')
        for el in group_info_id:
            await BOT.send_message(el, f'id {call.from_user.id}\nюзернейм {call.from_user.username}'
                                              f'\nполное имя {call.from_user.full_name}\n'
                                              f'вопрос\n{data1}\n', reply_markup=inline_send_data1)


    await state.finish()

@COMMANDS.callback_query_handler(text="back_to_menu", state=[Test.state01,Test.state11])
async def add_chat(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(f'Заполни заново', reply_markup=start_menu)
    await state.finish()

@COMMANDS.callback_query_handler(text="send_data1")
async def add_chat(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f"Введите ответ")
    _id = call.message.text.split()[1]
    await Test.state3.set()
    await state.update_data(state3=_id)

@COMMANDS.message_handler(state=[Test.state3])
async def send_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id_ = data.get('state3')
    await BOT.send_message(id_, f'Ответ администратора:\n{message.text}')
    await message.answer(f"Сообщение отправлено")
    await state.finish()


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