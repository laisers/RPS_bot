import asyncio
import sqlite3, random
from pyqiwip2p import QiwiP2P

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import *
from texts import *
from keyboards import *
import functions


class StorageFunctions(StatesGroup):
    here_game_start = State()
    here_continue_game = State()
    here_knb_game = State()
    here_pay_qiwi = State()


SQLITE_DATABASE = 'db.sqlite'

# Checking the presence of tables in the database, if not - create
with sqlite3.connect(SQLITE_DATABASE, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
    cur = con.cursor()
    # USERS
    try:
        cur.execute("SELECT * FROM users")
    except sqlite3.OperationalError:
        print("TABLE < users > NOT FOUND")
        cur.execute(
            "CREATE TABLE users(iduser TEXT, balance INT, wins INT, sub_notifications INT)")
        print("TABLE < users > SUCCESS CREATED")
if con:
    con.close()

# Подключениек к боту
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

p2p = QiwiP2P(auth_key=QIWI_TOKEN)


# Start command handler
@dp.message_handler(commands=['start'], state="*")
async def start_message(message: types.Message, state: FSMContext):
    await message.answer(welcome, parse_mode="HTML", reply_markup=but_menu())
    with sqlite3.connect(SQLITE_DATABASE, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
        cur = con.cursor()
        respone = cur.execute("SELECT * FROM users WHERE iduser = ?", (message.from_user.id,)).fetchone()
        if respone is None:
            cur.executemany(
                "INSERT INTO users(iduser, balance, wins, sub_notifications) VALUES (?, ?, ?, ?)",
                [(message.from_user.id, USER_STARTBALANCE, 0, 1)])


# В главное меню
@dp.message_handler(text='Вернуться в главное меню', state="*")
async def lk(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Главное меню', reply_markup=but_menu())


# Документация
@dp.message_handler(text='🔰 Документация', state="*")
async def document(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(documentation, parse_mode="HTML", reply_markup=but_menu())


# Личный кабинет
@dp.message_handler(text='📙 Личный кабинет', state="*")
async def lk(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text_profile(message.from_user.id), reply_markup=inline_profile,
                         parse_mode="Markdown")


# Обработка кнопки "Играть"
@dp.message_handler(text='🎲 Играть', state="*")
async def game(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Введите сумму ставки: ', reply_markup=but_back())
    await StorageFunctions.here_game_start.set()


# Other functions
@dp.message_handler(state=StorageFunctions.here_game_start)
async def check_bet(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await state.finish()
        await message.answer('Главное меню', reply_markup=but_menu())
        return
    with sqlite3.connect(SQLITE_DATABASE, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE iduser = ?", (message.from_user.id,))
        row = cur.fetchone()
        balance = row[1]
    bet = message.text
    if int(bet) <= 0:
        await message.answer('Вы ввели число равное или меньшее нулю, ставка отменена', reply_markup=but_back())
    elif int(bet) > balance:
        await message.answer('На вашем балансе недостаточно средств, ставка отменена', reply_markup=but_back())

    else:
        await message.answer("🔹 Ваша ставка: " + bet)
        captha = random.randint(10000, 99999)
        await message.answer(f'Введите:  <b>{captha}</b>  для подтверждения того, что вы не бот!')
        async with state.proxy() as data:
            data['bet'] = bet
            data['captha'] = captha
        await StorageFunctions.here_continue_game.set()


@dp.message_handler(state=StorageFunctions.here_continue_game)
async def knb_choice(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await state.finish()
        await message.answer('Главное меню', reply_markup=but_menu())
        return
    async with state.proxy() as data:
        captha = data['captha']
    if message.text == str(captha):
        await message.answer('Выберите предмет: ', reply_markup=keyboard_game)
        await StorageFunctions.here_knb_game.set()
    else:
        await message.answer('❌ Неверная капча', reply_markup=but_back())


@dp.message_handler(state=StorageFunctions.here_knb_game)
async def knb_game(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await state.finish()
        await message.answer('Главное меню', reply_markup=but_menu())
        return
    async with state.proxy() as data:
        bet = data['bet']
    with sqlite3.connect(SQLITE_DATABASE, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
        cur = con.cursor()
        sqlite3.connect('db.sqlite')
        cur.execute("SELECT * FROM users WHERE iduser = ?", (message.from_user.id,))
        row = cur.fetchone()
        balance = row[1]
    if int(bet) > int(balance):
        await state.finish()
        await message.answer('У вас недостаточно средств 😔', reply_markup=but_menu())
        return
    subjects = ["✊ Камень", "✌ Ножницы", "🤚 Бумага"]

    # Selection of items
    player_choice = message.text
    ii_choice = random.choice(subjects)
    print(player_choice)
    print(ii_choice)

    # Development of events
    if player_choice == "✊ Камень" and ii_choice == "✊ Камень":
        await message.answer('🌚 Ничья!', reply_markup=keyboard_game)
    elif player_choice == "✌ Ножницы" and ii_choice == "✌ Ножницы":
        await message.answer('🌚 Ничья!', reply_markup=keyboard_game)
    elif player_choice == "🤚 Бумага" and ii_choice == "🤚 Бумага":
        await message.answer('🌚 Ничья!', reply_markup=keyboard_game)
    elif player_choice == "✊ Камень" and ii_choice == "✌ Ножницы":
        await message.answer('💥 Вы победили!\nПротивник выбрал "✌ Ножницы", награда начислена к вам на баланс.',
                             reply_markup=keyboard_game)
        functions.user_update_balance(message.from_user.id, int(bet))
        functions.user_update_wins(message.from_user.id, 1)
    elif player_choice == "✌ Ножницы" and ii_choice == "🤚 Бумага":
        await message.answer('💥 Вы победили!\nПротивник выбрал "🤚 Бумагу", награда начислена к вам на баланс.',
                             reply_markup=keyboard_game)
        functions.user_update_balance(message.from_user.id, int(bet))
        functions.user_update_wins(message.from_user.id, 1)
    elif player_choice == "🤚 Бумага" and ii_choice == "✊ Камень":
        await message.answer('💥 Вы победили!\nПротивник выбрал "✊ Камень", награда начислена к вам на баланс.',
                             reply_markup=keyboard_game)
        functions.user_update_balance(message.from_user.id, int(bet))
        functions.user_update_wins(message.from_user.id, 1)
    elif player_choice == "✊ Камень" and ii_choice == "🤚 Бумага":
        await message.answer('😣 Вы проиграли!\nПротивник выбрал "🤚 Бумагу", ставка вычтена из баланса.',
                             reply_markup=keyboard_game)
        functions.user_un_balance(message.from_user.id, int(bet))
    elif player_choice == "🤚 Бумага" and ii_choice == "✌ Ножницы":
        await message.answer('😣 Вы проиграли!\nПротивник выбрал "✌ Ножницы", ставка вычтена из баланса.',
                             reply_markup=keyboard_game)
        functions.user_un_balance(message.from_user.id, int(bet))
    elif player_choice == "✌ Ножницы" and ii_choice == "✊ Камень":
        await message.answer('😣 Вы проиграли!\nПротивник выбрал "✊ Камень", ставка вычтена из баланса.',
                             reply_markup=keyboard_game)
        functions.user_un_balance(message.from_user.id, int(bet))


@dp.callback_query_handler(text='paybal_inline', state="*")
async def show_payment(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(text_profile(call.message.chat.id), parse_mode="Markdown")
    await call.message.answer('Введите сумму пополнения: ')
    await StorageFunctions.here_pay_qiwi.set()


@dp.message_handler(state=StorageFunctions.here_pay_qiwi)
async def payment(message: types.Message, state: FSMContext):
    await state.finish()
    amount = message.text
    if amount.isdigit():
        if int(amount) < 10:
            await message.answer('❌ Минимальная сумма 10 рублей')
            return
        bill = p2p.bill(amount=amount, lifetime=45)  # Выставление счета
        key = InlineKeyboardMarkup()
        key.add(InlineKeyboardButton('Оплатить', url=bill.pay_url))
        key.add(InlineKeyboardButton('Проверить', callback_data=f"checkpay:{bill.bill_id}:{amount}"))
        await message.answer('Нажмите кнопку "Оплатить" для пополнения.\nПосле оплаты нажмите "Проверить"',
                             reply_markup=key)
    else:
        await message.answer('❌ Введите число!')


# Проверка оплаты
@dp.callback_query_handler(text_startswith='checkpay', state="*")
async def checkpayf(call: CallbackQuery, state: FSMContext):
    await state.finish()
    bill_id = call.data.split(':')[1]
    amount = call.data.split(':')[2]
    status = p2p.check(bill_id=bill_id).status
    if status == 'PAID':
        pay_id = random.randint(10000, 99999)
        functions.add_refill(pay_id, call.message.chat.id, amount)
        await call.message.answer(f'✅ Ваш баланс пополнен\n<code>Номер чека: {pay_id}</code>')
        await call.answer('✅ Ваш баланс пополнен', False)
        await call.message.delete()
        functions.user_update_balance(call.message.chat.id, int(amount))
        await call.message.answer(text_profile(call.message.chat.id), reply_markup=inline_profile,
                                  parse_mode="Markdown")
    elif status == 'WAITING':
        await call.answer('⏳ Ожидание оплаты', False)
    else:
        await call.answer('❌ Оплата отменена', True)


###
with sqlite3.connect(SQLITE_DATABASE, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
    cur = con.cursor()
    cur.execute("SELECT Count(*) FROM users")  # Count na all players(Users)
    row = cur.fetchone()
print("Бот запущен")
print(f'Администраторы бота: {ADMINS}\nВсего пользователей в БД: {row[0]}')  # Mini statistics

if __name__ == "__main__":
    executor.start_polling(dp)
