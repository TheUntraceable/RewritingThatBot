import discord
from discord.ext import commands
import random
class Economy(commands.Cog):
  def __init__(self,client):
    self.client = client
    self.collection = self.client.economy

  @commands.command(cooldown_after_parsing=True)
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

        if slots(a,b,c):

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
    if not bankinfo:
      #make new entry
      await self.collection.insert_one({"user": ctx.author.id, "wallet": 0, "bank": 0,"inventory":{}})
      await ctx.send(f'{ctx.author.name} is new, opening new bank account.')
      return

    else:
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



      await self.collection.replace_one({"user": bankinfo['user']},{"user": bankinfo['user'], "wallet": bankinfo['wallet'], "bank": bankinfo['bank'],"inventory" : bankinfo['inventory']})

  @search.error
  async def search_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      embed=discord.Embed(title='Woah Slow it down buddy',description=f'You can try this command after {round(error.retry_after)} seconds,You already scouted this area, default cooldown - 20 seconds',colour=discord.Colour.blue())
      await ctx.send(embed=embed)


  @commands.command()
  async def give(self,ctx,amount:int,member:discord.Member=None):
    if member == None:
      await ctx.send('Try running the command again but this time tell who do you want to give your money to! :rolling_eyes:')
      return

    bankinfo = await self.collection.find_one({"user": ctx.author.id})
    if not bankinfo:
      #make new entry
      await self.collection.insert_one({"user": ctx.author.id, "wallet": 0, "bank": 0,"inventory":{}})
      await ctx.send(f'{ctx.author.name} is new, opening new bank account.')
      return

    bankinfo1 = await self.collection.find_one({"user": member.id})
    if not bankinfo1:
      #make new entry
      await self.collection.insert_one({"user": member.id, "wallet": 0, "bank": 0,"inventory":{}})
      await ctx.send(f'{member.name} is new, opening new bank account.')
      return

    else:
      if bankinfo['wallet'] < amount:
        await ctx.send('You do not have that much money in your wallet')

      else:
        bankinfo['wallet'] -= amount
        bankinfo1['wallet'] += amount
        await ctx.send(f"{ctx.author.mention} gave {amount} couns to {member.mention}, Now {ctx.author.mention} has {bankinfo['wallet']} coins and {member.mention} has {bankinfo1['wallet']} fluxes")
        await self.collection.replace_one({"user": bankinfo['user']},{"user": bankinfo['user'], "wallet": bankinfo['wallet'], "bank": bankinfo['bank'],"inventory" : bankinfo['inventory']})
        await self.collection.replace_one({"user": bankinfo1['user']},{"user": bankinfo1['user'], "wallet": bankinfo1['wallet'], "bank": bankinfo1['bank'],"inventory" : bankinfo1['inventory']})

        
  @commands.command()
  @commands.cooldown(1,20, commands.BucketType.user)
  async def fish(self,ctx):
    bankinfo = await self.collection.find_one({"user": ctx.author.id})
    if not bankinfo:
      #make new entry
      await self.collection.insert_one({"user": ctx.author.id, "wallet": 0, "bank": 0,"inventory":{}})
      await ctx.send(f'{ctx.author.name} is new, opening new bank account.')
      return

    else:
      caught = random.choice([0,1])

      if 'fishing pole' not in bankinfo['inventory'].keys():
        await ctx.send('First buy a fishing pole!')

      else:

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

      await self.collection.replace_one({"user": bankinfo['user']},{"user": bankinfo['user'], "wallet": bankinfo['wallet'], "bank": bankinfo['bank'],"inventory" : bankinfo['inventory']})

  
  @commands.command()
  @commands.cooldown(1,20, commands.BucketType.user)
  async def hunt(self,ctx):
    bankinfo = await self.collection.find_one({"user": ctx.author.id})
    if not bankinfo:
      #make new entry
      await self.collection.insert_one({"user": ctx.author.id, "wallet": 0, "bank": 0,"inventory":{}})
      await ctx.send(f'{ctx.author.name} is new, opening new bank account.')
      return

    else:
      caught = random.choice([0,1])

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

      await self.collection.replace_one({"user": bankinfo['user']},{"user": bankinfo['user'], "wallet": bankinfo['wallet'], "bank": bankinfo['bank'],"inventory" : bankinfo['inventory']})


  @commands.command(aliases=['postmeme'])
  @commands.cooldown(1, 20, commands.BucketType.user) 
  
  async def pm(self,ctx):
    bankinfo = await self.collection.find_one({"user": ctx.author.id})
    if not bankinfo:
      #make new entry
      await self.collection.insert_one({"user": ctx.author.id, "wallet": 0, "bank": 0,"inventory":{}})
      await ctx.send(f'{ctx.author.name} is new, opening new bank account.')
      return

    else:
      if 'laptop' not in bankinfo['inventory'].keys():
        await ctx.send('You need to buy a laptop for this!')

      else:
        if bankinfo['inventory']['laptop'] < 1:
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

      await self.collection.replace_one({"user": bankinfo['user']},{"user": bankinfo['user'], "wallet": bankinfo['wallet'], "bank": bankinfo['bank'],"inventory" : bankinfo['inventory']})

            
  @commands.command(aliases= ["bet"])
  @commands.cooldown(1, 20, commands.BucketType.user) 
  async def gamble(self,ctx,amount:int=None):

    bankinfo = await self.collection.find_one({"user": ctx.author.id})
    if not bankinfo:
      #make new entry
      await self.collection.insert_one({"user": ctx.author.id, "wallet": 0, "bank": 0,"inventory":{}})
      await ctx.send(f'{ctx.author.name} is new, opening new bank account.')
      return


    else:
    

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
  
        await self.collection.replace_one({"user": bankinfo['user']},{"user": bankinfo['user'], "wallet": bankinfo['wallet'], "bank": bankinfo['bank'],"inventory" : bankinfo['inventory']})

  @commands.command()
  @commands.has_permissions(manage_guild=True)
  async def enable(self,ctx,what):
    if what.lower() == 'rob':
      await self.collection.update_one({"guildID" : ctx.guild},{"$set" : {"robbing" : True}})
      await ctx.send('Rob Enabled!')
    if what.lower() == 'tips' or what.lower() == 'tip':
      await self.collection.update_one({"guilDID" : ctx.guild.id},{"$set" : {"tips" : True}})
      await ctx.send('Enabled Tips!')

  @commands.command()
  @commands.has_permissions(manage_guild=True)
  async def disable(self,ctx,what):
    if what.lower() == 'rob':
      await self.collection.update_one({"guildID" : ctx.guild},{"$set" : {"robbing" : False}})
      await ctx.send('Rob Enabled!')
    if what.lower() == 'tips' or what.lower() == 'tip':
      await self.collection.update_one({"guilDID" : ctx.guild.id},{"$set" : {"tips" : False}})
      await ctx.send('Enabled Tips!')

  @commands.command(aliases=['DAILY','Daily'])
  @commands.cooldown(1, 86400, commands.BucketType.user) 
  async def daily(self,ctx):
    bankinfo = await self.collection.find_one({"user": ctx.author.id})
    if not bankinfo:
      #make new entry
      await self.collection.insert_one({"user": ctx.author.id, "wallet": 0, "bank": 0,"inventory":{}})
      await ctx.send(f'{ctx.author.name} is new, opening new bank account.')
      return

    else:
      bankinfo['wallet'] += 1000
    await ctx.send('Daily Reward claimed for 1000 fluxes!!!')
   
    await self.collection.replace_one({"user": bankinfo['user']},{"user": bankinfo['user'], "wallet": bankinfo['wallet'], "bank": bankinfo['bank'],"inventory" : bankinfo['inventory']})

  @commands.command(aliases=['MONTHLY','Monthly'])
  @commands.cooldown(1, 2628288 , commands.BucketType.user) 
  async def monthly(self,ctx):
    bankinfo = await self.collection.find_one({"user": ctx.author.id})
    if not bankinfo:
      #make new entry
      await self.collection.insert_one({"user": ctx.author.id, "wallet": 0, "bank": 0,"inventory":{}})
      await ctx.send(f'{ctx.author.name} is new, opening new bank account.')
      return

    else:
      bankinfo['wallet'] += 10000
    await ctx.send('Daily Reward claimed for 10000 coins!!!')
  
    await self.collection.replace_one({"user": bankinfo['user']},{"user": bankinfo['user'], "wallet": bankinfo['wallet'], "bank": bankinfo['bank'],"inventory" : bankinfo['inventory']})

  @commands.command(aliases=['WEEKLY','Weekly'])
  @commands.cooldown(1, 604800, commands.BucketType.user) 
  async def weekly(self,ctx):
    bankinfo = await self.collection.find_one({"user": ctx.author.id})
    if not bankinfo:
      #make new entry
      await self.collection.insert_one({"user": ctx.author.id, "wallet": 0, "bank": 0,"inventory":{}})
      await ctx.send(f'{ctx.author.name} is new, opening new bank account.')
      return

    else:
      bankinfo['wallet'] += 5000

    await ctx.send('Daily Reward claimed for 5000 coins!!!')
    
    await self.collection.replace_one({"user": bankinfo['user']},{"user": bankinfo['user'], "wallet": bankinfo['wallet'], "bank": bankinfo['bank'],"inventory" : bankinfo['inventory']})


          
def slots(a,b,c):
  if a == b or a == c:
    return True

  if b == c:
    return True

  else:
    return False


def setup(client):
  client.add_cog(Economy(client))