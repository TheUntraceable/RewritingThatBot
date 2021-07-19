import discord, aiohttp, asyncio
from discord.ext import commands
from collections import deque

acceptableImageFormats = [".png",".jpg",".jpeg",".gif",".gifv",".webm",".mp4","imgur.com"]
memeHistory = deque()
memeSubreddits = ["BikiniBottomTwitter", "memes", "2meirl4meirl", "deepfriedmemes", "MemeEconomy"]

async def getSub(self, ctx, sub):
        """Get stuff from requested sub"""
        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://www.reddit.com/r{sub}/hot.json?limit=100") as response:
                    request = await response.json()
                    await session.close()
            attempts = 1
            while attempts < 5:
                if 'error' in request:
                    print("failed request {}".format(attempts))
                    await asyncio.sleep(2)
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"https://www.reddit.com/r/{sub}/hot.json?limit=100") as response:
                            request = await response.json()
                            await session.close()
                    attempts += 1
                else:
                    index = 0

                    for index, val in enumerate(request['data']['children']):
                        if 'url' in val['data']:
                            url = val['data']['url']
                            urlLower = url.lower()
                            accepted = False
                            for j, v, in enumerate(acceptableImageFormats): #check if it's an acceptable image
                                if v in urlLower:
                                    accepted = True
                            if accepted:
                                if url not in memeHistory:
                                    memeHistory.append(url)  #add the url to the history, so it won't be posted again
                                    if len(memeHistory) > 63: #limit size
                                        memeHistory.popleft() #remove the oldest

                                    break #done with this loop, can send image
                    await ctx.send(memeHistory[len(memeHistory) - 1]) #send the last image
                    return
            await ctx.send("_{}! ({})_".format(str(request['message']), str(request['error'])))

class meme(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def showerthought(self, ctx):
      async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.reddit.com/r/showerthoughts/hot.json?limit=100") as response:
                request = await response.json()
                await session.close()
        attempts = 1
        while attempts < 5:
            if 'error' in request:
                print("failed request {}".format(attempts))
                await asyncio.sleep(2)
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://www.reddit.com/r/showerthoughts/hot.json?limit=100") as response:
                        request = await response.json()
                        await session.close()
                attempts += 1
            else:
                index = 0

                for index, val in enumerate(request['data']['children']):
                    if 'title' in val['data']:
                        url = val['data']['title']
                        urlLower = url.lower()
                        accepted = False
                        if url == "What Is A Showerthought?":
                            accepted = False
                        elif url == "Showerthoughts is looking for new moderators!":
                            accepted = False
                        else:
                            accepted = True
                        if accepted:
                            if url not in memeHistory:
                                memeHistory.append(url)
                                if len(memeHistory) > 63:
                                    memeHistory.popleft()

                                break
                await ctx.send(memeHistory[len(memeHistory) - 1])
                return
        await ctx.send("_{}! ({})_".format(str(request['message']), str(request['error'])))

    @commands.command(aliases=['memes', 'dmeme', 'dankmeme', 'dank'])
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/memes/random/.json') as r:
                res = await r.json()

                image= res[0]['data']['children'][0]['data']['url']
                permalink= res[0]['data']['children'][0]['data']['permalink']
                url = f'https://reddit.com{permalink}'
                title = res[0]['data']['children'][0]['data']['title']
                ups = res[0]['data']['children'][0]['data']['ups']
                downs = res[0]['data']['children'][0]['data']['downs']
                comments = res[0]['data']['children'][0]['data']['num_comments']

                embed = discord.Embed(colour=discord.Color.blurple(), title=title, url=url)
                embed.set_image(url=image)
                embed.set_footer(text=f"🔺 {ups} 🔻 {downs} 💬 {comments}")
                await ctx.send(embed=embed, content=None)

    @commands.command(name="4chan", aliases=["greentextt"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def greentext(self, ctx):
        """Sends a greentext from r/greentext"""

        do_nsfw = False
        if isinstance(ctx.channel, discord.TextChannel):
            do_nsfw = ctx.channel.is_nsfw()

        jj = {"nsfw": True}

        async with ctx.typing():
            while (not do_nsfw and jj["nsfw"]) or jj.get("image") is None:
                resp = await self.client.aiohttp.get(
                    "https://api.iapetus11.me/reddit/gimme/4chan+greentext", headers={"Authorization": self.k.vb_api}
                )

                jj = await resp.json()

        embed = discord.Embed(color=self.d.cc)
        embed.set_image(url=jj["image"])

        await ctx.send(embed=embed)

def setup(client):
 client.add_cog(meme(client))
