import discord
import datetime
import os 
import asyncio
import aiohttp
from discord.ext import commands

afk_users = []
afk_reasons = {}

numbers = ("1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟")

class Other(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    @commands.command(aliases=['df','def','urban','ud','urbandictionary'])
    async def define(self, ctx,*,ud_query = None):
        if ud_query == None:
            await ctx.message.reply(embed=discord.Embed(
                title = "Incorrect Usage!",
                description = f"Please use the command like this: `{ctx.prefix}define <query>`",
                color = discord.Color.red()
            ).set_footer(text="Idiot!"))
            return
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term":ud_query}
        headers = {
            "x-rapidapi-key": os.environ.get("UD_API_KEY"),
            "x-rapidapi-host": "mashape-community-urban-dictionary.p.rapidapi.com",
		}
        ud_file = await self.session.get(url, headers=headers, params=querystring)
        total_definitions = len(ud_file.json()["list"])
        try:
            word_name = await ud_file.json()["list"][1]["word"]
            definition = await ud_file.json()["list"][1]["definition"]
            link = await ud_file.json()["list"][1]["permalink"]
            example = await ud_file.json()["list"][1]["example"]
            more_res = total_definitions - 1

            definition2 = await ud_file.json()["list"][0]["definition"]
            example2 = await ud_file.json()["list"][0]["example"]

            em_ud = discord.Embed(
            title= str(word_name),
            color=discord.Color.blue(),
            url = link
            )
            em_ud.add_field(name="Definition : ",value=definition,inline=False)
            em_ud.add_field(name="Example : ",value=example,inline=False)

            em_ud.add_field(name="Definition (2): ",value=definition2,inline=False)
            em_ud.add_field(name="Example (2): ",value=example2,inline=False)

            em_ud.set_footer(text=f'{more_res} more results.')
            em_ud.timestamp=datetime.datetime.utcnow()
            await ctx.send(embed=em_ud)

        except IndexError:
            try:
                word_name = await ud_file.json()["list"][0]["word"]
                definition = await ud_file.json()["list"][0]["definition"]
                link = await ud_file.json()["list"][0]["permalink"]
                example = await ud_file.json()["list"][0]["example"]
                more_res = total_definitions - 1
                em_ud = discord.Embed(
                title= str(word_name),
                color=discord.Color.blue(),
                url = link
                )
                em_ud.add_field(name="Definition : ",value=definition,inline=False)
                em_ud.add_field(name="Example : ",value=example,inline=False)
                em_ud.set_footer(text=f'{more_res} more results.')
                em_ud.timestamp=datetime.datetime.utcnow()
                await ctx.send(embed=em_ud)
            except IndexError:
                em_ud_no = discord.Embed(
                title = "\"" + str(ud_query) + "\" does not matched to any pages. Try another query!",
                color= discord.Color.red()
				)
                em_ud_no.timestamp=datetime.datetime.utcnow()
                await ctx.send(embed=em_ud_no)


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def poll(self, ctx, question, *options):
        if len(options) > 10:
            return await ctx.send(f"You can only enter upto 10 options. Please try again.")
        else:
            embed = discord.Embed(title = f"**Poll**",
                                description = f"{question}",
                                color = 0x00FF0C)
            embed.add_field(name = f"Options:", value = "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), inline = False)
            embed.add_field(name = "Instructions:", value = f"React with corresponding emotes to vote.", inline = False)
            embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()

            msg = await ctx.send(embed = embed)

            for emoji in numbers[:len(options)]:
                await msg.add_reaction(emoji)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['selfdestruct', 'timed_message', 'timedmessage', 'timed_msg', 'timedmsg'])
    @commands.has_permissions(manage_guild = True)
    async def self_destruct(self, ctx, textChannel: discord.TextChannel = None, time = None, *, message = None):
        if time == None or message == None or  textChannel == None:
            await ctx.send(f"Please enter all the parameters. `{ctx.prefix}selfdestruct <channel> <time> <message>`")
            return

        def convert(time):
            pos = ["s", "m", "h", "d"]

            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}

            unit = time[-1]

            if unit not in pos:
                return -1
            try:
                val = int(time[:-1])
            except:
                return -2

            return val * time_dict[unit]

        realTime = convert(time)

        if realTime == -1:
            await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time.")
            return
        elif realTime == -2:
            await ctx.send(f"The time must be an integer. Please enter an interger next time.")
            return

        embed = discord.Embed(title = "Timed Message", description = message, color = 0x00FFFF)
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.set_footer(text=f"This will get deleted after {time}.", icon_url=f"{ctx.author.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        try:
            msg = await textChannel.send(embed = embed)
            await ctx.send(f"The timed message has been sent in {textChannel.mention} and will self destruct itself in `{time}` time.")
        except:
            await ctx.send(f"I wasn't able to send the message in {textChannel.mention}, maybe i don't have permissions to send messages there please check my permissions and try again.")

        await asyncio.sleep(realTime)

        my_msg = await textChannel.fetch_message(msg.id)

        try:
            await my_msg.delete()
            await ctx.send(f"The timed message was deleted.")
        except:
            await ctx.send(f"{ctx.author.mention}, I tried to delete the timed message in {textChannel.mention} but i don't have enough permissions to do that, please check my permissions and try again.")

def setup(client):
    client.add_cog(Other(client))