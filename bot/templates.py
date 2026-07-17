"""
============================================================
 EDITABLE TEMPLATES — everything the bot posts automatically
============================================================

HOW TO EDIT
-----------
- Change any text between the quotes. Save the file, then restart the bot.
- Keep the {curly_brace} placeholders where they are — they get filled in
  automatically:
      {pair}       -> e.g. "EUR/USD"
      {direction}  -> "UP" or "DOWN"
      {arrow}      -> colored square based on direction
      {badge}      -> the CORRECT/MISS badge
      {game_url}   -> your channel/game link
      {disclaimer} -> the shared disclaimer line (SHARED SETTINGS below)
- Use \n for a line break.

TEMPLATES IN THIS FILE
----------------------
  TEMPLATE 1 — Signal / predict round   (posted every 5–15 min)
  TEMPLATE 2 — Game result              (CORRECT / MISS)
  TEMPLATE 3 — Game CTA reminder        (posted every 30 min)

To add a new template, copy a block below, give it the next number, and
wire it up in bot/messages.py.
"""

# ============================================================
#  SHARED SETTINGS (used by several templates)
# ============================================================

# Trading pairs the bot randomly picks from (add/remove freely).
PAIRS: tuple[str, ...] = (
    "AUD/CAD",
    "EUR/USD",
    "EUR/BRL",
    "AUD/JPY",
    "EUR/GBP",
    "USD/CAD",
)

# Directions the bot randomly picks from.
DIRECTIONS: tuple[str, ...] = ("UP", "DOWN")

# Arrows shown next to each direction.
ARROW_UP = "🟩"
ARROW_DOWN = "🟥"

# Disclaimer reused in several templates via {disclaimer}.
DISCLAIMER = "Entertainment game only — not real trading or financial advice."


# ============================================================
#  TEMPLATE 1 — Signal / predict round
#  Posted every 5–15 minutes.
#  Placeholders: {pair}, {direction}, {arrow}
# ============================================================
SIGNAL_TEMPLATE = "💰 {pair} ; {direction} {arrow}\n\n🕐EXPIRY TIME: 5MIN"


# ============================================================
#  TEMPLATE 2 — Game result (CORRECT / MISS)
#  Posted after a signal round.
#  Placeholders: {badge}, {disclaimer}
# ============================================================
RESULT_TEMPLATE = "🏁 GAME RESULT: {badge}\n\n⚠️ {disclaimer}"
BADGE_CORRECT = "✅ CORRECT"
BADGE_MISS = "❌ MISS"


# ============================================================
#  TEMPLATE 3 — Game CTA reminder
#  Posted every 30 minutes.
#  Placeholders: {game_url}, {disclaimer}
# ============================================================
CTA_TEMPLATE = (
    "🎮 Game round reminder\n\n"
    "We continue with game operations ✅\n\n"
    "Keep following the channel for the next predict round.\n\n"
    "For players who want to join👇🏻\n\n"
    "📊 Play / follow here:\n{game_url}\n\n"
    "⚠️ {disclaimer}"
)


# ============================================================
#  TEMPLATE 4 — (add your next template here)
#  Copy a block above, rename the constant, then use it in
#  bot/messages.py + bot/scheduler.py.
# ============================================================
