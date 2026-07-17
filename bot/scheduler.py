from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path

from bot import templates
from bot.config import Settings
from bot.messages import (
    build_cta_message,
    build_result_message,
    build_signal_message,
    pick_direction,
    pick_pair,
    roll_result,
)
from bot.telegram_client import TelegramClient

logger = logging.getLogger(__name__)

# Project root = parent of the bot package (also /app inside the container).
_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _resolve_asset(path: str) -> str:
    """Return an absolute asset path, resolving relative paths from the project root."""
    p = Path(path)
    if p.is_absolute():
        return str(p)
    return str(_PROJECT_ROOT / p)


class GameScheduler:
    def __init__(self, settings: Settings, telegram: TelegramClient) -> None:
        self.settings = settings
        self.telegram = telegram

    async def run_forever(self) -> None:
        logger.info("Starting entertainment game scheduler")
        cycle_seconds = self.settings.min_signal_minutes * 60
        while True:
            started = asyncio.get_event_loop().time()
            try:
                await self._run_cycle()
            except Exception:
                logger.exception("Cycle failed; retrying after short pause")
                await asyncio.sleep(30)
                continue

            # Keep a fixed cadence: next Template 1 fires cycle_seconds after this one.
            elapsed = asyncio.get_event_loop().time() - started
            remaining = cycle_seconds - elapsed
            if remaining > 0:
                await asyncio.sleep(remaining)

    async def _run_cycle(self) -> None:
        # Template 1 — signal / predict round
        pair = pick_pair()
        direction = pick_direction()
        await self.telegram.send_message(
            self.settings.channel_id, build_signal_message(pair, direction)
        )
        logger.info("Posted Template 1 (signal) %s %s at %s", pair, direction, datetime.now(timezone.utc))

        # 1 minute later — Template 2 — result (WIN posts a picture, LOSS posts text)
        await asyncio.sleep(self.settings.result_delay_seconds)
        result = roll_result(probability=self.settings.correct_probability)
        if result == "CORRECT":
            await self.telegram.send_photo(
                self.settings.channel_id,
                _resolve_asset(templates.RESULT_WIN_IMAGE),
                caption=templates.RESULT_WIN_CAPTION or None,
            )
        else:
            await self.telegram.send_message(
                self.settings.channel_id, build_result_message(result)
            )
        logger.info("Posted Template 2 (result) %s", result)

        # 1 minute later — Template 3 — game CTA reminder
        await asyncio.sleep(self.settings.result_delay_seconds)
        await self.telegram.send_message(
            self.settings.channel_id, build_cta_message(self.settings.game_cta_url)
        )
        logger.info("Posted Template 3 (CTA)")
