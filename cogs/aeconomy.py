import discord
from discord.ext import commands, tasks
from discord.ext.commands import BucketType
from copy import deepcopy
from dateutil.relativedelta import relativedelta
import random
import datetime

shop = [
    {
        "name": "Laptop", 
        "desc": "Used to post reddit memes and other stuff", 
        "cost": 5000,
        "id": "laptop"
    },
    {
        "name": "Fishing Pole", 
        "desc": "Used to go fishing with your old man", 
        "cost": 10000,
        "id": "fishingpole"
    }
]

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.heists = self.checkHeist.start()
        self.collection = self.client.economy
    
    def cog_unload(self):
        self.heists.cancel()

    @tasks.loop(seconds=15)
    async def checkHeist(self):
        heist = deepcopy(self.client.heistdata)
        for key, value in heist.items():
            member = value["_id"]
            member = await self.client.get_user(member)
            msg = value["messageId"]
            author = value['author']
            author = await self.client.get_user(author)
            currentTime = datetime.datetime.now()
            guild = self.client.get_guild(value['guildId'])
            channel = self.client.get_channel(value['channelId'])
            ctx = discord.utils.get(guild.text_channels, id=value['channelId'])
            data1 = await self.client.economy.find_one({'_id' : member.id})
            new_msg = await channel.fetch_message(msg)
            lost = []
            win = []
            unmuteTime = value['started'] + relativedelta(
                seconds=value['duration'])
            data = await self.client.economy.find_one({"_id" : author.id})
            users = await new_msg.reactions[0].users().flatten()
            users.pop(users.index(self.client.user))
            if currentTime >= unmuteTime:
                if len(users) < 2:
                    await ctx.send("Not enough users joined")
                    await self.client.heists.delete(member.id)
                    try:
                        self.client.heistdata.pop(member.id)
                    except KeyError:
                        pass
                    return
                for user in users:
                    await self.check_acc(user)
                    data = await self.client.economy.find_one({"_id" : user.id})
                    if data["wallet"] < 1000:
                        pass
                    else:
                        chance = random.randrange(100)
                        if chance > 75:
                            lost.append(user)
                        else:
                            win.append(user)
                winings = data1["bank"] / len(win)
                winings = int(winings)
                data1["bank"] -= data1["bank"]
                await self.client.economy.update_one({"user" : user.id},{ "$inc" : {"bank" : winings}},upsert=False)
                for user in win:
                    await self.client.economy.update_one({"user" : user.id},{ "$inc" : {"bank" : winings}},upsert=False)
                    data["wallet"] += winings

                wins = ""
                for user in win:
                    wins += f"{user} won {winings} from the heist\n"
                loses = ""
                for user in lost:
                    wins += f"{user} lost the heist :(\n"
                em = discord.Embed(
                    title="Heist results on {}'s bank".format(member.name),
                    color=random.choice(self.client.color_list),
                    description=wins)
                if len(loses) == 0:
                  pass
                else:
                    em.add_field(name="People who lost :(", value=loses)
                await self.client.heists.delete_one({"user.id" : member.id})
                try:
                    self.client.heistdata.pop(member.id)
                except KeyError:
                    pass
                await ctx.send(embed=em)

    @checkHeist.before_loop
    async def before_check_current_mutes(self):
        await self.client.wait_until_ready()

    @commands.command(
        description='b l a c k j a c k', usage='<amount>', aliases=["bj"])
    async def blackjack(self, ctx, amount):
        await self.check_acc(ctx.author)
        data = await self.client.economy.find(ctx.author.id)
        pcards = random.randrange(1, 20)
        bcards = random.randrange(1, 20)

        if amount == 'all':
            amount = data["wallet"]
        if amount == 'half':
            amount = data["wallet"] / 2

        amount = int(amount)
        if amount > data["wallet"]:
            await ctx.send("you dont have that much money!")
            return
        if amount < 0:
            await ctx.send("amount must be positive")
            return

        data["wallet"] -= amount

        em = discord.Embed(
            title=f"{ctx.author.name}'s blackjack game", color=random.choice(self.client.color_list))
        em.add_field(name=ctx.author.name, value=pcards)
        em.add_field(name='BreadBot', value='N/A')
        await ctx.send(
            'say `hit` to draw more cards and `stand` to end the game with your stack'
        )
        await ctx.send(embed=em)

        def check(z):
            return z.author == ctx.author and z.content.lower() == 'hit' or z.content.lower() == 'stand'

        msg2 = await self.client.wait_for('message', check=check, timeout=30)
        if msg2.content.lower() == 'hit':
            pcards2 = pcards + random.randrange(1, 10)
            if pcards2 > 21:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Busted!\n\nYou now have **{data["wallet"]:,d}** coins',
                    color=0xff0000)
                em.add_field(name=ctx.author.name, value=pcards2)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                return
            if pcards2 == 21:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You got to 21 before your opponent and won **{amount:,d}** coins\n\nYou now have **{data["wallet"]+amount*2:,d}** coins',
                    color=0x00ff00)
                em.add_field(name=ctx.author.name, value=pcards2)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                data["wallet"] += 2 * amount
                await self.client.economy.upsert(data)
                return
            em = discord.Embed(
                title=f"{ctx.author.name}'s blackjack game", color=random.choice(self.client.color_list))
            em.add_field(name=ctx.author.name, value=pcards2)
            em.add_field(name='BreadBot', value='N/A')
            await ctx.send(
                'say `hit` to draw more cards and `stand` to end the game with your stack'
            )
            await ctx.send(embed=em)
        elif msg2.content == 'stand' or msg2.content == 'Stand':
            if pcards < bcards:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Had Less Cards Than Your Opponent!\n\nYou now have **{data["wallet"]:,d}** coins',
                    color=0xff0000)
                em.add_field(name=ctx.author.name, value=pcards)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                await self.client.economy.upsert(data)
                return
            else:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Had More Cards Than Your Opponent and won **{amount:,d}** coins\n\nYou now have **{data["wallet"]+amount*2:,d}** coins',
                    color=0x00ff00)
                em.add_field(name=ctx.author.name, value=pcards)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                data["wallet"] += 2 * amount
                await self.client.economy.upsert(data)
                return


        msg2 = await self.client.wait_for('message', check=check, timeout=30)
        if msg2.content == 'hit' or msg2.content == 'Hit':
            pcards3 = pcards2 + random.randrange(1, 10)
            if pcards3 > 21:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Busted!\n\nYou now have **{data["wallet"]:,d}** coins',
                    color=0xff0000)
                em.add_field(name=ctx.author.name, value=pcards3)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                return
            if pcards3 == 21:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You got to 21 before your opponent and won **{amount:,d}** coins\n\nYou now have **{data["wallet"]+amount*2:,d}** coins',
                    color=0x00ff00)
                em.add_field(name=ctx.author.name, value=pcards3)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                data["wallet"] += 2 * amount
                await self.client.economy.upsert(data)
                return
            em = discord.Embed(
                title=f"{ctx.author.name}'s blackjack game", color=random.choice(self.client.color_list))
            em.add_field(name=ctx.author.name, value=pcards3)
            em.add_field(name='BreadBot', value='N/A')
            await ctx.send(
                'say `hit` to draw more cards and `stand` to end the game with your stack'
            )
            await ctx.send(embed=em)
        elif msg2.content == 'stand' or msg2.content == 'Stand':
            if pcards2 < bcards:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Had Less Cards Than Your Opponent!\n\nYou now have **{data["wallet"]:,d}** coins',
                    color=0xff0000)
                em.add_field(name=ctx.author.name, value=pcards2)
                em.add_field(name='BreadBot', value=bcards)
                await self.client.economy.upsert(data)
                await ctx.send(embed=em)
                return
            else:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Had More Cards Than Your Opponent and won **{amount:,d}** coins\n\nYou now have **{data["wallet"]+amount*2:,d}** coins',
                    color=0x00ff00)
                em.add_field(name=ctx.author.name, value=pcards2)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                data["wallet"] += 2 * amount
                await self.client.economy.upsert(data)
                return

        msg2 = await self.client.wait_for('message', check=check, timeout=30)
        if msg2.content == 'hit' or msg2.content == 'Hit':
            pcards4 = pcards3 + random.randrange(1, 10)
            if pcards4 > 21:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Busted!\n\nYou now have **{data["wallet"]:,d}** coins',
                    color=0xff0000)
                em.add_field(name=ctx.author.name, value=pcards4)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                await self.client.economy.upsert(data)
                return
            if pcards4 == 21:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You got to 21 before your opponent and won **{amount:,d}** coins\n\nYou now have **{data["wallet"]+amount*2:,d}** coins',
                    color=0x00ff00)
                em.add_field(name=ctx.author.name, value=pcards4)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                data["wallet"] += 2 * amount
                await self.client.economy.upsert(data)
                return
            em = discord.Embed(
                title=f"{ctx.author.name}'s blackjack game", color=random.choice(self.client.color_list))
            em.add_field(name=ctx.author.name, value=pcards4)
            em.add_field(name='BreadBot', value='N/A')
            await ctx.send(
                'say `hit` to draw more cards and `stand` to end the game with your stack'
            )
            await ctx.send(embed=em)
        elif msg2.content == 'stand' or msg2.content == 'Stand':
            if pcards3 < bcards:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Had Less Cards Than Your Opponent\n\nYou now have **{data["wallet"]:,d}** coins',
                    color=0xff0000)
                em.add_field(name=ctx.author.name, value=pcards3)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                await self.client.economy.upsert(data)
                return
            else:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Had More Cards Than Your Opponent and won **{amount:,d}** coins\n\nYou now have **{data["wallet"]+amount*2:,d}** coins',
                    color=0x00ff00)
                em.add_field(name=ctx.author.name, value=pcards3)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                data["wallet"] += 2 * amount
                await self.client.economy.upsert(data)
                return

        msg2 = await self.client.wait_for('message', check=check, timeout=30)
        if msg2.content == 'hit' or msg2.content == 'Hit':
            pcards5 = pcards4 + random.randrange(1, 10)
            if pcards5 > 21:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Busted!\n\nYou now have **{data["wallet"]:,d}** coins',
                    color=0xff0000)
                em.add_field(name=ctx.author.name, value=pcards5)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                await self.client.economy.upsert(data)
                return
            if pcards5 == 21:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You got to 21 before your opponent and won **{amount:,d}** coins\n\nYou now have **{data["wallet"]+amount*2:,d}** coins',
                    color=0x00ff00)
                em.add_field(name=ctx.author.name, value=pcards5)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                data["wallet"] += 2 * amount
                await self.client.economy.upsert(data)
                return
            em = discord.Embed(
                title=f"{ctx.author.name}'s blackjack game", color=random.choice(self.client.color_list))
            em.add_field(name=ctx.author.name, value=pcards5)
            em.add_field(name='BreadBot', value='N/A')
            await ctx.send(
                'say `hit` to draw more cards and `stand` to end the game with your stack'
            )
            await ctx.send(embed=em)
        elif msg2.content == 'stand' or msg2.content == 'Stand':
            if pcards4 < bcards:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Had Less Cards Than Your Opponent\n\nYou now have **{data["wallet"]:,d}** coins',
                    color=0xff0000)
                em.add_field(name=ctx.author.name, value=pcards4)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                await self.client.economy.upsert(data)
                return
            else:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Had More Cards Than Your Opponent and won **{amount:,d}** coins\n\nYou now have **{data["wallet"]+amount*2:,d}** coins',
                    color=0x00ff00)
                em.add_field(name=ctx.author.name, value=pcards4)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                data["wallet"] += 2 * amount
                await self.client.economy.upsert(data)
                return


        msg2 = await self.client.wait_for('message', check=check, timeout=30)
        if msg2.content == 'hit' or msg2.content == 'Hit':
            pcards6 = pcards5 + random.randrange(1, 10)
            if pcards6 > 21:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Busted!\n\nYou now have **{data["wallet"]-amount:,d}** coins',
                    color=0xff0000)
                em.add_field(name=ctx.author.name, value=pcards6)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                await self.client.economy.upsert(data)
                return
            if pcards6 == 21:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You got to 21 before your opponent and won **{amount:,d}** coins\n\nYou now have **{data["wallet"]+amount*2:,d}** coins',
                    color=0x00ff00)
                em.add_field(name=ctx.author.name, value=pcards6)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                data["wallet"] += 2 * amount
                await self.client.economy.upsert(data)
                return
            em = discord.Embed(
                title=f"{ctx.author.name}'s blackjack game",
                description=
                f'You drew 5 cards without busting and won **{amount:,d}** coins\n\nYou now have **{data["wallet"]+amount*2:,d}** coins',
                color=0x00ff00)
            em.add_field(name=ctx.author.name, value=pcards6)
            em.add_field(name='BreadBot', value=bcards)
            await ctx.send(embed=em)
            data["wallet"] += 2 * amount
            await self.client.economy.upsert(data)
        elif msg2.content == 'stand' or msg2.content == 'Stand':
            if pcards5 < bcards:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Had Less Cards Than Your Opponent!\n\nYou now have **{data["wallet"]:,d}** coins',
                    color=0xff0000)
                em.add_field(name=ctx.author.name, value=pcards5)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                await self.client.economy.upsert(data)
                return
            else:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=
                    f'You Had More Cards Than Your Opponent and won **{amount:,d}** coins\n\nYou now have **{data["wallet"]+amount*2:,d}** coins',
                    color=0x00ff00)
                em.add_field(name=ctx.author.name, value=pcards5)
                em.add_field(name='BreadBot', value=bcards)
                await ctx.send(embed=em)
                data["wallet"] += 2 * amount
                await self.client.economy.upsert(data)
                return


    @commands.command()
    async def shop(self,ctx):
        await self.check_acc(ctx.author)
        em = discord.Embed(
            title="Economy Shop",
            color=random.choice(self.client.color_list)
        )
        for item in shop:
            em.add_field(name=f'{item["name"]} — {item["cost"]:,d}',value="{}\nID: `{}`".format(item["desc"], item["id"]), inline=False)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 30, BucketType.user)
    async def beg(self,ctx):
        await self.check_acc(ctx.author)
        data = await self.client.economy.find_one({"user" : ctx.author.id})
        earnings = random.randint(0, 800)
        if earnings in range(0, 200):
            await ctx.send("**Some guy** donated {}".format(earnings))
        if earnings in range(201, 400):
            await ctx.send("**Elon Musk** donated {}".format(earnings))
        if earnings in range(401, 600):
            await ctx.send("**Bill Gates** donated {}".format(earnings))
        if earnings in range(601, 800):
            await ctx.send("**BongoPlayzYT** donated {}".format(earnings))
        await self.client.economy.update_one({"user" : ctx.author.id},{ "$inc" : {"wallet" : earnings}},upsert=False)

    @commands.command(aliases=["with"])
    async def withdraw(self,ctx,amount):
        await self.check_acc(ctx.author)
        data = await self.client.economy.find_one({"user" : ctx.author.id})
        if amount == "all":
            amount = data["bank"]
        if amount == "half":
            amount = data["bank"] / 2
        amount = int(amount)
        
        if amount > data["bank"]:
            return await ctx.send("You dont have that much money in your bank!")

        await self.client.economy.update_one({"user" : ctx.author.id}, {
          "$inc" : {
            "bank" : -amount,
            "wallet" : amount 
          }
        },upsert=False)
        await ctx.send("Successfully withdrew **{}** coins from your bank!".format(amount))

    @commands.command(aliases=["dep"])
    async def deposit(self,ctx,amount):
        await self.check_acc(ctx.author)
        data = await self.client.economy.find_one({"user" : ctx.author.id})
        if amount == "all":
            amount = data["wallet"]
            if amount + data["bank"] > data["banklimit"]:
                maths = data["wallet"] - data["banklimit"]
                amount = data["wallet"] - maths - data["bank"]
        if amount == "half":
            amount = data["wallet"] / 2

        amount = int(amount)
        if amount > data["wallet"]:
            await ctx.send("You dont have that much money!")
            return
        if amount < 0:
            await ctx.send("Amount must be positive")
            return
        if amount + data["bank"] > data["banklimit"]:
            await ctx.send("You dont have enough space in your bank!")
            return
        
        await self.client.economy.update_one({"user" : ctx.author.id}, {
          "$inc" : {
            "bank" : amount,
            "wallet" : -amount 
          }
        },upsert=False)
        await ctx.send("Successfully deposited **{}** coins!".format(amount))


    @commands.command()
    async def rich(self,ctx):
        data = self.client.economy.find()
        lb = sorted(data, key=lambda x: x["wallet"], reverse=True)
        em = discord.Embed(
            title="Top 10 Global Users With the most amount of money in their wallet"
        )
        index = 0
        async for user in lb:
            if index == 10 or index == len(lb):
                break
            else:
                index += 1
                em.add_field(name=f"{index}. {self.client.get_user(user['_id'])}", value=f"{user['wallet']}", inline=False)
        await ctx.send(embed=em)

    @commands.command()
    async def buy(self,ctx,item,amount=1):
        await self.check_acc(ctx.author)
        res = await self.buy_item(ctx.author, item, amount)
        if not res[0]:
            if res[1] == 1:
                return await ctx.send("That item was not found!")
            if res[1] == 2:
                return await ctx.send("You don't have enough money in your wallet for this!")
        await ctx.send("Item Bought Successfully!")

    @commands.command()
    async def sell(self,ctx,item,amount=1):
        await self.check_acc(ctx.author)
        res = await self.sell_item(ctx.author, item, amount)
        if not res[0]:
            if res[1] == 1:
                return await ctx.send("That item was not found!")
            if res[1] == 2:
                return await ctx.send("You don't have that much of that item to sell!")
        await ctx.send("Item Sold Successfully!")

    @commands.command(aliases=["inv"])
    async def inventory(self,ctx, member:discord.Member=None):
        member = member or ctx.author
        await self.check_acc(member)
        data = await self.client.economy.find_one({"user" : member.id})
        embed = discord.Embed(
            title="{}'s inventory".format(member.name),
            color = random.choice(self.client.color_list)
        )
        if len(data["bag"]) == 0:
            embed.add_field(name="This inventory is empty!", value="Use the shop command to get some items!")
        else:
            for item in data["bag"]:
                embed.add_field(name=f"{item['name']} ─ {item['amount']:,d}", value="ID: `{}`".format(item["id"]), inline=False)
        await ctx.send(embed=embed)

    @commands.command(description="rob a person")
    async def rob(self,ctx,member:discord.Member):
        await self.check_acc(ctx.author)
        data = await self.client.economy.find_one({"user" : ctx.author.id})
        await self.check_acc(member)
        data2 = await self.client.economy.find({"user" : member.id})
        if data2["passive"] == "true":
            await ctx.send(
                "This person is in passive mode leave them alone :(_ _")
            return
        if data["passive"] == "true":
            await ctx.send(
                "Mate you are in passive mode so you cant rob anyone"
            )
            return
        
        earnings = random.randint(0,data2["wallet"])
        await self.client.economy.update_one(
          {"user" : member.id},{"$inc" : {"wallet" : -earnings}},upsert=False)
        await self.client.economy.update_one(
          {"user" : ctx.author.id},{"$inc" : {"wallet" : earnings}},upsert=False)
        await ctx.send("You robbed this person and got {}".format(earnings))


    @commands.command(description="rob a person", usage="<user>")
    async def heist(self, ctx, member: discord.Member):
        await self.check_acc(ctx.author)
        data = await self.client.economy.find_one({"user" : ctx.author.id})
        await self.check_acc(member)
        data2 = await self.client.economy.find_one({"user" : member.id})
        if data["wallet"] < 1000:
            await ctx.send("You need atleast 1000 coins to start a heist!")
            return
        if data2["bank"] < 1000:
            await ctx.send("this person doesnt have enough for a good heist")
            return
        if data2["passive"] == "true":
            await ctx.send(
                "This person is in passive mode leave them alone :(_ _")
            return
        if data["passive"] == "true":
            await ctx.send(
                "Mate you are in passive mode so you cant heist against someone"
            )
            return
        msg = await ctx.send(
            "aight everyone looks like we gonna bust open a bank. React to this message within 2 minutes to join. Must have 1000 coins to join. Must have atleast 2 people to start."
        )

        await msg.add_reaction("👍")

        data = {
            '_id': member.id,
            'started': datetime.datetime.now(),
            'duration': 120,
            'channelId': ctx.channel.id,
            'messageId': msg.id,
            'guildId': ctx.guild.id,
            'author': ctx.author.id,
        }
        await self.client.heists.insert_one(data)
        self.client.heistdata[member.id] = data

    async def check_acc(self, member):
        data = await self.client.economy.find(member.id)
        if data:
            return True
        data = {
              "user": member.id,
              "wallet": 0,
              "bank": 0,
              "banklimit": 50000,
              "passive": False,
              "bag": []
          }
        await self.client.economy.insert_one(data)

    async def buy_item(self, member, item_name, amount):
        data = await self.client.economy.find(member.id)
        name_ = None
        item_name = item_name.lower()
        for item in shop:
            if item_name in item["id"]:
                name_ = item
                break
        
        if not name_:
            return [False, 1]
        
        amount = int(amount)
        if data["wallet"] < name_["cost"] * amount:
            return [False, 2]
        
        
        iteminbag = False
        for item in data["bag"]:
            if item["name"] == name_["name"]:
                item["amount"] += amount
                data["wallet"] -= name_["cost"] * amount
                iteminbag = True
                break
        if not iteminbag:
            data["bag"].append({"name": name_["name"], "id": name_["id"], "amount": amount})
            data["wallet"] -= name_["cost"] * amount
        await self.client.economy.upsert(data)
        return [True]
    
    async def sell_item(self, member, item_name, amount):
        data = await self.client.economy.find(member.id)
        name_ = None
        for item in data["bag"]:
            if item_name in item["id"]:
                name_ = item
                break
        
        if not name_:
            return [False, 1]

        amount = int(amount)
        if amount > name_["amount"]:
            return [False, 2]

        worth = 0
        for item in shop:
            if item["id"] == name_["id"]:
                worth = round((item["cost"] / 3) * amount)
                break

        for item in data["bag"]:
            if item == name_:
                item["amount"] -= amount
                data["wallet"] += worth
                if item["amount"] == 0:
                    data["bag"].remove(item)
                break
        await self.client.economy.upsert(data)
        return [True]

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def slots(self,ctx,amount:int):

      bankinfo = await self.collection.find_one({"user": ctx.author.id})
      if not bankinfo:
        #make new entry
        await self.collection.insert_one({"user": ctx.author.id, "wallet": 0, "bank": 0,"inventory":{}})
        await ctx.send(f'{ctx.author.name} is new, opening new bank account.')
        return

      else:

        if amount > bankinfo['wallet']:
          await ctx.send('You dont have that much money!')

        else:

          letters = [':blue_circle:',':red_circle:',':white_circle:',':green_circle:',':yellow_circle:',':purple_circle:']

          a = random.choice(letters)
          b = random.choice(letters)
          c = random.choice(letters)

          if self.slots(a,b,c):

            if a == b and a == c:
              await ctx.send(f'You Got {a},{b},{c} and you won {amount*2} coins! :sunglasses:')

              bankinfo['wallet'] += amount*2

            else: 

              await ctx.send(f'You Got {a},{b},{c} and you won {amount} coins! :sunglasses:')
              bankinfo['wallet'] += amount

          else:
            bankinfo['wallet'] -= amount
            await ctx.send(f'You Got {a},{b},{c} and you lost {amount} coins! :cry:')

          await self.collection.replace_one({"user": bankinfo['user']},{"user": bankinfo['user'], "wallet": bankinfo['wallet'], "bank": bankinfo['bank'],"inventory" : bankinfo['inventory']})

    @slots.error
    async def slots_error(self,ctx,error):
      if isinstance(error,commands.CommandOnCooldown):
        embed=discord.Embed(title='Woah Slow it down buddy',description=f'You can try this command after {round(error.retry_after)} seconds, there is a line..., default cooldown - 20 seconds',colour=discord.Colour.blue())
        await ctx.send(embed=embed)
        



    @commands.command()
    @commands.cooldown(1,30, commands.BucketType.user)
    async def search(self,ctx):
      bankinfo = await self.collection.find_one({"user": ctx.author.id})
      await self.check_acc(ctx.author)
    
      searching_places = ['van','area51','air','grass','hospital','dog','bank','shoe','tree','house','discord','pocket']
      messages = {
        'van':'This would happen in real life also! Very nice Falc!',
        'area51':'NOW RUN! the government is behind you',
        'air': 'How the Heck? Why were you even looking there?',
        'grass':'How? I wonder if somebody left there wallet',
        'hospital':'Are you proud of yourself Now?',
        'dog':'That poor poor Dog',
        'bank':'Did you just roub the bank?!',
        'shoe':'Why were you looking in your shoe?',
        'tree':'Why were you searching in a tree?',
        'house':'Be happy Your mother was nice',
        'discord':'Your DMs are valuable :thinking:',
        'pocket':'Now it is in your wallet!'}

      a = random.choice(searching_places)
      searching_places.remove(a)
      b = random.choice(searching_places)
      searching_places.remove(b)
      c = random.choice(searching_places)
      searching_places.remove(c)

      await ctx.send(f'**Where do you want to search** {ctx.author.mention}\nchoose from the following and type in the chat\n`{a}`,`{b}` or `{c}`')


      def check(m):
        return m.author == ctx.author

      msg = await self.client.wait_for('message',check=check)
    
      if msg.content.lower() != a and msg.content.lower() != b and msg.content.lower() != c:
          await ctx.send(f'What Are You Thinking {ctx.author.mention}, Thats Not a valid Option')
          
      else:
          coins = random.randint(60,500)
          if msg.content.lower() == a:
            await ctx.send(f'{ctx.author.mention} searched the {a}\nYou Found {coins} coins,{messages[a]}')

          if msg.content.lower() == c:
            await ctx.send(f'{ctx.author.mention} searched the {c}\nYou Found {coins} coins,{messages[c]}')

          if msg.content.lower() == b:
            await ctx.send(f'{ctx.author.mention} searched the {b}\nYou Found {coins} coins,{messages[b]}')

          bankinfo['wallet'] += coins



      await self.collection.update_one({"user": ctx.author.id},{"$inc" : {"wallet" : coins}})

    @search.error
    async def search_error(self,ctx,error):
      if isinstance(error,commands.CommandOnCooldown):
        embed=discord.Embed(title='Woah Slow it down buddy',description=f'You can try this command after {round(error.retry_after)} seconds,You already scouted this area, default cooldown - 20 seconds',colour=discord.Colour.blue())
        await ctx.send(embed=embed)


    @commands.command()
    async def send(self, ctx,member : discord.Member,amount = None):
      await self.check_acc(ctx.author)
      await self.check_acc(member)
      users = await self.client.economy.find_one({"user" : ctx.author.id})
      wallet_amt = users["wallet"] 
      bal = [users["wallet"],users["bank"]]
      if amount == ("all" or "max"):
        amount = bal[0]
      amount = int(amount)
      if amount == None:
        return await ctx.reply("Please enter an amount you would like to send!")
      elif amount>bal[1]:
        return await ctx.reply(f"You do not have that much money! You only have {wallet_amt} in your wallet!")
      elif amount<=0:
        return await ctx.reply("No. You can't do that. The amount must be positive")
        
          
    @commands.command()
    @commands.cooldown(1,20, commands.BucketType.user)
    async def fish(self,ctx):
      bankinfo = await self.collection.find_one({"user": ctx.author.id})
      await self.check_acc(ctx.author)
      caught = random.randint(0,3)

      if 'fishing pole' not in bankinfo['inventory'].keys():
        return await ctx.send('First buy a fishing pole!')

      if not bankinfo['inventory']['fishing pole'] >= 1:
          return await ctx.send('First buy a fishing pole!')

      if caught == 0:
        await ctx.send('LOL you are BAD You couldnt find anything')
      else:
        fishes = random.randint(1,5)
        await ctx.send(f'You brough back {fishes} fish 🐟!')
        if 'fish' in bankinfo['inventory'].keys():
          bankinfo['inventory']['fish'] += fishes
        else:
          bankinfo['inventory']['fish'] = fishes

        await self.client.economy.update_one({"user": ctx.author},{"$set" : {"inventory" : bankinfo["inventory"]}})

    
    @commands.command()
    @commands.cooldown(1,20, commands.BucketType.user)
    async def hunt(self,ctx):
      bankinfo = await self.collection.find_one({"user": ctx.author.id})
      await self.check_acc(ctx.author)
      caught = random.randint(0,3)

      if 'rifle' not in bankinfo['inventory'].keys():
        await ctx.send('First buy a rifle!')

      else:

        if not bankinfo['inventory']['rifle'] >=1:
          return await ctx.send('First buy a rifle!')

        if caught == 0:
          await ctx.send('LOL you are BAD You couldnt find anything')

        else:
          animals = ['rabbit🐇','deer🦌','horse🐎'] 
          animal = random.choice(animals)
          animalnum = random.randint(1,3)
          await ctx.send(f'You brough back {animalnum} {animal}!')
          if animal == 'rabbit🐇':
            if 'rabbit' in bankinfo['inventory'].keys():
              bankinfo['inventory']['rabbit'] += animalnum

            else:
              bankinfo['inventory']['rabbit'] = animalnum

          if animal == 'deer🦌':
            if 'deer' in bankinfo['inventory'].keys():
              bankinfo['inventory']['deer'] += animalnum

            else:
              bankinfo['inventory']['deer'] = animalnum

          if animal == 'horse🐎':
            if 'horse' in bankinfo['inventory'].keys():
              bankinfo['inventory']['horse'] += animalnum

            else:
              bankinfo['inventory']['horse'] = animalnum

      await self.collection.update_one({"user": ctx.author.id},{"$set" : {"inventory" : bankinfo["inventory"]}})


    @commands.command(aliases=['postmeme'])
    @commands.cooldown(1, 20, commands.BucketType.user) 
    
    async def pm(self,ctx):
      bankinfo = await self.collection.find_one({"user": ctx.author.id})
      await self.check_acc(ctx.author)
      if 'laptop' not in bankinfo['inventory'].keys():
        return await ctx.send('You need to buy a laptop for this!')

      await ctx.send('What type of meme do you want to post online:\n`a`Kind Meme\n`b`Inspirational Meme\n`c`Copypasta\n`d`Fresh Meme\n`e`Random Meme')

      def check(m):
        return m.author == ctx.author

      msg = await self.client.wait_for('message',check=check)

      if msg.content.lower() == 'a':
        choice = random.choice([0,1])
        if choice == 0:
          await ctx.send('Nobody Liked Your Kind Meme LOL!')

        else:
          decent_nice = random.choice(['decent','awesome'])
          if decent_nice == 'decent':
            amount = random.randint(300,600)
            bankinfo['wallet'] += amount
            await ctx.send(f'Your Kind meme got decent response online! you got {amount} coins from the ads!')

          else:
            amount = random.randint(600,800)
            bankinfo['wallet'] += amount
            await ctx.send(f'Your Kind meme is VIRAL!!! you got {amount} coins by the ads')

      elif msg.content.lower() == 'b':
        choice = random.choice([0,1])
        if choice == 0:
          await ctx.send('Nobody Liked Your Inspirational Meme LOL!')

        else:
          decent_nice = random.choice(['decent','awesome'])
          if decent_nice == 'decent':
            amount = random.randint(100,300)
            bankinfo['wallet'] += amount
            await ctx.send(f'Your Inspirational meme got decent response online! you got {amount} coins from the ads!')

          else:
            amount = random.randint(300,500)
            bankinfo['wallet'] += amount
            await ctx.send(f'Your Inspirational meme went VIRAL online! you got {amount} coins from the ads!')

      elif msg.content.lower() == 'c':
        choice = random.choice([0,1])
        if choice == 0:
          await ctx.send('Nobody Liked Your CopyPasta Meme LOL!')

        else:
          decent_nice = random.choice(['decent','awesome'])
          if decent_nice == 'decent':
            amount = random.randint(100,400)
            bankinfo['wallet'] += amount
            await ctx.send(f'Your CopyPasta meme got decent response online! you got {amount} coins from the ads!')
            
          else:
            amount = random.randint(400,600)
            bankinfo['wallet'] += amount
            await ctx.send(f'Your CopyPasta meme went VIRAL online! you got {amount} coins from the ads!')
            

      elif msg.content.lower() == 'd':
        choice = random.choice([0,1])
        if choice == 0:
          await ctx.send('Nobody Liked Your Fresh Meme LOL!')

        else:
          decent_nice = random.choice(['decent','awesome'])
          if decent_nice == 'decent':
            amount = random.randint(300,600)
            bankinfo['wallet'] += amount
            await ctx.send(f'Your Fresh meme got decent response online! you got {amount} coins from the ads!')

          else:
            amount = random.randint(600,1000)
            bankinfo['wallet'] += amount
            await ctx.send(f'Your Fresh meme went VIRAL online! you got {amount} coins from the ads!')

      elif msg.content.lower() == 'e':
        choice = random.choice([0,1])
        if choice == 0:
          await ctx.send('Nobody Liked Your Random Meme LOL!')

        else:
          decent_nice = random.choice(['decent','awesome'])
          if decent_nice == 'decent':
            amount = random.randint(100,300)
            bankinfo['wallet'] += amount
            await ctx.send(f'Your Random meme decent response online! you got {amount} coins from the ads!')

          else:
            amount = random.randint(300,500)
            bankinfo['wallet'] += amount
            await ctx.send(f'Your Random meme went VIRAL online! you got {amount} coins from the ads!')

      else:
        await ctx.send('Thats Not a Valid Option')

      await self.collection.update_one({"user": ctx.author.id},{"$inc" : {"wallet" : amount}})

              
    @commands.command(aliases= ["bet"])
    @commands.cooldown(1, 20, commands.BucketType.user) 
    async def gamble(self,ctx,amount:int=None):
      bankinfo =  await self.client.economy.find_one({"user" : ctx.author.id})
      await self.check_acc(ctx.author)
      if amount == None:
        await ctx.send('Try the command again but next time tell me how much money are you want to bet')

      elif amount > bankinfo['wallet']:
        await ctx.send('You cant bet more than how much money you have ')

      else:

        a = random.randint(0,10)
        b = random.randint(0,10)

        embed=discord.Embed(title=f"{ctx.author.name}'s Gambling Game",colour=discord.Colour.blue())
        embed.add_field(name=f'Falc rolled `{a}`',value="\u200b")
        embed.add_field(name=f'{ctx.author.name} rolled `{b}`',value="\u200b")

        if a<b:
          embed.add_field(name='**You Won!**',value=f'You win {amount} coins!',inline=False)
          bankinfo['wallet'] += amount
        elif a>b:
          embed.add_field(name='**I won!**',value=f'You loose {amount} coins!',inline=False)
          bankinfo['wallet'] -= amount
        else:
          embed.add_field(name='**Its a Draw**',value='No one wins or looses any money',inline=False)

        await ctx.send(embed=embed)
  
        await self.collection.update_one({"user": ctx.author.id},{"$inc" : {"wallet" : amount}},upsert=False)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def enable(self,ctx,what):
      if what.lower() == 'rob':
        await self.collection.update_one({"guildID" : ctx.guild},{"$set" : {"robbing" : True}},upsert=True)
        await ctx.send('Rob Enabled!')
      if what.lower() == 'tips' or what.lower() == 'tip':
        await self.collection.update_one({"guilDID" : ctx.guild.id},{"$set" : {"tips" : True}},upsert=True)
        await ctx.send('Enabled Tips!')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def disable(self,ctx,what):
      if what.lower() == 'rob':
        await self.collection.update_one({"guildID" : ctx.guild},{"$set" : {"robbing" : False}},upsert=True)
        await ctx.send('Rob Enabled!')
      if what.lower() == 'tips' or what.lower() == 'tip':
        await self.collection.update_one({"guilDID" : ctx.guild.id},{"$set" : {"tips" : False}},upsert=True)
        await ctx.send('Enabled Tips!')

    @commands.command(aliases=['DAILY','Daily'])
    @commands.cooldown(1, 86400, commands.BucketType.user) 
    async def daily(self,ctx):
      await self.check_acc(ctx.author)
      await ctx.send('Daily Reward claimed for 1000 fluxes!!!')
    
      await self.collection.update_one({"user": ctx.author.id},{"$inc" : {"wallet" : 1000}},upsert=False)

    @commands.command(aliases=['MONTHLY','Monthly'])
    @commands.cooldown(1, 2628288 , commands.BucketType.user) 
    async def monthly(self,ctx):
      await self.check_acc(ctx.author)
      await ctx.send('Monthly reward claimed for 10000 coins!!!')
    
      await self.collection.update_one({"user": ctx.author.id},{"$inc" : {"wallet" : 10000}})

    @commands.command(aliases=['WEEKLY','Weekly'])
    @commands.cooldown(1, 604800, commands.BucketType.user) 
    async def weekly(self,ctx):
      bankinfo = await self.collection.find_one({"user": ctx.author.id})
      if not bankinfo:
        #make new entry
        await self.check_acc(ctx.author)
        await ctx.send(f'{ctx.author.name} is new, opening new bank account.')
        return
      await ctx.send('Daily Reward claimed for 5000 coins!!!')
      
      await self.client.economy.update_one({"user": ctx.author.id},{"$inc" : {"wallet" : 5000}},upsert=False)


              
    def slots(a,b,c):
      if a == b or a == c:
        return True

      if b == c:
        return True
      return False
    






def setup(client):
  client.add_cog(Economy(client))