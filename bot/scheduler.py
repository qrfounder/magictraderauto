from __future__ import annotations

import asyncio
import logging
import random
from datetime import datetime, timezone

from bot.config import Settings
from bot.messages import (
    build_cta_message,
    build_signal_message,
    pick_direction,
    pick_pair,
)
from bot.telegram_client import TelegramClient

logger = logging.getLogger(__name__)


class GameScheduler:
    def __init__(self, settings: Settings, telegram: TelegramClient) -> None:
        self.settings = settings
        self.telegram = telegram

    async def run_forever(self) -> None:
        logger.info("Starting entertainment game scheduler")
        signal_task = asyncio.create_task(self._signal_loop(), name="signal-loop")
        cta_task = asyncio.create_task(self._cta_loop(), name="cta-loop")
        try:
            await asyncio.gather(signal_task, cta_task)
        finally:
            signal_task.cancel()
            cta_task.cancel()

    async def _signal_loop(self) -> None:
        while True:
            try:
                await self._post_round()
            except Exception:
                logger.exception("Signal round failed; retrying after short pause")
                await asyncio.sleep(30)
                continue

            wait_s = random.randint(
                self.settings.min_signal_minutes * 60,
                self.settings.max_signal_minutes * 60,
            )
            logger.info("Next game round in %s seconds", wait_s)
            await asyncio.sleep(wait_s)

    async def _post_round(self) -> None:
        pair = pick_pair()
        direction = pick_direction()
        signal = build_signal_message(pair, direction)
        await self.telegram.send_message(self.settings.channel_id, signal)
        logger.info("Posted signal %s %s at %s", pair, direction, datetime.now(timezone.utc))

    async def _cta_loop(self) -> None:
        interval = self.settings.cta_interval_minutes * 60
        while True:
            await asyncio.sleep(interval)
            try:
                text = build_cta_message(self.settings.game_cta_url)
                await self.telegram.send_message(self.settings.channel_id, text)
                logger.info("Posted game CTA")
            except Exception:
                logger.exception("CTA post failed")
