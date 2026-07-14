# Entertainment game channel bot

Posts **labeled game predict rounds** to a Telegram channel on a random 5–15 minute schedule, then a result after 1 minute. Every 30 minutes it posts a game CTA.

This is an **entertainment bot**, not real trading signals or financial advice. Results use transparent fair odds (default 50% CORRECT).

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
| `GAME_CTA_URL` | `https://t.me/magicroomofficial` |
| `MIN_SIGNAL_MINUTES` | `5` |
| `MAX_SIGNAL_MINUTES` | `15` |
| `RESULT_DELAY_SECONDS` | `60` |
| `CTA_INTERVAL_MINUTES` | `30` |
| `CORRECT_PROBABILITY` | `0.5` |

6. Deploy / Start. Check logs for `Posted game signal`.
7. Confirm posts appear in **Magic Trader Signals**.
8. Close your laptop — the VPS keeps running.

## Security

- Never commit `.env` or paste bot tokens in chat.
- If a token was exposed, revoke it in BotFather and set the new one in EasyPanel only.
