from configs import admin_id, bot

import asyncio

from aiogram import Dispatcher
from aiogram.types import BotCommand


from handlers import user_handlers


async def main():
    dp = Dispatcher()

    await bot.set_my_commands([BotCommand(command='/start', description='баланс и адрес кошелька')])

    await bot.send_message(admin_id, text='онлайн кошелек tBTC запущен')

    dp.include_routers(user_handlers.router)

    await dp.start_polling(bot, polling_timeout=30)


if __name__ == '__main__':
    asyncio.run(main())
