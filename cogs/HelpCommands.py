import discord
from discord.ext import commands

class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(invoke_without_command=True)
    async def help(self, ctx, type=None):

      if type == None:
        em = discord.Embed(
            title="Falc Help",
            description=
            f"Thanks for using Falc!\nMy prefix is `{ctx.prefix}`\nIf you'd like to view all cogs and commands, run `{ctx.prefix}<command>`. If not, you can view a category's cogs and commands using `{ctx.prefix}help <Category>`.")
    
        em.add_field(name="<a:moderator:826953436481323008> | Moderation", 
                      value=f"`{ctx.prefix}help moderation`\nPowerful moderation tools.",
                      inline=True)
        em.add_field(name="<:image:841955288269848606> | Image",
                      value=f"`{ctx.prefix}help image`\nGenerate images, memes, and animals!",
                      inline=True)
        em.add_field(name="<a:fun:826468935494926376> | Fun",
                      value=f"`{ctx.prefix}help fun`\nSolo and group fun!",
                      inline=True)
        em.add_field(name="🎶 | Music",
                      value=f"`{ctx.prefix}help music`\nListen to music!",
                      inline=True)
        em.add_field(name="🧰 | Utilities",
                      value=f"`{ctx.prefix}help utility`\nTons of Utility Commands",
                      inline=True)
        #em.add_field(name="<:dankmemer:841916312501878804> | Dank Memer",
        #              value=f"`{ctx.prefix}help dankmemer`\nDank Memer Utility Commands",
        #              inline=True)
        em.add_field(name="<a:settings:841976945503371305> | Settings",
                      value=f"`{ctx.prefix}help settings`\nSettings configuration",
                      inline=True)
        em.add_field(name="<a:tada_ibl:817091472779116574> | Giveaways and Timers",
                      value=f"`{ctx.prefix}help giveaway`\nGiveaways and Timers",
                      inline=True)
        em.add_field(name="<:stonks_leveling:847133180166799390> | Leveling",
                      value=f"`{ctx.prefix}help leveling`\nLeveling and ranks",
                      inline=True)
        em.add_field(name="<a:DogeCoin:843783888937680916> | Economy",
                      value=f"`{ctx.prefix}help economy`\nPlay on the bot's economy!",
                      inline=True)
        em.add_field(name="Documentation",
                      value="You could also view the [Documentation](https://app.gitbook.com/@goldlion/s/fal/)",
                      inline=False)
        await ctx.send(embed=em)

      if str(type) == "utility":
        em = discord.Embed(title="Utility Commands")
        em.add_field(name=f"Run `{ctx.prefix}help <command>` for more info on each one.", value="`use` `react` `userinfo` `serverinfo` `roleinfo` `membercount` `giverole` `poll` `codeblock` `math` `add` `multiply` `divide` `subtract` `remainder` `power` `factorial` `mods` `servericon` `serverbanner` `covid` `embed` `invites` `messages` `emojis` `pings` `channelinfo` `enlarge` `userid` `bans` `createchannel` `deletechannel` `nuke` `createrole` `afk` `remind` `announce` `tickets` `snipe` `esnipe` `run` `selfdestruct` `reactionrole` `createcategory` `deletecatrgory` `emojiinfo`")
        await ctx.send(embed=em)

      elif str(type) == "moderation":
        em = discord.Embed(title="Moderation Commands")
        em.add_field(name=f"Run `{ctx.prefix}help <command>` for more info on each one.", value="`kick` `hackban` `softban` `unban` `nickset` `purge` `unmute` `mute` `slowmode` `lock` `unlock` `massnick` `botkick` `botban`")
        await ctx.send(embed=em)

      elif str(type) == "leveling":
        em = discord.Embed(title="Leveling Commands")
        em.add_field(name=f"Run `{ctx.prefix}help <command>` for more info on each one.", value="`levels` `levelupchannel` `rank` `leaderboard`")
        await ctx.send(embed=em)

      elif str(type) == "fun":
        em = discord.Embed(title="Fun Commands")
        em.add_field(name=f"Run `{ctx.prefix}help <command>` for more info on each one.",
        value=" `ai` `encode` `flip` `rockpaperscissors` `face` `ninenine` `8ball` `say` `ctr` `fakeban` `clap` `type` `tableflip` `howgay` `howsimp` `simpfor` `howstupid` `punch` `choose` `cuddle` `fight` `roast` `reverse` `spellout` `dice` `asktrump` `chat` `badjoke` `hotcalc` `beer` `rate` `password` `jebait` `mock` `advice` `quote` `hack` `coffee` `slurpjuice` `emojify` `lick` `slap` `fight` `hug` `kiss` `pat` `numberfact` `comic` `iq` `pp` `kill` `fight` `wide` `respect` `thank` `meme` `showerthought` `punchmachine` `weight` `boxingweight` `lifeexpectancy` `odds` `parents` `begrate` `fly` `stabrate` `wobbler`")
        em.add_field(name="Games", value="`tictactoe` `wumpus` `2048` `minesweeper` `aki` `amongus` `coinflip` `rockpaperscissors`")
        await ctx.send(embed=em)

      elif str(type) == "image":
        em = discord.Embed(title="Image Commands")
        em.add_field(name=f"Run `{ctx.prefix}help <command>` for more info on each one.",
         value="`wanted` `trash` `delete` `disability` `triggered` `affect` `rip` `stab` `bed` `shit` `fakenews` `spank` `comment` `youtube` `gay` `glass` `cat` `dog` `fox` `panda` `meme` `koala` `bird` `wasted` `greyscale` `slap` `pixilate` `admin` `team` `invert` `invertgreyscale` `brightness` `threshold` `red` `blue` `blurple` `green` `trumptweet` `changemymind` `deepfry` `clyde`")
        await ctx.send(embed=em)
        
      elif str(type) == "music":
        em = discord.Embed(title="Image Commands")
        em.add_field(name=f"Run `{ctx.prefix}help <command>` for more info on each one.", value="`play` `pause` `resume` `queue` `loop` `shuffle` `skip` `stop` `playing` `volume` `leave` `summon` `disconnect`")
        await ctx.send(embed=em)

      elif str(type) == "giveaway":
        em = discord.Embed(title="Image Commands")
        em.add_field(name=f"Run `{ctx.prefix}help <command>` for more info on each one.", value="`gstart` `gend` `reroll` `timer`")
        await ctx.send(embed=em)

      elif str(type) == "settings":
        em = discord.Embed(title="Configuration Commands")
        em.add_field(name=f"Run `{ctx.prefix}help <command>` for more info on each one.", value="`nqn` `levels` `setprefix` `autorole` `welcome` `welcomechannel` `leavemessage` `leavechannel` `enable` `disable`")
        await ctx.send(embed=em)

      elif str(type) == "tickets":
        em = discord.Embed(title="Ticket Commands")
        em.add_field(name=f"Run `{ctx.prefix}help <command>` for more info on each one.", value="`createticket` `addticketrole` `setticketlogs` `closeticket`")
        await ctx.send(embed=em)

      elif str(type) == "dankmemer":
        em = discord.Embed(title="Dank Memer Commands")
        em.add_field(name=f"Run `{ctx.prefix}help <command>` for more info on each one.", value="`multis` `taxcalc`")
        await ctx.send(embed=em)

      elif str(type) == "math":
        em = discord.Embed(title="Math Commands")
        em.add_field(name=f"Run `{ctx.prefix}help <command>` for more info on each one.", value="`add <a> <b>` `subtract <a> <b>` `multiply <a> <b>` `divide <a><b>` `remainder <a> <b>` `power <a> <b>` `factorial <a>` `ceiling <a>` `floor <a>` `floordivision <a>` `squareroot <a>` `exponent <a>` `round <a>` `modulus <a>` `sin <a>` `cos <a>` `tan <a>` `cot <a>` `secant <a>` `cosecant <a>` `asine <a>` `acosine <a>` `atangent <a>` `acotangent <a>` `asecant <a>` `acosecant <a>` `sineh <a>` `cosineh <a>` `tangenth <a>` `asineh <a>` `acosineh <a>` `atangenth <a>` `pi` `e` `tau` `infinity` `nan`")
        await ctx.send(embed=em)

      elif str(type) == "reactionrole":
        em = discord.Embed(title="Dank Memer Commands")
        em.add_field(name=f"Run `{ctx.prefix}help <command>` for more info on each one.", value="`rrcreate` `rrdelete` `rrmini`")
        await ctx.send(embed=em)
        
      elif str(type) == "currency":
        em = discord.Embed(title="Currency Commands")
        em.add_field(name=f"Run `{ctx.prefix}help <command>` for more info on each one.", value="`balance` `beg` `deposit` `withdraw` `slots` `rob` `search` `give` `buy` `shop` `inventory` `fish` `hunt` `sell` `postmeme` `gamble` `enable` `disable`")
        await ctx.send(embed=em)

      elif str(type) == "economy":
        em = discord.Embed(title="Currency Commands")
        em.add_field(name=f"Run `{ctx.prefix}help <command>` for more info on each one.", value="`balance` `beg` `deposit` `withdraw` `slots` `rob` `search` `give` `buy` `shop` `inventory` `fish` `hunt` `sell` `postmeme` `gamble` `enable` `disable`")
        await ctx.send(embed=em)

      elif str(type) == "enable":
        em = discord.Embed(title="Enable Commands")
        em.add_field(value="Enable or Disable rob.")
        em.add_field(name="Syntax:", value="```f!enable rob```")
        em.add_field(name="Syntax:", value="```f!disable rob```")
        await ctx.send(embed=em)



def setup(bot):
 bot.add_cog(Giveaway(bot))