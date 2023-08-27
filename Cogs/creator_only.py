import discord
from discord.ext import commands
import json
import os  

# Define a global variable for the owner's ID for quick access
ownerID = 1234 

class CreatorOnly(commands.Cog):
    """Cog that contains commands only accessible by the bot creator."""

    def __init__(self, client):
        """Initialize the Cog with the bot client."""
        self.client = client

    def is_owner(self, ctx):
        """Check if the command caller is the bot owner."""
        return ctx.author.id == ownerID

    @commands.command()
    async def cf(self, ctx):
        """Create a JSON file for every member in the guild if they don't already have one."""
        if self.is_owner(ctx):
            members = ctx.guild.members
            for member in members:
                file_path = f"Users/{member.id}.json"
                if not os.path.isfile(file_path):  # Check if file doesn't exist
                    with open(file_path, 'w+') as f:
                        data = {
                            'Balance': 0,
                            'Inventory': {}
                        }
                        # Write the default data to the JSON file
                        json.dump(data, f, indent=2)

    @commands.command()
    async def guilds(self, ctx):
        """Print the details of all guilds the bot is in."""
        if self.is_owner(ctx):
            message = "\n".join([f"{guild.id}: {guild.name} {guild.owner} {len(guild.members)}" for guild in self.client.guilds])
            print(message)

    @commands.command()
    async def guildsinfo(self, ctx, member: discord.Member = None):
        """Send the details of all guilds owned by a given member."""
        if self.is_owner(ctx) and member:
            message = "\n".join([f"{guild.id}: {guild.name} {len(guild.members)}" for guild in self.client.guilds if guild.owner == member])
            await ctx.send(message if message else "This user is not the owner of any guilds I am in.")

    @commands.command()
    async def setstatus(self, ctx, *, status):
        """Set the bot's status."""
        if self.is_owner(ctx):
            await self.client.change_presence(activity=discord.Game(name=status))
            await ctx.send(f"Changed status to `{status}`")

    @commands.command()
    async def channeltype(self, ctx):
        """Send the type of the channel where the command was invoked."""
        if self.is_owner(ctx):
            await ctx.send(ctx.channel.type)

    @commands.command()
    async def getinvite(self, ctx, guild_id):
        """Get an invite link for a specific guild."""
        if self.is_owner(ctx):
            guild = self.client.get_guild(int(guild_id))
            invite = await guild.channels[0].create_invite(unique=False)
            await ctx.send(f"discord.gg/{invite.code}")

    @commands.command()
    async def forcegive(self, ctx, member: discord.Member, amount: int):
        """Forcefully give a specific amount to a member."""
        if self.is_owner(ctx):
            with open(f"Users/{member.id}.json", 'r') as f:
                user = json.load(f)
                user['Balance'] += amount
            with open(f"Users/{member.id}.json", 'w') as f:
                json.dump(user, f)
            await ctx.send(f"Gave {member} `{amount}`")

    @commands.command()
    async def forceremove(self, ctx, member: discord.Member, amount: int):
        """Forcefully remove a specific amount (or all) from a member's balance."""
        if self.is_owner(ctx):
            with open(f"Users/{member.id}.json", 'r') as f:
                user = json.load(f)
                user['Balance'] -= amount if amount != "all" else user['Balance']
                if user['Balance'] < 0:
                    user['Balance'] = 0
            with open(f"Users/{member.id}.json", 'w') as f:
                json.dump(user, f)
            await ctx.send(f"Removed `{amount}` from {member}")

    @commands.command()
    async def icon(self, ctx):
        """Send the bot's avatar URL."""
        if self.is_owner(ctx):
            await ctx.send(str(self.client.user.avatar_url))

def setup(client):
    """Function to set up the Cog in the bot. It's called when the Cog is loaded."""
    client.add_cog(CreatorOnly(client))
