"""
Run this script locally on your own device (not in GitHub Actions).
It creates a Telethon StringSession for your own Telegram account.
Never share the resulting session string or commit it to GitHub.
"""
import asyncio
import getpass

from telethon import TelegramClient
from telethon.sessions import StringSession


async def main():
    api_id = int(input("Telegram API ID: ").strip())
    api_hash = getpass.getpass("Telegram API Hash (hidden): ").strip()
    phone = input("Phone number with country code (e.g. +7...): ").strip()

    client = TelegramClient(StringSession(), api_id, api_hash)
    await client.start(phone=phone)

    print("\nSESSION STRING (keep private; do not send it in chat):\n")
    print(client.session.save())
    print("\nCopy it directly into GitHub Secret TG_SESSION, then delete this output.")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
