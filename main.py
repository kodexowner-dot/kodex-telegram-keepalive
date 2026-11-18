import asyncio
import logging
import os
import sys

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError, RPCError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("telegram-keepalive")


def required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        log.error("Missing required GitHub Actions secret: %s", name)
        sys.exit(2)
    return value


async def main() -> None:
    api_id_raw = required_env("TG_API_ID")
    api_hash = required_env("TG_API_HASH")
    session_string = required_env("TG_SESSION")
    target_bot = os.getenv("TARGET_BOT", "KodexAIMGroupBot").strip().lstrip("@")

    try:
        api_id = int(api_id_raw)
    except ValueError:
        log.error("TG_API_ID must be a number.")
        sys.exit(2)

    client = TelegramClient(StringSession(session_string), api_id, api_hash)

    try:
        await client.connect()
        if not await client.is_user_authorized():
            log.error("Telegram session is not authorized. Generate a fresh session string.")
            sys.exit(3)

        bot = await client.get_entity(target_bot)
        await client.send_message(bot, "/start")
        log.info("Sent /start to @%s", target_bot)

        # Give the bot a moment to reply, then mark this bot chat as read.
        await asyncio.sleep(3)
        await client.send_read_acknowledge(bot)
        log.info("Marked the bot chat as read.")
    except FloodWaitError as exc:
        log.error("Telegram rate limit: wait %s seconds. Stopping.", exc.seconds)
        raise
    except RPCError:
        log.exception("Telegram API error.")
        raise
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
