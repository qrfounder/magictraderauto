from __future__ import annotations

from pathlib import Path

import httpx


class TelegramClient:
    def __init__(self, bot_token: str, timeout: float = 30.0) -> None:
        self._base = f"https://api.telegram.org/bot{bot_token}"
        self._client = httpx.AsyncClient(timeout=timeout)

    async def send_message(self, chat_id: str, text: str) -> dict:
        response = await self._client.post(
            f"{self._base}/sendMessage",
            json={"chat_id": chat_id, "text": text, "disable_web_page_preview": False},
        )
        response.raise_for_status()
        payload = response.json()
        if not payload.get("ok"):
            raise RuntimeError(f"Telegram API error: {payload}")
        return payload

    async def send_photo(self, chat_id: str, photo_path: str, caption: str | None = None) -> dict:
        path = Path(photo_path)
        data: dict[str, str] = {"chat_id": chat_id}
        if caption:
            data["caption"] = caption
        with path.open("rb") as fh:
            response = await self._client.post(
                f"{self._base}/sendPhoto",
                data=data,
                files={"photo": (path.name, fh, "image/png")},
            )
        response.raise_for_status()
        payload = response.json()
        if not payload.get("ok"):
            raise RuntimeError(f"Telegram API error: {payload}")
        return payload

    async def aclose(self) -> None:
        await self._client.aclose()
