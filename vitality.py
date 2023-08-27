import discord
from discord.ext import commands
import os
import mysql.connector

# Set up intents for the bot
intents = discord.Intents.default()

# Bot configuration
prefix = "V-"
client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), help_command=None, intents=intents)

# Database connection
client.dbname = 'DBNAME'
client.mydb = mysql.connector.connect(
    host='DBNAME',
    user=client.dbname,
    passwd='PASSWD'
)

# Print connection details for debugging
print("Established connection with mySQL DB")
print(client.mydb)

# Set up cursor for SQL operations
client.cursor = client.mydb.cursor(buffered=True)
client.cursor.execute(f"USE {client.dbname}")

# Define owner's ID for restricted commands
ownerID = 1234  # Replace with your ID

# Load extension command
@client.command()
async def load(ctx, extension):
    if ctx.author.id == ownerID:
        client.load_extension(f'Cogs.{extension}')
        await ctx.send(f"Loaded `{extension}`")

# Unload extension command
@client.command()
async def unload(ctx, extension):
    if ctx.author.id == ownerID:
        client.unload_extension(f'Cogs.{extension}')
        await ctx.send(f"Unloaded `{extension}`")

# Reload extension command
@client.command()
async def reload(ctx, extension):
    if ctx.author.id == ownerID:
        client.reload_extension(f'Cogs.{extension}')
        await ctx.send(f"Reloaded `{extension}`")

# Shutdown bot command
@client.command()
async def shutdown(ctx):
    if ctx.author.id == ownerID:
        await ctx.send("Client shutting down.")
        exit()

# Automatically load all extensions (cogs) in the Cogs directory
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')
        print(f'Cogs.{filename[:-3]}')

# Run the bot
client.run('TOKEN')
