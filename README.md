# Entertainment game channel bot

Posts **labeled game predict rounds** to a Telegram channel on a **premium UTC schedule**: selective signal rounds during London (07:00–11:00) and New York (13:00–17:00) windows, with market briefs, tips, trust recaps, and thinned demo CTAs between them.

This is an **entertainment bot**, not real trading signals or financial advice. Result images use configurable win odds (`WIN_PERCENT` in `bot/templates.py`).

## Cadence (premium defaults)

| Window (UTC) | Content |
| --- | --- |
| 06:50–07:10 | London session open (once/day) |
| 07:00–11:00 | Signal rounds every 45–60 min (jittered) |
| 11:00–13:00 | Market brief / tip / soft trust (max 2) |
| 12:50–13:10 | New York session open (once/day) |
| 13:00–17:00 | Signal rounds every 45–60 min (jittered) |
| 17:00–17:20 | Session wrap (once/day) |
| Elsewhere | Rare tip or market brief (max 2/night) |

Hard demo CTA posts only on every **2nd** completed round and only if `CTA_INTERVAL_MINUTES` has elapsed since the last hard CTA.

Edit copy in `bot/templates.py`. Restart the bot after changes.

## Local run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env — set BOT_TOKEN (never commit .env)
python -m bot.main
```

## EasyPanel (Hostinger) — 24/7 with laptop off

1. Push this repo to GitHub (private recommended), **or** deploy from Dockerfile on the server.
2. In EasyPanel → **Create Project** → **App**.
3. Source: GitHub repo **or** upload / paste Dockerfile build context.
4. Build method: **Dockerfile** (root `Dockerfile`).
5. Environment variables:

| Key | Example |
| --- | --- |
| `BOT_TOKEN` | your regenerated BotFather token |
| `CHANNEL_ID` | `-1001948808705` |
| `GAME_CTA_URL` | `https://bit.ly/Saferegister` |
| `MIN_SIGNAL_MINUTES` | `45` |
| `MAX_SIGNAL_MINUTES` | `60` |
| `RESULT_DELAY_SECONDS` | `60` |
| `CTA_INTERVAL_MINUTES` | `30` |
| `CORRECT_PROBABILITY` | `0.5` |

6. Deploy / Start. Check logs for `Posted signal` / `Posted filler`.
7. Confirm posts appear in **Magic Trader Signals**.
8. Close your laptop — the VPS keeps running.

## Security

- Never commit `.env` or paste bot tokens in chat.
- If a token was exposed, revoke it in BotFather and set the new one in EasyPanel only.
