import discord
from discord.ext import commands

message_info = {
    "author-name": None,
    "time": None
}

class Antiraid(commands.Cog):

    def __init__(self, client):
        self.client = client

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author.name == message_info["author-name"]:



    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)} ms")


def setup(client):
    client.add_cog(Antiraid(client))