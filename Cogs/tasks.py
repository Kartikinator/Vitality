import discord
from discord.ext import commands
import random
import asyncio


class tasks(commands.Cog):

    def __init__(self, client):
        # async def change_status(self):
        #     await client.wait_until_ready()
        #     statuses = [f"-help", f"{len(client.guilds)} servers", f"{len(client.users)} users"]
        #
        #     while not self.client.is_closed():
        #         status = random.choice(statuses)
        #         await client.change_presence(activity=discord.Game(name=status))
        #         await asyncio.sleep(15)

        self.client = client
        # self.client.loop.create_task(change_status(self))









def setup(client):
    client.add_cog(tasks(client))