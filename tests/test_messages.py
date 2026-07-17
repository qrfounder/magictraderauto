from bot.messages import (
    PAIRS,
    build_cta_message,
    build_signal_message,
    pick_direction,
    pick_pair,
    roll_result,
)


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


def test_cta_includes_url():
    text = build_cta_message("https://t.me/example")
    assert "https://t.me/example" in text
    assert "broker" in text.lower()
