import discord
from discord.ext import commands
import random
import asyncio
from discord import utils
from discord.utils import get
from datetime import datetime
import asyncio
from datetime import datetime, timedelta
import aiohttp
import paginator
import humanize
import pytz
audit_actions = {
        discord.AuditLogAction.guild_update: "**updated the guild**",
        discord.AuditLogAction.channel_update: "**updated channel**",
        discord.AuditLogAction.channel_create: "**created channel**",
        discord.AuditLogAction.channel_delete: "**deleted channel**",
        discord.AuditLogAction.overwrite_create: "**created overwrite**",
        discord.AuditLogAction.overwrite_update: "**updated overwrite**",
        discord.AuditLogAction.overwrite_delete: "**deleted overwrite**",
        discord.AuditLogAction.kick: "**kicked**",
        discord.AuditLogAction.ban: "**banned**",
        discord.AuditLogAction.unban: "**unbanned**",
        discord.AuditLogAction.member_role_update: "**updated roles of**",
        discord.AuditLogAction.member_move: "**moved member**",
        discord.AuditLogAction.member_disconnect: "**disconnected member**",
        discord.AuditLogAction.bot_add: "**added bot**",
        discord.AuditLogAction.role_create: "**created role**",
        discord.AuditLogAction.role_update: "**updated role**",
        discord.AuditLogAction.role_delete: "**deleted role**",
        discord.AuditLogAction.invite_create: "**created invite**",
        discord.AuditLogAction.invite_update: "**updated invite**",
        discord.AuditLogAction.invite_delete: "**deleted invite**",
        discord.AuditLogAction.webhook_create: "**created webhook**",
        discord.AuditLogAction.webhook_delete: "**deleted webhook**",
        discord.AuditLogAction.webhook_update: "**updated webhook**",
        discord.AuditLogAction.emoji_create: "**created emoji**",
        discord.AuditLogAction.emoji_update: "**updated emoji**",
        discord.AuditLogAction.emoji_delete: "**deleted emoji**",
        discord.AuditLogAction.message_delete: "**deleted message by**",
        discord.AuditLogAction.message_pin: "**pinned a message by**",
        discord.AuditLogAction.message_unpin: "**unpinned a message by**",
        discord.AuditLogAction.message_bulk_delete: "**bulk deleted messages**",
        discord.AuditLogAction.integration_create: "**created integration**",
        discord.AuditLogAction.integration_delete: "**deleted integration**",
        discord.AuditLogAction.integration_update: "**updated integration**",
        discord.AuditLogAction.member_update: "**updated member**"
        }
def convert(time):
  pos = ["s","m","h","d"]

  time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

  unit = time[-1]

  if unit not in pos:
      return -1
  try:
      val = int(time[:-1])
  except:
      return -2


  return val * time_dict[unit]

urls = {"anime1":"https://i.pinimg.com/originals/a3/19/db/a319db489eb10c63d34f286d6d81008d.jpg"
        ,"gaming1":"https://wallpaperaccess.com/full/2541966.jpg",
        "coding1":"https://www.teahub.io/photos/full/87-879470_computer-programming-coding-technology.jpg",
        "default":"https://wallpapercave.com/wp/wp4464897.jpg"}

color = 0xabffcf
numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣", "🔟")


