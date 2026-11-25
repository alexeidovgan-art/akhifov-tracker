"""
Получение TG_SESSION. Запускать ОДИН РАЗ в Google Colab.

Порядок в Colab:
  1. В первой ячейке:  !pip install telethon -q   и нажать ▶
  2. Во второй ячейке вставить весь этот файл и нажать ▶
  3. По очереди ввести: API_ID, API_HASH, телефон (+7...),
     код из Telegram, а если включена двухфакторка — облачный пароль.
  4. В конце появится строка — это TG_SESSION. Скопировать целиком.
"""
import asyncio

from telethon import TelegramClient
from telethon.errors import (
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
)
from telethon.sessions import StringSession


async def get_session():
    api_id = int(input("API_ID: ").strip())
    api_hash = input("API_HASH: ").strip()
    phone = input("Телефон (в формате +7...): ").strip()

    client = TelegramClient(StringSession(), api_id, api_hash)
    await client.connect()

    sent = await client.send_code_request(phone)
    print("Код отправлен в Telegram (в приложении, в чате с Telegram).")

    while True:
        code = input("Код из Telegram: ").strip()
        try:
            await client.sign_in(phone=phone, code=code, phone_code_hash=sent.phone_code_hash)
            break
        except PhoneCodeInvalidError:
            print("Неверный код, попробуй ещё раз.")
        except PhoneCodeExpiredError:
            print("Код устарел. Перезапусти ячейку и попробуй снова.")
            await client.disconnect()
            return None
        except SessionPasswordNeededError:
            password = input("Облачный пароль (двухэтапная проверка): ")
            await client.sign_in(password=password)
            break

    session_string = client.session.save()
    await client.disconnect()

    print("\n✅ Готово. Вот твоя TG_SESSION (скопируй целиком):\n")
    print(session_string)
    print("\nВставь её в Render -> Environment -> TG_SESSION.")
    return session_string


# В Google Colab работает top-level await.
await get_session()
