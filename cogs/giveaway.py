import discord, random
from discord.ext import commands
import asyncio
from discord import Embed
from random import choice

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

class giveaways(commands.Cog, name='giveaways'):
	def __init__(self, client):
		self.client = client

	@commands.command(name="giftdel", aliases=["gcancel", "gftdel", "gdl"])
	async def gstop(self, ctx, channel : discord.TextChannel, id_: int,reason):
		role = discord.utils.find(lambda r: r.name == '・Giveaways', ctx.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'Giveaway Manager', ctx.guild.roles)
		role3 = discord.utils.find(lambda r: r.name == 'Giveaways Manager', ctx.guild.roles)
		if ctx.author.guild_permissions.manage_channels == True or ctx.author.guild_permissions.administrator == True or role in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles:
			try:
					msg = await channel.fetch_message(id_)
					newEmbed = Embed(title="Giveaway Cancelled", description=f"The giveaway has been cancelled!!\n **Reason:** {reason}")
					#Set Giveaway cancelled
					self.cancelled = True
					await msg.edit(embed=newEmbed) 
			except:
					embed = Embed(title="Failure!", description="Cannot cancel Giveaway")
					await ctx.send(emebed=embed)
					return
		else:
			await ctx.send("missing permissions, required premissons are manage_channels")

	@commands.command(aliases=['gstart','giveaway'])
	async def gcreate(self,ctx):
		role = discord.utils.find(lambda r: r.name == '・Giveaways', ctx.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'Giveaway Manager', ctx.guild.roles)
		role3 = discord.utils.find(lambda r: r.name == 'Giveaways Manager', ctx.guild.roles)
		if ctx.author.guild_permissions.manage_channels == True or ctx.author.guild_permissions.administrator == True or role in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles:
			await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

			questions = ["Which channel should it be hosted in?", 
									"What should be the duration of the giveaway? (s|m|h|d)",
									"What is the prize of the giveaway?"]

			answers = []

			def check(m):
					return m.author == ctx.author and m.channel == ctx.channel 

			for i in questions:
					await ctx.send(i)

					try:
							msg = await self.client.wait_for('message', timeout=15.0, check=check)
					except asyncio.TimeoutError:
							await ctx.send('You didn\'t answer in time, please be quicker next time!')
							return
					else:
							answers.append(msg.content)
			try:
					c_id = int(answers[0][2:-1])
			except:
					await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
					return

			channel = self.client.get_channel(c_id)

			time = convert(answers[1])
			if time == -1:
					await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
					return
			elif time == -2:
					await ctx.send(f"The time must be an integer. Please enter an integer next time")
					return            

			prize = answers[2]

			await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")


			embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)

			embed.add_field(name = "Hosted by:", value = ctx.author.mention)

			embed.set_footer(text = f"Ends {answers[1]} from now!")
			embed.set_thumbnail(url="https://i.pinimg.com/originals/eb/2a/8f/eb2a8f4ddfb50c23712a3cd0d5cc2a3a.gif")

			my_msg = await channel.send(embed = embed)


			await my_msg.add_reaction("🎉")


			await asyncio.sleep(time)


			new_msg = await channel.fetch_message(my_msg.id)


			users = await new_msg.reactions[0].users().flatten()
			users.pop(users.index(self.client.user))

			winner = random.choice(users)

			await channel.send(f"Congratulations! {winner.mention} won {prize}!")
			await winner.send(f"You won a giveaway")
		else:
			await ctx.send("missing permissions, required permissions are manage_channels or administrator")
	@commands.command()
	async def gawreroll(self,ctx, channel : discord.TextChannel, id_ : int):
		role = discord.utils.find(lambda r: r.name == '・Giveaway Manager', ctx.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'Giveaway Manager', ctx.guild.roles)
		role3 = discord.utils.find(lambda r: r.name == 'Giveaways Manager', ctx.guild.roles)
		if ctx.author.guild_permissions.manage_channels == True or ctx.author.guild_permissions.administrator == True or role in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles:
			try:
					new_msg = await channel.fetch_message(id_)
			except:
					await ctx.send("The id was entered incorrectly.")
					return
			
			users = await new_msg.reactions[0].users().flatten()
			users.pop(users.index(self.client.user))

			winner = random.choice(users)

			await channel.send(f"Congratulations! The new winner is {winner.mention}.!") 
			await winner.send(f"You won a giveaway")
		else:
			await ctx.send("missing permissions, required premissons are manage_channels or administrator")
	@commands.command(name="giftrrl", aliases=["gifreroll", "greroll", "grr","gend"])
	async def gawend(self, ctx, channel : discord.TextChannel, id_: int):
		role = discord.utils.find(lambda r: r.name == '・Giveaway Manager', ctx.message.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'Giveaway Manager', ctx.message.guild.roles)
		role3 = discord.utils.find(lambda r: r.name == 'Giveaways Manager', ctx.message.guild.roles)
		if ctx.author.guild_permissions.manage_channels == True or ctx.author.guild_permissions.administrator == True or role in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles:
			try:
					msg = await channel.fetch_message(id_)
			except:
					await ctx.send("The channel or ID mentioned was incorrect")
			users = await msg.reactions[0].users().flatten()
			if len(users) <= 0:
					emptyEmbed = Embed(title="Giveaway Time !!",
																	description=f"Win a Prize today")
					emptyEmbed.add_field(name="Hosted By:", value=ctx.author.mention)
					emptyEmbed.set_footer(text="No one won the Giveaway")
					await msg.edit(embed=emptyEmbed)
					return
			if len(users) > 0:
					winner = choice(users)
					winnerEmbed = Embed(title="Giveaway Time !!",
															description=f"Win a Prize today",
															colour=0x00FFFF)
					winnerEmbed.add_field(name=f"Congratulations On Winning Giveaway", value=winner.mention)
					winnerEmbed.set_image(url="https://i.pinimg.com/originals/eb/2a/8f/eb2a8f4ddfb50c23712a3cd0d5cc2a3a.gif")
					await msg.edit(embed=winnerEmbed)
					await channel.send(f"Congratulations! The new winner is {winner.mention}.!")
					await winner.send(f"You won the giveaway")
					return
		else:
			await ctx.send("missing permissions, required permissions are manage_channels or administrator")

def setup(bot):
    bot.add_cog(giveaways(bot))