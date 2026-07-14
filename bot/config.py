from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    bot_token: str
    channel_id: str
    game_cta_url: str
    min_signal_minutes: int
    max_signal_minutes: int
    result_delay_seconds: int
    cta_interval_minutes: int
    correct_probability: float


def load_settings() -> Settings:
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN", "").strip()
    channel_id = os.getenv("CHANNEL_ID", "").strip()
    game_cta_url = os.getenv("GAME_CTA_URL", "https://t.me/magicroomofficial").strip()

    if not bot_token or bot_token.startswith("replace_"):
        raise SystemExit("Set BOT_TOKEN in environment or .env")
    if not channel_id:
        raise SystemExit("Set CHANNEL_ID in environment or .env")

    min_m = int(os.getenv("MIN_SIGNAL_MINUTES", "5"))
    max_m = int(os.getenv("MAX_SIGNAL_MINUTES", "15"))
    if min_m < 1 or max_m < min_m:
        raise SystemExit("MIN_SIGNAL_MINUTES / MAX_SIGNAL_MINUTES are invalid")

    prob = float(os.getenv("CORRECT_PROBABILITY", "0.5"))
    if not 0.0 <= prob <= 1.0:
        raise SystemExit("CORRECT_PROBABILITY must be between 0 and 1")

    return Settings(
        bot_token=bot_token,
        channel_id=channel_id,
        game_cta_url=game_cta_url,
        min_signal_minutes=min_m,
        max_signal_minutes=max_m,
        result_delay_seconds=int(os.getenv("RESULT_DELAY_SECONDS", "60")),
        cta_interval_minutes=int(os.getenv("CTA_INTERVAL_MINUTES", "30")),
        correct_probability=prob,
    )
