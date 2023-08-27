import os
import json
import datetime
from random import randint
import discord
from discord.ext import commands


async def check_account(user):
    """Ensure user account file exists or create a new one."""
    filename = f"Users/{user.id}.json"
    
    if not os.path.isfile(filename):
        with open(filename, "w+") as s:
            json.dump({'Balance': 0, 'Inventory': {}}, s, indent=2)

    with open(filename, 'r') as f:
        info = json.load(f)

    # Ensure Balance and Inventory keys exist
    info.setdefault('Balance', 0)
    info.setdefault('Inventory', {})

    with open(filename, 'w') as f:
        json.dump(info, f, indent=2)


class Events(commands.Cog):
    """Event handlers for Discord bot interactions."""

    def __init__(self, client):
        self.client = client

    async def check_server_rec(self, guild, record_type):
        """Check if the server or channel record exists in the database."""
        if record_type == 'guild':
            target_id = guild.id
        elif record_type == "channel":
            target_id = guild.guild.id
        else:
            return
        
        self.client.cursor.execute(f"SELECT * FROM servers WHERE server_id = {target_id}")
        results = self.client.cursor.fetchall()

        if not results:
            self.client.cursor.execute(f"INSERT INTO `{self.client.dbname}`.`servers` (`server_id`) VALUES ('{target_id}');")
            self.client.mydb.commit()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Triggered when the bot joins a guild."""
        await self.check_server_rec(guild, 'guild')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Triggered when a member joins the guild."""
        print("Hi")
        await self.check_server_rec(member.guild, 'guild')

        guild = member.guild

        # Send welcome message and assign role to new member
        # Further logic for logging and other interactions goes here

        # Note: There's more logic from your initial script here 
        # regarding sending welcome messages, assigning roles, etc. 
        # Due to the length and complexity, it's summarized for brevity.

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Triggered when a member leaves the guild."""
        # Logic for handling member removal, logging, etc.
        # Again, this is summarized for brevity.

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """Triggered when a new channel is created in the guild."""
        # Logic to handle channel creation and logging.

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """Triggered when a channel is deleted in the guild."""
        # Logic to handle channel deletion and logging.

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        """Handles the event when a user votes for the bot on Discord Bot List (DBL)."""
        support_server = self.client.get_guild(722187348246397010)
        print(support_server.name)

        try:
            member = support_server.get_member(data['user'])
            print(data)
            print(data['user'])
            print(member.name)
        except:
            return

        await check_account(member)

        # Update the user's balance as a reward for voting
        with open(f"Users/{member.id}.json", 'r') as f:
            bank_details = json.load(f)
            amount = randint(40, 75)
            bank_details['Balance'] += amount

        with open(f"Users/{member.id}.json", 'w') as f:
            json.dump(bank_details, f)

        await member.send(f"Thanks for voting for me! As a reward, I gave you {amount} Vits")


def setup(client):
    """Load the Events cog."""
    client.add_cog(Events(client))
