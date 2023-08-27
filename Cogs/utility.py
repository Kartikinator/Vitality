import discord
from discord.ext import commands
import random
import asyncio
import wikipediaapi
import dbl


class Utility(commands.Cog):

    def __init__(self, client):
        client.green = 0x18d100
        client.yellow = 0xd1d100
        client.red = 0xeb4034

        self.client = client

    # @commands.command()
    # async def changeprefix(self, ctx, prefix=None):
    #     if prefix is None:
    #         await ctx.send("The proper command usage is `changeprefix <new-prefix>`")
    #

    @commands.command()
    async def dm(self, ctx):
        await ctx.author.send("Sup homie!")

    @commands.command()
    async def support(self, ctx):
        await ctx.send("Here is my support server: https://discord.gg/7QvmYfE")

    @commands.command(aliases=["8ball"])
    async def eightball(self, ctx, *, question=None):
        if question is None:
            return await ctx.send("Please specify a question.")

        responses = ["As I see it, yes.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don’t count on it.",
                     "It is certain.",
                     "It is decidedly so.",
                     "Most likely.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Outlook good.",
                     "Reply hazy, try again.",
                     "Signs point to yes.",
                     "Very doubtful.",
                     "Without a doubt.",
                     "Yes.",
                     "Yes – definitely.",
                     "You may rely on it."]
        await ctx.send(random.choice(responses))

    @commands.command()
    async def roll(self, ctx):
        rollNumbers = ["1", "2", "3", "4", "5", "6"]
        await ctx.send(f'I rolled a {random.choice(rollNumbers)}')

    @commands.command()
    async def coinflip(self, ctx):
        sides = ["heads", "tails"]
        await ctx.send(f"It's {random.choice(sides)}")

    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(title="Title", description="Desc", color=0xFFFF00)
        embed.add_field(name="Field1", value="Test1", inline=False)
        embed.add_field(name="Field2", value="Test2", inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def botstats(self, ctx):
        embed = discord.Embed(title="My Statistics", color=0xFFFF00)
        embed.add_field(name="My Name", value=f"```Vitality#9610```", inline=True)
        embed.add_field(name="Creator", value=f"```CitrusSponge#5745```", inline=True)
        embed.add_field(name="Servers", value=f"```{len(self.client.guilds)}```", inline=False)
        embed.add_field(name="Users", value=f"```{len(self.client.users)}```", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def serverstats(self, ctx):
        online = 1
        for member in ctx.guild.members:
            if str(member.status) == "online":
                online += 1

        embed = discord.Embed(title=f"{ctx.guild.name}'s Statistics", color=0xFFFF00)
        embed.add_field(name="Server ID", value=f"```{ctx.guild.id}```", inline=False)
        embed.add_field(name="Members", value=f"```{len(ctx.guild.members)}```", inline=True)
        embed.add_field(name="Online", value=f"```{online}```", inline=True)
        embed.add_field(name="Max Members", value=f"```{ctx.guild.max_members}```", inline=True)
        embed.add_field(name="Custom Emojis", value=f"```{len(ctx.guild.emojis)}```", inline=True)
        embed.add_field(name="Total Roles", value=f"```{len(ctx.guild.roles)}```", inline=True)
        embed.add_field(name="Region", value=f"```{ctx.guild.region}```", inline=True)
        embed.add_field(name="Creation Date", value=f"```{ctx.guild.created_at}```", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        if member is None:
            sender = ctx.author
        else:
            sender = member
        embed = discord.Embed(title=f"{sender.name}'s User Information", color=0xFFFF00)
        embed.add_field(name="User ID", value=f"```{sender.id}```", inline=False)
        embed.add_field(name="User Name", value=f"```{sender.name}```", inline=True)
        embed.add_field(name="Discriminator", value=f"```{sender.discriminator}```", inline=True)
        embed.add_field(name="Status", value=f"```{sender.status}```", inline=True)
        embed.add_field(name="Highest Role", value=f"```{sender.top_role}```", inline=False)
        embed.add_field(name="Account Created", value=f"```{sender.created_at}```", inline=False)
        embed.set_thumbnail(url=sender.avatar_url)

        await ctx.send(embed=embed)

    @info.error
    async def info_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.BadArgument):
            return await ctx.send("An invalid user was specified.")
        else:
            print(error)

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(
            "Invite me to your server using this link: https://discord.com/api/oauth2/authorize?client_id=236318880757317632&permissions=2147483639&scope=bot")

    @commands.command()
    async def echo(self, ctx, *, message=None):
        if message is None:
            return await ctx.send("Please specify a word or phrase that I should echo.")
        if "@everyone" in message or "@here" in message:
            return await ctx.send("Nice try, but no.")
        await ctx.send(message)

    # @commands.command()
    # async def serverinvite(self, ctx):
    #     await ctx.send(f"Here is a server invite for this server: {await ctx.channel.create_invite(unique=False)}")

    @commands.command()
    async def wiki(self, ctx, *, search_term=None):
        if search_term is None:
            return await ctx.send("Please specify a term or phrase to search.")
        message = await ctx.send("Finding...")
        wiki_wiki = wikipediaapi.Wikipedia('en')

        page_py = wiki_wiki.page(search_term)

        if not page_py.exists():
            return await message.edit(content="This Wikipedia page does not exist")

        if len(page_py.summary.split()) > 50:
            content_array = page_py.summary.split()[:50]
            content = " ".join(content_array)

        else:
            content = page_py.summary

        embed = discord.Embed(url=page_py.fullurl)
        embed.set_author(name="Wikipedia",
                         icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Wikipedia_svg_logo.svg/1200px-Wikipedia_svg_logo.svg.png")
        embed.title = page_py.title
        embed.description = content + "..."

        await message.edit(content="", embed=embed)

    @commands.command()
    async def rename(self, ctx, *, name):
        await ctx.author.edit(nick=name)

    @rename.error
    async def rename_error(self, ctx, error):
        await ctx.send("I do not have the proper permissions to rename you.")

    @commands.command()
    async def hug(self, ctx, *, member=None):
        if member is None:
            return await ctx.send("Who do you want to hug?")

        pics = ["https://media.tenor.com/images/cb9bffb9b0e88808fa156f2432233aa7/tenor.gif", "https://i.pinimg.com/originals/0a/16/52/0a1652de311806ce55820a7115993853.gif"]

        embed = discord.Embed(
            description=f"{ctx.author.name} **hugged** {member}",
            colour=0x12ba01
        )

        embed.set_image(url=f"{random.choice(pics)}")

        await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, *, member=None):
        if member is None:
            return await ctx.send("Who or what do you want to slap?")

        pics = ["https://media3.giphy.com/media/ylqr4JvFaZqnK/giphy.gif",
                "https://thumbs.gfycat.com/CleanSpiritedBug-size_restricted.gif"]


        embed = discord.Embed(
            description=f"{ctx.author.name} **slapped** {member}",
            colour=0x12ba01
        )

        embed.set_image(url=f"{random.choice(pics)}")

        await ctx.send(embed=embed)

    @commands.command()
    async def punch(self, ctx, *, member=None):
        if member is None:
            return await ctx.send("Who or what do you want to slap?")

        pics = ["https://media0.giphy.com/media/39BdMOJMK2YVqktnlS/giphy.gif",
                "https://media2.giphy.com/media/vcdZUjtcK8fPraAKm5/source.gif"]

        embed = discord.Embed(
            description=f"{ctx.author.name} **punched** {member}",
            colour=0x12ba01
        )

        embed.set_image(url=f"{random.choice(pics)}")

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def poll(self, ctx):
        def check(message):
            return message.author == ctx.author

        try:
            msg = await ctx.send("Write the title of the poll. Type `CANCEL` to cancel. This message times out in 1 "
                                 "minute.")
            poll_title = await self.client.wait_for('message', check=check, timeout=60)

            if poll_title.content == "CANCEL":
                return await ctx.send("The setup process has been cancelled")
        except asyncio.TimeoutError:
            return await msg.edit(content="**This message timed out**")

        try:
            msg = await ctx.send("Write the options for the poll, separate each option using a comma (`,`) . Type "
                                 "`CANCEL` to cancel. This message times out in 1 minute.")
            poll_options = await self.client.wait_for('message', check=check, timeout=60)

            if poll_options.content == "CANCEL":
                return await ctx.send("The setup process has been cancelled")

        except asyncio.TimeoutError:
            return await msg.edit(content="**This message timed out**")

        try:
            msg = await ctx.send("Tag the channel where I should post the poll. Type `CANCEL` to cancel.")
            poll_channel = await self.client.wait_for('message', check=check, timeout=60)

            if poll_channel.content == "CANCEL":
                return await ctx.send("The setup process has been cancelled")

            if ctx.guild.get_channel(int(poll_channel.content[2:-1])) is None:
                return await ctx.send("Invalid channel. The setup process has been cancelled.")

        except asyncio.TimeoutError:
            return await msg.edit(content="**This message timed out**")

        options = poll_options.content.split(",")

        poll_msg_channel = ctx.guild.get_channel(int(poll_channel.content[2:-1]))

        if len(options) < 2 or len(options) > 10:
            return await ctx.send("The poll must have at least two and less than 10 options. Cancelling poll setup.")

        emojis = [
            "\U0001f1e6",
            "\U0001f1e7",
            "\U0001f1e8",
            "\U0001f1e9",
            "\U0001f1ea",
            "\U0001f1eb",
            "\U0001f1ec",
            "\U0001f1ed",
            "\U0001f1ee",
            "\U0001f1ef"
        ]

        display = ""
        numbers = 0

        print(options)

        for option in options:
            index = options.index(option)
            display += f"{emojis[index]} {option} \n \n"
            numbers += 1

        embed = discord.Embed(title=poll_title.content, description=display, color=0xff9129)
        poll = await poll_msg_channel.send(embed=embed)

        for number in range(numbers):
            await poll.add_reaction(emojis[number])

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed = discord.Embed(title="Only users with the `manage server` permission can start polls", color=0xFFFF00)
            await ctx.send(embed=embed)

    # @commands.command()
    # @commands.has_permissions(manage_guild=True)
    # async def giveaway(self, ctx):
    #     def check(message):
    #         return message.author == ctx.author
    #
    #     try:
    #         msg = await ctx.send(":gift: Beginning the giveaway setup process. Type `CANCEL` at any time to cancel. "
    #                              "You have 2 minutes to provide an answer to each question. \n\n"
    #                              "`What are you giving away?`")
    #         give_item = await self.client.wait_for('message', check=check, timeout=120)
    #
    #         if give_item.content == "CANCEL":
    #             return await ctx.send("The setup process has been cancelled")
    #     except asyncio.TimeoutError:
    #         return await msg.edit(content="**This message timed out**")
    #
    #     try:
    #         msg = await ctx.send(f":gift: Okay, you are giving away **{give_item.content}** \n\n"
    #                              f"`How many winners will your giveaway have?`")
    #         give_winners = await self.client.wait_for('message', check=check, timeout=120)
    #
    #         if give_winners.content == "CANCEL":
    #             return await ctx.send("The setup process has been cancelled")
    #
    #     except asyncio.TimeoutError:
    #         return await msg.edit(content="**This message timed out**")
    #
    #     try:
    #         msg = await ctx.send(f"Okay, {give_winners.content} winners. \n\n")
    #         winner_number = await self.client.wait_for('message', check=check, timeout=120)
    #
    #         if winner_number.content == "CANCEL":
    #             return await ctx.send("The setup process has been cancelled")
    #
    #         if ctx.guild.get_channel(int(winner_number.content[2:-1])) is None:
    #             return await ctx.send("Invalid channel. The setup process has been cancelled.")
    #
    #     except asyncio.TimeoutError:
    #         return await msg.edit(content="**This message timed out**")
    #
    #     try:
    #         msg = await ctx.send(f"Okay, {give_winners.content} winners. \n\n")
    #         giveaway_channel = await self.client.wait_for('message', check=check, timeout=120)
    #
    #         if winner_number.content == "CANCEL":
    #             return await ctx.send("The setup process has been cancelled")
    #
    #         if ctx.guild.get_channel(int(winner_number.content[2:-1])) is None:
    #             return await ctx.send("Invalid channel. The setup process has been cancelled.")
    #
    #     except asyncio.TimeoutError:
    #         return await msg.edit(content="**This message timed out**")
    #
    #     embed = discord.Embed(title=give_item.content, description="React :gift: to win", color=0xff9129)
    #     poll = await poll_msg_channel.send(embed=embed)


    @poll.error
    async def giveaway_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed = discord.Embed(title="Only users with the `manage server` permission can start polls",
                                  color=0xFFFF00)
            await ctx.send(embed=embed)

    @commands.command()
    async def vote(self, ctx):
        await ctx.send("Vote for me here and receive some free Vits once every 12 hours! https://top.gg/bot/236318880757317632/vote")


def setup(client):
    client.add_cog(Utility(client))
