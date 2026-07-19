"""Premium UTC session scheduler for the entertainment channel bot."""

from __future__ import annotations

import asyncio
import logging
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

from bot import templates
from bot.config import Settings
from bot.messages import (
    SessionStats,
    build_cta_message,
    build_fomo,
    build_market_brief,
    build_overnight,
    build_pre_cta_message,
    build_pre_result_message,
    build_profit_tease,
    build_session_open,
    build_session_wrap,
    build_signal_message,
    build_soft_cta,
    build_streak_hype,
    build_tip,
    build_trust_recap,
    build_welcome,
    pick_direction,
    pick_filler_kind,
    pick_pair,
    roll_result,
)
from bot.telegram_client import TelegramClient

logger = logging.getLogger(__name__)

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Tick sleep when idle (seconds).
_IDLE_TICK_SECONDS = 30
# Minimum pause after a filler before another content decision (seconds).
_FILLER_COOLDOWN_SECONDS = 20 * 60
# Overnight fillers: max per UTC day outside peak/bridge.
_MAX_OVERNIGHT_FILLERS = 2
# Bridge (11–13 UTC) fillers: max per UTC day.
_MAX_BRIDGE_FILLERS = 2


def _resolve_asset(path: str) -> str:
    p = Path(path)
    if p.is_absolute():
        return str(p)
    return str(_PROJECT_ROOT / p)


def _hm(now: datetime) -> tuple[int, int]:
    return now.hour, now.minute


def in_london_open_slot(now: datetime) -> bool:
    return (6, 50) <= _hm(now) < (7, 10)


def in_ny_open_slot(now: datetime) -> bool:
    return (12, 50) <= _hm(now) < (13, 10)


def in_wrap_slot(now: datetime) -> bool:
    return (17, 0) <= _hm(now) < (17, 20)


def in_london_peak(now: datetime) -> bool:
    return (7, 0) <= _hm(now) < (11, 0)


def in_ny_peak(now: datetime) -> bool:
    return (13, 0) <= _hm(now) < (17, 0)


def in_peak_window(now: datetime) -> bool:
    return in_london_peak(now) or in_ny_peak(now)


def in_bridge_window(now: datetime) -> bool:
    return (11, 0) <= _hm(now) < (13, 0)


def session_label(now: datetime) -> str:
    if in_london_open_slot(now) or in_london_peak(now):
        return "London"
    if in_ny_open_slot(now) or in_ny_peak(now) or in_wrap_slot(now):
        return "New York"
    if in_bridge_window(now):
        return "between sessions"
    return "Overnight"


def should_post_hard_cta(
    *,
    completed_rounds: int,
    last_hard_cta_at: datetime | None,
    now: datetime,
    cta_interval_minutes: int,
    last_post_was_soft_cta: bool,
) -> bool:
    """Every 2nd round, after cooldown, and never right after a soft CTA."""
    if last_post_was_soft_cta:
        return False
    if completed_rounds < 1 or completed_rounds % 2 != 0:
        return False
    if last_hard_cta_at is None:
        return True
    elapsed = (now - last_hard_cta_at).total_seconds()
    return elapsed >= cta_interval_minutes * 60


