from __future__ import annotations

import asyncio
import logging

from bot.config import load_settings
from bot.scheduler import GameScheduler
from bot.telegram_client import TelegramClient


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


async def amain() -> None:
    settings = load_settings()
    telegram = TelegramClient(settings.bot_token)
    scheduler = GameScheduler(settings, telegram)
    try:
        await scheduler.run_forever()
    finally:
        await telegram.aclose()


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()
