import discord
from akinator import Akinator as aki
import asyncio
from discord.ext import commands
import akinator


class AkinatorCog(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @commands.cooldown(1, 30, commands.BucketType.user)
  @commands.command(name="akinator", aliases=["aki"])
  async def _akinator(self, ctx, mode=None):
    modes = ["nsfw", "child_mode"]
    if mode is None:
      mode = False
    elif mode in modes:
      if mode == "nsfw":
        mode = False
      elif mode == "child_mode":
        mode = True
    else:
      embed = discord.Embed(description="Invalid mode!")
      embed.set_author(name="<a:crossno:816542621333848084> Error")
      embed.add_field(name="NSFW", value="`f!aki nsfw`", inline=False)
      embed.add_field(name="CHILD MODE", value="`f!aki child_mode`", inline=False)
      return await ctx.send(embed=embed)
    await ctx.send("Akinator is here to guess!")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["y", "yes", "n","no","p","probably","pn","probably not","b", "idk"]
    try:
        aki = akinator.Akinator()
        q = aki.start_game(language="en", child_mode=mode)
        while aki.progression <= 80:
            question_embed = discord.Embed(description=f"**{q}**\n[yes (**y**) / no (**n**) / i don't know (**idk**) / probably (**p**) / probably not (**pn**)]\n[go back (**b**)]", colour=discord.Colour.blurple())
            question_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=question_embed)
            try:
              msg = await self.client.wait_for("message", check=check, timeout=15.0)
              if msg.content.lower() == "b":
                  try:
                      q = aki.back()
                  except aki.CantGoBackAnyFurther:
                      await ctx.send("This is the first question!")
                      continue
              else:
                  try:
                      q = aki.answer(msg.content.lower())
                  except aki.InvalidAnswerError:
                      await ctx.send("Invalid answer!")
                      continue
            except asyncio.TimeoutError:
              pass
        aki.win()
        win_embed = discord.Embed(title="Is this your character?", colour=0xFFFF00)
        win_embed.add_field(name=aki.first_guess['name'], value=f"{aki.first_guess['description']}\n\n[yes (**y**) / no (**n**)]")
        if aki.first_guess['absolute_picture_path'] is not None:
          win_embed.set_image(url=aki.first_guess['absolute_picture_path'])
        else:
          win_embed.set_image(url="https://photos.clarinea.fr/BL_1_fr/none.jpg")
        await ctx.send(embed=win_embed)
        try:
          correct = await self.client.wait_for("message", check=check, timeout=5.0)
          if correct.content.lower() in ["y","yes"]:
              correct_guessed_embed = discord.Embed(title="Great! I guessed it right.", description="I love playing with you!", colour=discord.Colour.green())
              await ctx.send(embed=correct_guessed_embed)
          else:
              await ctx.send("Oof")
        except asyncio.TimeoutError:
          pass
    except Exception as e:
        await ctx.send(e)

def setup(client):
  client.add_cog(AkinatorCog(client))