class GameScheduler:
    def __init__(self, settings: Settings, telegram: TelegramClient) -> None:
        self.settings = settings
        self.telegram = telegram
        self.stats = SessionStats()
        self._next_signal_at: datetime | None = None
        self._last_hard_cta_at: datetime | None = None
        self._last_filler_at: datetime | None = None
        self._last_post_kind: str | None = None
        self._completed_rounds = 0
        self._posted_london_open_day: str | None = None
        self._posted_ny_open_day: str | None = None
        self._posted_wrap_day: str | None = None
        self._bridge_fillers_today = 0
        self._overnight_fillers_today = 0
        self._counters_day: str | None = None

    def _utc_now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _utc_day(self, now: datetime) -> str:
        return now.strftime("%Y-%m-%d")

    def _reset_daily_flags(self, now: datetime) -> None:
        day = self._utc_day(now)
        self.stats.ensure_day(day)
        if self._counters_day != day:
            self._counters_day = day
            self._bridge_fillers_today = 0
            self._overnight_fillers_today = 0
            self._posted_london_open_day = None
            self._posted_ny_open_day = None
            self._posted_wrap_day = None

    def _jitter_signal_delay(self) -> timedelta:
        low = self.settings.min_signal_minutes
        high = self.settings.max_signal_minutes
        minutes = random.randint(low, high)
        return timedelta(minutes=minutes)

    def _schedule_next_signal(self, now: datetime) -> None:
        self._next_signal_at = now + self._jitter_signal_delay()
        logger.info("Next signal round at %s", self._next_signal_at.isoformat())

    def _signal_due(self, now: datetime) -> bool:
        if not in_peak_window(now):
            return False
        if self._next_signal_at is None:
            return True
        return now >= self._next_signal_at

    def _filler_allowed(self, now: datetime) -> bool:
        """Block stacked fillers; allow another only after cooldown."""
        if self._last_filler_at is not None:
            since = (now - self._last_filler_at).total_seconds()
            if since < _FILLER_COOLDOWN_SECONDS:
                return False
        return True

    async def run_forever(self) -> None:
        logger.info("Starting premium entertainment game scheduler")
        while True:
            try:
                await self._tick()
            except Exception:
                logger.exception("Tick failed; retrying after short pause")
                await asyncio.sleep(30)
                continue
            await asyncio.sleep(_IDLE_TICK_SECONDS)

    async def _tick(self) -> None:
        now = self._utc_now()
        self._reset_daily_flags(now)
        day = self._utc_day(now)

        if in_london_open_slot(now) and self._posted_london_open_day != day:
            await self._post_session_open("London")
            self._posted_london_open_day = day
            return

        if in_ny_open_slot(now) and self._posted_ny_open_day != day:
            await self._post_session_open("New York")
            self._posted_ny_open_day = day
            return

        if in_wrap_slot(now) and self._posted_wrap_day != day:
            await self._post_session_wrap("New York")
            self._posted_wrap_day = day
            return

        if in_peak_window(now):
            if self._next_signal_at is None:
                # First entry into a peak window: fire ASAP.
                self._next_signal_at = now
            if self._signal_due(now):
                await self._run_signal_round()
                return
            if self._filler_allowed(now) and self._last_post_kind == "signal_round":
                # At most one filler between signal rounds.
                await self._post_filler(now)
                return
            return

        if in_bridge_window(now):
            if (
                self._bridge_fillers_today < _MAX_BRIDGE_FILLERS
                and self._filler_allowed(now)
            ):
                await self._post_filler(now)
                self._bridge_fillers_today += 1
            return

        # Overnight / quiet: rare tips or briefs only.
        if (
            self._overnight_fillers_today < _MAX_OVERNIGHT_FILLERS
            and self._filler_allowed(now)
            and random.random() < 0.08
        ):
            await self._post_filler(now, allow_soft_cta=False, overnight=True)
            self._overnight_fillers_today += 1

    async def _post_session_open(self, session: str) -> None:
        text = build_session_open(session)
        await self.telegram.send_message(self.settings.channel_id, text)
        self._last_post_kind = "session"
        logger.info("Posted session open (%s)", session)

    async def _post_session_wrap(self, session: str) -> None:
        text = build_session_wrap(session)
        await self.telegram.send_message(self.settings.channel_id, text)
        self._last_post_kind = "session"
        logger.info("Posted session wrap (%s)", session)

    async def _post_filler(
        self,
        now: datetime,
        *,
        allow_soft_cta: bool = True,
        overnight: bool = False,
    ) -> None:
        allow_trust = self.stats.total > 0
        allow_streak = self.stats.streak >= 2
        # Never soft CTA back-to-back with hard CTA.
        if self._last_post_kind == "hard_cta":
            allow_soft_cta = False

        weights = (
            templates.OVERNIGHT_FILLER_WEIGHTS
            if overnight
            else templates.FILLER_WEIGHTS
        )
        kind = pick_filler_kind(
            weights,
            allow_trust=allow_trust and not overnight,
            allow_soft_cta=allow_soft_cta and not overnight,
            allow_streak=allow_streak and not overnight,
            allow_overnight=overnight,
        )
        if not overnight and kind == "overnight":
            kind = "tip"

        channel = self.settings.channel_id
        text: str
        post_kind = "filler"

        if kind == "market_brief":
            pair = self.stats.preferred_pair() or pick_pair()
            text = build_market_brief(pair)
        elif kind == "tip":
            text = build_tip()
        elif kind == "trust_recap":
            text = build_trust_recap(
                session=session_label(now),
                wins=self.stats.wins,
                total=self.stats.total,
            )
        elif kind == "streak_hype":
            text = build_streak_hype(self.stats.streak)
        elif kind == "fomo":
            text = build_fomo()
        elif kind == "welcome":
            text = build_welcome()
        elif kind == "overnight":
            text = build_overnight()
        elif kind == "profit_tease":
            text = build_profit_tease()
        else:  # soft_cta
            text = build_soft_cta()
            post_kind = "soft_cta"

        await self.telegram.send_message(channel, text)
        self._last_post_kind = post_kind
        self._last_filler_at = now
        logger.info("Posted filler (%s)", kind)

    async def _run_signal_round(self) -> None:
        now = self._utc_now()
        count = max(1, int(templates.SIGNALS_PER_ROUND))
        channel = self.settings.channel_id

        for _ in range(count):
            pair = pick_pair()
            direction = pick_direction()
            self.stats.note_pair(pair)
            await self.telegram.send_message(
                channel, build_signal_message(pair, direction)
            )
            logger.info(
                "Posted signal %s %s at %s",
                pair,
                direction,
                now.isoformat(),
            )

        await asyncio.sleep(self.settings.result_delay_seconds)
        await self.telegram.send_message(channel, build_pre_result_message())
        logger.info("Posted pre-result message")

        for _ in range(count):
            result = roll_result(probability=templates.WIN_PERCENT / 100)
            correct = result == "CORRECT"
            self.stats.record_result(correct=correct)
            if correct:
                image, caption = templates.RESULT_WIN_IMAGE, templates.RESULT_WIN_CAPTION
            else:
                image, caption = templates.RESULT_LOSS_IMAGE, templates.RESULT_LOSS_CAPTION
            await self.telegram.send_photo(
                channel,
                _resolve_asset(image),
                caption=caption or None,
            )
            logger.info("Posted result %s", result)

        await self.telegram.send_message(channel, build_pre_cta_message())
        logger.info("Posted pre-CTA message")

        self._completed_rounds += 1
        self._last_post_kind = "signal_round"
        post_now = self._utc_now()

        if should_post_hard_cta(
            completed_rounds=self._completed_rounds,
            last_hard_cta_at=self._last_hard_cta_at,
            now=post_now,
            cta_interval_minutes=self.settings.cta_interval_minutes,
            last_post_was_soft_cta=False,
        ):
            await asyncio.sleep(self.settings.result_delay_seconds)
            await self.telegram.send_message(
                channel, build_cta_message(self.settings.game_cta_url)
            )
            self._last_hard_cta_at = self._utc_now()
            self._last_post_kind = "hard_cta"
            logger.info("Posted hard CTA")

        self._schedule_next_signal(self._utc_now())
