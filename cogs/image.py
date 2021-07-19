import discord
from discord.ext import commands
import os
from PIL import Image
from io import BytesIO
from discord.ext import commands
import os
from io import BytesIO
import aiohttp
import os
import sr_api


client = sr_api.Client()

class Images(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Loaded Image")

    @commands.command()
    async def wanted(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author

      wanted = Image.open("./images/wanted.jpg")

      asset = user.avatar_url_as(size= 512)

      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      pfp = pfp.resize((300, 300))

      wanted.paste(pfp, (78, 219))

      wanted.save("wantedposter.jpg")

      await ctx.send(file = discord.File("wantedposter.jpg"))

    @commands.command()
    async def trash(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author

      wanted = Image.open("./images/trash.jpg")

      asset = user.avatar_url_as(size= 512)

      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      pfp = pfp.resize((170, 170))

      wanted.paste(pfp, (50, 108))

      wanted.save("trashposter.jpg")

      await ctx.send(file = discord.File("trashposter.jpg"))



    @commands.command()
    async def delete(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author

      wanted = Image.open("./images/deleted.jpg")

      asset = user.avatar_url_as(size= 512)

      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      pfp = pfp.resize((130, 130))

      wanted.paste(pfp, (80, 90))

      wanted.save("deletedposter.jpg")

      await ctx.send(file = discord.File("deletedposter.jpg"))

    @commands.command()
    async def disability(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author

      wanted = Image.open("./images/disability.jpg")

      asset = user.avatar_url_as(size= 512)

      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      pfp = pfp.resize((100, 100))

      wanted.paste(pfp, (330, 190))

      wanted.save("disabilityposter.jpg")

      await ctx.send(file = discord.File("disabilityposter.jpg"))

    @commands.command()
    async def affect(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author

      wanted = Image.open("./images/affect.jpg")

      asset = user.avatar_url_as(size= 512)

      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      pfp = pfp.resize((285, 240))

      wanted.paste(pfp, (240, 420))

      wanted.save("affectposter.jpg")

      await ctx.send(file = discord.File("affectposter.jpg"))

    @commands.command()
    async def bed(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author

      wanted = Image.open("./images/bed.jpg")

      asset = user.avatar_url_as(size= 512)

      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      pfp = pfp.resize((70, 70))

      wanted.paste(pfp, (350, 300))

      wanted.save("bedposter.jpg")

      await ctx.send(file = discord.File("bedposter.jpg"))

    @commands.command()
    async def boycott(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author

      wanted = Image.open("./images/ban.png")

      asset = user.avatar_url_as(size= 512)

      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      pfp = pfp.resize((70, 344))

      wanted.paste(pfp, (400, 400))

      wanted.save("banposter.jpg")

      await ctx.send(file = discord.File("banposter.jpg"))


    @commands.command()
    async def shit(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author

      wanted = Image.open("./images/shit.jpg")

      asset = user.avatar_url_as(size= 512)

      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      pfp = pfp.resize((200, 200))

      wanted.paste(pfp, (700, 400))

      wanted.save("shitposter.jpg")

      await ctx.send(file = discord.File("shitposter.jpg"))

    @commands.command()
    async def fakenews(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author

      wanted = Image.open("./images/fake.jpg")

      asset = user.avatar_url_as(size= 512)

      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      pfp = pfp.resize((440, 310))

      wanted.paste(pfp, (450, 30))

      wanted.save("fakeposter.jpg")

      await ctx.send(file = discord.File("fakeposter.jpg"))

    @commands.command()
    async def slapp(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author

        slap = Image.open("./images/slap.jpeg")
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        asset2 = ctx.author.avatar_url_as(size=128)
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)
        pfp = pfp.resize((249,254))
        pfp2 = pfp2.resize((238,235))
        slap = slap.copy()
        slap.paste(pfp, (35,34))
        slap.paste(pfp2, (859,49))
        slap.save("slap.jpg")
        await ctx.send(file=discord.File("slap.jpg"))
        os.remove("slap.jpg")

    @commands.command()
    async def spank(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author

        spank = Image.open("./images/spank.jpg")
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        asset2 = ctx.author.avatar_url_as(size=128)
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)
        pfp = pfp.resize((260,260))
        pfp2 = pfp2.resize((219,219))
        spank = spank.copy()
        spank.paste(pfp, (825,377))
        spank.paste(pfp2, (575,5))
        spank.save("spank.jpg")
        await ctx.send(file=discord.File("spank.jpg"))
        os.remove("spank.jpg")


    @commands.command()
    async def triggered(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
                
        wastedsession = aiohttp.ClientSession()
        async with wastedsession.get(f"https://some-random-api.ml/canvas/triggered?avatar={member.avatar_url_as(format='png')}") as img:
            if img.status != 200:
                await ctx.send("Unable to get image")
                await wastedsession.close()      
            else:
                data = BytesIO(await img.read())
                await ctx.send(file=discord.File(data, 'wasted.gif'))
                await wastedsession.close()

    @commands.command()
    async def youtube(self, ctx, member: discord.Member,*,comment="Imagine not giving the comment"):
        wastedsession = aiohttp.ClientSession()
        async with wastedsession.get(f"https://some-random-api.ml/canvas/youtube-comment?avatar={member.avatar_url_as(format='png')}&comment={comment}&username={member.name}") as img:
            if img.status != 200:
                await ctx.send("Unable to get image")
                await wastedsession.close()      
            else:
                data = BytesIO(await img.read())
                await ctx.send(file=discord.File(data, 'wasted.gif'))
                await wastedsession.close()

    @commands.command()
    async def gay(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author

        wastedsession = aiohttp.ClientSession()
        async with wastedsession.get(f"https://some-random-api.ml/canvas/gay?avatar={member.avatar_url_as(format='png')}") as img:
            if img.status != 200:
                await ctx.send("Unable to get image")
                await wastedsession.close()      
            else:
                data = BytesIO(await img.read())
                await ctx.send(file=discord.File(data, 'wasted.gif'))
                await wastedsession.close()

    @commands.command()
    async def glass(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author

        wastedsession = aiohttp.ClientSession()
        async with wastedsession.get(f"https://some-random-api.ml/canvas/glass?avatar={member.avatar_url_as(format='png')}") as img:
            if img.status != 200:
                await ctx.send("Unable to get image")
                await wastedsession.close()      
            else:
                data = BytesIO(await img.read())
                await ctx.send(file=discord.File(data, 'wasted.gif'))
                await wastedsession.close()

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def greyscale(self,ctx,member: discord.Member = None):
        """
        Converts an Image to Greyscale
        """
        member = member or ctx.author
        url = f"https://some-random-api.ml/canvas/greyscale?avatar={member.avatar_url_as(format='png')}"
        em = discord.Embed(color = ctx.author.color)
        em.set_image(url=url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def invert(self,ctx,member: discord.Member = None):
        member = member or ctx.author
        url = f"https://some-random-api.ml/canvas/invert?avatar={member.avatar_url_as(format='png')}"
        em = discord.Embed(color = ctx.author.color)
        em.set_image(url=url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def invertgreyscale(self,ctx,member: discord.Member = None):
        member = member or ctx.author
        url = f"https://some-random-api.ml/canvas/invertgreyscale?avatar={member.avatar_url_as(format='png')}"
        em = discord.Embed(color = ctx.author.color)
        em.set_image(url=url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def brightness(self,ctx,member: discord.Member = None):
        member = member or ctx.author
        url = f"https://some-random-api.ml/canvas/brightness?avatar={member.avatar_url_as(format='png')}"
        em = discord.Embed(color = ctx.author.color)
        em.set_image(url=url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def threshold(self,ctx,member: discord.Member = None):
        member = member or ctx.author
        url = f"https://some-random-api.ml/canvas/threshold?avatar={member.avatar_url_as(format='png')}"
        em = discord.Embed(color = ctx.author.color)
        em.set_image(url=url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sepia(self,ctx,member: discord.Member = None):
        member = member or ctx.author
        url = f"https://some-random-api.ml/canvas/sepia?avatar={member.avatar_url_as(format='png')}"
        em = discord.Embed(color = ctx.author.color)
        em.set_image(url=url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def green(self,ctx,member: discord.Member = None):
        member = member or ctx.author
        url = f"https://some-random-api.ml/canvas/red?avatar={member.avatar_url_as(format='png')}"
        em = discord.Embed(color = ctx.author.color)
        em.set_image(url=url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)


    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def red(self,ctx,member: discord.Member = None):
        member = member or ctx.author
        url = f"https://some-random-api.ml/canvas/red?avatar={member.avatar_url_as(format='png')}"
        em = discord.Embed(color = ctx.author.color)
        em.set_image(url=url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def blue(self,ctx,member: discord.Member = None):
        member = member or ctx.author
        url = f"https://some-random-api.ml/canvas/blue?avatar={member.avatar_url_as(format='png')}"
        em = discord.Embed(color = ctx.author.color)
        em.set_image(url=url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def blurple(self,ctx,member: discord.Member = None):
        member = member or ctx.author
        url = f"https://some-random-api.ml/canvas/blurple?avatar={member.avatar_url_as(format='png')}"
        em = discord.Embed(color = ctx.author.color)
        em.set_image(url=url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def blur(self,ctx,member: discord.Member = None):
        member = member or ctx.author
        url = f"https://some-random-api.ml/canvas/blur?avatar={member.avatar_url_as(format='png')}"
        em = discord.Embed(color = ctx.author.color)
        em.set_image(url=url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pixelate(self,ctx,member: discord.Member = None):
        member = member or ctx.author
        url = f"https://some-random-api.ml/canvas/pixelate?avatar={member.avatar_url_as(format='png')}"
        em = discord.Embed(color = ctx.author.color)
        em.set_image(url=url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command(aliases=['deep-fry','deep_fry'])
    async def deepfry(self,ctx,member: discord.Member = None):
        member = member or ctx.author
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://nekobot.xyz/api/imagegen?type=deepfry&image={member.avatar_url}')
            req = await request.json()
            embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
            embed.set_image(url=req['message'])
            embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command()
    async def magik(self,ctx,member: discord.Member = None):
        member = member or ctx.author
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://nekobot.xyz/api/imagegen?type=magik&image={member.avatar_url}')
            req = await request.json()
            embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
            embed.set_image(url=req['message'])
            embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command()
    async def baguette(self,ctx,member: discord.Member = None):
        member = member or ctx.author
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://nekobot.xyz/api/imagegen?type=baguette&image={member.avatar_url}')
            req = await request.json()
            embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
            embed.set_image(url=req['message'])
            embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command()
    async def tweet(self,ctx,message=None,member: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://nekobot.xyz/api/imagegen?type=tweet&username={member}&text={message}')
            req = await request.json()
            embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
            embed.set_image(url=req['message'])
            embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
        await ctx.send(embed=embed)


    @commands.command(aliases=['phc','pornhub_comment','ph-comment', 'ph_comment'])
    async def pornhubcomment(self,ctx,*,message):
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://nekobot.xyz/api/imagegen?type=phcomment&text={message}')
            req = await request.json()
            embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
            embed.set_image(url=req['message'])
            embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command()
    async def clyde(self,ctx,*,message):
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://nekobot.xyz/api/imagegen?type=clyde&text={message}')
            req = await request.json()
            embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
            embed.set_image(url=req['message'])
            embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def whowouldwin(self, ctx: commands.Context, user1: discord.Member, user2: discord.Member = None):
        """Who would win"""
        await ctx.trigger_typing()
        if user2 is None:
            user2 = ctx.author
        user1url = user1.avatar_url
        user2url = user2.avatar_url

        async with self.session.get("https://nekobot.xyz/api/imagegen?type=whowouldwin&user1=%s&user2=%s" % (user1url, user2url,)) as r:
            res = await r.json()

        await ctx.send(embed=self.__embed_json(res))

    @commands.command(aliases=['tt','trump_tweet','trump-tweet'])
    async def trumptweet(self,ctx,*,message):
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://nekobot.xyz/api/imagegen?type=trumptweet&text={message}')
            req = await request.json()
            embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
            embed.set_image(url=req['message'])
            embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command(aliases=['cmm','change-my-mind','change_my_mind'])
    async def changemymind(self,ctx,*,message):
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://nekobot.xyz/api/imagegen?type=changemymind&text={message}')
            req = await request.json()
            embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
            embed.set_image(url=req['message'])
            embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Images(client))