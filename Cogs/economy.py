import discord
from discord.ext import commands
from random import choice, randint
import asyncio


def convert_seconds_to_time(seconds: int) -> str:
    """Converts seconds to a time format: hh:mm:ss"""
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


class economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def check_account(self, user):
        """Checks if the user has an account. If not, create one."""
        self.client.cursor.execute(f"SELECT * FROM users WHERE user_id = {user.id}")
        result = self.client.cursor.fetchall()

        if len(result) == 0:
            self.client.cursor.execute(f"INSERT INTO `{self.client.dbname}`.`users` (`user_id`, `money`) VALUES ('{user.id}', '0');")
            self.client.mydb.commit()

    async def add_balance(self, ctx, amount: int, user: discord.Member, multiple: int = 1):
        """Adds the specified balance to a user's account."""
        # Access User Balance
        self.client.cursor.execute(f"SELECT * FROM users WHERE user_id = {user.id}")
        balance = int(self.client.cursor.fetchall()[0][1])

        winAmount = amount * multiple
        balance += winAmount

        # Update User Balance
        self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`users` SET `money` = '{balance}' WHERE (`user_id` = '{user.id}');")
        self.client.mydb.commit()

    async def check_balance(self, user: discord.Member) -> int:
        """Checks the balance of a user."""
        await self.check_account(user)
        self.client.cursor.execute(f"SELECT * FROM users WHERE user_id = {user.id}")
        return int(self.client.cursor.fetchall()[0][1])

    async def deduct_balance(self, ctx, amount: int, user: discord.Member):
        """Deducts the specified balance from a user's account."""
        # Access User Balance
        self.client.cursor.execute(f"SELECT * FROM users WHERE user_id = {user.id}")
        balance = int(self.client.cursor.fetchall()[0][1])

        balance -= amount

        # Update User Balance
        self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`users` SET `money` = '{balance}' WHERE (`user_id` = '{user.id}');")
        self.client.mydb.commit()

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        """Displays the balance of a specified user or the command author if no user is specified."""
        sender = member or ctx.author
        await self.check_account(sender)

        self.client.cursor.execute(f"SELECT * FROM users WHERE user_id = '{sender.id}';")
        balance = self.client.cursor.fetchall()[0][1]

        embed = discord.Embed(title=f"{sender}'s Balance", color=0xFFFF00)
        embed.set_thumbnail(url=sender.avatar_url)
        embed.add_field(name="Balance", value=f"V$ {balance}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def gamble(self, ctx, amount):
        """Allows a user to gamble a specified amount."""
        await self.check_account(ctx.author)

        amount = int(amount)
        if amount < 10:
            return await ctx.send("You must gamble at least `10` Vits")

        # Access User Balance
        self.client.cursor.execute(f"SELECT * FROM users WHERE user_id = {ctx.author.id}")
        balance = int(self.client.cursor.fetchall()[0][1])

        if balance < amount:
            await ctx.send("You do not have enough money to make this gamble.")
            return

        balance -= amount

        # Initiate Gamble
        gamble_chance = [False, True, False]
        if choice(gamble_chance):
            win_amount = amount * 2
            balance += win_amount
            await ctx.send(f"{ctx.author.mention} Congratulations! You got `{amount}` Vits.")
        else:
            await ctx.send(f"{ctx.author.mention}, you lost the gamble that time.")

        # Update User Balance
        self.client.cursor.execute(f"UPDATE `{self.client.dbname}`.`users` SET `money` = '{balance}' WHERE (`user_id` = '{ctx.author.id}');")
        self.client.mydb.commit()

    @gamble.error
    async def gamble_error(self, ctx, error):
        """Handles errors for the gamble command."""
        if isinstance(error, (commands.errors.MissingRequiredArgument, commands.errors.CommandInvokeError)):
            await ctx.send("You have to specify a numerical amount to gamble: `gamble <amount>`")

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.member)
    async def claim(self, ctx):
        """Allows a user to claim a random amount."""
        await self.check_account(ctx.author)

        random_amount = randint(100, 175)
        await self.add_balance(ctx, random_amount, ctx.author)
        await ctx.send(f"{ctx.author.mention}, you've claimed `{random_amount}` Vits. You can claim again in 24 hours.")

    @claim.error
    async def claim_error(self, ctx, error):
        """Handles errors for the claim command."""
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_seconds = round(error.retry_after)

            time_remaining = convert_seconds_to_time(cooldown_seconds)
            await ctx.send(f"You can claim again in: {time_remaining}")


    @commands.command()
    async def casino(self, ctx, game=None, amount=None):
        await self.check_account(ctx.author)

        if game is None:
            return await ctx.send("The proper usage of this command is `casino <game> <amount>` **|** Games: `slots`")

        if amount is None:
            pass
        else:
            amount = int(amount)
            if await self.check_balance(ctx.author) < amount:
                return await ctx.send("Insufficient Funds")

        if game == "slots":
            if amount is None:
                slot_help = discord.Embed(title=f"How to Play `Slot Machine`",
                                          description=f"If you receive one of the following combinations you will "
                                                      f"make the amount of money specified: \n1 Diamond: 2x \n2 "
                                                      f"Diamonds: 3x \n3 Diamonds: 5x \n3 Cherries: 10x \n3 Hearts: "
                                                      f"25x \n3 Sevens: 50x",
                                          color=0xFFFF00)
                await ctx.send(embed=slot_help)
                return
            await self.deduct_balance(ctx, amount, ctx.author)
            slots = ["Horseshoe", "Lemon", "Watermelon", "Heart", "Seven", "Bell", "Diamond", "Cherry", "Bar"]
            slotone = random.choice(slots)
            slottwo = random.choice(slots)
            slotthree = random.choice(slots)

            embed = discord.Embed(title=f"Slot Machine", desc=f"Requested by {ctx.author}", color=0xFFFF00)
            embed.add_field(name="Slot One", value=slotone, inline=False)
            embed.add_field(name="Slot Two", value=slottwo, inline=False)
            embed.add_field(name="Slot Three", value=slotthree, inline=False)
            await ctx.send(embed=embed)
            # 1 Diamond: 2x
            # 2 Diamonds: 3x
            # 3 Diamonds: 5x
            # 3 Cherries: 10x
            # 3 Hearts: 25x
            # 3 Sevens: 50x
            if slotone == slottwo and slottwo == slotthree:
                if slotone == "Diamond":
                    await add_balance(ctx, amount, 5, ctx.author)
                    await ctx.send(
                        f"{ctx.author.mention} Congratulations, you won 5x your money and received `{5 * amount}` Vits.")
                    return

                if slotone == "Cherry":
                    await add_balance(ctx, amount, 10, ctx.author)
                    await ctx.send(
                        f"{ctx.author.mention} Congratulations, you won 10x your money and received `{10 * amount}` Vits.")
                    return

                if slotone == "Heart":
                    await add_balance(ctx, amount, 25, ctx.author)
                    await ctx.send(
                        f"{ctx.author.mention} Congratulations, you won 25x your money and received `{25 * amount}` Vits.")
                    return

                if slotone == "Seven":
                    await add_balance(ctx, amount, 50, ctx.author)
                    await ctx.send(
                        f"{ctx.author.mention} Congratulations, you won 50x your money and received `{50 * amount}` Vits.")
                    return
            elif "Diamond" in (slotone, slottwo) or "Diamond" in (slotone, slotthree) or "Diamond" in (slottwo, slotthree):
                await add_balance(ctx, amount, 3)
                await ctx.send(
                    f"{ctx.author.mention} Congratulations, you've tripled your money and received `{3 * amount}` Vits.")
                return

            elif slotone == "Diamond" or slottwo == "Diamond" or slotthree == "Diamond":
                await add_balance(ctx, amount, 2)
                await ctx.send(
                    f"{ctx.author.mention} Congratulations, you've doubled your money and received `{2 * amount}` Vits.")
                return

            else:
                await ctx.send(f"{ctx.author.mention} Sorry, better luck next time!")

    @commands.command()
    async def give(self, ctx, member: discord.Member, amount):
        if member is None:
            return await ctx.send("Please specify a member to send Vits.")

        await self.check_account(ctx.author)
        await self.check_account(member)

        amount = int(amount)

        if await self.check_balance(ctx.author) - amount < 0:
            await ctx.send("You do not have enough money to make this transaction")
            return

        await self.deduct_balance(ctx, amount, ctx.author)

        await self.add_balance(ctx, amount, member)

        await ctx.send(f"Gave {member} `{amount}`")

    # Shop System Disabled

    # @commands.command()
    # async def shop(self, ctx, shop_name=None):
    #     if shop_name is None:
    #         embed = discord.Embed(title="Vitality Shop", description="Use `shop <shop-name>` to view the items of a "
    #                                                                  "shop", color=0xff9129)
    #         embed.add_field(name="Drinks", value="Choose from a variety of drinks")
    #         return await ctx.send(embed=embed)

    #     if shop_name.lower() == "drinks":
    #         drinks = ""
    #         f = open("shops.json", "r")
    #         shop_list = json.load(f)
    #         for drink in shop_list["drinks"]:
    #             drinks += f"`{drink}` V$ {shop_list['drinks'][drink]} \n"

    #         embed = discord.Embed(title="Drinks Shop", description=drinks, color=0xff9129)
    #         embed.set_footer(text="Use `buy <item>` to get an item")
    #         return await ctx.send(embed=embed)

    # @commands.command()
    # async def buy(self, ctx, item=None):
    #     await check_account(ctx.author)

    #     if item is None:
    #         embed = discord.Embed(title="Vitality Shop", description="Use `shop <shop-name>` to view the items of a "
    #                                                                  "shop", color=0xff9129)
    #         embed.add_field(name="Drinks", value="Choose from a variety of drinks")
    #         await ctx.send("You must specify an item to buy")
    #         return await ctx.send(embed=embed)

    #     f = open("shops.json", "r")
    #     shop_list = json.load(f)
        
    #     if item in shop_list["drinks"].keys():

    #         amount = shop_list["drinks"][item.lower()]

    #         with open(f"Users/{ctx.author.id}.json", 'r') as s:

    #             sender = json.load(s)
    #             if sender['Balance'] - amount < 0:
    #                 await ctx.send("You do not have enough money to make this transaction")
    #                 s.close()
    #                 return

    #             sender['Balance'] = sender['Balance'] - amount
    #             with open(f"Users/{ctx.author.id}.json", 'w') as s:
    #                 json.dump(sender, s)
    #                 s.close()

    #         drink = await ctx.send("Your drink is being created. Please wait a moment...")

    #         await asyncio.sleep(5)

    #         embed = discord.Embed(title=f"Here is your {item}")
    #         drink_image = discord.File(f"Items/Drinks/{item.lower()}.jpg", filename="drink.jpg")
    #         embed.set_image(url=f"attachment://drink.jpg")

    #         await ctx.send(file=drink_image, embed=embed)




def setup(client):
    client.add_cog(economy(client))
