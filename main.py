import logging
from aiogram import Bot, Dispatcher, executor, types
import markups as nav
from db import Database

API_TOKEN = ''

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

db = Database('database.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Ваше Имя и Фамилия')
    else:
        await bot.send_message(message.from_user.id, 'Вы уже зарегистрированы', reply_markup=nav.mainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'Profile':
            pass
        else:
            if db.get_signup(message.from_user.id) == "setnickname":
                db.set_name(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, ' d o n e ')
                await bot.send_message(message.from_user.id, 'Вы зарегистрированы', reply_markup=nav.mainMenu)
            else:
                await bot.send_message(message.from_user.id, 'непонял')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
