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
      {session}    -> "London" or "New York"
      {wins}       -> greencount this session
      {total}      -> total results this session
      {streak}     -> current win streak
- Use \\n for a line break.

PREMIUM POSTING MODEL (see bot/scheduler.py)
--------------------------------------------
  Signal rounds only in London (07–11 UTC) and NY (13–17 UTC) windows,
  every ~45–60 minutes (jittered). Hard CTA is cooldown-gated.
  Between rounds: market briefs, tips, trust, soft CTAs, hype, welcome, etc.
  Session open / wrap posts fire once per day around those windows.
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
#  Placeholders: {pair}, {direction}, {arrow}
# ============================================================
SIGNAL_TEMPLATE = "💰 {pair} ; {direction} {arrow}\n\n🕐EXPIRY TIME: 5MIN"

SIGNALS_PER_ROUND = 2


# ============================================================
#  TEMPLATE 1.5 — After signals, before results (rotated)
# ============================================================
PRE_RESULT_MESSAGES: tuple[str, ...] = (
    "Please close all trades now. 🔥🔥",
    "⏱ TIME!!! Close everything NOW 🔥🔥",
    "Close close close!!! don’t wait 😱💸",
    "⚠️ Expiry hitting — CLOSE all open trades rn 🔥",
    "Hands up off the broker… we checking results 👀💣",
)


# ============================================================
#  TEMPLATE 2 — Result (WIN / LOSS)
# ============================================================
RESULT_WIN_IMAGE = "bot/assets/win.png"
RESULT_LOSS_IMAGE = "bot/assets/loss.png"
RESULT_WIN_CAPTION = ""
RESULT_LOSS_CAPTION = ""

WIN_PERCENT = 80


# ============================================================
#  TEMPLATE 2.5 — After results (rotated)
# ============================================================
PRE_CTA_MESSAGES: tuple[str, ...] = (
    "Let's gooo!! 💸💰",
    "WOOO that’s how we move 😤🔥💰",
    "Another one in the bag!! 💥💸",
    "Energy through the ROOF rn 🚀🤑",
    "Yessirrrr keep that momentum 🔥🔥💰",
)


# ============================================================
#  TEMPLATE 3 — Hard CTA (rotated). Placeholders: {game_url}
# ============================================================
CTA_TEMPLATES: tuple[str, ...] = (
    (
        "We continue with operations ✅\n\n"
        "Keep the broker open!!\n\n"
        "For those who haven't joined yet 👇🏻\n\n"
        "📊 create your account here and get 10,000$ FREE :\n{game_url}"
    ),
    (
        "Still watching from the sidelines?? 👀\n\n"
        "Jump in with the FREE 10,000$ demo and follow the next calls 🔥\n\n"
        "👇🏻 {game_url}"
    ),
    (
        "Bro the setups keep coming ✅\n\n"
        "Don’t sit out another round… grab your free demo:\n{game_url}\n\n"
        "10,000$ practice money. Zero excuses 💰😤"
    ),
    (
        "New here? Perfect timing ⚡\n\n"
        "Open demo → follow the signals → learn live\n\n"
        "📊 Free 10,000$ demo 👇🏻\n{game_url}"
    ),
)

# Soft CTA — nudge without hard register push.
SOFT_CTA_TEMPLATES: tuple[str, ...] = (
    "Yoo quick check 👀 is your demo open?? Don’t miss the next one 🔥",
    "Bro keep the broker ready 😤 next call could hit anytime 💰",
    "If you’re waiting for a “perfect moment”… this is it ⚡ get that demo loaded 👇🏻",
    "Real ones already locked in 🔒 who’s still waiting?? Demo up. NOW 🔥",
    "Don’t tell me you still don’t have an account open… 😤💸",
    "Next call loading… be ready or be jealous later 😏💰",
    "Ping!! 🔔 stay awake. One missed call = one missed bag ⚡",
)


