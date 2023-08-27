import discord
from discord.ext import commands
import random
import asyncio
import os
import json

class ServerAdmin(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def check_server_rec(self, ctx):

        self.client.cursor.execute(f"SELECT * FROM servers WHERE server_id = {ctx.guild.id}")

        results = self.client.cursor.fetchall()

        if len(results) == 0:
            self.client.cursor.execute(f"INSERT INTO `{self.client.dbname}`.`servers` (`server_id`) VALUES ('{ctx.guild.id}');")
            self.client.mydb.commit()

        


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setupwelcome(self, ctx):
        await self.check_server_rec(ctx)

        guild = ctx.guild

        def check(message):
            return message.author == ctx.author

        try:
            msg = await ctx.send("Write the welcome message that you would like to use. Type `{}` where the member's "
                                 "name should go. Type `CANCEL` to cancel. This request times out in 3 minutes.")
            welcome_msg = await self.client.wait_for('message', check=check, timeout=300)
            if welcome_msg.content == "CANCEL":
                return await ctx.send("The setup process has been cancelled")

            if "{}" not in welcome_msg.content:
                return await ctx.send("At least one instance of `{}` is required in your message. The setup process "
                                      "has been cancelled")

        except asyncio.TimeoutError:
            return await msg.edit(content="**This message timed out**")

        try:
            msg = await ctx.send("Now, tag the channel that you would like to send the message to. Type `CANCEL` to "
                                 "cancel. This request times out in 60 seconds.")
            channel_id = await self.client.wait_for('message', check=check, timeout=60)
            if channel_id.content == "CANCEL":
                return await ctx.send("The setup process has been cancelled")

            if guild.get_channel(int(channel_id.content[2:-1])) is None:
                return await ctx.send("Invalid channel. The setup process has been cancelled")
        except asyncio.TimeoutError:
            return await msg.edit(content="**This message timed out**")


        self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`servers` SET `welcome_channel_id` = '{channel_id.content[2:-1]}' WHERE (`server_id` = '{ctx.guild.id}');")
        self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`servers` SET `welcome_msg` = '{welcome_msg.content}' WHERE (`server_id` = '{ctx.guild.id}');")
        self.client.mydb.commit()

        await ctx.send(f"Your welcome message has been successfully setup.")

    @setupwelcome.error
    async def welcome_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            return await ctx.send("You need the `administrator` permission to use this command.")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setupwelcomerole(self, ctx, role: discord.Role = None):
        await self.check_server_rec(ctx)

        if role is None:
            await ctx.send("Please tag the role that I should assign. `setupwelcomerole <@MENTIONROLENAME>`")

        guild = ctx.guild

        self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`servers` SET `welcome_role_id` = '{role.id}' WHERE (`server_id` = '{ctx.guild.id}');")
        self.client.mydb.commit()

        await ctx.send(f"Your welcome role has been successfully setup. Please make sure that my role is higher than "
                       f"the role you are trying to assign.")

    @setupwelcomerole.error
    async def welcomerole_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            return await ctx.send("You need the `administrator` permission to use this command.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setupwelcomedm(self, ctx):
        await self.check_server_rec(ctx)

        guild = ctx.guild

        def check(message):
            return message.author == ctx.author

        try:
            msg = await ctx.send(
                "Write the message that I should DM the user when they join. Type `CANCEL` to cancel. This request "
                "times out in 5 minutes.")
            welcome_msg = await self.client.wait_for('message', check=check, timeout=300)
            if welcome_msg.content == "CANCEL":
                return await ctx.send("The setup process has been cancelled")

        except asyncio.TimeoutError:
            return await msg.edit(content="**This message timed out**")

        self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`servers` SET `welcome_dm_msg` = '{welcome_msg.content}' WHERE (`server_id` = '{ctx.guild.id}');")
        self.client.mydb.commit()

        await ctx.send(f"Your welcome DM has been successfully setup.")

    @setupwelcomedm.error
    async def welcomedm_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            return await ctx.send("You need the `administrator` permission to use this command.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removewelcome(self, ctx, type=None):
        await self.check_server_rec(ctx)

        if type is None:
            return await ctx.send("Please specify what to remove. Proper command usage `removewelcome [message | dm | "
                                  "role]`")

        options = ["message", "dm", "role"]

        if type.lower() not in options:
            return await ctx.send("Please specify a valid argument. Proper command usage `removewelcome [message | dm "
                                  "| role]`")
        guild = ctx.guild

        if type.lower() == "message":
            
            self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`servers` SET `welcome_msg` = null WHERE (`server_id` = '{ctx.guild.id}');")
            self.client.mydb.commit()

            await ctx.send("The welcome message for this server has been removed")

        elif type.lower() == "dm":

            self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`servers` SET `welcome_dm_msg` = null WHERE (`server_id` = '{ctx.guild.id}');")
            self.client.mydb.commit()

            await ctx.send("The welcome DM for this server has been removed")

        elif type.lower() == "role":

            self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`servers` SET `welcome_role_id` = null WHERE (`server_id` = '{ctx.guild.id}');")
            self.client.mydb.commit()

            await ctx.send("The welcome role for this server has been removed")

    @removewelcome.error
    async def rmwelcome_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            return await ctx.send("You need the `administrator` permission to use this command.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setupleave(self, ctx):
        await self.check_server_rec(ctx)

        guild = ctx.guild

        def check(message):
            return message.author == ctx.author

        try:
            msg = await ctx.send("Write the leave message that you would like to use. Type `{}` where the member's "
                                 "name should go. Type `CANCEL` to cancel. This request times out in 3 minutes.")
            leave_msg = await self.client.wait_for('message', check=check, timeout=300)
            if leave_msg.content == "CANCEL":
                return await ctx.send("The setup process has been cancelled")

            if "{}" not in leave_msg.content:
                return await ctx.send("At least one instance of `{}` is required in your message. The setup process "
                                      "has been cancelled")

        except asyncio.TimeoutError:
            return await msg.edit(content="**This message timed out**")

        try:
            msg = await ctx.send("Now, tag the channel that you would like to send the message to. Type `CANCEL` to "
                                 "cancel. This request times out in 60 seconds.")
            channel_id = await self.client.wait_for('message', check=check, timeout=60)
            if channel_id.content == "CANCEL":
                return await ctx.send("The setup process has been cancelled")

            if guild.get_channel(int(channel_id.content[2:-1])) is None:
                return await ctx.send("Invalid channel. The setup process has been cancelled")
        except asyncio.TimeoutError:
            return await msg.edit(content="**This message timed out**")

        self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`servers` SET `leave_channel_id` = '{channel_id.content[2:-1]}' WHERE (`server_id` = '{ctx.guild.id}');")
        self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`servers` SET `welcome_msg` = '{leave_msg.content}' WHERE (`server_id` = '{ctx.guild.id}');")
        self.client.mydb.commit()

        await ctx.send(f"Your leave message has been successfully setup.")

    @setupleave.error
    async def sl_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            return await ctx.send("You need the `administrator` permission to use this command.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removeleave(self, ctx):

        await self.check_server_rec(ctx)

        self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`servers` SET `leave_msg` = null WHERE (`server_id` = '{ctx.guild.id}');")
        self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`servers` SET `leave_channel_id` = null WHERE (`server_id` = '{ctx.guild.id}');")
        self.client.mydb.commit()
        
        await ctx.send("The leave message for this server has been removed")

    @removeleave.error
    async def rl_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            return await ctx.send("You need the `administrator` permission to use this command.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setuplogging(self, ctx, channel: discord.TextChannel=None):
        if channel is None:
            return await ctx.send("Please tag a channel to start logging in")

        await self.check_server_rec(ctx)

        self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`servers` SET `log_channel_id` = '{channel.id}' WHERE (`server_id` = '{ctx.guild.id}');")
        self.client.mydb.commit()

        await ctx.send(f"Your logging channel has been successfully set to <#{channel.id}>")

    @setuplogging.error
    async def setuplogging_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            return await ctx.send("You need the `administrator` permission to use this command.")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def testcmd(self, ctx):
        self.client.cursor.execute(f"SELECT welcome_channel_id FROM servers WHERE server_id = '{ctx.guild.id}';")

        print(self.client.cursor.fetchall()[0][0])




def setup(client):
    client.add_cog(ServerAdmin(client))
