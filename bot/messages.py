"""Message builders and fair game rolls for the entertainment channel bot.

The actual text/content that gets posted lives in ``bot/templates.py`` —
edit that file to change any message. This module only fills in the
placeholders and handles the random/fair-odds logic.
"""

from __future__ import annotations

import random
from typing import Callable, Sequence

from bot import templates
from bot.templates import DIRECTIONS, PAIRS

__all__ = [
    "PAIRS",
    "DIRECTIONS",
    "pick_pair",
    "pick_direction",
    "roll_result",
    "build_signal_message",
    "build_result_message",
    "build_cta_message",
]


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
    arrow = templates.ARROW_UP if direction == "UP" else templates.ARROW_DOWN
    return templates.SIGNAL_TEMPLATE.format(pair=pair, direction=direction, arrow=arrow)


def build_result_message(result: str) -> str:
    badge = templates.BADGE_CORRECT if result == "CORRECT" else templates.BADGE_MISS
    return templates.RESULT_TEMPLATE.format(badge=badge)


def build_cta_message(game_url: str) -> str:
    return templates.CTA_TEMPLATE.format(game_url=game_url)
