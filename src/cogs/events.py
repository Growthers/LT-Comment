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
        self.isSend = False

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.channel.id == CHAT_ID and self.isSend:
            content = re.sub(
                r"https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+", "", message.content
            )

            if content.startswith("chat!"):
                return

            if content:
                sending_data = {
                    "id": "Discord",
                    "name": message.author.display_name,
                    "content": content,
                }
                ws.send(json.dumps(sending_data))

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def start(self, ctx):
        self.isSend = True
        await ctx.send(f"<#{CHAT_ID}> に送信されたメッセージの反映を開始します")

    @start.error
    async def start_error(self, ctx, error):
        pass

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def stop(self, ctx):
        self.isSend = False
        await ctx.send(f"<#{CHAT_ID}> に送信されたメッセージの反映を停止します")

    @stop.error
    async def stop_error(self, ctx, error):
        pass


def setup(bot):
    bot.add_cog(Events(bot))
