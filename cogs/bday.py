import discord
from discord.ext import commands
from datetime import date

class Birthday(commands.Cog):
  def __init__(self,client):
    self.client=client

  @commands.command()
  async def date(self,ctx):
    await ctx.send(str(date.today())[4:])
  @commands.command()
  async def bday(self,ctx,user : discord.User):
    data = await self.client.bdays.find_one({"memberID" : user.id})
    await ctx.send(f"{user.display_name} has said their birthday is: {data['data'][0]} - {data['data'][1]}")

  @commands.command(aliases=["setbirthday", "birthdayset", "birthday", "setbday"])
  async def setbdy(self,ctx,datee):
    month,day = datee.split('-')
    await ctx.send(f'Birthday Set to {month}-{day}')
    check = await self.client.bdays.find_one({"memberID" : ctx.author.id,"data" : [month,day]})
    if check:
        await self.client.bdays.update_one(
          {"memberID" : ctx.author.id}
          ,{"$set" :
            {"data" : [month,day]}
            },upsert=False)
        return
    else:
        await self.client.bdays.insert_one({"memberID" : ctx.author.id,"data" : [month,day]})

def setup(client):
  client.add_cog(Birthday(client))