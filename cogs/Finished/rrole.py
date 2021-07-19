import discord
from discord.ext import commands

class rr(commands.Cog):
  def __init__(self,client):
    self.client=client

  @commands.command(aliases=["rrcreate", "reactionrole"])
  @commands.has_permissions(manage_roles=True)
  async def rrmake(self,ctx):


    def check(m):
      return m.author == ctx.author and m.channel.id == ctx.channel.id



    await ctx.send('Which Channel Do you want me to make a reaction role? `enter the id of the channel`')

    channelid = await self.client.wait_for('message',check=check)

    if not channelid.content.isdigit():
      return await ctx.send('An id should have been sent {}'.format(ctx.author.mention))

    nice = False

    for channel in ctx.guild.channels:
      if channel.id == int(channelid.content):
        nice=True
        break
      else:
        continue

    if not nice:
      return await ctx.send('Invalid ID provided')

    await ctx.send(f'Alright I will send the message in <#{int(channelid.content)}>')


    await ctx.send('Now tell me how do you want the embed to look?, seperate the title and description like this ``` title here | description here ```')

    embed_t_d = await self.client.wait_for('message',check=check)
    list_t_d = list(embed_t_d.content.split('|'))
    if len(list_t_d) < 2:
      return await ctx.send('Error occured please check your content!')

    await ctx.send('Now send the colour of the embed `black`, `blue` , `red` , `green` any of these choices are available')

    msg = await self.client.wait_for('message',check=check)
    print(msg.content.lower())
    if msg.content.lower() not in ['blue','black','green','red'] :
      return await ctx.send('Invalid Color!')

    color = msg.content.lower()

    titles = list_t_d[0]
    descriptions = list_t_d[1]

    if color == 'blue':
      embed=discord.Embed(title=titles,description = descriptions,colour=discord.Colour.blue())

    elif color == 'red':
      embed=discord.Embed(title=titles,description = descriptions,colour=discord.Colour.red())

    elif color == 'black':
      embed=discord.Embed(title=titles,description = descriptions,color=0x000000)

    elif color == 'green':
      embed=discord.Embed(title=titles,description = descriptions,colour=discord.Colour.green())

    await ctx.send('Alright! The embed will look something like this-', embed=embed)

    await ctx.send('Enter the number of reaction roles')
    num = await self.client.wait_for('message',check=check)
    if not num.content.isdigit():
      return await ctx.send('Should have been a number')

    else:
      list_needed = {}
      count = 1
      for j in range(int(num.content)):
        await ctx.send(f'Send an emoji for the {count} reaction role')
        emoji = await self.client.wait_for('message',check=check)
        try:
          await emoji.add_reaction(str(emoji.content))
        except:
          return await ctx.send('An emoji should have been sent')

        await ctx.send('Enter the role id')
        role_id = await self.client.wait_for('message',check=check)
        if not role_id.content.isdigit():
          return await ctx.send('The role id should have been sent')

        try:
          role = ctx.guild.get_role(int(role_id.content))
          if role.position > ctx.author.top_role.position:
            return await ctx.send('You dont have the perms to add that role')
          if role.position > ctx.guild.me.top_role.position:
            return await ctx.send('Role higher than my top role')
        except:
          return await ctx.send('Invalid id')

        list_needed[str(emoji.content)] = role.id
        count += 1

      for s in list_needed.keys():
          role = ctx.guild.get_role(list_needed[s])
          embed.add_field(name=s,value=role.name)
      channel = ctx.guild.get_channel(int(channelid.content))
      print(list_needed)

      message_id = await channel.send(embed=embed)

      for q in list_needed.keys():
          await message_id.add_reaction(q)

      await ctx.send(f'Check it out in this link below\[Jump!]({message_id.jump_url})')
      check = await self.client.reactroles.find_one({"guildID" : ctx.guild.id})
      if check:
          check['roles'].append(str(list_needed))
          Roles = check['roles']
          check['message_id'].append(message_id.id)
          Message = check['message_id']
          await self.client.reactroles.update_one({'guildID' : ctx.guild.id},
          {
            '$set' : {
              'roles' : Roles
            }
          },upsert=False)
      else:
          await self.client.reactroles.insert_one({
            'guildID' : ctx.guild.id,
            'roles' : [str(list_needed)],
            'message_id' : [message_id.id]
          })
  @commands.Cog.listener()
  async def on_raw_reaction_remove(self,payload):
    n = await self.client.reactroles.find_one({
      'guildID' : payload.guild_id
    })
    try:

      data = eval(n)
      for i in data.keys():
          if str(payload.emoji) == i:
            guild = self.client.get_guild(payload.guild_id)
            role = guild.get_role(int(data[i]))
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)
            break
          else: return
    except:
        pass

  @commands.Cog.listener()
  async def on_raw_reaction_add(self,payload):
    n = await self.client.reactroles.find_one({
      'guildID' : payload.guild_id
    })
    try:
      data = eval(n)
      for i in data.keys():

          if str(payload.emoji) == i:
            guild = self.client.get_guild(payload.guild_id)
            role = guild.get_role(int(data[i]))
            await payload.member.add_roles(role)
            break
          else:return
    except:
      pass


  @commands.command()
  @commands.has_permissions(manage_roles=True)
  async def rrdelete(self,ctx,message_id=None):
    if message_id == None:
      return await ctx.send('Send a Message id to delete like `f!rrdelete <message id of the reaction role>`')
    if not message_id.isdigit():
      return await ctx.send('Send a Message id to delete like `f!rrdelete <message id of the reaction role>`')
    nice = False
    for i in ctx.guild.channels:
      try:
        message = await i.fetch_message(id=message_id)
        nice = True
        break
      except:
        continue
    if nice:
        await self.client.reactroles.delete_one({
        'message_id' : message_id })
        await ctx.send('Done!')

  @commands.command()
  async def rrmini(self,ctx,emoji,role_id : int,channel:discord.TextChannel,*,message):
    try:

      await ctx.message.add_reaction(str(emoji))

    except:
      return await ctx.send(f'Try again Like this `{ctx.prefix}rrmini <emoji> (role_id) [channel] <title or message>`')

    role_check = ctx.guild.get_role(role_id)

    if not role_check:
      return await ctx.send(f'Try again Like this `{ctx.prefix}rrmini <emoji> (role_id) [channel] <title or message>`')

    embed=discord.Embed(description=message,colour=discord.Colour.blue())
    embed.add_field(name='\u200b',value=f'{emoji} : {role_check}')


    lol = await channel.send(embed=embed)
    await lol.add_reaction(str(emoji))
    await ctx.send(f'Check it out in this link below\n[Jump!]({lol.jump_url})')



    list_needed = {str(emoji) : role_check.id}

    check = await self.client.reactroles.find_one({
      'message_id' : lol.id
    })
    if check:
        await self.client.reactroles.update_one({
          'message_id' : lol.id 
        },
        {'$set' : {
            'message_id' : lol.id,
            'list_needed' : str(list_needed)
        }},upsert=False)
    else:
        await self.client.reactroles.insert_one({
          'guildID' : ctx.guild.id,
          'message_id' : lol.id,
          'list_needed' : str(list_needed)})
  @rrmini.error
  async def rrmini_error(self,ctx,error):
    await ctx.send(f'Try again like this `{ctx.prefix}rrmini <emoji> (role_id) [channel] <title or message>`')


def setup(client):
  client.add_cog(rr(client))