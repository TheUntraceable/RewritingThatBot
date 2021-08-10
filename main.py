import discord
import json
from discord.ext import commands
import random
import os
import asyncio
from datetime import datetime
import aiohttp
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()
cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://untraceable:mKFDsMJBzDmlebNr@database.s6qen.mongodb.net/database?retryWrites=true&w=majority")
db  = cluster["discord"]["prefixes"]

async def get_prefix(client, message):
    data = await db.find_one({"guildID" : message.guild.id})
    prefix = data["prefix"] if data["prefix"] is not None else "f!"
    return prefix

client = commands.AutoShardedBot(command_prefix=get_prefix,allowed_mentions=discord.AllowedMentions(roles=False,users=True,replied_user=True,everyone=False), intents = discord.Intents.all(), case_insensitive=True,shard_count=15)

class UserHasBeenBlacklisted(commands.CommandError):
    pass

client.afk  = cluster["discord"]["afk"]
client.userphone = cluster["discord"]["userphone"]
client.prefixes = cluster["discord"]["prefixes"]
client.bdays = cluster["discord"]["bdays"]
client.blacklist = cluster["discord"]["blacklist"]
client.welcome = cluster["discord"]["welcome"]
client.auto_role = cluster["discord"]["autorole"]
client.leave = cluster["discord"]["leave"]
client.warns = cluster["discord"]["warns"]
client.economy = cluster["discord"]["economy"]
client.levels_cooldown = cluster["discord"]["levels_cooldown"]
client.guild_levels = cluster["discord"]["guild_levels"]
client.levelling = cluster["discord"]["levelling"]
client.nqn = cluster["discord"]["nqn"]
client.reactroles = cluster['discord']['reactroles']
client.tickets = cluster['discord']['tickets']
client.remove_command("help")

@client.command()
@commands.is_owner()
async def MoveToMongo(ctx):
    with open("./DontKnowWhatToDoWith/prefixes.json","r") as f:
        data = json.load(f)
    prefixes = []
    async with ctx.typing():
        for guild,prefix in data:
            existing = await client.prefixes.find_one({
                "guildID" : guild
            })
            
            prefixes.append(prefix)
            
            if not existing:
                await client.prefixes.insert_one({
                    "guildID" : int(guild),
                    "prefixes" : [  prefixes]
                })
        await ctx.send("Uploaded all prefixes to MongoDB")
@client.event
async def on_guild_join(guild):
    await client.prefixes.insert_one({"guildID": guild.id,"prefix" : ["f!"] })
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title="❌ Member not found!", name="Enter a valid member", colour=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(title=f'❌ I do not have permission to do this! {error}', colour=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandOnCooldown):
        msg = 'This command on cooldown please try again in {:.2f}s!'.format(
        error.retry_after)
        await ctx.send(msg)
    elif isinstance(error,UserHasBeenBlacklisted):
        return await ctx.send("You have been blacklisted by GoldLion.")
    else:
        raise error

@client.event
async def on_message(message):
    if message.author.bot:
        return
    data = await client.prefixes.find_one({"guildID" : message.guild.id}) 
    pre = data["prefix"] if data["prefix"] != None else "f!"
    if client.user.mentioned_in(message):
        embed = discord.Embed(title=f"Need some help?", description= f"Use the following for help:\n`{pre}help`\nThe prefix for this server is:\n`{pre}`\nIf you would like to change the prefix, use `{pre}setprefix <prefix>`",
        color = discord.Colour.blue())
        await message.channel.send(embed=embed)
    brooklyn_99_quotes = [
        'Im the human form of the 💯 emoji.',
        'B\'mngpot!',
        'Hello, unsolved case. Do you bring me joy? No, because you’re boring and you’re too hard. See ya.',
        'I dont want to hang out with some stupid baby whos never met Jake.',
        'Fine but in protest Im walking over there extremely slowly!',
        'Title of your sex tape.',
        'Sarge, with all due respect, I am gonna completely ignore everything you just said.',
        'The English language can not fully capture the depth and complexity of my thoughts, so I’m incorporating emojis into my speech to better express myself. Winky face.',
        'Captain Wuntch, good to see you. But if you’re here, who’s guarding Hades?',
        'Captain? The kids want to know where Paulie the Pigeon is. I told them he got sucked up into an airplane engine. Is that all right?',
        'Cool. Cool cool cool cool cool cool cool, '
        'no doubt no doubt no doubt no doubt.',
    ]

    if message.content == 'ninenine':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
    data = await client.blacklist.find_one({"_id" : message.author.id})
    blacklisted = await client.blacklist.find_one({"memberID":message.author.id})
    if blacklisted:
        raise UserHasBeenBlacklisted()

    await client.process_commands(message)


