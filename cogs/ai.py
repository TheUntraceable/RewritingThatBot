import discord
from discord.ext import commands
from prsaw import RandomStuff
#Get an API Key at https://api-info.pgamerx.com/register.html/ for free
class ai(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.rs = RandomStuff(async_mode=True, api_key='LyQw1aCdSQcL')

    @commands.command(aliases=['chatbot', 'chat', 'talk'])
    async def ai(self, ctx,*,message):
        async with ctx.typing():
            response = await self.rs.get_ai_response(message,unique_id=ctx.author.id)
        await ctx.reply(response[0]["message"])

def setup(client):
    client.add_cog(ai(client))