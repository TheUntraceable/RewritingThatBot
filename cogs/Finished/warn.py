import discord
from discord.ext import commands
import motor.motor_asyncio
from discord.ext.buttons import Paginator

cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://untraceable:MGCLANUPINHERE21@database.hdgmq.mongodb.net/database?retryWrites=true&w=majority")

db = cluster["discord"]["warns"] 
class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass


class Warns(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.warns = self.client.warns
    
    @commands.command(description="Warns a specified user.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx,member: discord.Member,*,reason=None):
        await open_account(member)
        users = await self.warns.find_one({"_id" : member.id})
        if self.client.user == member:
            return
        if ctx.author == member:
            return await ctx.reply("You can't warn yourself!")
        if ctx.author.top_role <= member.top_role:
            return await ctx.reply("They have a higher or the same top role as you!")

        obj = {
            "reason" : reason, 
            "user_id" : member.id,
            "timestamp" : ctx.message.created_at, # 
            "warned_by" : ctx.author.id, # 
            "Jump" : ctx.message.jump_url,
            "count" : len(users['warns']) + 1
        }
        users["warns"].append(obj)
        Warns = users["warns"]
        embed = discord.Embed(
            title="You are being warned:",
            description=f"__**Reason**__:\n{reason}",
            colour=discord.Colour.red(),
            timestamp=ctx.message.created_at
        )
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_footer(text=f"Warn: {len(users['warns'])}") 
        try:
            await member.send(embed=embed)
            await ctx.send("Warned that user in dm's for you.")
        except discord.HTTPException:
            await ctx.send(member.mention, embed=embed)

        await db.update_one({
            "_id" : member.id
            },{
            "$set" : {
                "warns" : Warns
            }
            },upsert=False)
    @commands.command()
    @commands.guild_only()
    async def warns(self, ctx, member: discord.Member):
        member = member or ctx.author
        await open_account(member)
        users = await self.warns.find_one({"_id" : member.id})
        warns = users["warns"] 
        print(warns)
        if not bool(warns):
           return await ctx.send(f"Couldn't find any warns related to `{member.display_name}`.")

        warns = sorted(warns, key=lambda x: x["count"])
        
        pages = []
        for warn in warns:
            description = f"""
            Warn Number: `{warn['count']}`
            Warn Reason: `{warn['reason']}`
            Warned By: <@{warn['warned_by']}>
            Warn Date: {warn['timestamp'].strftime("%I:%M %p %B %d, %Y")}
            Warn Jump URL: {warn["Jump"]}
            """
            pages.append(description)
        
        await Pag(
            title=f"Warns for `{member.display_name}`",
            colour=0xCE2029,
            entries=pages,
            length=1
        ).start(ctx)
async def open_account(member):
    data = await db.find_one({"_id" : member.id})
    if data:
        return
    await db.insert_one(
        {
            "_id" : member.id, "warns" : []
            }
        )
def setup(client):
    client.add_cog(Warns(client))