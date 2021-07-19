import discord
from discord.ext import commands

class afk(commands.Cog):
    def __init__(self, client):
       self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if len(msg.mentions) == 0:
            return
        for mention in msg.mentions:
            data = await self.client.afk.find_one({"memberID" : mention.id})
            if not data:
                pass
            msgs = f"{msg.name} is AFK with reason : {data['reason']}"
            await msg.channel.send(msgs)

        CheckForAuthor = await self.client.afk.find_one({"memberID" : msg.author.id})
        if not CheckForAuthor:
            return
        else:
            await self.client.afk.delete_one({"memberID" : msg.author.id})
            await msg.channel.send("Welcome back {}, I removed your AFK.".format(msg.author.mention), delete_after = 10)
            await msg.author.edit(nick=None)


    @commands.command(aliases=["away_from_keyboard"], 
   description="Sets your AFK when you wanna let others know ur gone.", 
   usage="[reason]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def afk(self, ctx, *, message = "AFK"):
        self.client.afk.insert_one({"memberID" : ctx.author.id,"reason" : message})
        await ctx.reply("{}, I have set your AFK with reason : {}".format(ctx.author.mention, message))  
        try:
            await ctx.author.edit(nick = f"[AFK] {ctx.author.name}")
        except discord.Forbidden:
            pass
        else:
            return



def setup(client):
    client.add_cog(afk(client))