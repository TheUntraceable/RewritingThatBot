from discord.ext import commands

class UserPhone(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command(description="Connects you to someone somewhere random, anywhere in the world.")
    async def userphone(self,ctx):
        obj = {
            "guildID" : ctx.guild.id,
            "connected" : False,
            "connectedto" : None,
            "channel" : ctx.channel.id 
             }
        await self.client.userphone.insert_one(obj)
        data = await self.client.userphone.find_one({"guildID" : ctx.guild.id})
        while not data["connected"]:
            async with ctx.typing():
                async for doc in self.client.userphone.find():
                    if doc["connected"] == False and doc["guildID"] != ctx.guild.id:
                        await self.client.userphone.update_one({"guildID" : ctx.guild.id},{"$set" : {"connected" : True, "connectedto" : doc["channel"]}})

                        await self.client.userphone.update_one({"guildID" : doc["guildID"]},{"$set" : {"connected" : True, "connectedto" : ctx.channel.id}})
                        await ctx.send("You are now connected! Say hi!")
    @commands.command(description="Ends the call making your server no longer be connected to another server.")
    async def hangup(self,ctx):
        data = await self.client.userphone.find_one({"guildID" : ctx.guild.id})

        await self.client.userphone.delete_one({"guildID" : ctx.guild.id})
        await self.client.userphone.delete_one({"guildID" : self.client.get_channel(data["connectedto"]).guild.id})
        await ctx.reply("Hung up the phone :(")
        await self.client.get_channel(data["connectedto"]).send("They hung up the phone. :(")
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot or message.content.lower() == f"{await self.client.get_prefix(message)}hangup":
            return
        Raw_Data = await self.client.userphone.find_one({"guildID" : message.guild.id})
        try:

            if not Raw_Data or Raw_Data == None:
                return
            await self.client.get_channel(Raw_Data["connectedto"]).send(f"{message.author.name}: {message.content}")
        except: pass

def setup(client):
    client.add_cog(UserPhone(client))