@client.command(name="rate", description="Rate something")
async def _rate(ctx, *, thing: commands.clean_content):
    rate_amount = random.randrange(0, 100)
    await ctx.reply(f"I'd rate `{thing}` a **{round(rate_amount, 4)} / 100**")


@client.command(name="cat", description="Get a cute cat picture")
async def _cat(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thecatapi.com/v1/images/search") as resp:
            r = await resp.json() 
            await session.close()
    print(r)
    cat_em = discord.Embed(title=':cat: Meow',colour=discord.Colour.blue())
    cat_em.set_image(url=f'{r[0]["url"]}')

    await ctx.reply(embed=cat_em)

@client.command(name="dog", description="Get an adorable dog picture")
async def _dog(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thedogapi.com/v1/images/search") as resp:
            r = await resp.json()
            await session.close()

    cat_em = discord.Embed(title=':dog: Woof',colour=discord.Colour.blue())
    cat_em.set_image(url=f'{r[0]["url"]}')

    await ctx.reply(embed=cat_em)


@client.command(name="panda", description="Get an super cute panda picture")
async def _panda(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://some-random-api.ml/img/panda") as resp:
            r = await resp.json()
            await session.close()
    cat_em = discord.Embed(title=':panda_face: aww',colour=discord.Colour.blue())
    cat_em.set_image(url=f'{r[0]["url"]}')

    await ctx.reply(embed=cat_em)

@client.command(name="fox", description="Get a fox picture")
async def _fox(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://some-random-api.ml/img/fox") as resp:
            r = await resp.json()
            await session.close()
        print(r)
    cat_em = discord.Embed(title='fox: what a cute fox!', colour=discord.Colour.blue())
    cat_em.set_image(url=f'{r[0]["link"]}')

    await ctx.reply(embed=cat_em)

@client.event
async def on_guild_remove(guild):
    await client.prefixes.delete_one({"guildID" : guild.id})

for fn in os.listdir('./cogs'):
    if fn.endswith('.py') and fn != 'global_functions.py' and fn != "discordlist.py":
        client.load_extension(f'cogs.{fn[:-3]}')


@client.command()
@commands.has_permissions(manage_messages=True)
async def announce(ctx, ch : discord.TextChannel = None):
    if ch == None:
        return await ctx.reply('Specify a channel')
    def check(m):
        return m.author == ctx.message.author and m.channel == ctx.message.channel

    await ctx.reply('Enter the title:')
    t = await client.wait_for('message', check=check, timeout=60)
    await ctx.reply('Enter the message:')
    msg = await client.wait_for('message', check=check, timeout=120)
    embed = discord.Embed(title = t.content, description = msg.content, color = 0xffff)
    embed.set_footer(text=f"{ctx.guild.name}")
    embed.set_author(name=f"{ctx.author}")
    await ch.send(embed = embed)


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.reply(f"Loaded {extension}")
@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.reload_extension(f'cogs.{extension}')
    await ctx.reply(f'Reloaded {extension}')
@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.reply(f'Unloaded {extension}')

@client.command()
@commands.is_owner()
async def check(ctx, cog_name):
    try:
        client.load_extension(f"cogs.{cog_name}")
    except commands.ExtensionAlreadyLoaded:
        await ctx.reply(f"{cog_name} is loaded.")
    except commands.ExtensionNotFound:
        await ctx.reply(f"{cog_name} was not found.")
    except commands.ExtensionNotLoaded:
        await ctx.reply(f"{cog_name} was unloaded.")
    except Exception as e:
        raise e


client.launch_time = datetime.utcnow()


@client.command(aliases = ["remind", "remindme", "remind_me"])
@commands.bot_has_permissions(attach_files = True, embed_links = True)
async def reminder(ctx, time, *, reminder):
    embed = discord.Embed(color=0x55a7f7)
    embed.set_footer(text=f"Falc", icon_url=f"{client.user.avatar_url}")
    seconds = 0
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Error, Invalid Duration',
                        value=f'Please use duration in s|m|h|d format.')
    elif seconds < 10:
        embed.add_field(name='Error',
                        value='You have specified a too short duration!\nMinimum duration is 10 seconds.')
    elif seconds > 7776000:
        embed.add_field(name='Error', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        await ctx.reply(f"Alright, I will remind you about `{reminder}` in {counter}.")
        await asyncio.sleep(seconds)
        await ctx.reply(f"Hey there {ctx.author.mention}, you asked me to remind you about `{reminder}` {counter} ago.")
        return
    await ctx.reply(embed=embed)

@reminder.error
async def reminder_error(ctx, error):
    data = await client.prefixes.find_one({"guildID" : ctx.guild.id})
    prefix = data["prefix"][0]
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(title='❌Error, missing required arguments:', description=f'{prefix}remind [Duration] [Reminder]', colour=discord.Colour.red())
        embed.add_field(name='Example:',value=f'{prefix}remind 10h play games')
        await ctx.reply(embed=embed)

@client.command(case_insensitive=True,
                aliases=['suggestion'],
                brief=" | Write your suggestions for the server here")
async def suggest(ctx, *, question=None):
    if question == None:
        await ctx.reply('Please write a suggestion!')
    else:
    
        embed = discord.Embed(title="New Suggestion!",
                              description=f"{question}")
        embed.set_footer(text=f"Suggested by {ctx.author.mention}")
        embed.timestamp = datetime.utcnow()

        await client.get_channel(831057920019136563).reply(embed=embed)

@client.command(aliases=['quit'])
@commands.is_owner()
async def shutdown(ctx):
    await ctx.reply('Shutting down the bot!')
    await client.logout()

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




@client.command()
@commands.is_owner()
async def dm(ctx, member: discord.Member = None, *, text = None):
    if not member:
        return await ctx.author.send("You didn't supply a member to DM that to.")
    if not text:
        return await ctx.author.send("I can't DM nothing.")
    await member.send(text)
    await ctx.channel.purge(limit=1)

@client.event
async def on_ready():
  print("READY")

@client.command()
async def face(ctx):
  FACES=[
    "¢‿¢",
    "©¿© o",
    "ª{•̃̾_•̃̾}ª",
    "¬_¬",
    "¯＼(º_o)/¯",
    "¯\\(º o)/¯",
    "¯\\_(⊙︿⊙)_/¯",
    "¯\\_(ツ)_/¯",
    "°ω°",
    "°Д°",
    "°‿‿°",
    "°ﺑ°",
    "´ ▽ ` )ﾉ",
    "¿ⓧ_ⓧﮌ",
    "Ò,ó",
    "ó‿ó",
    "ô⌐ô",
    "ôヮô",
    "ŎםŎ",
    "ŏﺡó",
    "ʕ•̫͡•ʔ",
    "ʕ•ᴥ•ʔ",
    "ʘ‿ʘ",
    "˚•_•˚",
    "˚⌇˚",
    "˚▱˚",
    "̿ ̿̿'̿'\\̵͇̿̿\\=(•̪●)=/̵͇̿̿/'̿̿ ̿ ̿ ̿",
    "͡° ͜ʖ ͡°",
    "Σ ◕ ◡ ◕",
    "Σ (ﾟДﾟ;)",
    "Σ(ﾟДﾟ；≡；ﾟдﾟ)",
    "Σ(ﾟДﾟ )",
    "Σ(||ﾟДﾟ)",
    "Φ,Φ",
    "δﺡό",
    "σ_σ",
    "д_д",
    "ф_ф",
    "щ（ﾟДﾟщ）",
    "щ(ಠ益ಠщ)",
    "щ(ಥДಥщ)",
    "Ծ_Ծ",
    "أ‿أ",
    "ب_ب",
    "ح˚௰˚づ",
    "ح˚ᆺ˚ว",
    "حᇂﮌᇂ)",
    "٩๏̯͡๏۶",
    "٩๏̯͡๏)۶",
    "٩◔̯◔۶",
    "٩(×̯×)۶",
    "٩(̾●̮̮̃̾•̃̾)۶",
    "٩(͡๏̯͡๏)۶",
    "٩(͡๏̯ ͡๏)۶",
    "٩(ಥ_ಥ)۶",
    "٩(•̮̮̃•̃)۶",
    "٩(●̮̮̃•̃)۶",
    "٩(●̮̮̃●̃)۶",
    "٩(｡͡•‿•｡)۶",
    "٩(-̮̮̃•̃)۶",
    "٩(-̮̮̃-̃)۶",
    "۞_۞",
    "۞_۟۞",
    "۹ↁﮌↁ",
    "۹⌤_⌤۹",
    "॓_॔",
    "१✌◡✌५",
    "१|˚–˚|५",
    "ਉ_ਉ",
    "ଘ_ଘ",
    "இ_இ",
    "ఠ_ఠ",
    "రృర",
    "ಠ¿ಠi",
    "ಠ‿ಠ",
    "ಠ⌣ಠ",
    "ಠ╭╮ಠ",
    "ಠ▃ಠ",
    "ಠ◡ಠ",
    "ಠ益ಠ",
    "ಠ益ಠ",
    "ಠ︵ಠ凸",
    "ಠ , ಥ",
    "ಠ.ಠ",
    "ಠoಠ",
    "ಠ_ృ",
    "ಠ_ಠ",
    "ಠ_๏",
    "ಠ~ಠ",
    "ಡ_ಡ",
    "ತಎತ",
    "ತ_ತ",
    "ಥдಥ",
    "ಥ‿ಥ",
    "ಥ⌣ಥ",
    "ಥ◡ಥ",
    "ಥ﹏ಥ",
    "ಥ_ಥ",
    "ಭ_ಭ",
    "ರ_ರ",
    "ಸ , ໖",
    "ಸ_ಸ",
    "ക_ക",
    "อ้_อ้",
    "อ_อ",
    "โ๏௰๏ใ ื",
    "๏̯͡๏﴿",
    "๏̯͡๏",
    "๏̯͡๏﴿",
    "๏[-ิิ_•ิ]๏",
    "๏_๏",
    "໖_໖",
    "༺‿༻",
    "ლ(´ڡ`ლ)",
    "ლ(́◉◞౪◟◉‵ლ)",
    "ლ(ಠ益ಠლ)",
    "ლ(╹◡╹ლ)",
    "ლ(◉◞౪◟◉‵ლ)",
    "ლ,ᔑ•ﺪ͟͠•ᔐ.ლ",
    "ᄽὁȍ ̪ őὀᄿ",
    "ᕕ( ᐛ )ᕗ",
    "ᕙ(⇀‸↼‶)ᕗ",
    "ᕦ(ò_óˇ)ᕤ",
    "ᶘ ᵒᴥᵒᶅ",
    "‘︿’",
    "•▱•",
    "•✞_✞•",
    "•ﺑ•",
    "•(⌚_⌚)•",
    "•_•)",
    "‷̗ↂ凸ↂ‴̖",
    "‹•.•›",
    "‹› ‹(•¿•)› ‹›",
    "‹(ᵒᴥᵒ­­­­­)›",
    "‹(•¿•)›",
    "ↁ_ↁ",
    "⇎_⇎",
    "∩(︶▽︶)∩",
    "∩( ・ω・)∩",
    "≖‿≖",
    "≧ヮ≦",
    "⊂•⊃_⊂•⊃",
    "⊂⌒~⊃｡Д｡)⊃",
    "⊂(◉‿◉)つ",
    "⊂(ﾟДﾟ,,⊂⌒｀つ",
    "⊙ω⊙",
    "⊙▂⊙",
    "⊙▃⊙",
    "⊙△⊙",
    "⊙︿⊙",
    "⊙﹏⊙",
    "⊙０⊙",
    "⊛ठ̯⊛",
    "⋋ō_ō`",
    "━━━ヽ(ヽ(ﾟヽ(ﾟ∀ヽ(ﾟ∀ﾟヽ(ﾟ∀ﾟ)ﾉﾟ∀ﾟ)ﾉ∀ﾟ)ﾉﾟ)ﾉ)ﾉ━━━",
    "┌∩┐(◕_◕)┌∩┐",
    "┌( ಠ_ಠ)┘",
    "┌( ಥ_ಥ)┘",
    "╚(•⌂•)╝",
    "╭╮╭╮☜{•̃̾_•̃̾}☞╭╮╭╮",
    "╭✬⌢✬╮",
    "╮(─▽─)╭",
    "╯‵Д′)╯彡┻━┻",
    "╰☆╮",
    "□_□",
    "►_◄",
    "◃┆◉◡◉┆▷",
    "◉△◉",
    "◉︵◉",
    "◉_◉",
    "○_○",
    "●¿●\\ ~",
    "●_●",
    "◔̯◔",
    "◔ᴗ◔",
    "◔ ⌣ ◔",
    "◔_◔",
    "◕ω◕",
    "◕‿◕",
    "◕◡◕",
    "◕ ◡ ◕",
    "◖♪_♪|◗",
    "◖|◔◡◉|◗",
    "◘_◘",
    "◙‿◙",
    "◜㍕◝",
    "◪_◪",
    "◮_◮",
    "☁ ☝ˆ~ˆ☂",
    "☆¸☆",
    "☉‿⊙",
    "☉_☉",
    "☐_☐",
    "☜ق❂Ⴢ❂ق☞",
    "☜(⌒▽⌒)☞",
    "☜(ﾟヮﾟ☜)",
    "☜-(ΘLΘ)-☞",
    "☝☞✌",
    "☮▁▂▃▄☾ ♛ ◡ ♛ ☽▄▃▂▁☮",
    "☹_☹",
    "☻_☻",
    "☼.☼",
    "☾˙❀‿❀˙☽",
    "♀ح♀ヾ",
    "♥‿♥",
    "♥╣[-_-]╠♥",
    "♥╭╮♥",
    "♥◡♥",
    "✌♫♪˙❤‿❤˙♫♪✌",
    "✌.ʕʘ‿ʘʔ.✌",
    "✌.|•͡˘‿•͡˘|.✌",
    "✖‿✖",
    "✖_✖",
    "❐‿❑",
    "⨀_⨀",
    "⨀_Ꙩ",
    "⨂_⨂",
    "〆(・∀・＠)",
    "《〠_〠》",
    "【•】_【•】",
    "〠_〠",
    "〴⋋_⋌〵",
    "の� �の",
    "ニガー? ━━━━━━(ﾟ∀ﾟ)━━━━━━ ニガー?",
    "ペ㍕˚\\",
    "ヽ(´ｰ｀ )ﾉ",
    "ヽ(๏∀๏ )ﾉ",
    "ヽ(｀Д´)ﾉ",
    "ヽ(ｏ`皿′ｏ)ﾉ",
    "ヽ(`Д´)ﾉ",
    "ㅎ_ㅎ",
    "乂◜◬◝乂",
    "凸ಠ益ಠ)凸",
    "句_句",
    "Ꙩ⌵Ꙩ",
    "Ꙩ_Ꙩ",
    "ꙩ_ꙩ",
    "Ꙫ_Ꙫ",
    "ꙫ_ꙫ",
    "ꙮ_ꙮ",
    "흫_흫",
    "句_句",
    "﴾͡๏̯͡๏﴿ O'RLY?",
    "¯\\(ºдಠ)/¯",
    "（·×·）",
    "（⌒Д⌒）",
    "（╹ェ╹）",
    "（♯・∀・）⊃",
    "（　´∀｀）☆",
    "（　´∀｀）",
    "（゜Д゜）",
    "（・∀・）",
    "（・Ａ・）",
    "（ﾟ∀ﾟ）",
    "（￣へ￣）",
    "（ ´☣///_ゝ///☣｀）",
    "（ つ Д ｀）",
    "＿☆（ ´_⊃｀）☆＿",
    "｡◕‿‿◕｡",
    "｡◕ ‿ ◕｡",
    "!⑈ˆ~ˆ!⑈",
    "!(｀･ω･｡)",
    "(¬‿¬)",
    "(¬▂¬)",
    "(¬_¬)",
    "(°ℇ °)",
    "(°∀°)",
    "(´ω｀)",
    "(´◉◞౪◟◉)",
    "(´ヘ｀;)",
    "(´・ω・｀)",
    "(´ー｀)",
    "(ʘ‿ʘ)",
    "(ʘ_ʘ)",
    "(˚இ˚)",
    "(͡๏̯͡๏)",
    "(ΘεΘ;)",
    "(ι´Д｀)ﾉ",
    "(Ծ‸ Ծ)",
    "(॓_॔)",
    "(० ्०)",
    "(ு८ு_ .:)",
    "(ಠ‾ಠ)",
    "(ಠ‿ʘ)",
    "(ಠ‿ಠ)",
    "(ಠ⌣ಠ)",
    "(ಠ益ಠ ╬)",
    "(ಠ益ಠ)",
    "(ಠ_ృ)",
    "(ಠ_ಠ)",
    "(ಥ﹏ಥ)",
    "(ಥ_ಥ)",
    "(๏̯͡๏ )",
    "(ღ˘⌣˘ღ) ♫･*:.｡. .｡.:*･",
    "(ღ˘⌣˘ღ)",
    "(ᵔᴥᵔ)",
    "(•ω•)",
    "(•‿•)",
    "(•⊙ω⊙•)",
    "(• ε •)",
    "(∩▂∩)",
    "(∩︵∩)",
    "(∪ ◡ ∪)",
    "(≧ω≦)",
    "(≧◡≦)",
    "(≧ロ≦)",
    "(⊙ヮ⊙)",
    "(⊙_◎)",
    "(⋋▂⋌)",
    "(⌐■_■)",
    "(─‿‿─)",
    "(┛◉Д◉)┛┻━┻",
    "(╥_╥)",
    "(╬ಠ益ಠ)",
    "(╬◣д◢)",
    "(╬ ಠ益ಠ)",
    "(╯°□°）╯︵ ┻━┻",
    "(╯ಊ╰)",
    "(╯◕_◕)╯",
    "(╯︵╰,)",
    "(╯3╰)",
    "(╯_╰)",
    "(╹◡╹)凸",
    "(▰˘◡˘▰)",
    "(●´ω｀●)",
    "(●´∀｀●)",
    "(◑‿◐)",
    "(◑◡◑)",
    "(◕‿◕✿)",
    "(◕‿◕)",
    "(◕‿-)",
    "(◕︵◕)",
    "(◕ ^ ◕)",
    "(◕_◕)",
    "(◜௰◝)",
    "(◡‿◡✿)",
    "(◣_◢)",
    "(☞ﾟ∀ﾟ)☞",
    "(☞ﾟヮﾟ)☞",
    "(☞ﾟ ∀ﾟ )☞",
    "(☼◡☼)",
    "(☼_☼)",
    "(✌ﾟ∀ﾟ)☞",
    "(✖╭╮✖)",
    "(✪㉨✪)",
    "(✿◠‿◠)",
    "(✿ ♥‿♥)",
    "(　・∀・)",
    "(　･ัω･ั)？",
    "(　ﾟ∀ﾟ)o彡゜えーりんえーりん!!",
    "(。・_・。)",
    "(つд｀)",
    "(づ｡◕‿‿◕｡)づ",
    "(ノಠ益ಠ)ノ彡┻━┻",
    "(ノ ◑‿◑)ノ",
    "(ノ_・。)",
    "(・∀・ )",
    "(屮ﾟДﾟ)屮",
    "(︶ω︶)",
    "(︶︹︺)",
    "(ﺧ益ﺨ)",
    "(；一_一)",
    "(｀・ω・´)”",
    "(｡◕‿‿◕｡)",
    "(｡◕‿◕｡)",
    "(｡◕ ‿ ◕｡)",
    "(｡♥‿♥｡)",
    "(｡･ω..･)っ",
    "(･ｪ-)",
    "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧",
    "(ﾟДﾟ)",
    "(ﾟДﾟ)y─┛~~",
    "(ﾟ∀ﾟ)",
    "(ﾟヮﾟ)",
    "(￣□￣)",
    "(￣。￣)",
    "(￣ー￣)",
    "(￣(エ)￣)",
    "( °٢° )",
    "( ´_ゝ｀)",
    "( ͡° ͜ʖ ͡°)",
    "( ͡~ ͜ʖ ͡°)",
    "( ಠ◡ಠ )",
    "( •_•)>⌐■-■",
    "( 　ﾟ,_ゝﾟ)",
    "( ･ิз･ิ)",
    "( ﾟдﾟ)､",
    "( ^▽^)σ)~O~)",
    "((((゜д゜;))))",
    "(*´д｀*)",
    "(*..Д｀)",
    "(*..д｀*)",
    "(*~▽~)",
    "(-’๏_๏’-)",
    "(-＿- )ノ",
    "(/◔ ◡ ◔)/",
    "(///_ಥ)",
    "(;´Д`)",
    "(=ω=;)",
    "(=゜ω゜)",
    "(>'o')>♥<('o'<)",
    "(n˘v˘•)¬",
    "(o´ω｀o)",
    "(V)(°,,°)(V)",
    "(\/) (°,,°) (\/) WOOPwoopwowopwoopwoopwoop!",
    "(^▽^)",
    "(`･ω･´)",
    "(~￣▽￣)~",
    "/╲/\\╭ºoꍘoº╮/\\╱\\",
    "<【☯】‿【☯】>",
    "= (ﾟдﾟ)ｳ",
    "@_@",
    "d(*⌒▽⌒*)b",
    "o(≧∀≦)o",
    "o(≧o≦)o",
    "q(❂‿❂)p",
    "y=ｰ( ﾟдﾟ)･∵.",
    "\\˚ㄥ˚\\",
    "\\ᇂ_ᇂ\\",
    "\\(ಠ ὡ ಠ )/",
    "\\(◕ ◡ ◕\\)",
    "^̮^",
    "^ㅂ^",
    "_(͡๏̯͡๏)_",
    "{´◕ ◡ ◕｀}",
    "{ಠ_ಠ}__,,|,",
    "{◕ ◡ ◕}",
  ]
  FACE=random.choice(FACES)
  await ctx.reply(FACE)
@commands.command(aliases=['flip', 'flipping'])
async def flip_command(self,ctx):
    try:
        cancel = False
        EmbedHead = discord.Embed(
            description='What you choose? (Heads/Tails)', color=random.randint(0, 0xffffff))
        EmbedHead.set_footer(text='You have 1 minute to choose!')
        headORtail = await ctx.reply(embed=EmbedHead)
        message = await client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
        if str(message.content.lower()) == 'heads':
            user_choose = message.content
            await message.delete()
            fliping = await ctx.reply('Flipping. ')
            await asyncio.sleep(0.4)
            await fliping.edit(content='Flipping.. ')
            await asyncio.sleep(0.5)
            await fliping.edit(content='Flipping... ')
            chooses = ['heads', 'tails']
            random_select = random.choice(chooses)
            await fliping.delete()
            if user_choose == random_select:
                await headORtail.delete()
                choose_embed = discord.Embed(color=0x2ecc71)
                choose_embed.add_field(
                    name='You Chose :bust_in_silhouette:', value=f'**{user_choose}**', inline=True)
                choose_embed.add_field(
                    name='Falc Chose :robot:', value=f'**{random_select}**', inline=True)
                choose_embed.set_author(
                    name='You Win!', icon_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/259/check-mark-button_2705.png')
                await ctx.send(embed=choose_embed)
            else:
                await headORtail.delete()
                choose_embed = discord.Embed(color=0xe74c3c)
                choose_embed.add_field(
                    name='You Chose :bust_in_silhouette:', value=f'**{user_choose}**', inline=True)
                choose_embed.add_field(
                    name='Falc Chose :robot:', value=f'**{random_select}**', inline=True)
                choose_embed.set_author(
                    name='You Lose!', icon_url='https://images.emojiterra.com/mozilla/512px/274c.png')
                await ctx.send(embed=choose_embed)
        if str(message.content.lower()) == 'tails':
            user_choose = message.content
            await message.delete()
            fliping = await ctx.send(f'Flipping. ')
            await asyncio.sleep(1)
            await fliping.edit(content=f'Flipping.. ')
            await asyncio.sleep(1)
            await fliping.edit(content=f'Flipping... ')
            chooses = ['heads', 'tails']
            random_select = random.choice(chooses)
            await fliping.delete()
            if user_choose == random_select:
                choose_embed = discord.Embed(color=0x2ecc71)
                choose_embed.add_field(
                    name='You Chose :bust_in_silhouette:', value=f'**{user_choose}**', inline=True)
                choose_embed.add_field(
                    name='Falc Chose :robot:', value=f'**{random_select}**', inline=True)
                choose_embed.set_author(
                    name='You Win!', icon_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/259/check-mark-button_2705.png')
                choose_embed.set_footer(
                    text=ctx.author.name, icon_url=ctx.author.icon_url)
                await ctx.send(embed=choose_embed)
            else:
                choose_embed = discord.Embed(color=0xe74c3c)
                choose_embed.add_field(
                    name='You Chose :bust_in_silhouette:', value=f'**{user_choose}**', inline=True)
                choose_embed.add_field(
                    name='Falc Chose :robot:', value=f'**{random_select}**', inline=True)
                choose_embed.set_author(
                    name='You Lose!', icon_url='https://images.emojiterra.com/mozilla/512px/274c.png')
                choose_embed.set_footer(
                    text=ctx.author.name, icon_url=ctx.author.icon_url)
                await ctx.send(embed=choose_embed)
        else:
            try:
                cancel = True
                await headORtail.delete()
                temp_message = await ctx.send('You flip a coin not your mum. Choose **HEADS or TAILS**')
                await temp_message.delete(delay=2)
            except:
                pass
    except asyncio.TimeoutError:
        if not cancel:
            await headORtail.edit(content='Lucky for you I was made for my time to be wasted. Next time **respond**')




#response = requests.post(f'https://space-bot-list.xyz/api/bots/{489682676157120513}', headers = {"Authorization": "942292990d0fe954c70e539429ee8ac6e3cb55100bcfb798acb6b3046120c233f243b2417b6fe49e21303c2cac30860a", "Content-Type": "application/json"})
client.load_extension("jishaku")
client.run("ODUzNTkxOTg0NTU5MzU3OTcz.YMXnfA.tYiEulI20uGiqH8pF9mbyTaB4Zk")