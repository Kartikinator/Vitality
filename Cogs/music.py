import discord
from discord.ext import commands
import youtube_dl as yt
from discord.utils import get
import os
import asyncio
import subprocess
import requests
import shutil


class music(commands.Cog):

    def __init__(self, client):
        client.queues = {}
        self.client = client

    async def check_role(self, member):
        for role in member.roles:
            if role.name in ["Creator", "Moderator" "Admin?"]:
                return True
        else:
            return False


    async def download(self, ctx, song, name):
        def select_skip(iterable, select, skip):
            return [x for i, x in enumerate(iterable) if i % (select + skip) < select]

        search = subprocess.check_output(f'youtube-dl -e --get-title -g --get-url "ytsearch5:{song}"')

        results = search.decode(encoding='cp1252').split("\n")

        description = ""
        i = 0

        for song in range(len(select_skip(results, 1, 2)) - 1):
            i += 1
            description += f"**{i}.** {select_skip(results, 1, 2)[i - 1]} \n"

        embed = discord.Embed(description=description)
        await ctx.send(embed=embed)

        def check(message):
            return message.author == ctx.author

        try:
            msg = await ctx.send("Select a song from 1-5")
            user_option = await self.client.wait_for('message', check=check, timeout=60)
            if user_option.content == "CANCEL":
                return await ctx.send("The setup process has been cancelled")
            message = await ctx.send(f"Getting `{select_skip(results, 1, 2)[int(user_option.content) - 1]}`")

        except asyncio.TimeoutError:
            return await msg.edit(content="**This message timed out**")

        r = requests.get(results[(int(user_option.content) * 2) + (int(user_option.content) - 1)], allow_redirects=True)
        open(f'{name}.mp3', 'wb').write(r.content)
        await message.edit(content=f"Got `{select_skip(results, 1, 2)[int(user_option.content) - 1]}`")

    # Voice Commands

    @commands.command(aliases=["j", "joi"])
    async def join(self, ctx):
        print("Work?")
        # if ctx.guild.id != 722187348246397010:
        #     return

        # if await self.check_role(ctx.author) is False:
        #     return

        global voice
        print("Begining of function")

        if ctx.message.author.voice is None:

            await ctx.send("You are not connected to a voice channel")

        else:
            print("Else")
            channel = ctx.message.author.voice.channel
            voice = get(self.client.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()

            await ctx.send(f"Joined `{channel}` Voice Room")

    @commands.command(aliases=["leave", "disc", "d", "l"])
    async def disconnect(self, ctx):
        # if ctx.guild.id != 722187348246397010:
        #     return

        if await self.check_role(ctx.author) is False:
            return
        global voice
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice == None:

            await ctx.send("I am not in a voice channel")

        else:
            channel = ctx.message.author.voice.channel

            if voice and voice.is_connected():
                await voice.disconnect()

            await ctx.send(f"Left `{channel}` Voice Room")

    @commands.command(aliases=["p"])
    async def play(self, ctx, url: str = None):
        # if ctx.guild.id != 722187348246397010:
        #     return

        # if await self.check_role(ctx.author) is False:
        #     return

        if url is None:
            return await ctx.send("Specify a song to play.")

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice is None:
            await music.join(self, ctx)

        now_voice = get(self.client.voice_clients, guild=ctx.guild)

        async def queue(ctx, urlqueue: str):

            Queue_infile = os.path.isdir("./Queue")

            if Queue_infile is False:
                os.mkdir("Queue")

            DIR = os.path.abspath(os.path.realpath("Queue"))

            q_num = len(os.listdir(DIR))

            q_num += 1

            queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

            add_queue = True
            while add_queue:
                if q_num in self.client.queues:
                    q_num += 1

                else:
                    add_queue = False
                    self.client.queues[q_num] = q_num

            await self.download(ctx, urlqueue, f"Queue/song{q_num}")

            await ctx.send("Added song to the queue")

        # End of queue function

        def check_queue(error):
            Queue_infile = os.path.isdir("./Queue")
            if Queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(DIR))
                still_q = length
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    voice = get(self.client.voice_clients, guild=ctx.guild)
                    noMore = ctx.send("No more audios queued")
                    safe = asyncio.run_coroutine_threadsafe(noMore, self.client.loop)
                    safe.result()
                    self.client.queues.clear()
                    return
                main_location = os.path.dirname(os.path.realpath(__file__))
                if '\\Cogs' in main_location:
                    main_location = main_location[0:len(main_location) - 5]
                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                if length != 0:
                    embed = discord.Embed(title="Audio completed, playing next audio",
                                          description=f"Songs still queued: {still_q}", color=0xFFFF00)
                    stillQueue = ctx.send(embed=embed)
                    safe = asyncio.run_coroutine_threadsafe(stillQueue, self.client.loop)
                    safe.result()
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, "song.mp3")

                    now_voice.play(discord.FFmpegPCMAudio("song.mp3"), after=check_queue)
                    now_voice.source = discord.PCMVolumeTransformer(now_voice.source)
                    now_voice.source.volume = 0.07

                else:
                    self.client.queues.clear()
                    return
            else:
                self.client.queues.clear()
                noMore = ctx.send("No more audios queued")
                safe = asyncio.run_coroutine_threadsafe(noMore, self.client.loop)
                safe.result()

        # End of check queue function

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")

        except:
            print("Trying to delete song file.")
            await queue(ctx, url)
            return

        Queue_infile = os.path.isdir("./Queue")
        try:
            Queue_folder = "./Queue"
            if Queue_infile:
                print("Removed old Queue")
                shutil.rmtree(Queue_folder)
        except:
            print("No old queue folder")

        await ctx.send("Getting everything ready now")

        await self.download(ctx, url, "song")

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        try:
            now_voice.play(discord.FFmpegPCMAudio("song.mp3"), after=check_queue)
            now_voice.source = discord.PCMVolumeTransformer(now_voice.source)
            now_voice.source.volume = 0.07
        except discord.errors.ClientException:
            await music.join(self, ctx)
            now_voice.play(discord.FFmpegPCMAudio("song.mp3"), after=check_queue)
            now_voice.source = discord.PCMVolumeTransformer(now_voice.source)
            now_voice.source.volume = 0.07

    # @play.error
    # async def play_error(self, ctx, error):
    #     if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
    #         await music.join(self, ctx)
    #         split = str(self, ctx.message.content).rsplit(" ", 1)
    #         await music.play(self, ctx, split[1])
    #         print(error)

    @commands.command(aliases=["pa"])
    async def pause(self, ctx):
        # if ctx.guild.id != 722187348246397010:
        #     return
        if await self.check_role(ctx.author) is False:
            return
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("Audio paused")

        else:
            await ctx.send("No audio is currently playing")

    @commands.command(aliases=["r", "res"])
    async def resume(self, ctx):
        # if ctx.guild.id != 722187348246397010:
        #     return
        if await self.check_role(ctx.author) is False:
            return
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("Audio resumed")

        else:
            await ctx.send("No audio is currently playing or audio is not paused")

    @commands.command(aliases=["s"])
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        # if ctx.guild.id != 722187348246397010:
        #     return

        if await self.check_role(ctx.author) is False:
            return

        voice = get(self.client.voice_clients, guild=ctx.guild)
        self.client.queues.clear()

        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("Audio stopped")

        else:
            await ctx.send("No audio is currently playing")

    @stop.error
    async def stop_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed = discord.Embed(title="You do not have the permissions to run this command",
                                  description="`Administrator` permission required", color=0xFFFF00)
            await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):

        # if ctx.guild.id != 722187348246397010:
        #     return

        if await self.check_role(ctx.author) is False:
            return
        voice = get(self.client.voice_clients, guild=ctx.guild)

        self.client.queues.clear()

        if voice and voice.is_playing():
            print("Music skipped")
            voice.stop()
            await ctx.send("Music skipped")
        else:
            print("No music playing failed to skip")
            await ctx.send("No music playing failed to skip")


def setup(client):
    client.add_cog(music(client))
