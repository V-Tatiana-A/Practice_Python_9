import random

from bot_config import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import Text

game_status=False

button_game = types.KeyboardButton('/play')
start_game = types.KeyboardButton('/start')
help_game = types.KeyboardButton('/help')
play_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
play_kb.add(start_game, button_game, help_game)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, text="Привет! Я бот для игры в конфетки.\n "
                        "Хочешь сыграть? Жми /play", reply_markup=play_kb)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await bot.send_message(message.from_user.id, text="На столе лежит 150 конфет.\n"
                           "Первый ход определяется жеребьёвкой.\n"
                           "За один ход можно забрать не более чем 28 конфет.\n"
                           "Побеждает тот, кто забрал последние конфеты со стола.")


total = 150
first_turn=0


@dp.message_handler(commands=['play'])
async def get_ready(message: types.Message):
    global game_status
    global total
    global first_turn
    game_status=True
    total=150
    first_turn=0
    await bot.send_message(message.from_user.id, 'Начинаем новую игру!\n'
                                                 'Можете подкинуть монетку (/heads (решка) или /tails (орёл) и узнать кто ходит первым.\n'
                                                 'Иначе по умолчанию первым ходит бот.')


async def computer_turn(message: types.Message):
    global total
    global game_status
    if total>28:
        с_take = total % (28 + 1)
        if с_take == 0:
            с_take = random.randint(0, 28)
        await bot.send_message(message.from_user.id, f'Бот взял {с_take} конфет(ы)')
        total = total - с_take
        await bot.send_message(message.from_user.id, f'Осталось {total} конфет(ы)')
    else:
        await bot.send_message(message.from_user.id, f'Бот взял оставшиеся {total} конфет(ы). Вы проиграли.')
        total = total - total
        game_status=False


@dp.message_handler(commands=['heads', 'tails'])
async def game(message: types.Message):
    global first_turn
    if message=='/heads':
        pl = 1
    else:
        pl = 0
    toss=random.randint(0,1)
    if toss==pl:
        await bot.send_message(message.from_user.id, f'Вы выиграли и ходите первым.')
        first_turn=1
    else:
        await bot.send_message(message.from_user.id, f'Вы проиграли и первый ход за ботом.')
        await computer_turn(message)


@dp.message_handler()
async def game(message: types.Message):
    global total
    global game_status
    if game_status==True:
        if message.text.isdigit():
            if 0<int(message.text)<29:
                total -= int(message.text)
                await bot.send_message(message.from_user.id, f'Вы взяли со стола {message.text} конфет(ы).\n'
                                                             f'На столе осталось {total} конфет(ы)')
                if total==0:
                    await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, поздравляем с победой!')
                    game_status = False
                else:
                    await computer_turn(message)
            else:
                await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, это не по правилам.\n'
                                                             f'Напомню - от 1 до 28 конфет!')
        else:
            await bot.send_message(message.from_user.id, f'Ваш запрос вне моей компетенции.')
    else:
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, '
                                                     f'кажется игра не запущена.')



