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
                        return await ctx.send("You are now connected! Say hi!")
    @commands.command(description="Ends the call making your server no longer be connected to another server.")
    async def hangup(self,ctx):
        try:
            data = await self.client.userphone.find_one({"guildID" : ctx.guild.id,"channel" : ctx.channel.id})
            channel = await self.client.userphone.find_one({"guildID" : self.client.get_channel(data["connectedto"]).guild.id})
        except AttributeError:
            return await ctx.send("You're not on a call!")    

        await self.client.userphone.delete_one({"guildID" : ctx.guild.id,"channel" : ctx.channel.id})
        await self.client.userphone.delete_one({"guildID" : data["guildID"],"channel" : channel["channel"]})

        await ctx.reply("I hung up the phone :(")
        await self.client.get_channel(data["connectedto"]).send(f"{ctx.author.display_name} hung up the phone. :(")
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot or message.content.lower().startswith(await self.client.get_prefix(message)):
            return
        Raw_Data = await self.client.userphone.find_one({"guildID" : message.guild.id})
        Raw_Data_ = await self.client.userphone.find_one({"guildID" : self.client.get_channel(Raw_Data["connectedto"]).guild.id})
        try:
            if not Raw_Data or Raw_Data == None or Raw_Data_["connectedto"] != message.channel.id:
                return

            await self.client.get_channel(Raw_Data["connectedto"]).send(f"{message.author.display_name}: {message.content}")
        except: pass    

def setup(client):
    client.add_cog(UserPhone(client))