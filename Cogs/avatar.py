import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from PIL import Image

class Avatar(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    # Command to display a user's avatar
    @commands.command()
    @commands.cooldown(1, 2, BucketType.user)
    async def avatar(self, ctx, *, member: discord.Member = None):
        
        # If no member is provided, default to the command author
        target_member = member or ctx.author
        
        embed = discord.Embed(title=f"{target_member.name}'s Avatar", colour=0x12ba01)
        f = discord.File("Avatar.png", filename="avatar.png")
        embed.set_image(url=f"attachment://avatar.png")
        await ctx.send(file=f, embed=embed)

    # Command to equip an accessory to an avatar
    @commands.command()
    async def equip(self, ctx, accessory=None):
        if accessory is None:
            return await ctx.send("Pick an accessory to equip")

        # Equip a hat to the avatar
        if accessory == "hat":
            filename = 'Hat.png'
            hat_image = Image.open(filename, 'r')
            
            filename1 = 'Avatar.png'
            avatar_bg = Image.open(filename1, 'r')
            
            # Composite the avatar and the hat
            text_img = Image.new('RGBA', (800, 600), (0, 0, 0, 0))
            text_img.paste(avatar_bg, (0, 0))
            text_img.paste(hat_image, (170, -185), mask=hat_image)
            
            text_img.save("ball.png", format="png")

            # Send the updated avatar
            avatar = discord.File("ball.png", filename="avatar.png")
            embed = discord.Embed(title=f"{ctx.author.name}'s Avatar")
            embed.set_image(url=f"attachment://avatar.png")
            await ctx.send(file=avatar, embed=embed)

# Setup function to add the cog
def setup(client):
    client.add_cog(Avatar(client))
