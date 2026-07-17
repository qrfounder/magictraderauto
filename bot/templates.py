"""
============================================================
 EDITABLE TEMPLATES — everything the bot posts automatically
============================================================

You can safely edit anything in this file to change what the bot posts.
Save the file and restart the bot for changes to take effect.

Keep the {curly_brace} placeholders where they are — they get filled in
automatically:
    {pair}       -> e.g. "EUR/USD"
    {direction}  -> "UP" or "DOWN"
    {arrow}      -> colored square based on direction
    {badge}      -> the CORRECT/MISS badge
    {game_url}   -> your channel/game link
    {disclaimer} -> the disclaimer line below

Use \n for a line break.
"""

# ---- Trading pairs the bot randomly picks from --------------
# Add or remove pairs freely (keep quotes and commas).
PAIRS: tuple[str, ...] = (
    "AUD/CAD",
    "EUR/USD",
    "EUR/BRL",
    "AUD/JPY",
    "EUR/GBP",
    "USD/CAD",
)

# ---- Directions the bot randomly picks from -----------------
DIRECTIONS: tuple[str, ...] = ("UP", "DOWN")

# ---- Arrows shown next to each direction --------------------
ARROW_UP = "🟩"
ARROW_DOWN = "🟥"

# ---- Disclaimer reused in several messages ------------------
DISCLAIMER = "Entertainment game only — not real trading or financial advice."

# ---- Signal / predict round message -------------------------
SIGNAL_TEMPLATE = "💰 {pair} ; {direction} {arrow}\n\n🕐EXPIRY TIME: 5MIN"

# ---- Result message -----------------------------------------
# {badge} becomes one of the two badges below.
RESULT_TEMPLATE = "🏁 GAME RESULT: {badge}\n\n⚠️ {disclaimer}"
BADGE_CORRECT = "✅ CORRECT"
BADGE_MISS = "❌ MISS"

# ---- Game CTA reminder (posted every CTA_INTERVAL_MINUTES) ---
CTA_TEMPLATE = (
    "🎮 Game round reminder\n\n"
    "We continue with game operations ✅\n\n"
    "Keep following the channel for the next predict round.\n\n"
    "For players who want to join👇🏻\n\n"
    "📊 Play / follow here:\n{game_url}\n\n"
    "⚠️ {disclaimer}"
)
