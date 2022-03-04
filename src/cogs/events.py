import json
import os
import re

from discord.ext import commands
from dotenv import load_dotenv

from websocket_connection import ws

load_dotenv()
CHAT_ID = os.environ["CHAT_ID"]
try:
    CHAT_ID = int(CHAT_ID)
except Exception as e:
    print(e)
    CHAT_ID = 0


class Events(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.channel.id == CHAT_ID:
            content = re.sub(
                r"https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+", "", message.content
            )

            if content:
                sending_data = {
                    "id": "Discord",
                    "name": message.author.display_name,
                    "content": content,
                }
                ws.send(json.dumps(sending_data))


def setup(bot):
    bot.add_cog(Events(bot))
