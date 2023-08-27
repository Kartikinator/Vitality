import discord
from discord.ext import commands
import os
import datetime
import asyncio
import datetime

async def send_dm(moderator, member, action_type, reason, color):
    embed = discord.Embed(title=moderator.guild.name, description=f"You have been {action_type}ed", timestamp=datetime.datetime.utcnow(), color=color)
    embed.add_field(name="Moderator", value=f"{moderator.name}#{moderator.discriminator}", inline=False)
    embed.add_field(name="Reason", value=reason)

    await member.send(embed=embed)


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def check_server_rec(self, ctx):

        self.client.cursor.execute(f"SELECT * FROM servers WHERE server_id = {ctx.guild.id}")

        results = self.client.cursor.fetchall()

        if len(results) == 0:
            self.client.cursor.execute(f"INSERT INTO `{self.client.dbname}`.`servers` (`server_id`) VALUES ('{ctx.guild.id}');")
            self.client.mydb.commit()

    async def log(self, moderator, member, action_type, reason, infraction_text):
        guild = member.guild

        time = datetime.datetime.utcnow()

        if action_type == "Infraction Clear":

            # -- Database Log --

            if reason is not None:

                self.client.cursor.execute(f"INSERT INTO `{self.client.dbname}`.`infractions` (`action_date`, `server_id`, `moderator_id`, `action_type`, `reason`) VALUES ('{time}','{member.guild.id}', {moderator.id}', '{action_type}', '{reason}');")

            else:

                self.client.cursor.execute(f"INSERT INTO `{self.client.dbname}`.`infractions` (`action_date`, `server_id`, `moderator_id`, `action_type`) VALUES ('{time}','{member.guild.id}', '{moderator.id}', '{action_type}');")

            self.client.mydb.commit()

            # -- Channel Log --

            self.client.cursor.execute(f"SELECT log_channel_id FROM servers WHERE server_id = '{member.guild.id}';")

            channel_ID = self.client.cursor.fetchall()[0][0]

            self.client.cursor.execute(f"SELECT action_id FROM infractions WHERE action_date = '{time}' AND server_id = '{member.guild.id}' AND moderator_id = '{moderator.id}' AND action_type = '{action_type}';")

            action_id = self.client.cursor.fetchall()[-1][0]


            if channel_ID is not None:

                embed = discord.Embed(title=f"{infraction_text}", timestamp=datetime.datetime.utcnow())

                embed.add_field(name="Moderator", value=f"{moderator.name}#{moderator.discriminator}", inline=False)

                embed.add_field(name="Reason", value=reason)

                embed.set_footer(text=f"Action ID: {action_id}")

                embed.set_thumbnail(url=member.avatar_url)

                channel = guild.get_channel(int(channel_ID))

                await channel.send(embed=embed)

        else:

            # -- Database Log --

            if reason is not None:

                self.client.cursor.execute(f"INSERT INTO `{self.client.dbname}`.`infractions` (`action_date`, `server_id`, `offender_id`, `moderator_id`, `action_type`, `reason`) VALUES ('{time}', '{member.guild.id}', '{member.id}', '{moderator.id}', '{action_type}', '{reason}');")

            else:

                self.client.cursor.execute(f"INSERT INTO `{self.client.dbname}`.`infractions` (`action_date`, `server_id`, `offender_id`, `moderator_id`, `action_type`) VALUES ('{time}' ,'{member.guild.id}', '{member.id}', '{moderator.id}', '{action_type}');")

            self.client.mydb.commit()

            # -- Channel Log --

            self.client.cursor.execute(f"SELECT log_channel_id FROM servers WHERE server_id = '{member.guild.id}';")

            channel_ID = self.client.cursor.fetchall()[0][0]

            self.client.cursor.execute(f"SELECT action_id FROM infractions WHERE server_id = '{member.guild.id}' AND offender_id = '{member.id}' AND moderator_id = '{moderator.id}' AND action_type = '{action_type}';")

            action_id = self.client.cursor.fetchall()[-1][0]

            if channel_ID is not None:

                embed = discord.Embed(title=f"{infraction_text}ed {member.name}#{member.discriminator} - {member.id}", timestamp=datetime.datetime.utcnow())

                embed.add_field(name="Moderator", value=f"{moderator.name}#{moderator.discriminator}", inline=False)

                embed.add_field(name="Reason", value=reason)

                embed.set_footer(text=f"Action ID: {action_id}")

                embed.set_thumbnail(url=member.avatar_url)

                channel = guild.get_channel(int(channel_ID))

                await channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, amount='5'):
        await self.check_server_rec(ctx)

        if amount == "all":
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=int(amount))


        # Special Log ---- Clear Cmd Only
        # This log is in place because no members are referenced

        self.client.cursor.execute(f"SELECT log_channel_id FROM servers WHERE server_id = '{member.guild.id}';")

        channel_ID = self.client.cursor.fetchall()[0][0]

        if channel_ID is not None:

            embed = discord.Embed(title=f"Cleared {amount} messages", timestamp=datetime.datetime.utcnow())

            embed.add_field(name="Moderator", value=f"{moderator.name}#{moderator.discriminator}", inline=False)

            embed.add_field(name="Channel", value=f"<#{ctx.channel.id}>")

            embed.set_thumbnail(url=member.avatar_url)

            channel = guild.get_channel(int(channel_ID))

            await channel.send(embed=embed)


    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed = discord.Embed(title="You must have the `manage_messages` permission to run this command.", color=0xFFFF00)
            await ctx.send(embed=embed)

        if isinstance(error, discord.errors.Forbidden):
            embed = discord.Embed(title="I don't have the necessary permissions for this command.", description='This commands requires me to have the `manage messages` permission',
                                  color=0xFFFF00)
            await ctx.send(embed=embed)

        if isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
            embed = discord.Embed(title="I don't have the necessary permissions for this command.",
                                  description='This commands requires me to have the `manage messages` permission',
                                  color=0xFFFF00)
            await ctx.send(embed=embed)

    # Kick Command -------------------

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            await ctx.send("Specify a member to kick")
            return
        await member.kick(reason=reason)
        embed = discord.Embed(title=f"Kicked {member} from the server", color=0xFFFF00)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

        await self.log(ctx.author, member, "Kick", reason, "Kick")
        await send_dm(ctx.author, member, "kick", reason, self.client.red)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed = discord.Embed(title="You must have the `kick_members` permission to run this command.", color=0xFFFF00)
            await ctx.send(embed=embed)


    # Ban Command -------------------

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            await ctx.send("Specify a member to ban")
            return

        try:
            await member.ban(reason=reason)
        except:
            return await ctx.send("Failed to ban user, move my highest role above this user.")
        embed = discord.Embed(title=f"Banned {member} from the server", color=0xCC0000)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

        await log(ctx.author, member, "Ban", reason, "Bann")
        await send_dm(ctx.author, member, "ban", reason, self.client.red)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed = discord.Embed(title="You must have the `ban_members` permission to run this command.", color=0xFFFF00)
            await ctx.send(embed=embed)

    # Unban Command ---------------------

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member=None):
        if member is None:
            await ctx.send("Specify a member to unban")
            return
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(title=f"Unbanned {user.name}#{user.discriminator} from the server",
                                      color=0x38761D)
                await ctx.send(embed=embed)
                await log(ctx.author, member, "Unban", reason, "Unbann")
                break
        else:
            await ctx.send(f"**{user.name}#{user.discriminator}** is not banned from this server.")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed = discord.Embed(title="You must have the `ban_members` permission to run this command.", color=0xFFFF00)
            await ctx.send(embed=embed)

    # Mute Command ---------

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def roles(self, ctx):
        await ctx.send(ctx.guild.me.roles[len(ctx.guild.me.roles) - 1].position)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            await ctx.send("Specify a member to mute")
            return

        guild = member.guild

        self.client.cursor.execute(f"SELECT mute_role_id FROM servers WHERE server_id = '{ctx.guild.id}';")
        role_id = self.client.cursor.fetchall()[0][0]

        if role_id is None:
            role_create = await guild.create_role(name="Muted")

            await role_create.edit(position=ctx.guild.me.roles[len(ctx.guild.me.roles) - 1].position - 1)

            self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`servers` SET `mute_role_id` = '{role_create.id}' WHERE (`server_id` = '{ctx.guild.id}');")

            role_id = role_create.id

            await ctx.send(f"This is the first time you are using the mute command. Please wait while I setup the necessary permissions to activate this command. This process will take approximately **{len(ctx.guild.channels)}** seconds")

            for channel in ctx.guild.channels:
                await channel.set_permissions(role_create, send_messages=False)
                await asyncio.sleep(1)


        role = guild.get_role(int(role_id))

        await member.add_roles(role, atomic=True)

        embed = discord.Embed(title=f"Muted {member}", color=0xCC0000)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

        await self.log(ctx.author, member, "Mute", reason, "Mut")
        await send_dm(ctx.author, member, "mut", reason, self.client.red)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed = discord.Embed(title="You must have the `manage_messages` permission to run this command.", color=0xFFFF00)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            embed = discord.Embed(title="The user you are trying to mute has a role higher than mine or I am missing "
                                        "the `manage roles` permission", color=0xFFFF00)
            await ctx.send(embed=embed)
        else:
            print(error)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            return await ctx.send("Specify a member to unmute")

        guild = ctx.author.guild

        self.client.cursor.execute(f"SELECT mute_role_id FROM servers WHERE server_id = '{ctx.guild.id}';")
        role_id = self.client.cursor.fetchall()[0][0]

        if role_id is not None:

            for role in member.roles:

                if role.id == int(role_id):

                    role = guild.get_role(int(role_id))

                    break
            else:

                return await ctx.send("This user is not muted.")

        await member.remove_roles(role)
        embed = discord.Embed(title=f"Unmuted {member}", color=0xFFFF00)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

        await self.log(ctx.author, member, "Unmute", reason, "Unmut")
        await send_dm(ctx.author, member, "unmut", reason, self.client.green)

    # @unmute.error
    # async def unmute_error(self, ctx, error):
    #     if isinstance(error, discord.ext.commands.errors.MissingPermissions):
    #         embed = discord.Embed(title="You do not have the permissions to run this command", color=0xFFFF00)
    #         await ctx.send(embed=embed)
    #     elif isinstance(error, discord.errors.Forbidden):
    #         embed = discord.Embed(title="The user you are trying to mute has a role higher than mine or I am missing the `manage roles` permission", color=0xFFFF00)
    #         await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            return await ctx.send("Specify a member to warn")

        embed = discord.Embed(title=f"{member} has been warned", color=0xFFFF00)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

        await self.log(ctx.author, member, "Warn", reason, 'Warn')
        await send_dm(ctx.author, member, "warn", reason, self.client.yellow)

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed = discord.Embed(title="You must have the `manage_messages` permission to run this command.",
                                  color=0xFFFF00)
            await ctx.send(embed=embed)

    @commands.command()
    async def infractions(self, ctx, member: discord.Member = None):
        if member is None:
            sender = ctx.author
        else:
            sender = member

        self.client.cursor.execute(f"SELECT * FROM infractions WHERE offender_id = '{sender.id}' AND cleared is null;")
        results = self.client.cursor.fetchall()


        embed = discord.Embed(title=f"{sender.name}'s infractions", color=0xFFFF00, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Last 5 Infractions • {len(results)} Total ")
        embed.set_thumbnail(url=sender.avatar_url)

        if len(results) == 0:
            embed.add_field(name="Infractions", value="User has no infractions", inline=False)
            return await ctx.send(embed=embed)

        guild = ctx.author.guild
        description = ""
        i = 0


        for infraction in results:
            if i == 5:
                break
            server = self.client.get_guild(int(results[i][2]))
            description += f"**{results[i][0]}. {results[i][5]}** · {server.name} \n" # action_id. action_type. reason
            i += 1

        embed.description = description

        await ctx.send(embed=embed)

    # TO BE UPDATED ----------

    @commands.command(aliases=["clearinfractions", "ci", "removeinfraction"])
    @commands.has_permissions(manage_messages=True)
    async def clearinfraction(self, ctx, member: discord.Member = None, action_id=None, *, reason=None):
        if member is None or action_id is None:
            await ctx.send("The proper usage of this command is `clearinfraction <user> [infraction id | all] <reason>`")

        time = datetime.datetime.utcnow()

        if action_id == "all":

            self.client.cursor.execute(f"SELECT * FROM infractions WHERE offender_id = '{member.id}' AND server_id = '{ctx.guild.id}' AND cleared is null;")
            results = self.client.cursor.fetchall()
            print(results)

            for record in results:
                self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`infractions` SET `cleared` = 'Yes', `cleared_date` = '{time}' WHERE `action_id` = '{record[0]}';")
                self.client.mydb.commit()

            await ctx.send(f"All of {member.name}'s infractions have been cleared for this server.")

            # Logging Channel
            self.client.cursor.execute(f"SELECT log_channel_id FROM servers WHERE server_id = '{ctx.guild.id}';")
            channel_id = self.client.cursor.fetchall()[0][0]
            if channel_id is None:
                return

            channel = ctx.guild.get_channel(int(channel_id))


            embed = discord.Embed(title=f"Cleared all of {member.name}#{member.discriminator} infractions",
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Moderator", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=False)
            embed.add_field(name="Reason", value=reason)
            embed.set_footer(text=f"ID: {member.id}")
            embed.set_thumbnail(url=member.avatar_url)
            await channel.send(embed=embed)

            await self.log(ctx.author, member, "Infraction Clear", reason, "Infractions Cleared")

        else:

            self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`infractions` SET `cleared` = 'Yes', `cleared_date` = '{time}' WHERE `action_id` = '{action_id}';")
            self.client.mydb.commit()
            
            await ctx.send("This infraction has been deleted.")

            # Logging Channel
            self.client.cursor.execute(f"SELECT log_channel_id FROM servers WHERE server_id = '{ctx.guild.id}';")
            channel_id = self.client.cursor.fetchall()[0][0]
            if channel_id is None:
                return

            embed = discord.Embed(
                title=f"Cleared one of {member.name}#{member.discriminator} infractions",
                timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Moderator", value=f"{ctx.author.name}#{ctx.author.discriminator}",
                            inline=False)
            embed.add_field(name="Infraction ID", value=action_id)
            embed.set_footer(text=f"ID: {member.id}")
            embed.set_thumbnail(url=member.avatar_url)
            channel = ctx.guild.get_channel(int(channel_id))
            await channel.send(embed=embed)

    @commands.command(aliases=["vmute"])
    @commands.has_permissions(manage_messages=True)
    async def voicemute(self, ctx, member=None, *, reason=None):
        if member is None:
            await ctx.send("Specify a member to mute")
            return

        mute_num = 0

        if member == "all":
            channel = ctx.message.author.voice.channel
            for member in channel.members:
                if member.permissions_in(ctx.channel).administrator is False:
                    await member.edit(mute=True)
                    mute_num += 1

            await ctx.send(f"**Everyone** has been voice muted in `{channel.name}` (`{mute_num}` users)")
        else:
            try:
                member = ctx.guild.get_member(member.id)
            except:
                return await ctx.send("Please specify a valid user.")

            await member.edit(mute=True)

            await ctx.send(f"**{member.name}#{member.discriminator}** has been voice muted.")

        await log(ctx.author, member, "Voice Mut", reason)

    @voicemute.error
    async def voice_mute_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed = discord.Embed(title="You must have the `manage_messages` permission to run this command.",
                                  color=0xFFFF00)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            embed = discord.Embed(title="The user you are trying to mute has a role higher than mine or I am missing "
                                        "the `manage roles` permission", color=0xFFFF00)
            await ctx.send(embed=embed)
        else:
            print(error)

    @commands.command(aliases=["vunmute"])
    @commands.has_permissions(manage_messages=True)
    async def voicunemute(self, ctx, member=None, *, reason=None):
        if member is None:
            await ctx.send("Specify a member to unmute")
            return

        if member == "all":
            channel = ctx.message.author.voice.channel
            mute_num = 0
            for member in channel.members:
                if member.permissions_in(ctx.channel).administrator is False:
                    await member.edit(mute=False)
                    mute_num += 1

            await ctx.send(f"**Everyone** has been voice unmuted in `{channel.name}` (`{mute_num}` users)")
        else:
            try:
                member = ctx.guild.get_member(member.id)
            except:
                return await ctx.send("Please specify a valid user.")

            await member.edit(mute=False)

            await ctx.send(f"**{member.name}#{member.discriminator}** has been voice unmuted.")

        await log(ctx.author, member, "Voice Unmut", reason)

    @voicunemute.error
    async def voice_unmute_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed = discord.Embed(title="You must have the `manage_messages` permission to run this command.",
                                  color=0xFFFF00)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            embed = discord.Embed(title="The user you are trying to mute has a role higher than mine or I am missing "
                                        "the `manage roles` permission", color=0xFFFF00)
            await ctx.send(embed=embed)
        else:
            print(error)

def setup(client):
    client.add_cog(Moderation(client))
