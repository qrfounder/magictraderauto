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
      {badge}      -> the WIN/LOSS badge
      {game_url}   -> your channel/register link
- Use \n for a line break.

POSTING ORDER (see bot/scheduler.py)
------------------------------------
  TEMPLATE 1 — Signal / predict round   (posted every 5 minutes)
  TEMPLATE 2 — Result                    (1 min after Template 1)
  TEMPLATE 3 — CTA reminder              (1 min after Template 2)

To add a new template, copy a block below, give it the next number, and
wire it up in bot/messages.py + bot/scheduler.py.
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


# ============================================================
#  TEMPLATE 1 — Signal / predict round
#  Posted every 5 minutes.
#  Placeholders: {pair}, {direction}, {arrow}
# ============================================================
SIGNAL_TEMPLATE = "💰 {pair} ; {direction} {arrow}\n\n🕐EXPIRY TIME: 5MIN"


# ============================================================
#  TEMPLATE 2 — Result (WIN / LOSS)
#  Posted 1 minute after Template 1.
#  Placeholders: {badge}
# ============================================================
RESULT_TEMPLATE = "🏁 RESULT: {badge}"
BADGE_CORRECT = "✅ WIN"
BADGE_MISS = "❌ LOSS"


# ============================================================
#  TEMPLATE 3 — CTA reminder
#  Posted 1 minute after Template 2.
#  Placeholders: {game_url}
# ============================================================
CTA_TEMPLATE = (
    "We continue with operations ✅\n\n"
    "Keep the broker open!!\n\n"
    "For those who haven't joined yet 👇🏻\n\n"
    "📊 create your account here:\n{game_url}"
)


# ============================================================
#  TEMPLATE 4 — (add your next template here)
#  Copy a block above, rename the constant, then use it in
#  bot/messages.py + bot/scheduler.py.
# ============================================================
