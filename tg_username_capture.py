import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command


class TelegramBot:
    def __init__(self, bot_token, logger):
        # bot_token = '7236138991:AAHAecN8Rl4utPCtM3DhthdOsWcY8TWLqrA'
        self.bot = Bot(token=bot_token)
        self.dp = Dispatcher()
        self.logger = logger

    @self.dp.message(Command("start", "help"))
    async def welcome_message(self, message: types.Message):
        await message.reply("Hi, I'm your bot. Send me any message and I'll reply with your username.")


    @self.dp.message()
    async def send_username(self, message: types.Message):
        username = message.from_user.username
        if username:
            response = f"Your username is {username}"

        else:
            response = "You don't have a username set in Telegram."
        await message.reply(response)
        await self.store_username(message.from_user.id, username)

    async def store_username(self, user_id, username):
        self.logger.info(f"Username {username} for {user_id} stored.")

    async def start(self):
        await self.dp.start_polling(self.bot)

    async def stop(self):
        await self.dp.stop_polling()



