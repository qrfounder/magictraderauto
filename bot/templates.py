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
RESULT_TEMPLATE = "RESULT: {badge}\n\n"
BADGE_CORRECT = "✅ WIN"
BADGE_MISS = "❌ LOSS"


# ============================================================
#  TEMPLATE 3 — Game CTA reminder
#  Posted every 30 minutes.
#  Placeholders: {game_url}, {disclaimer}
# ============================================================
CTA_TEMPLATE = (
   
    "We continue with  operations ✅\n\n"
    "Keep the broker open!!.\n\n"
    "For those who haven't join yet 👇🏻\n\n"
    "📊 create your account here:\n{game_url}\n\n"
)


# ============================================================
#  TEMPLATE 4 — (add your next template here)
#  Copy a block above, rename the constant, then use it in
#  bot/messages.py + bot/scheduler.py.
# ============================================================
