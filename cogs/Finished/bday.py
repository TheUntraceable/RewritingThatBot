import discord
from discord.ext import commands
from datetime import date
import random
import asyncio

class Birthday(commands.Cog):
  def __init__(self,client):
    self.client=client

  @commands.command()
  async def date(self,ctx):
    await ctx.send(str(date.today())[4:])


  @commands.command(aliases=["setbirthday", "birthdayset", "birthday", "bday", "setbday"])
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

  @commands.command()
  async def guess(self,ctx):
    await ctx.send('**Welcome to the guessing game**\nMy number is between 1 - 10, you have 3 guesses to guess my number')
    number = random.randint(1,10)
    guess_count = 0
    while guess_count < 3:
      await ctx.send('What is your guess?')

      def check(m):
        return m.author == ctx.author and m.content.isdigit()
      try:
        msg = await self.client.wait_for('message', timeout=10.0,check=check)
        guess = int(msg.content)
        if guess < number:
          await ctx.send('Your guess is smaller than my number')
        elif guess > number:
          await ctx.send('Your guess is bigger than my number')
        elif guess == number:
          return await ctx.send('Your guess is correct!!!')
        guess_count += 1
        if guess_count == 3 and guess != number:
          await ctx.send(f'YOU LOOSE!!! MY NUMBER WAS {number}')
      except asyncio.TimeoutError:
        await ctx.send(f'Game ended with no response, my number was {number}')

def setup(client):
  client.add_cog(Birthday(client))