# ============================================================
#  MARKET NEWS / PAIR BRIEFS — Placeholders: {pair}
# ============================================================
MARKET_BRIEF_TEMPLATES: tuple[str, ...] = (
    "👀 Eyes on {pair} rn… market looking spicy 🌶️ something’s cooking",
    "📰 {pair} update: volume picking up and I’m not sleeping on this one 😤",
    "⚡ {pair} moving weird today… stay sharp, next setup might be close 🔥",
    "💬 Quick vibe check on {pair} — liquidity is here, don’t go AFK 🤑",
    "🔥 {pair} looking alive!! feeling good about this window ngl",
    "📊 {pair}: noise fading, real moves starting… stay locked in 🔒",
    "🚨 Heads up on {pair}… candles getting aggressive 😮💨",
    "💰 {pair} feels ready for a clean push… I’m watching hard 👀🔥",
    "🌊 {pair} surfing some wild price action rn… don’t blink",
    "📈 {pair} heating up for real… next round could be 🔥",
    "🫣 Quiet on {pair}? Nah… that’s usually before the fireworks 💥",
    "🗞️ Market tea on {pair}: traders piling in… stay ready fam 💪",
)


# ============================================================
#  SESSION OPEN / WRAP — Placeholders: {session}
# ============================================================
SESSION_OPEN_TEMPLATES: tuple[str, ...] = (
    "🚨 {session} SESSION OPEN 🚨\n\nWe are LIVE. Locks in, fingers ready 💪💰",
    "☀️ {session} is ON!! Let’s make this session count 🔥 who’s here??",
    "🟢 {session} desk liveeeee… only clean setups today. Let’s eat 😤📈",
    "💥 {session} STARTING NOW\n\nWake uppp energy through the roof 🚀💸",
    "⏰ {session} bells ringing!! Markets open — we’re hunting 👀🔥",
    "🔥 {session} gang assembleee… drop a 🔥 if you’re ready",
)

SESSION_WRAP_TEMPLATES: tuple[str, ...] = (
    "✅ {session} DONE\n\nGood work team 👏 rest up — we come back stronger 💪",
    "🏁 {session} closed. Proud of everyone who stayed disciplined 🔥 see you next open",
    "💨 {session} wrapped!! Take the wins, shake the losses… we go again soon 💰",
    "🌙 {session} over… go stretch, hydrate, come back hungry next round 😤",
    "👏 {session} in the books. Love the energy today fam ❤️💰",
    "💤 Closing {session}. Screenshots saved? Good. See you next open 🔥",
)


# ============================================================
#  AUTHORITY MICRO-TIPS
# ============================================================
TIP_TEMPLATES: tuple[str, ...] = (
    "💡 Reminder: respect that 5MIN expiry fr… early exit = free L sometimes 😅",
    "🧠 Don’t go crazy with size. Small and consistent beats one big ego trade 💯",
    "⚠️ Missed a signal? Chill. Chase mode is how accounts die 😭 wait for the next one",
    "🎯 Demo first if you’re new. Learn the rhythm then go bigger… trust me 🙏",
    "📌 Keep it simple: 1 pair, 1 direction, 1 expiry. Don’t overthink it 😌",
    "✍️ Screenshot your results. You’ll thank yourself later when patterns click 👀",
    "🛡️ Protect your capital like it’s your last… because emotions don’t pay bills 😤",
    "⏳ Patience is a strategy. Forcing trades is gambling with extra steps 🎲",
    "📵 Mute the noise. Follow the call… don’t invent your own mid-trade 😅",
    "💪 Losing streak? Reset size, breathe, come back clean. Revenge trades = ☠️",
)


# ============================================================
#  TRUST / SOCIAL PROOF — Placeholders: {wins}, {total}, {session}
# ============================================================
TRUST_RECAP_TEMPLATES: tuple[str, ...] = (
    "🔥 {session} so far: {wins}/{total} GREEN… we moving!! who’s still in?? 💰",
    "📈 Pulse check — {wins} out of {total} hitting this {session} window 😮‍💨 keep going",
    "💬 Chat energy: {wins}/{total} closed green in {session}… proud of y’all 👏🔥",
    "🟢 Scoreboard {session}: {wins}/{total} … not bad for selective play 😏💸",
    "💥 {wins} greens out of {total} this {session}… the room is LOUD rn 🗣️🔥",
    "🏆 {session} report card: {wins}/{total} closed clean. Keep that focus fam 💪",
)


