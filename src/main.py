import os
import threading

import discord
from discord.ext import commands
from dotenv import load_dotenv

from twitter import stream
from websocket_connection import ws

load_dotenv()

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
cogs = ["cogs.events"]


class LT_Chat(commands.Bot):
    def __init__(self, prefix) -> None:
        intents = discord.Intents.default()
        super().__init__(
            command_prefix=prefix,
            intents=intents,
            help_command=None,
            case_insensitive=True,
        )

        for cog in cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                print(e)

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")

    @commands.Cog.listener()
    async def on_reload(self):
        for cog in cogs:
            try:
                self.reload_extension(cog)
            except Exception as e:
                print(e)


bot = LT_Chat(prefix="chat!")

if __name__ == "__main__":
    try:
        stream_thread = threading.Thread(target=stream)
        ws_thread = threading.Thread(target=ws.run_forever)
        stream_thread.start()
        ws_thread.start()
        bot.run(TOKEN)
    except Exception as e:
        print(e)
