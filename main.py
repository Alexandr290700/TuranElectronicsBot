import asyncpg
import asyncio
import logging
import sys

from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from config import dp, bot, DB_CONFIG, TELEGRAM_CONFIG


async def get_new_orders(last_order_id):
    conn = await asyncpg.connect(**DB_CONFIG)
    new_orders = await conn.fetch("SELECT * FROM orders WHERE id > $1", last_order_id)
    await conn.close()
    return new_orders


async def send_message(message_text):
    await bot.send_message(chat_id=TELEGRAM_CONFIG["chat_id"], text=message_text)


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(f"Привет {hbold(message.from_user.full_name)}.\
                         Я бот который будет отправлять информацию о новых заказах")
    



async def main():
    await dp.start_polling(bot)

    last_order_id = 0

    while True:
        new_orders = await get_new_orders(last_order_id)
        for order in new_orders:
            message_text = f"Новый заказ!\nID заказа: {order['id']}\nПользователь: {order['name']}\nНомер телефона: {order['phone']}\nРегион: {order['region']}\nГород: {order['city']}\nУлица: {order['street']}\nДом: {order['house']}\nСоздан: {order['created_at']}"
            await send_message(message_text)
            last_order_id = order['id']
        await asyncio.sleep(60)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