# ============================================================
#  STREAK HYPE — Placeholders: {streak}
# ============================================================
STREAK_HYPE_TEMPLATES: tuple[str, ...] = (
    "🔥🔥 STREAK ALERT: {streak} in a row!! don’t break the vibe now 😤💰",
    "😈 {streak} straight greens… who’s feeling unstoppable rn??",
    "🚀 Streak mode: {streak}… keep riding don’t get greedy don’t get scared ⚡",
    "💎 {streak} W’s stacked. This is why we stay locked in 🔒🔥",
    "📣 CAN WE GET A {streak} STREAK IN THE CHAT?? 💸💸",
)


# ============================================================
#  FOMO / URGENCY (between rounds)
# ============================================================
FOMO_TEMPLATES: tuple[str, ...] = (
    "⏳ Next call loading… if you’re not ready you’ll watch from outside 👀🔥",
    "😱 People sleeping on these setups then ask “what happened” later… stay awake",
    "⚡ Don’t scroll away rn. Something’s about to drop…",
    "🔔 Last chance energy before the next round… broker open?? 💰",
    "🚪 Door’s open for this window… after that it’s FOMO city 😤",
    "🫣 Imagining you miss the next one… yeah me neither. Stay here 🔥",
)


# ============================================================
#  WELCOME / COMMUNITY
# ============================================================
WELCOME_TEMPLATES: tuple[str, ...] = (
    "👋 New faces in the room?? Welcome fam… stick around, we move selective 🔥💰",
    "🎉 Welcome welcome!! Glad you’re here. Follow the calls, don’t force chaos 💪",
    "💎 To everyone just joining — you’re early enough. Demo up and ride with us 👇🏻🔥",
    "🤝 Real traders don’t gatekeep… we grow together. Glad you found the channel ❤️",
    "🌟 Shoutout to the new members!!! Drop a 🔥 if you just joined today",
)


# ============================================================
#  OVERNIGHT / LATE VIBES
# ============================================================
OVERNIGHT_TEMPLATES: tuple[str, ...] = (
    "🌙 Market napping… we’re resting too. Big money window comes with London/NY 💤💰",
    "😴 Quiet hours. Recharge. Tomorrow’s opens gon’ be loud again 🔥",
    "🌌 Late night crew still here?? Respect. Next session we eat 😤📈",
    "🕯️ Slow candles tonight… don’t force it. Save energy for the real session 💪",
    "🌚 Overnight chill mode. Dream about greens, wake up ready 🤑",
)


# ============================================================
#  PROFIT / SCREENSHOT TEASE
# ============================================================
PROFIT_TEASE_TEMPLATES: tuple[str, ...] = (
    "📸 That last result still looks pretty in the screenshots ngl 😮‍💨💸",
    "🤑 Some of y’all pocketed clean bags on that last round… I see you 👀🔥",
    "💥 Profit bounce hitting different… who just smiled at their phone?? 📱💰",
    "🟩 Green on the chart hits the brain like dopamine… stay humble stay hungry 😤",
    "✨ If your P/L just winked at you… type “LET’S GO” 🗣️💸",
)


# ============================================================
#  FILLER WEIGHTS (scheduler picks idle content from these keys)
# ============================================================
FILLER_WEIGHTS: dict[str, int] = {
    "market_brief": 28,
    "tip": 16,
    "trust_recap": 12,
    "soft_cta": 8,
    "streak_hype": 10,
    "fomo": 10,
    "welcome": 6,
    "profit_tease": 6,
    "overnight": 4,
}

# Overnight-only preferred weights (no soft CTA spam at night).
OVERNIGHT_FILLER_WEIGHTS: dict[str, int] = {
    "overnight": 50,
    "tip": 25,
    "market_brief": 15,
    "welcome": 10,
}
