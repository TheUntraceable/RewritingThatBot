import discord 
import os 
from discord.ext import commands 

class Blacklist(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def block(self, ctx, user: discord.User = None):
        if user == None:
            await ctx.send("Please enter a user.")
        realUser = self.client.blacklist.find_one({"_id": user.id})
        if realUser == None:
            self.clientblacklist.insert_one(
                {
                    "_id": user.id
                }
            )
            return await ctx.send(f"{user.mention} ({user.id}) can now no longer use any commands.")
        await ctx.send(f"This user is already in the database, please try again.")

    @commands.command()
    @commands.is_owner()
    async def unblock(self, ctx, user: discord.User = None):
        if user == None:
            await ctx.send("Please enter a user.")
        realUser = self.clientblacklist.find_one({"_id": user.id})
        if realUser != None:
            self.client.blacklist.delete_one(
                {
                    "_id": user.id
                }
            )
            return await ctx.send(f"{user.mention} ({user.id}) can now use all the commands.")
        
        await ctx.send(f"This user isn't in the database, please try again.")


def setup(client):
    client.add_cog(Blacklist(client))