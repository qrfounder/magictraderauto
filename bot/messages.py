"""Message builders and fair game rolls for the entertainment channel bot.

The actual text/content that gets posted lives in ``bot/templates.py`` —
edit that file to change any message. This module only fills in the
placeholders and handles the random/fair-odds logic.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, Sequence

from bot import templates
from bot.templates import DIRECTIONS, PAIRS

__all__ = [
    "PAIRS",
    "DIRECTIONS",
    "SessionStats",
    "pick_pair",
    "pick_direction",
    "pick_variant",
    "roll_result",
    "build_signal_message",
    "build_cta_message",
    "build_pre_result_message",
    "build_pre_cta_message",
    "build_soft_cta",
    "build_market_brief",
    "build_session_open",
    "build_session_wrap",
    "build_tip",
    "build_trust_recap",
    "build_streak_hype",
    "build_fomo",
    "build_welcome",
    "build_overnight",
    "build_profit_tease",
    "pick_filler_kind",
]


def pick_pair(rng: Callable[[Sequence[str]], str] | None = None) -> str:
    picker = rng or random.choice
    return picker(PAIRS)


def pick_direction(rng: Callable[[Sequence[str]], str] | None = None) -> str:
    picker = rng or random.choice
    return picker(DIRECTIONS)


def pick_variant(
    variants: Sequence[str],
    rng: Callable[[Sequence[str]], str] | None = None,
) -> str:
    picker = rng or random.choice
    return picker(variants)


def roll_result(*, probability: float = 0.5, random_value: float | None = None) -> str:
    """Return CORRECT or MISS using transparent fair odds (default 50%)."""
    value = random.random() if random_value is None else random_value
    return "CORRECT" if value < probability else "MISS"


def build_signal_message(pair: str, direction: str) -> str:
    arrow = templates.ARROW_UP if direction == "UP" else templates.ARROW_DOWN
    return templates.SIGNAL_TEMPLATE.format(pair=pair, direction=direction, arrow=arrow)


def build_cta_message(
    game_url: str,
    rng: Callable[[Sequence[str]], str] | None = None,
) -> str:
    return pick_variant(templates.CTA_TEMPLATES, rng=rng).format(game_url=game_url)


def build_pre_result_message(rng: Callable[[Sequence[str]], str] | None = None) -> str:
    return pick_variant(templates.PRE_RESULT_MESSAGES, rng=rng)


def build_pre_cta_message(rng: Callable[[Sequence[str]], str] | None = None) -> str:
    return pick_variant(templates.PRE_CTA_MESSAGES, rng=rng)


def build_soft_cta(rng: Callable[[Sequence[str]], str] | None = None) -> str:
    return pick_variant(templates.SOFT_CTA_TEMPLATES, rng=rng)


def build_market_brief(
    pair: str,
    rng: Callable[[Sequence[str]], str] | None = None,
) -> str:
    return pick_variant(templates.MARKET_BRIEF_TEMPLATES, rng=rng).format(pair=pair)


def build_session_open(
    session: str,
    rng: Callable[[Sequence[str]], str] | None = None,
) -> str:
    return pick_variant(templates.SESSION_OPEN_TEMPLATES, rng=rng).format(session=session)


def build_session_wrap(
    session: str,
    rng: Callable[[Sequence[str]], str] | None = None,
) -> str:
    return pick_variant(templates.SESSION_WRAP_TEMPLATES, rng=rng).format(session=session)


def build_tip(rng: Callable[[Sequence[str]], str] | None = None) -> str:
    return pick_variant(templates.TIP_TEMPLATES, rng=rng)


def build_trust_recap(
    *,
    session: str,
    wins: int,
    total: int,
    rng: Callable[[Sequence[str]], str] | None = None,
) -> str:
    return pick_variant(templates.TRUST_RECAP_TEMPLATES, rng=rng).format(
        session=session,
        wins=wins,
        total=total,
    )


def build_streak_hype(
    streak: int,
    rng: Callable[[Sequence[str]], str] | None = None,
) -> str:
    return pick_variant(templates.STREAK_HYPE_TEMPLATES, rng=rng).format(streak=streak)


def build_fomo(rng: Callable[[Sequence[str]], str] | None = None) -> str:
    return pick_variant(templates.FOMO_TEMPLATES, rng=rng)


def build_welcome(rng: Callable[[Sequence[str]], str] | None = None) -> str:
    return pick_variant(templates.WELCOME_TEMPLATES, rng=rng)


def build_overnight(rng: Callable[[Sequence[str]], str] | None = None) -> str:
    return pick_variant(templates.OVERNIGHT_TEMPLATES, rng=rng)


def build_profit_tease(rng: Callable[[Sequence[str]], str] | None = None) -> str:
    return pick_variant(templates.PROFIT_TEASE_TEMPLATES, rng=rng)


def pick_filler_kind(
    weights: dict[str, int] | None = None,
    *,
    allow_trust: bool = True,
    allow_soft_cta: bool = True,
    allow_streak: bool = True,
    allow_overnight: bool = True,
    random_value: float | None = None,
) -> str:
    """Weighted pick among filler kinds. Returns e.g. 'market_brief'."""
    table = dict(weights or templates.FILLER_WEIGHTS)
    if not allow_trust:
        table.pop("trust_recap", None)
    if not allow_soft_cta:
        table.pop("soft_cta", None)
    if not allow_streak:
        table.pop("streak_hype", None)
    if not allow_overnight:
        table.pop("overnight", None)
    if not table:
        return "market_brief"

    keys = list(table.keys())
    totals = [table[k] for k in keys]
    weight_sum = sum(totals)
    pick = random.random() if random_value is None else random_value
    threshold = pick * weight_sum
    running = 0.0
    for key, weight in zip(keys, totals):
        running += weight
        if threshold < running:
            return key
    return keys[-1]


@dataclass
class SessionStats:
    """In-memory win/loss counters for trust/streak posts (resets per UTC day)."""

    utc_day: str = ""
    wins: int = 0
    total: int = 0
    streak: int = 0
    recent_pairs: list[str] = field(default_factory=list)

    def ensure_day(self, utc_day: str) -> None:
        if self.utc_day != utc_day:
            self.utc_day = utc_day
            self.wins = 0
            self.total = 0
            self.streak = 0
            self.recent_pairs.clear()

    def record_result(self, *, correct: bool) -> None:
        self.total += 1
        if correct:
            self.wins += 1
            self.streak += 1
        else:
            self.streak = 0

    def note_pair(self, pair: str) -> None:
        self.recent_pairs.append(pair)
        if len(self.recent_pairs) > 12:
            self.recent_pairs = self.recent_pairs[-12:]

    def preferred_pair(self) -> str | None:
        return self.recent_pairs[-1] if self.recent_pairs else None