class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession
        self.messagem = []
        self.messager = []
        print("Loaded Utils")

    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 2)
        await ctx.send(f"**{days} day(s), {hours} hour(s), {minutes} mminutes, {seconds} seconds**")

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title="Invite The Bot or Join our Support Server",
        colour=discord.Colour.red())
        embed.add_field(
        name="__Invite__",
        value=
        "[Add Now!](https://discord.com/api/oauth2/authorize?client_id=790525985266597918&permissions=3757436406&scope=bot%20applications.commands)",
        inline=False)
        embed.add_field(name="__Support Server__",
                    value="[Join Now!](https://discord.gg/euBuYefshR)",
                    inline=True)
        embed.add_field(name="__Falc's code on Github__",
                    value="[View Now!](https://www.youtube.com/watch?v=GXltvIbyCrk)",
                    inline=False)
        await ctx.send(embed=embed)


    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(description =f" <a:Tick:827851647463718963> **|** Pong! I have a Botping of: **{round(self.client.latency * 1000)}ms**", color =discord.Colour.random())
        embed.set_footer(text = "It's your turn now!")
        await ctx.send(embed = embed)

    @commands.command()
    async def use(self, ctx, *, arg):
        try:
            em = get(ctx.guild.emojis, name=arg)
            await ctx.message.delete()
            await ctx.send(em)
        except:
            await ctx.send("No such emoji found")


    @commands.command()
    async def react(self, ctx, msg: discord.Message, *, arg):
        try:
            em = get(ctx.guild.emojis, name=arg)
            await ctx.message.delete()
            await msg.add_reaction(em)
        except:
            await ctx.send("No such emoji found")

    @commands.command(aliases=['servers'],
                brief=" | Shows the number of servers I am in")
    async def servercount(self, ctx):
        await ctx.send(f"Falc is in {len(self.client.guilds)} guilds.")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def trashh(self, ctx, user: discord.Member = None):
        """It's Trash smh! """
        user = user or ctx.author
        async with ctx.typing:
            url = user.avatar_url_as(format="jpg")
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://nekobot.xyz/api/imagegen type=trash&url=%s" % (url,)) as r:
                    res = await r.json()
                    embed = discord.Embed(
                        title = "Trash SMH!",
                        color=0x5f3fd8

                    )
                    embed.set_image(url=res['message'])
                    embed.set_author(name = f"{user.name}" , icon_url = user.avatar_url)
                    embed.set_footer(text=f'Requested by {user.name}',icon_url = user.avatar_url)
            await ctx.send(embed=embed)
    @commands.command(aliases=["whois", "ui"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, ctx, user: discord.Member = None):
      user = user or ctx.author
      mentions = [role.mention for role in user.roles]
      roles = mentions[1:]
      no_of_roles = len(roles)
      fmt = "%a, %b %d, %Y, %I:%M %p"
      created_at = user.created_at.strftime(fmt)
      joined_at = user.joined_at.strftime(fmt)
      permission = []


      for perms in user.guild_permissions:
      	if "administrator" in perms and 'True' in str(perms[1]):
      		permission.append('Administrator')
      	if "manage_guild" in perms and 'True' in str(perms[1]):
      		permission.append('Manage Server')
      	if "manage_nicknames" in perms and 'True' in str(perms[1]):
      		permission.append('Manage Nicknames')
      	if "manage_messages" in perms and 'True' in str(perms[1]):
      		permission.append('Manage Message')
      	if "kick_members" in perms and 'True' in str(perms[1]):
      		permission.append('Kick Members')
      	if "ban_members" in perms and 'True' in str(perms[1]):
      		permission.append('Ban Members')
      	if "manage_roles" in perms and 'True' in str(perms[1]):
      		permission.append('Manage Roles')
      	if "mention_everyone" in perms and 'True' in str(perms[1]):
      		permission.append('Mention Everyone')
      	if "manage_channels" in perms and 'True' in str(perms[1]):
      		permission.append('Manage Channels')

      if roles == []:
      	roles.append('@everyone')
      	no_of_roles = 1

      roles = roles[::-1]
      roles = ' '.join(roles)
      permission = ', '.join(permission)


      embed = discord.Embed(
      	description = user.mention,
      	timestamp = ctx.message.created_at,
      	colour = discord.Color.blue()
      )
      embed.set_author(name= user, url=user.avatar_url, icon_url=user.avatar_url)
      embed.add_field(name= "**Joined**", value = joined_at  , inline = True)
      embed.add_field(name= "**Registered**", value = created_at  , inline = True)
      embed.add_field(name= f"**Roles**[{no_of_roles}]", value = roles  , inline = False)
      embed.add_field(name= "**Permissions**", value = permission  , inline = False)
      embed.set_thumbnail(url=user.avatar_url)
      embed.set_footer(text = f"ID: {user.id}")
      await ctx.send(embed=embed)
    
    @commands.command(aliases=["si"], no_pm=True)
    async def serverinfo(self, ctx):
        guild = ctx.guild
        online = len([m.status for m in guild.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(guild.members)
        total_bots = len([member for member in guild.members if member.bot == True])
        total_humans = total_users - total_bots
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        passed = (ctx.message.created_at - guild.created_at).days
        created_at = ("Since {}. Over {} days ago!"
                      "".format(guild.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        embed = discord.Embed(description=created_at, colour=discord.Colour.blue())
        embed.add_field(name="Region", value=str(guild.region))
        embed.add_field(name="Online Users", value="{}/{}".format(online, total_users))
        embed.add_field(name="Humans", value=total_humans)
        embed.add_field(name="Bots", value=total_bots)
        embed.add_field(name="Text Channels", value=text_channels)
        embed.add_field(name="Voice Channels", value=voice_channels)
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.add_field(name="Owner", value=str(guild.owner))
        embed.set_footer(text=f"Guild ID:{str(guild.id)}")

        if guild.icon_url:
            embed.set_author(name=guild.name, url=guild.icon_url)
            embed.set_thumbnail(url=guild.icon_url)
        else:
            embed.set_author(name=guild.name)

        await ctx.send(embed=embed)



    @commands.command()
    async def about(self, ctx):
        embed = discord.Embed(title="About", description=None )
        embed.add_field(name="Falc", value="Falc was originally thought of by GoldLion and once the code was written, they got me, the Co-Owner, The Untraceable to rewrite the entire bot. To pay respects to The Untraceable for spending her 3 weeks in hell rewriting confusing code, feel free to invite her bot [here](https://dsc.gg/security). 3 Weeks. The goal of the bot is one thing; to be recognised anywhere and everywhere.")
        await ctx.send(embed=embed)

    @commands.command()
    async def updates(self, ctx):
        embed = discord.Embed(title="Whats New or Coming Soon!", description=None )
        embed.add_field(name="Update 2.0", value="``Entire bot has been rewrote, you probably lost your data but it's alright, because everyone probably has, anyways that's all, I'll add more updates later.```")
        embed.add_field(name="Coming Soon: Update 1.4", value="```Soon, the timer will be integrated with the giveaway command so that you can see the amount of time left on your giveaway!```")
        await ctx.send(embed=embed)

    @commands.command(aliases=['prefix'], brief=" | Change the prefix for the bot")
    async def setprefix(self, ctx, *, prefixset):
        prefixlist = prefixset.replace(" ", ",")
        if (not ctx.author.guild_permissions.manage_channels):
            await ctx.send('This command requires ``Manage Channels``')

        else:
            check = await self.client.prefixes.find_one({"guildID" : ctx.guild.id})
            if check:
                await self.client.prefixes.update_one({"guildID" : ctx.guild.id},{"$addToSet" : {"prefixes" : prefixset}})
            else:
                await self.client.prefixes.insert_one({
                    "guildID" : ctx.guild.id,
                    "prefixes" : [prefixset]
                },upsert=False)
            await ctx.send(f'The bots prefix has been changed to {prefixset}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed = discord.Embed(description = f"You seem to be missing some arguments Error: {error}", color=ctx.author.color))

    @commands.command()
    async def vote(self, ctx):
          embed=discord.Embed(title="Vote for Falc", colour=discord.Colour.red())
          embed.add_field(name="__top.gg__", value="[Vote Now!](https://top.gg/bot/790525985266597918/vote)",  inline=False)
          embed.add_field(name="__discordbotlist.com__", value="[Vote Now!](https://discordbotlist.com/bots/falc/upvote)", inline=False)
          embed.add_field(name="__botsfordiscord.com__", value="[Vote Now!](https://botsfordiscord.com/bot/790525985266597918/vote)", inline=False)
          embed.add_field(name="__discordbots.gg__", value="[Vote Now!](https://discord.bots.gg/bots/790525985266597918)", inline=False)
          embed.add_field(name="__infinitybotlist.com__", value="[Vote Now!](https://infinitybotlist.com/bots/790525985266597918/vote)", inline=False)
          embed.add_field(name="discordlist.space.com__", value="[Vote Now!](https://discordlist.space/bot/790525985266597918)", inline=False)

          await ctx.send(embed=embed)


    @commands.command(name='membercount', aliases=['memcount', "mc"])
    async def guild_member_count(self, ctx):
        bots = 0

        for member in ctx.guild.members:
            if member.bot:
                bots += 1

        embed = discord.Embed(title=f'Member Count of {ctx.guild}',
                      description=f'**Humans:** {len(ctx.guild.members) - bots}\n**Bots:** {bots}\n**Total:** {len(ctx.guild.members)}', color=random.randint(0x000000, 0xFFFFFF))
        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)


    @commands.command(alias=["botinfo", "info"])
    async def bot(self, ctx):
        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 2)
        servers = str(len(self.client.guilds))
        users = 0
        for guild in self.client.guilds:
            users += len(guild.members)
        channels = str(len(set(self.client.get_all_channels())))
        em = discord.Embed(Title="Falc's Stats", colour=discord.Colour(value=0x36393e))
        em.add_field(name="Guild Count:", value=servers, inline=True)
        em.add_field(name="Total Users:",value=str(users), inline=True)
        em.add_field(name="Channels:",value=channels, inline=True)
        em.add_field(name="Python Version:", value="3.8.5", inline=True)
        em.add_field(name="Discord.py Version:", value="1.7.2", inline=True)
        em.add_field(name="Developer:", value="<@!489682676157120513> and <@!507969622876618754>", inline=True)
        em.add_field(name="Uptime:", value=f"**{days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} seconds**", inline=True)
        await ctx.send(embed=em)

    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.command(aliases = ["rrole"])
    async def removerole(self, ctx, user : discord.Member, *, role : discord.Role):
        if ctx.author.top_role >= user.top_role or ctx.author == ctx.guild.owner:
            try:
                await user.remove_roles(role)
            except:
                return await ctx.send("Could not remove that role from that member!")
            msg = await ctx.send(f"**The `{role}` role was removed from {user.mention}**")
            await msg.add_reaction(":white_check_mark:")


    @commands.command()
    async def codeblock(self, ctx, *, msg):
        await ctx.send("```LANG\n\n\```")
    @commands.command()
    @commands.guild_only()
    async def mods(self, ctx):

        message = ""
        all_status = {
            "online": {"users": [], "emoji": "🟢"},
            "idle": {"users": [], "emoji": "🟡"},
            "dnd": {"users": [], "emoji": "🔴"},
            "offline": {"users": [], "emoji": "⚫"}
        }

        for user in ctx.guild.members:
            user_perm = ctx.channel.permissions_for(user)
            if user_perm.kick_members or user_perm.ban_members:
                if not user.bot:
                    all_status[str(user.status)]["users"].append(f"**{user}**")

        for g in all_status:
            if all_status[g]["users"]:
                message += f"{all_status[g]['emoji']} {', '.join(all_status[g]['users'])}\n"

        await ctx.send(f"Mods in **{ctx.guild.name}**\n{message}")

    @commands.command(aliases=["icon", "servericon"])
    async def server_icon(self, ctx):
        if not ctx.guild.icon:
            return await ctx.send("This server does not have an icon")
        await ctx.send(f"Icon of **{ctx.guild.name}**\n{ctx.guild.icon_url_as(size=1024)}")

    @commands.command(name="banner", aliases=["serverbanner"])
    async def server_banner(self, ctx):
        if not ctx.guild.banner:
            return await ctx.send("This server does not have a banner")
        await ctx.send(f"Banner of **{ctx.guild.name}**\n{ctx.guild.banner_url_as(format='png')}")

    @commands.command()
    async def credits(self, ctx):
      await ctx.send("Credits to: NightZan#9999 for my ticket system, billyeatcookies#0173 for the among us mini game. Not to forget, the person I owe the most to, Nirlep_5252_#0001. Thanks for your games command. Another thank to The Untraceable#4852 for rewriting the entire bot, you're a Co-Owner so yay. If you think that your name should be here, please dont hesitate to dm me (@GoldLion#8190)")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['covid-19', 'covid19'])
    async def covid(self, ctx, *, countryName = None):
        try:
            if countryName is None:
                await ctx.send(f"You didn't enter a country name, use the command like this - `f!covid <country>`")
            else:
                url = f"https://coronavirus-19-api.herokuapp.com/countries/{countryName.lower()}"
                stats = await self.session.get(url)
                json_stats = await stats.json()
                country = json_stats["country"]
                totalCases = json_stats["cases"]
                todayCases = json_stats["todayCases"]
                totalDeaths = json_stats["deaths"]
                todayDeaths = json_stats["todayDeaths"]
                recovered = json_stats["recovered"]
                active = json_stats["active"]
                critical = json_stats["critical"]
                casesPerOneMillion = json_stats["casesPerOneMillion"]
                deathsPerOneMillion = json_stats["deathsPerOneMillion"]
                totalTests = json_stats["totalTests"]
                testsPerOneMillion = json_stats["testsPerOneMillion"]

                embed2 = discord.Embed(title = f"**COVID - 19 Status of {country}**", description = f"This information isn't always live, so it may not be accurate.", color =  0xFFA500)
                embed2.add_field(name = f"Total Cases", value = f"{totalCases}", inline = True)
                embed2.add_field(name = f"Today Cases", value = f"{todayCases}", inline = True)
                embed2.add_field(name = f"Total Deaths", value = f"{totalDeaths}", inline = True)
                embed2.add_field(name = f"Today Deaths", value = f"{todayDeaths}", inline = True)
                embed2.add_field(name = f"Recovered", value = f"{recovered}", inline = True)
                embed2.add_field(name = f"Active", value = f"{active}", inline = True)
                embed2.add_field(name = f"Critical", value = f"{critical}", inline = True)
                embed2.add_field(name = f"Cases Per One Million", value = f"{casesPerOneMillion}", inline = True)
                embed2.add_field(name = f"Deaths Per One Million", value = f"{deathsPerOneMillion}", inline = True)
                embed2.add_field(name = f"Total Tests", value = f"{totalTests}", inline = True)
                embed2.add_field(name = f"Tests Per One Million", value = f"{testsPerOneMillion}", inline = True)
                embed2.set_thumbnail(url = "https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
                await ctx.send(embed = embed2)
        except:
            await ctx.send("Invalid country name or API error. Please try again.")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def embed(self, ctx, *, arg=None):
        async def send_error_msg():
            await ctx.send(f"Invalid args! Correct usage is `{ctx.prefix}embed <#hexcolor> | <title> | <description>`")

        if arg == None:
            await send_error_msg()
            return
        if arg.count(" | ") != 2:
            await send_error_msg()
            return

        try:
            args = arg.split(" | ")
            col = int(args[0][1:], 16)
            title = args[1]
            desc = args[2]
            e = discord.Embed(
                title=title,
                description=desc,
                color=col
            )
            await ctx.send(embed=e)
        except:
            await send_error_msg()



    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=["atc", "aes"])
    async def aesthetic(self, ctx, *, args=None):
        if args == None:
            await ctx.send(f"Invalid args. Correct usage: `{ctx.prefix}atc <msg> | [mode]`. Mode can be b (bold), i (italic), or n (none).")
            return

        if args.count(" | ") == 0:
            m = "n"
        else:
            m = args[-1]

        s = ""
        if m == "b":
            s += "**"
        elif m == "i":
            s += "_"

        msg = "".join(args.split(" | ")[0])
        args = args.split(" | ")[:-1]
        for c in msg:
            s += c + " "
        if m == "b":
            s += "**"
        elif m == "i":
            s += "_"

        await ctx.reply(s)

    @commands.command()
    async def invites(self, ctx, user:discord.Member=None):
        if user is None:
            total_invites = 0
            for i in await ctx.guild.invites():
                if i.inviter == ctx.author:
                    total_invites += i.uses
            await ctx.send(f"You've invited {total_invites} member{'' if total_invites == 1 else 's'} to the server!")
        else:
            total_invites = 0
            for i in await ctx.guild.invites():
                member = ctx.message.guild.get_member_named(user)
                if i.inviter == member:
                    total_invites += i.uses

            await ctx.send(f"{user} has invited {total_invites} member{'' if total_invites == 1 else 's'} to the server!")

    @commands.command()
    async def messages(self, ctx, timeframe=7, channel: discord.TextChannel = None, *, user: discord.Member = None):
        if timeframe > 1968:
            await ctx.channel.send("Sorry. The maximum of days you can check is 1968.")
        elif timeframe <= 0:
            await ctx.channel.send("Sorry. The minimum of days you can check is one.")

        else:
            channel = channel or ctx.channel
            user = user or ctx.author
            async with ctx.channel.typing():
                msg = await ctx.send('Calculating...')
                await msg.add_reaction('🔎')

                counter = 0
                async for message in channel.history(limit=5000, after=datetime.today() - timedelta(days=timeframe)):
                    if message.author.id == user.id:
                        counter += 1

                await msg.remove_reaction('🔎', member=message.author)

                if counter >= 5000:
                    await msg.edit(content=f'{user} has sent over 5000 messages in the channel "{channel}" within the last {timeframe} days!')
                else:
                    await msg.edit(content=f'{user} has sent {str(counter)} messages in the channel "{channel}" within the last {timeframe} days.')


    @commands.command()
    async def emojis(self, ctx, msg: str = None):
        """List all emojis in this server."""
        emojis = ''
        for i in ctx.guild.emojis:
            emojis += str(i)
        await ctx.send(emojis)
        await ctx.message.delete()

    @commands.command(aliases = ["mentions"])
    @commands.bot_has_guild_permissions(read_message_history=True, read_messages=True)
    async def pings(self, ctx, limit : int=100, user: discord.Member = None):
        user = user or ctx.author
        counter = 0
        async for message in ctx.channel.history(limit=limit):
            if user in message.mentions:
                counter += 1
        await ctx.send('You have been pinged {} times in the last {} messages'.format(counter, limit))

    @commands.command()
    async def stats(self, ctx):
        em = discord.Embed(title=  "Stats about me", color = self.client.user.color, description = "My stats :partying_face:")
        em.add_field(name = "Users:", value = f"{len(self.client.users)}")
        em.add_field(name = "Servers:", value = f"{len(self.client.guilds)}")
        em.add_field(name = "Total Commands:", value = f"{len(self.client.commands)}")
        em.add_field(name = "Channels:", value = f"{len(self.client.channels)}")
        await ctx.send(embed = em)

    @commands.command(aliases = ["ci"])
    async def channelinfo(self, ctx, channel : discord.TextChannel = None):
        channel = channel or ctx.channel
        em = discord.Embed(title = f"Info about {channel.name}", color = ctx.author.color, description = f"Here is an insight into {channel.mention}")
        em.add_field(name = "ID:", value = f"`{channel.id}`")
        em.add_field(name = "Name:", value = f"`{channel.name}`")
        em.add_field(name = "Server it belongs to:", value = f"{channel.guild.name}", inline = True)

        try:
            em.add_field(name = "Category ID:", value = f"`{channel.category_id}`", inline = False)
        except:
            pass
        em.add_field(name = "Topic:", value = f"`{channel.topic}`")
        em.add_field(name = "Slowmode:", value = f"`{channel.slowmode_delay}`", inline = True)

        em.add_field(name = "People who can see the channel:", value = f"`{len(channel.members)}`", inline = False)
        em.add_field(name = "Is NSFW:", value = f"`{channel.is_nsfw()}`")
        em.add_field(name = "Is News:", value = f"`{channel.is_news()}`", inline = True)

        em.set_footer(text = "invite me ;)", icon_url = ctx.author.avatar_url)
        em.set_thumbnail(url = str(ctx.guild.icon_url))
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em)

    @commands.command(aliases=["ri","role"])
    async def roleinfo(self, ctx, *, role: discord.Role = None):
        if role is None:
            return await ctx.send("Please provide a valid role")
        em = discord.Embed(title = f"Info about {role.name}", color = ctx.author.color, description = f"Here is an insight into {role.mention}")
        em.add_field(name = "ID:", value = f"`{role.id}`")
        em.add_field(name = "Name:", value = f"`{role.name}`")
        em.add_field(name = "Server it belongs to:", value = f"{role.guild.name}", inline = True)

        em.add_field(name = "Hoisted:", value = f"`{role.hoist}`")
        em.add_field(name = "Managed by extension:", value = f"`{role.managed}`", inline = True)
        em.add_field(name = "Boost Role:", value = f"`{role.is_premium_subscriber()}`", inline = True)

        em.add_field(name = "Mentionable:", value = f"`{role.mentionable}`" )
        em.add_field(name = "Is Default:", value = f"`{role.is_default()}`", inline = True)
        em.add_field(name = "Bot Role:", value = f"`{role.is_bot_managed()}`", inline = True)

        em.add_field(name = "Color:", value = f"{role.color}")
        em.add_field(name = "Created At:", value = f"{role.created_at}", inline = True)
        em.add_field(name = "People with it:", value =f"{len(role.members)}", inline = True)
        msg = "```diff\n"
        if role.permissions.administrator:
            msg += "+ Administrator\n"
        else:
            msg += "- Administrator\n"
        if role.permissions.manage_guild:
            msg += "+ Manage Server\n"
        else:
            msg += "- Manage Server\n"
        if role.permissions.mention_everyone:
            msg += "+ Ping Everyone\n"
        else:
            msg += "- Ping Everyone\n"
        if role.permissions.manage_roles:
            msg += "+ Manage Roles\n"
        else:
            msg += "- Manage Roles\n"
        if role.permissions.manage_channels:
            msg += "+ Manage Channels\n"
        else:
            msg += "- Manage Channels\n"
        if role.permissions.ban_members:
            msg += "+ Ban Members\n"
        else:
            msg += "- Ban Members\n"
        if role.permissions.kick_members:
            msg += "+ Kick Members\n"
        else:
            msg += "- Kick Members\n"
        if role.permissions.view_audit_log:
            msg += "+ View Audit Log\n"
        else:
            msg += "- View Audit Log\n"
        if role.permissions.manage_messages:
            msg += "+ Manage Messages\n"
        else:
            msg += "- Manage Messages\n"
        if role.permissions.add_reactions:
            msg += "+ Add Reactions\n"
        else:
            msg += "- Add Reactions\n"
        if role.permissions.view_channel:
            msg += "+ Read Messages\n"
        else:
            msg += "- Read Messages\n"
        if role.permissions.send_messages:
            msg += "+ Send Messages\n"
        else:
            msg += "- Send Messages\n"
        if role.permissions.embed_links:
            msg += "+ Embed Links\n"
        else:
            msg += "- Embed Links\n"
        if role.permissions.read_message_history:
            msg += "+ Read Message History\n"
        else:
            msg += "- Read Message History\n"
        if role.permissions.view_guild_insights:
            msg += "+ View Guild Insights\n"
        else:
            msg += "- View Guild Insights\n"
        if role.permissions.connect:
            msg += "+ Join VC\n"
        else:
            msg += "- Join VC\n"
        if role.permissions.speak:
            msg += "+ Speak in VC\n"
        else:
            msg += "- Speak in VC\n"

        if role.permissions.change_nickname:
            msg += "+ Change Nickname\n"
        else:
            msg += "- Change Nickname\n"

        if role.permissions.manage_nicknames:
            msg += "+ Manage Nicknames\n"
        else:
            msg += "- Manage Nicknames\n"

        if role.permissions.manage_webhooks:
            msg += "+ Manage Webhooks\n"
        else:
            msg += "- Manage Webhooks\n"

        if role.permissions.manage_emojis:
            msg += "+ Manage Emojis\n"
        else:
            msg += "- Manage Emojis\n"


        msg += "\n```"
        em.add_field(name = "Permissions:", value = msg, inline = False)

        em.set_footer(text = "invite me ;)", icon_url = ctx.author.avatar_url)
        em.set_thumbnail(url = str(ctx.guild.icon_url))
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = em)

    @commands.command()
    async def enlarge(self, ctx,emoji : discord.Emoji = None):
        if emoji == None:
            await ctx.send("You need to enter an emoji next to the command smh")
        try:
            e = discord.Embed(title="Enalrged Emoji:")
            e.set_image(url=f"{emoji.url}")
            await ctx.send(embed=e)
        except:
            await ctx.send("You cannot enlarge text ")

    @commands.command()
    @commands.guild_only()
    async def pressf(self, ctx, user : discord.User=None):
        """Pay Respects by pressing f"""

        author = ctx.author
        if ctx.channel.id in self.messager or ctx.channel.id in self.messagem:
            return await ctx.send("Oops! I'm still paying respects in this channel, you'll have to wait until I'm done.")

        if user:
            answer = user.display_name
        else:
            await ctx.send("What do you want to pay respects to?")
            try:
                message = await self.client.wait_for('message', timeout=120, check = lambda message : message.author == ctx.author and message.channel == ctx.channel)
            except asyncio.TimeoutError:
                return await ctx.send("You took too long to reply.")

            answer = message.content

        message = await ctx.send("Everyone, let's pay respects to **{}**! Press f reaction on this message to pay respects.".format(answer))

        try:
            await message.add_reaction("<:f_key:585955067010744320>")
            self.messager[ctx.channel.id] = []
            react = True
        except:
            self.messagem[ctx.channel.id] = []
            react = False
            await message.edit(message, "Everyone, let's pay respects to **{}**! Type `f` reaction on the this message to pay respects.".format(answer))
            await self.client.wait_for('message',check = lambda message :  message.channel == ctx.channel)
        await asyncio.sleep(120)
        await message.delete()
        if react:
            amount = len(self.messager[ctx.channel.id])
        else:
            amount = len(self.messagem[ctx.channel.id])

        await ctx.send("**{}** {} paid respects to **{}**.".format(amount, "person has" if amount == 1 else "people have", answer))

        if react:
            del self.messager[ctx.channel.id]
        else:
            del self.messagem[ctx.channel.id]
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id == self.client.user.id:
            return
        if reaction.message.channel.id not in self.messager:
            return
        if user.id not in self.messager[reaction.message.channel.id]:
            if str(reaction.emoji) == "<:f_key:585955067010744320>":
                await reaction.message.channel.send( "**{}** has paid respects.".format(user.display_name))
                self.messager[reaction.message.channel.id].append(user.id)
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id not in self.messagem:
            return
        if message.author.id not in self.messagem[message.channel.id]:
            if message.content.lower() == "f":
                await message.channel.send("**{}** has paid respects.".format(message.author.display_name))
                self.messagem[message.channel.id].append(message.author.id)

    @commands.command()
    @commands.has_permissions(manage_webhooks=True)
    async def webhook_send(ctx, channel: discord.TextChannel, *, msg):
        await ctx.send('Done!')
        webhooks = await channel.webhooks()
        webhook = utils.get(webhooks, name = ctx.author.name)
        if webhook is None:
            webhook = await channel.create_webhook(name = ctx.author.name)
        await webhook.send(msg, username = ctx.author.name, avatar_url = ctx.author.avatar_url)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx) :
        '''Gets a list of all banned users '''
        users = await ctx.guild.bans()
        if len(users) > 0 :
            msg = f'`{"ID":21}{"Name":25} Reason\n'
            for entry in users :
                userID = entry.user.id
                userName = str(entry.user)
                reason = str(entry.reason)  # Could be None
                msg += f'{userID:<21}{userName:25} {reason}\n'
            embed = discord.Embed(color=0xe74c3c)  # Red
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f'Server: {ctx.guild.name}')
            embed.add_field(name='Ranks', value=msg + '`', inline=True)
            return await ctx.send(embed=embed)
        return await ctx.send('**:negative_squared_cross_mark:** There arent banned people!')

    @commands.command(aliases=["id"], brief="ID")
    @commands.guild_only()
    @commands.cooldown(2, 2, commands.BucketType.user)
    async def userid(self, ctx, member: discord.Member = None):
        """Get a members Discord id."""

        member = member or ctx.author

        embed = discord.Embed(
            title=f"{member.display_name}'s ID:",
            description=f"{member.id}",
            color=0x0EC2E1,
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['createinvite', 'generateinvite'])
    @commands.has_permissions(create_instant_invite=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def makeinvite(self, ctx, channel = None, max_age=0, max_uses=0, temporary=False, *, reason=None):
        """Make an invite for the current channel (if none is specified).  Takes in max_age (int, days), max_uses (int),  temporary membership (True/False), and a reason for creation.  Cooldown: 30 seconds"""
        try:
          if not channel:
            channel = ctx.channel.mention
          try:
            c_id = int(channel[2:-1])
          except:
            embed = discord.Embed(title="Invalid Embed Value(s)", value=f"You didn't mention a channel properly! Do it like this   {ctx.channel.mention} next time.",color=0xff0000)
            await ctx.send(embed=embed)
            return
          chnl = self.client.get_channel(c_id)
          if not chnl:
            chnl = ctx.channel
          inv = await chnl.create_invite(max_age=max_age, max_uses=max_uses, temporary=temporary, reason=reason)
          embed = discord.Embed(title="Invite Creation Successful", value=f"Your invite was created!  Check it out here:   {inv}",color=0x51ff00)
          await ctx.send(embed=embed)
        except:
          embed = discord.Embed(title="Invite Creation Failed", value="Please check to make sure your values are valid.  (**max_age** and **max_uses** should be an int >= 0, **temporary** should be True or False, and **reason**   should be a str.",color=0xff0000)
          await ctx.send(embed=embed)


    @commands.command()
    async def time(self, ctx, name=""):
        check = 1
        aest = ["aest", "tt", "equus", "ivy"]
        est = ["est", "lime", "carl", "mental", "wale", "wubba", "rubik", "shin'a", "shina", "yasu", "oishi", "fluffy", "bb", "batsy", "pumpkin", "deb", "peri", "shadow"]
        pst = ["pst", "memes", "twg", "zamas", "ded", "merc"]
        cst = ["cst", "satan", "red", "jay", "idc", "brush", "haiku", "chickaen", "septa", "arc", "rac", "ayia"]
        name = name.lower()
        if name in est:
            tz = pytz.timezone('US/Eastern')
        elif name in cst:
            tz = pytz.timezone('US/Central')
        elif name in aest:
            tz = pytz.timezone('Australia/NSW')
        elif name == "tomer":
            tz = pytz.timezone('Israel')
        elif name in pst:
            tz = pytz.timezone('PST8PDT')
        elif name == "octo":
            tz = pytz.timezone('MST7MDT')
        elif name == "acoustic":
            tz = pytz.timezone('Singapore')
        elif name == "jake":
            tz = pytz.timezone("Pacific/Auckland")
        elif name == "sma":
            tz = pytz.timezone('Asia/Singapore')
        elif name == "mlg":
            tz = pytz.timezone('WET')
        elif name == "rigin":
            tz = pytz.timezone('America/Fortaleza')
        elif name =="green":
            tz = pytz.timezone('Europe/Amsterdam')
        elif name == "marco":
            tz = pytz.timezone('Asia/Novosibirsk')
        elif name == "ash":
            tz = pytz.timezone('US/Hawaii')
        elif name == "steven":
            tz = pytz.timezone("Asia/Seoul")
        elif name == "ist":
            tz = pytz.timezone("Asia/Kolkata")
        else:
            await ctx.send("Invalid Name")
            return
        today = datetime.datetime.now(tz)
        await ctx.send(today.strftime("%d-%m-%Y | %I:%M:%S %p"))

    @commands.command(name='randcolour',
                      aliases=['randcolor'])
    async def randcolour(self, ctx):
        hexval = [ '0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F',]
        msg = ''.join(random.choices(hexval, k=6))
        await ctx.send('#' + msg)



def setup(client):
  client.add_cog(Utilities(client))