"""Message builders and fair game rolls for the entertainment channel bot."""

from __future__ import annotations

import random
from typing import Callable, Sequence

PAIRS: tuple[str, ...] = (
    "EUR/USD",
    "GBP/USD",
    "USD/JPY",
    "AUD/USD",
    "USD/CAD",
    "AUD/CAD",
    "EUR/GBP",
    "EUR/JPY",
    "GBP/JPY",
    "NZD/USD",
    "USD/CHF",
    "EUR/AUD",
)

DIRECTIONS: tuple[str, ...] = ("UP", "DOWN")

DISCLAIMER = "Entertainment game only — not real trading or financial advice."


def pick_pair(rng: Callable[[Sequence[str]], str] | None = None) -> str:
    picker = rng or random.choice
    return picker(PAIRS)


def pick_direction(rng: Callable[[Sequence[str]], str] | None = None) -> str:
    picker = rng or random.choice
    return picker(DIRECTIONS)


def roll_result(*, probability: float = 0.5, random_value: float | None = None) -> str:
    """Return CORRECT or MISS using transparent fair odds (default 50%)."""
    value = random.random() if random_value is None else random_value
    return "CORRECT" if value < probability else "MISS"


def build_signal_message(pair: str, direction: str) -> str:
    arrow = "🟩" if direction == "UP" else "🟥"
    return (
        f"🎮 GAME PREDICT\n"
        f"💰 {pair} ; {direction} {arrow}\n\n"
        f"🕐 ROUND TIME: 5MIN\n\n"
        f"📲 Join the game: see channel CTA\n\n"
        f"⚠️ {DISCLAIMER}"
    )


def build_result_message(result: str) -> str:
    badge = "✅ CORRECT" if result == "CORRECT" else "❌ MISS"
    return (
        f"🏁 GAME RESULT: {badge}\n\n"
        f"⚠️ {DISCLAIMER}"
    )


def build_cta_message(game_url: str) -> str:
    return (
        "🎮 Game round reminder\n\n"
        "We continue with game operations ✅\n\n"
        "Keep following the channel for the next predict round.\n\n"
        "For players who want to join👇🏻\n\n"
        f"📊 Play / follow here:\n{game_url}\n\n"
        f"⚠️ {DISCLAIMER}"
    )
