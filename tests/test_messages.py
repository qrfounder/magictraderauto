from datetime import datetime, timezone

from bot.messages import (
    PAIRS,
    SessionStats,
    build_cta_message,
    build_market_brief,
    build_session_open,
    build_session_wrap,
    build_signal_message,
    build_soft_cta,
    build_tip,
    build_trust_recap,
    pick_direction,
    pick_filler_kind,
    pick_pair,
    roll_result,
)
from bot.scheduler import (
    in_bridge_window,
    in_london_open_slot,
    in_london_peak,
    in_ny_open_slot,
    in_ny_peak,
    in_peak_window,
    in_wrap_slot,
    should_post_hard_cta,
)


def _utc(hour: int, minute: int = 0) -> datetime:
    return datetime(2026, 7, 19, hour, minute, tzinfo=timezone.utc)


def test_pick_pair_from_known_list():
    pair = pick_pair(rng=lambda seq: seq[0])
    assert pair in PAIRS
    assert "/" in pair


def test_pick_direction_up_or_down():
    assert pick_direction(rng=lambda seq: seq[0]) in {"UP", "DOWN"}
    assert pick_direction(rng=lambda seq: seq[1]) in {"UP", "DOWN"}


def test_signal_message_format():
    text = build_signal_message("AUD/CAD", "UP")
    assert text == "💰 AUD/CAD ; UP 🟩\n\n🕐EXPIRY TIME: 5MIN"
    assert "broker" not in text.lower()
    down = build_signal_message("EUR/USD", "DOWN")
    assert down == "💰 EUR/USD ; DOWN 🟥\n\n🕐EXPIRY TIME: 5MIN"


def test_pairs_are_configured_list():
    assert PAIRS == (
        "AUD/CAD",
        "EUR/USD",
        "EUR/BRL",
        "AUD/JPY",
        "EUR/GBP",
        "USD/CAD",
    )


def test_roll_result_respects_probability():
    always_correct = roll_result(probability=1.0, random_value=0.99)
    always_miss = roll_result(probability=0.0, random_value=0.0)
    assert always_correct == "CORRECT"
    assert always_miss == "MISS"


def test_cta_includes_game_url():
    text = build_cta_message("https://t.me/example", rng=lambda seq: seq[0])
    assert "https://t.me/example" in text
    assert "broker" in text.lower()
    assert "We continue with operations" in text


def test_soft_cta_has_no_register_url():
    text = build_soft_cta(rng=lambda seq: seq[0])
    assert "http" not in text.lower()


def test_market_brief_includes_pair():
    text = build_market_brief("EUR/USD", rng=lambda seq: seq[0])
    assert "EUR/USD" in text


def test_session_open_and_wrap():
    open_text = build_session_open("London", rng=lambda seq: seq[0])
    wrap_text = build_session_wrap("New York", rng=lambda seq: seq[0])
    assert "London" in open_text
    assert "New York" in wrap_text


def test_tip_and_trust_recap():
    tip = build_tip(rng=lambda seq: seq[0])
    assert tip
    recap = build_trust_recap(
        session="London",
        wins=3,
        total=4,
        rng=lambda seq: seq[0],
    )
    assert "3" in recap and "4" in recap
    assert "London" in recap


def test_new_template_families():
    from bot.messages import (
        build_fomo,
        build_overnight,
        build_pre_cta_message,
        build_pre_result_message,
        build_profit_tease,
        build_streak_hype,
        build_welcome,
    )

    assert "close" in build_pre_result_message(rng=lambda seq: seq[0]).lower()
    assert "gooo" in build_pre_cta_message(rng=lambda seq: seq[0]).lower()
    assert "3" in build_streak_hype(3, rng=lambda seq: seq[0])
    assert build_fomo(rng=lambda seq: seq[0])
    assert build_welcome(rng=lambda seq: seq[0])
    assert build_overnight(rng=lambda seq: seq[0])
    assert build_profit_tease(rng=lambda seq: seq[0])


def test_pick_filler_kind_respects_weights():
    kind = pick_filler_kind(
        {"market_brief": 100, "tip": 0},
        random_value=0.0,
    )
    assert kind == "market_brief"


def test_pick_filler_kind_can_disable_soft_cta():
    kind = pick_filler_kind(
        {"soft_cta": 100, "tip": 1},
        allow_soft_cta=False,
        random_value=0.0,
    )
    assert kind == "tip"


def test_session_stats_tracks_wins_and_pairs():
    stats = SessionStats()
    stats.ensure_day("2026-07-19")
    stats.note_pair("EUR/USD")
    stats.record_result(correct=True)
    stats.record_result(correct=True)
    assert stats.streak == 2
    stats.record_result(correct=False)
    assert stats.streak == 0
    assert stats.wins == 2
    assert stats.total == 3
    assert stats.preferred_pair() == "EUR/USD"
    stats.ensure_day("2026-07-20")
    assert stats.wins == 0
    assert stats.total == 0
    assert stats.preferred_pair() is None


def test_utc_window_gates():
    assert in_london_open_slot(_utc(6, 55))
    assert not in_london_open_slot(_utc(7, 15))
    assert in_london_peak(_utc(8, 0))
    assert in_bridge_window(_utc(12, 0))
    assert in_ny_open_slot(_utc(13, 0))
    assert in_ny_peak(_utc(15, 0))
    assert in_wrap_slot(_utc(17, 10))
    assert in_peak_window(_utc(9, 0))
    assert in_peak_window(_utc(14, 0))
    assert not in_peak_window(_utc(2, 0))


def test_hard_cta_only_every_second_round_with_cooldown():
    now = _utc(10, 0)
    assert not should_post_hard_cta(
        completed_rounds=1,
        last_hard_cta_at=None,
        now=now,
        cta_interval_minutes=30,
        last_post_was_soft_cta=False,
    )
    assert should_post_hard_cta(
        completed_rounds=2,
        last_hard_cta_at=None,
        now=now,
        cta_interval_minutes=30,
        last_post_was_soft_cta=False,
    )
    assert not should_post_hard_cta(
        completed_rounds=2,
        last_hard_cta_at=_utc(9, 45),
        now=now,
        cta_interval_minutes=30,
        last_post_was_soft_cta=False,
    )
    assert should_post_hard_cta(
        completed_rounds=4,
        last_hard_cta_at=_utc(9, 0),
        now=now,
        cta_interval_minutes=30,
        last_post_was_soft_cta=False,
    )
    assert not should_post_hard_cta(
        completed_rounds=2,
        last_hard_cta_at=None,
        now=now,
        cta_interval_minutes=30,
        last_post_was_soft_cta=True,
    )
