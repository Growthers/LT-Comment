import os

import requests
from dotenv import load_dotenv

load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def to_discord(message: str, webhook: str = DISCORD_WEBHOOK_URL) -> None:
    if not webhook:
        return

    data = {"content": message}

    try:
        requests.post(webhook, data=data)
    except Exception:
        pass
