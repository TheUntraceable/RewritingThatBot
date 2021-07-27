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
            return await ctx.send("Please enter a user.")
        realUser = self.client.blacklist.find_one({"_id": user.id})

        if not realUser:
            self.client.blacklist.insert_one(
                {
                    "_id": user.id
                }
            )
            try:
                await user.send(f"You have now been blacklisted from using `{self.client.user.mention}` by {ctx.author.mention}")
                await ctx.send("Informed them in DM's for you.")
            except discord.Forbidden:
                await ctx.send("Couldn't inform that user in DM's.")
            return await ctx.send(f"{user.mention} ({user.id}) can now no longer use any commands.")
        await ctx.send(f"This user is already in the database.")

    @commands.command()
    @commands.is_owner()
    async def unblock(self, ctx, user: discord.User = None):
        if user == None:
            await ctx.send("Please enter a user.")
        try:
            await user.send(f"You are now whitelisted again! You can now use {self.client.user.mention}!")
            await ctx.send("Informed them in DM's for you.")
        except discord.Forbidden:
            await ctx.send("Could not warn them in DM's for you.")
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