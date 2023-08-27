import discord
from discord.ext import commands
import random
import asyncio


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.bot_has_permissions(add_reactions=True, manage_messages=True)
    async def help(self, ctx):
        total_pages = 5
        timeout = 60

        async def pageone(help_message, total_pages):
            embed = discord.Embed(title="Moderation Help", color=0xff9129)
            embed.add_field(name="kick <user> <reason>",
                            value="Kicks a user from the server", inline=False)
            embed.add_field(name="ban <user> <reason>",
                            value="Bans a user from the server",
                            inline=False)
            embed.add_field(name="unban <user>",
                            value="Unbans a user from the server",
                            inline=False)
            embed.add_field(name="clear <amount>",
                            value="Clears <amount> of messages in the channel, <amount> can also be 'all' to clear all messages",
                            inline=False)
            embed.add_field(name="mute <user> <reason>",
                            value="Mutes a user in the server",
                            inline=False)
            embed.add_field(name="unmute <user> <reason>",
                            value="Unmutes a user in the server",
                            inline=False)
            embed.add_field(name="warn <user> <reason>",
                            value="Warns a user in the server for the specified reason",
                            inline=False)
            embed.add_field(name="infractions <user>",
                            value="Displays a user's infractions, if <user> is not specified then it displays the author's infractions",
                            inline=False)
            embed.set_footer(text=f"Page 1/{total_pages}")

            await help_message.edit(embed=embed)

            try:
                [reaction, user] = await self.client.wait_for('reaction_add', check=check, timeout=timeout)

                if str(reaction) == "\U000023ee\U0000fe0f":
                    await help_message.remove_reaction("\U000023ee\U0000fe0f", ctx.author)
                    await pageone(help_message, total_pages)

                if str(reaction) == "\U000025c0\U0000fe0f":
                    await help_message.remove_reaction("\U000025c0\U0000fe0f", ctx.author)
                    await pageone(help_message, total_pages)

                if str(reaction) == "\U000023f9\U0000fe0f":
                    await help_message.remove_reaction("\U000023f9\U0000fe0f", ctx.author)
                    await help_message.clear_reaction("\U000023ee\U0000fe0f")
                    await help_message.clear_reaction("\U000025c0\U0000fe0f")
                    await help_message.clear_reaction("\U000023f9\U0000fe0f")
                    await help_message.clear_reaction("\U000025b6\U0000fe0f")
                    await help_message.clear_reaction("\U000023ed\U0000fe0f")
                    await help_message.delete()
                    await ctx.message.delete()

                if str(reaction) == "\U000025b6\U0000fe0f":
                    await help_message.remove_reaction("\U000025b6\U0000fe0f", ctx.author)
                    await pagetwo(help_message, total_pages)

                if str(reaction) == "\U000023ed\U0000fe0f":
                    await help_message.remove_reaction("\U000023ed\U0000fe0f", ctx.author)
                    await pagefive(help_message, total_pages)

            except asyncio.TimeoutError:
                await help_message.clear_reaction("\U000023ee\U0000fe0f")
                await help_message.clear_reaction("\U000025c0\U0000fe0f")
                await help_message.clear_reaction("\U000023f9\U0000fe0f")
                await help_message.clear_reaction("\U000025b6\U0000fe0f")
                await help_message.clear_reaction("\U000023ed\U0000fe0f")
                return

        async def pagetwo(help_message, total_pages):
            embed2 = discord.Embed(title="Economy Help Page", color=0xff9129)
            embed2.add_field(name="balance <user>",
                             value="Displays the balance of <user>", inline=False)
            embed2.add_field(name="claim",
                             value="Claim some Vits once a day in each server that I am in",
                             inline=False)
            embed2.add_field(name="gamble <amount>",
                             value="Gamble your money for a chance to win double",
                             inline=False)
            embed2.add_field(name="casino <game> <amount>",
                             value="Gamble your money at the casino || Games: `slots`",
                             inline=False)
            embed2.set_footer(text=f"Page 2/{total_pages}")

            await help_message.edit(embed=embed2)

            try:
                [reaction, user] = await self.client.wait_for('reaction_add', check=check, timeout=timeout)

                if str(reaction) == "\U000023ee\U0000fe0f":
                    await help_message.remove_reaction("\U000023ee\U0000fe0f", ctx.author)
                    await pageone(help_message, total_pages)

                if str(reaction) == "\U000025c0\U0000fe0f":
                    await help_message.remove_reaction("\U000025c0\U0000fe0f", ctx.author)
                    await pageone(help_message, total_pages)

                if str(reaction) == "\U000023f9\U0000fe0f":
                    await help_message.remove_reaction("\U000023f9\U0000fe0f", ctx.author)
                    await help_message.clear_reaction("\U000023ee\U0000fe0f")
                    await help_message.clear_reaction("\U000025c0\U0000fe0f")
                    await help_message.clear_reaction("\U000023f9\U0000fe0f")
                    await help_message.clear_reaction("\U000025b6\U0000fe0f")
                    await help_message.clear_reaction("\U000023ed\U0000fe0f")
                    await help_message.delete()
                    await ctx.message.delete()

                if str(reaction) == "\U000025b6\U0000fe0f":
                    await help_message.remove_reaction("\U000025b6\U0000fe0f", ctx.author)
                    await pagethree(help_message, total_pages)

                if str(reaction) == "\U000023ed\U0000fe0f":
                    await help_message.remove_reaction("\U000023ed\U0000fe0f", ctx.author)
                    await pagefive(help_message, total_pages)

            except asyncio.TimeoutError:
                await help_message.clear_reaction("\U000023ee\U0000fe0f")
                await help_message.clear_reaction("\U000025c0\U0000fe0f")
                await help_message.clear_reaction("\U000023f9\U0000fe0f")
                await help_message.clear_reaction("\U000025b6\U0000fe0f")
                await help_message.clear_reaction("\U000023ed\U0000fe0f")
                return

        async def pagethree(help_message, total_pages):
            embed3 = discord.Embed(title="Fun Help Page", color=0xff9129)
            embed3.add_field(name="8ball <question>",
                             value="Gives your a random 8Ball response to your question", inline=False)
            embed3.add_field(name="roll",
                             value="Rolls a die",
                             inline=False)
            embed3.add_field(name="coinflip",
                             value="Flips a coin",
                             inline=False)
            embed3.add_field(name="echo <message>",
                             value="Repeats your message",
                             inline=False)
            embed3.add_field(name="wiki <search>",
                             value="Search Wikipedia using your search term",
                             inline=False)
            embed3.set_footer(text=f"Page 3/{total_pages}")

            await help_message.edit(embed=embed3)

            try:
                [reaction, user] = await self.client.wait_for('reaction_add', check=check, timeout=timeout)

                if str(reaction) == "\U000023ee\U0000fe0f":
                    await help_message.remove_reaction("\U000023ee\U0000fe0f", ctx.author)
                    await pageone(help_message, total_pages)

                if str(reaction) == "\U000025c0\U0000fe0f":
                    await help_message.remove_reaction("\U000025c0\U0000fe0f", ctx.author)
                    await pagetwo(help_message, total_pages)

                if str(reaction) == "\U000023f9\U0000fe0f":
                    await help_message.remove_reaction("\U000023f9\U0000fe0f", ctx.author)
                    await help_message.clear_reaction("\U000023ee\U0000fe0f")
                    await help_message.clear_reaction("\U000025c0\U0000fe0f")
                    await help_message.clear_reaction("\U000023f9\U0000fe0f")
                    await help_message.clear_reaction("\U000025b6\U0000fe0f")
                    await help_message.clear_reaction("\U000023ed\U0000fe0f")
                    await help_message.delete()
                    await ctx.message.delete()

                if str(reaction) == "\U000025b6\U0000fe0f":
                    await help_message.remove_reaction("\U000025b6\U0000fe0f", ctx.author)
                    await pagefour(help_message, total_pages)

                if str(reaction) == "\U000023ed\U0000fe0f":
                    await help_message.remove_reaction("\U000023ed\U0000fe0f", ctx.author)
                    await pagefive(help_message, total_pages)

            except asyncio.TimeoutError:
                await help_message.clear_reaction("\U000023ee\U0000fe0f")
                await help_message.clear_reaction("\U000025c0\U0000fe0f")
                await help_message.clear_reaction("\U000023f9\U0000fe0f")
                await help_message.clear_reaction("\U000025b6\U0000fe0f")
                await help_message.clear_reaction("\U000023ed\U0000fe0f")
                return

        async def pagefour(help_message, total_pages):
            embed3 = discord.Embed(title="Miscellaneous Help Page", color=0xff9129)
            embed3.add_field(name="info <user>",
                             value="Returns information on a user",
                             inline=False)
            embed3.add_field(name="serverstats",
                             value="Gives the statistics of the server",
                             inline=False)
            embed3.add_field(name="botstats",
                             value="Returns my statistics",
                             inline=False)
            embed3.add_field(name="invite",
                             value="Returns the invite link to invite me to your server",
                             inline=False)
            embed3.add_field(name="support",
                             value="Returns the invite link to my support server",
                             inline=False)
            embed3.set_footer(text=f"Page 4/{total_pages}")

            await help_message.edit(embed=embed3)

            try:
                [reaction, user] = await self.client.wait_for('reaction_add', check=check, timeout=timeout)

                if str(reaction) == "\U000023ee\U0000fe0f":
                    await help_message.remove_reaction("\U000023ee\U0000fe0f", ctx.author)
                    await pageone(help_message, total_pages)

                if str(reaction) == "\U000025c0\U0000fe0f":
                    await help_message.remove_reaction("\U000025c0\U0000fe0f", ctx.author)
                    await pagethree(help_message, total_pages)

                if str(reaction) == "\U000023f9\U0000fe0f":
                    await help_message.remove_reaction("\U000023f9\U0000fe0f", ctx.author)
                    await help_message.clear_reaction("\U000023ee\U0000fe0f")
                    await help_message.clear_reaction("\U000025c0\U0000fe0f")
                    await help_message.clear_reaction("\U000023f9\U0000fe0f")
                    await help_message.clear_reaction("\U000025b6\U0000fe0f")
                    await help_message.clear_reaction("\U000023ed\U0000fe0f")
                    await help_message.delete()
                    await ctx.message.delete()

                if str(reaction) == "\U000025b6\U0000fe0f":
                    await help_message.remove_reaction("\U000025b6\U0000fe0f", ctx.author)
                    await pagefive(help_message, total_pages)

                if str(reaction) == "\U000023ed\U0000fe0f":
                    await help_message.remove_reaction("\U000023ed\U0000fe0f", ctx.author)
                    await pagefive(help_message, total_pages)

            except asyncio.TimeoutError:
                await help_message.clear_reaction("\U000023ee\U0000fe0f")
                await help_message.clear_reaction("\U000025c0\U0000fe0f")
                await help_message.clear_reaction("\U000023f9\U0000fe0f")
                await help_message.clear_reaction("\U000025b6\U0000fe0f")
                await help_message.clear_reaction("\U000023ed\U0000fe0f")
                return

        async def pagefive(help_message, total_pages):
            embed3 = discord.Embed(title="Admin Help Page", color=0xff9129)
            embed3.add_field(name="setupwelcome",
                             value="Begins the process to setup welcome messages.", inline=False)
            embed3.add_field(name="setupwelcomedm",
                             value="Begins the process to setup DM welcome messages", inline=False)
            embed3.add_field(name="setupwelcomerole <role>",
                             value="Automatically assigns the role when a user joins the server.", inline=False)
            embed3.add_field(name="removewelcome [message | dm | role]",
                             value="Removes the welcome message, dm, or role depending on what you choose.", inline=False)
            embed3.add_field(name="setupleave",
                             value="Begins the process to setup leave messages.", inline=False)
            embed3.add_field(name="poll",
                             value="Begins the process to start a server poll.", inline=False)
            embed3.set_footer(text=f"Page 5/{total_pages}")

            await help_message.edit(embed=embed3)

            try:
                [reaction, user] = await self.client.wait_for('reaction_add', check=check, timeout=timeout)

                if str(reaction) == "\U000023ee\U0000fe0f":
                    await help_message.remove_reaction("\U000023ee\U0000fe0f", ctx.author)
                    await pageone(help_message, total_pages)

                if str(reaction) == "\U000025c0\U0000fe0f":
                    await help_message.remove_reaction("\U000025c0\U0000fe0f", ctx.author)
                    await pagefour(help_message, total_pages)

                if str(reaction) == "\U000023f9\U0000fe0f":
                    await help_message.remove_reaction("\U000023f9\U0000fe0f", ctx.author)
                    await help_message.clear_reaction("\U000023ee\U0000fe0f")
                    await help_message.clear_reaction("\U000025c0\U0000fe0f")
                    await help_message.clear_reaction("\U000023f9\U0000fe0f")
                    await help_message.clear_reaction("\U000025b6\U0000fe0f")
                    await help_message.clear_reaction("\U000023ed\U0000fe0f")
                    await help_message.delete()
                    await ctx.message.delete()

                if str(reaction) == "\U000025b6\U0000fe0f":
                    await help_message.remove_reaction("\U000025b6\U0000fe0f", ctx.author)
                    await pagefive(help_message, total_pages)

                if str(reaction) == "\U000023ed\U0000fe0f":
                    await help_message.remove_reaction("\U000023ed\U0000fe0f", ctx.author)
                    await pagefive(help_message, total_pages)

            except asyncio.TimeoutError:
                await help_message.clear_reaction("\U000023ee\U0000fe0f")
                await help_message.clear_reaction("\U000025c0\U0000fe0f")
                await help_message.clear_reaction("\U000023f9\U0000fe0f")
                await help_message.clear_reaction("\U000025b6\U0000fe0f")
                await help_message.clear_reaction("\U000023ed\U0000fe0f")
                return

        # Initial Help Code

        embed = discord.Embed(title="Moderation Help", color=0xff9129)
        embed.add_field(name="kick <user> <reason>",
                        value="Kicks a user from the server", inline=False)
        embed.add_field(name="ban <user> <reason>",
                        value="Bans a user from the server",
                        inline=False)
        embed.add_field(name="unban <user>",
                        value="Unbans a user from the server",
                        inline=False)
        embed.add_field(name="clear <amount>",
                        value="Clears <amount> of messages in the channel, <amount> can also be 'all' to clear all messages",
                        inline=False)
        embed.add_field(name="mute <user> <reason>",
                        value="Mutes a user in the server",
                        inline=False)
        embed.add_field(name="Unmute <user> <reason>",
                        value="Unmutes a user in the server",
                        inline=False)
        embed.add_field(name="Warn <user> <reason>",
                        value="Warns a user in the server for the specified reason",
                        inline=False)
        embed.add_field(name="Infractions <user>",
                        value="Displays a user's infractions, if <user> is not specified then it displays the author's infractions",
                        inline=False)
        embed.set_footer(text=f"Page 1/{total_pages}")

        help_message = await ctx.send(embed=embed)

        await help_message.add_reaction("\U000023ee\U0000fe0f")
        await help_message.add_reaction("\U000025c0\U0000fe0f")
        await help_message.add_reaction("\U000023f9\U0000fe0f")
        await help_message.add_reaction("\U000025b6\U0000fe0f")
        await help_message.add_reaction("\U000023ed\U0000fe0f")

        def check(reaction, user):
            return user == ctx.author

        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=timeout)

            if str(reaction) == "\U000023ee\U0000fe0f":
                await help_message.remove_reaction("\U000023ee\U0000fe0f", ctx.author)
                await pageone(help_message, total_pages)

            if str(reaction) == "\U000025c0\U0000fe0f":
                await help_message.remove_reaction("\U000025c0\U0000fe0f", ctx.author)
                await pageone(help_message, total_pages)

            if str(reaction) == "\U000023f9\U0000fe0f":
                await help_message.remove_reaction("\U000023f9\U0000fe0f", ctx.author)
                await help_message.clear_reaction("\U000023ee\U0000fe0f")
                await help_message.clear_reaction("\U000025c0\U0000fe0f")
                await help_message.clear_reaction("\U000023f9\U0000fe0f")
                await help_message.clear_reaction("\U000025b6\U0000fe0f")
                await help_message.clear_reaction("\U000023ed\U0000fe0f")
                await help_message.delete()
                await ctx.message.delete()

            if str(reaction) == "\U000025b6\U0000fe0f":
                await help_message.remove_reaction("\U000025b6\U0000fe0f", ctx.author)
                await pagetwo(help_message, total_pages)

            if str(reaction) == "\U000023ed\U0000fe0f":
                await help_message.remove_reaction("\U000023ed\U0000fe0f", ctx.author)
                await pagefive(help_message, total_pages)

        except asyncio.TimeoutError:
            await help_message.clear_reaction("\U000023ee\U0000fe0f")
            await help_message.clear_reaction("\U000025c0\U0000fe0f")
            await help_message.clear_reaction("\U000023f9\U0000fe0f")
            await help_message.clear_reaction("\U000025b6\U0000fe0f")
            await help_message.clear_reaction("\U000023ed\U0000fe0f")
            return

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, discord.errors.Forbidden) or isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
            ctx.handled_in_local = True
            embed = discord.Embed(title="Help Command", description="It seems that I do not have permissions to display the detailed help command, so here is my backup", color=0xff9129)
            mod_cmds = ["kick", "ban", "unban", "clear", "mute", "unmute", "warn", "infractions"]
            economy_cmds = ["balance", "claim", "gamble", "casino"]
            fun_cmds = ["8ball", "roll", "coinflip", "echo", "wiki"]
            misc_cmds = ["info", "serverstats", "botstats", "invite", "support"]
            admin_cmds = ["setupwelcome", "setupwelcomedm", "setupwelcomerole", "removewelcome", "setupleave", "poll"]
            description = ""
            for command in mod_cmds:
                description += f"`{command}` "
            embed.add_field(name="Moderation", value=description)

            description = ""
            for command in economy_cmds:
                description += f"`{command}` "
            embed.add_field(name="Economy", value=description)

            description = ""
            for command in fun_cmds:
                description += f"`{command}` "
            embed.add_field(name="Fun", value=description)

            description = ""
            for command in misc_cmds:
                description += f"`{command}` "
            embed.add_field(name="Miscellaneous", value=description)

            description = ""
            for command in admin_cmds:
                description += f"`{command}` "
            embed.add_field(name="Admin", value=description)

            await ctx.send(embed=embed)




def setup(client):
    client.add_cog(Help(client))