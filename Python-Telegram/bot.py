import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = '7444782836:AAHn1GF5rFzqbVPFe7uhAuszYPL-M3cp4Xw'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

player_codes = {}
player_attempts = {}
players = []


def generate_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])


def compare_codes(code1, code2):
    return sum(1 for a, b in zip(code1, code2) if a == b)


def count_matching_digits(code1, code2):
    count = 0
    code2_list = list(code2)
    for digit in code1:
        if digit in code2_list:
            count += 1
            code2_list.remove(digit)
    return count


@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    player_id = message.from_user.id
    if player_id not in player_codes:
        if len(players) < 2:
            player_codes[player_id] = generate_code()
            player_attempts[player_id] = []
            players.append(player_id)
            await message.answer(f"Ваш код сгенерирован. Ожидаем второго игрока.")
            if len(players) == 2:
                await bot.send_message(players[0], f"Игра началась! Ваш код: {player_codes[players[0]]}")
                await bot.send_message(players[1], f"Игра началась! Ваш код: {player_codes[players[1]]}")
        else:
            await message.answer(f"Игра уже идет с двумя участниками.")
    else:
        await message.answer(f"Вы уже участвуете в игре.")


@dp.message_handler()
async def guess_code(message: types.Message):
    player_id = message.from_user.id
    guess = message.text.strip()

    if player_id not in players:
        await message.answer(f"Вы не участвуете в текущей игре. Ожидайте окончания.")
        return

    if len(players) < 2:
        await message.answer(f"Ожидаем второго игрока.")
        return

    opponent_id = players[0] if players[1] == player_id else players[1]
    opponent_code = player_codes[opponent_id]

    if len(guess) != 4 or not guess.isdigit():
        await message.answer(f"Введите корректный код из 4 цифр.")
        return

    player_attempts[player_id].append(guess)
    matched_digits = count_matching_digits(guess, opponent_code)

    if guess == opponent_code:
        await message.answer(f"Поздравляем, вы угадали все цифры! Вы выиграли.")
        await bot.send_message(opponent_id, f"Ваш соперник угадал ваш код: {guess}. Вы проиграли.")

        player_codes.clear()
        player_attempts.clear()
        players.clear()
    else:
        await message.answer(f"Вы угадали {matched_digits} цифры.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
