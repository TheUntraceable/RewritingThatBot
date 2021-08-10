import discord 

from discord.ext import commands
from cogs.config import *
class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def serverconfig(self, ctx):
        hmm_welcome = await self.client.welcome.find_one({"_id": ctx.guild.id})
        hmm_leave = await self.client.leave.find_one({"_id": ctx.guild.id})
        hmm_autorole = await self.client.auto_role.find_one({"_id": ctx.guild.id})
        hmm_leveling = await self.client.leveling.find_one({"_id": ctx.guild.id})
        hmm_nqn = await self.client.nqn.find_one({"_id": ctx.guild.id})

        def check_if_enabled_or_disabled(something):
            if something == None:
                return "\❌ Disabled"
            if something != None:
                return "\✅ Enabled"

        embed = discord.Embed(
            title = "Server Configuration",
            description = "Admins or Server managers can change this configuration.",
            color = discord.Color.blue()
        )
        embed.add_field(
            name = "Welcome Messages",
            value = f"""
{check_if_enabled_or_disabled(hmm_welcome)}
            """,
            inline = False
        )
        embed.add_field(
            name = "Leave Messages",
            value = f"""
{check_if_enabled_or_disabled(hmm_leave)}
            """,
            inline = False
        )
        embed.add_field(
            name = "Autorole",
            value = f"""
{check_if_enabled_or_disabled(hmm_autorole)}
            """,
            inline = False
        )
        embed.add_field(
            name = "Leveling",
            value = f"""
{check_if_enabled_or_disabled(hmm_leveling)}
            """,
            inline = False
        )
        embed.add_field(
            name = "NQN",
            value = f"""
{check_if_enabled_or_disabled(hmm_nqn)}
            """,
            inline = False
        )

        await ctx.message.reply(embed=embed)

    # autorole on join 

    @commands.has_permissions(manage_guild = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def autorole(self, ctx, role: discord.Role = None):
        hmm = await self.client.auto_role.find_one({"_id": ctx.guild.id})
        if hmm == None:
            uwu_autorole = None
            uwu_autorole_mention = "\❌ None"
        if hmm != None:
            uwu_autorole = ctx.guild.get_role(hmm['role_id'])
            uwu_autorole_mention = uwu_autorole.mention
        if role == None:
            embed = discord.Embed(
                title = "Autorole Configuration",
                description = f"""
**Current Autorole:** {uwu_autorole_mention}
To change this you can use `f!autorole <role>`
Please make sure I have **Manage Role** permissions.
                """,
                color = discord.Color.blue()
            )
            await ctx.message.reply(embed=embed)
        if role != None:
            bots_top_role = ctx.guild.me.top_role
            if role.position > bots_top_role.position:
                await ctx.message.reply(
                    embed = discord.Embed(
                        title = "Error!",
                        description = f"I do not have permission to give {role.mention} to others.\nThis is because the role is above my top role.\nPlease give me a higher role to fix this issue.",
                        color = discord.Color.red()
                    )
                )
            if role.position == bots_top_role.position:
                await ctx.message.reply(
                    embed = discord.Embed(
                        title = "Error!",
                        description = f"I do not have permission to give {role.mention} to others.\nThis is because the role is same as my top role.\nPlease give me a higher role to fix this issue.",
                        color = discord.Color.red()
                    )
                )
            else:
                if hmm == None:
                    await self.client.auto_role.insert_one({
                        "_id": ctx.guild.id,
                        "role_id": role.id
                    })
                    await ctx.message.reply(
                        embed = discord.Embed(
                            title = "Autorole Setup Complete",
                            description = f"""
New members will now be given the {role.mention} role.
Please make sure that I have **Manage Role** permissions to avoid problems.
                            """,
                            color = discord.Color.blue()
                        )
                    )
                if hmm != None:
                    await self.client.auto_role.update_one(
                        {"_id": ctx.guild.id},
                        {"$set": {"role_id": role.id}}
                    )
                    await ctx.message.reply(
                        embed = discord.Embed(
                            title = "Autorole Updated",
                            description = f"""
New members will now be given the {role.mention} role.
Please make sure that I have **Manage Role** permissions to avoid problems.
                            """,
                            color = discord.Color.blue()
                        )
                    )

    # welcome messages 

    @commands.has_permissions(manage_guild = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def welcome(self, ctx, choice = None):
        if choice == None:
            await ctx.message.reply(
                embed = discord.Embed(
                    title = "Invalid Usage",
                    description = "Correct Usage: `f!welcome enable/disable`",
                    color = discord.Color.red()
                )
            )
            return
        hmm = await self.client.welcome.find_one({"_id": ctx.guild.id})
        if choice.lower() == "enable":
            if hmm != None:
                await ctx.message.reply(
                    embed = discord.Embed(
                        title = "Error",
                        description = f"Welcome messages are already **enabled** and are set to {self.client.get_channel(hmm['channel_id']).mention}.",
                        color = discord.Color.red()
                    )
                )
                return 
            await self.client.welcome.insert_one(
                {
                    "_id": ctx.guild.id,
                    "channel_id": ctx.channel.id,
                    "message": None,
                    "embed_color": None,
                }
            )
            await ctx.message.reply(
                embed = discord.Embed(
                    title = "Welcome Messages Enabled",
                    description = f"""
Welcome message have now been **enabled**
Welcome channel has been set to {ctx.channel.mention}
In order to customize the settings please use `f!help settings`.
                    """,
                    color = discord.Color.blue()
                )
            )
            return
            
        if choice.lower() == "disable":
            if hmm == None:
                await ctx.message.reply(
                    embed = discord.Embed(
                        title = "Error",
                        description = f"Welcome messages are already **disabled**",
                        color = discord.Color.red()
                    )
                )
                return
            await self.client.welcome.delete_one(
                {
                    "_id": ctx.guild.id
                }
            )
            await ctx.message.reply(
                embed = discord.Embed(
                    title = "Welcome Messages Disabled",
                    description = f"""
Welcome message have now been **disabled**
To enable them again you can use `f!welcome enable`
                    """,
                    color = discord.Color.blue()
                )
            )

    @commands.has_permissions(manage_guild = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['welcomechannel'])
    async def welcome_channel(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            await ctx.message.reply(
                embed = discord.Embed(
                    title = "Invalid Usage",
                    description = "Correct Usage: `f!welcomechannel <channel>`",
                    color = discord.Color.red()
                )
            )
            return
        hmm = await self.client.welcome.find_one({"_id": ctx.guild.id})
        if hmm == None:
            await ctx.message.reply(
                embed = discord.Embed(
                    title = "Error",
                    description = f"Welcome message have not been enabled yet.\nUse `f!welcome enable` to enable welcome messages.",
                    color = discord.Color.red()
                )
            )
            return
        await self.client.welcome.update_one(
            {"_id": ctx.guild.id},
            {"$set": {"channel_id": channel.id}}
        )
        await ctx.message.reply(
            embed = discord.Embed(
                title = "Done!",
                description = f"Welcome channel has now been updated to {channel.mention}",
                color = discord.Color.blue()
            )
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        hmm = await self.client.welcome.find_one({"_id": member.guild.id})
        hmm_aaa = await self.client.auto_role.find_one({"_id": member.guild.id})
        if hmm != None:
            welcome_channel = self.client.get_channel(hmm['channel_id'])

            if hmm['message'] == None:
                embed_description = f"Yay! {member.mention} has joined our server!"
            elif hmm['message'] != None:
                embed_description = hmm['message']

            if hmm['embed_color'] == None:
                embed_color = discord.Color.blue()
            elif hmm['embed_color'] != None:
                embed_color = hmm['embed_color']

            welcome_embed = discord.Embed(
                title = "Welcome",
                description = embed_description,
                color = embed_color
            )
            welcome_embed.set_thumbnail(url=member.avatar_url)

            await welcome_channel.send(embed=welcome_embed)

        if hmm_aaa != None:
            role = member.guild.get_role(hmm_aaa["role_id"])
            await member.add_roles(role, reason="Falc Autorole")


# leave msgs


    @commands.has_permissions(manage_guild = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def leavemessage(self, ctx, choice = None):
        if choice == None:
            await ctx.message.reply(
                embed = discord.Embed(
                    title = "Invalid Usage",
                    description = "Correct Usage: `f!leavemessage enable/disable`",
                    color = discord.Color.red()
                )
            )
            return
        hmm = await self.client.leave.find_one({"_id": ctx.guild.id})
        if choice.lower() == "enable":
            if hmm != None:
                await ctx.message.reply(
                    embed = discord.Embed(
                        title = "Error",
                        description = f"Leave messages are already **enabled** and are set to {self.client.get_channel(hmm['channel_id']).mention}.",
                        color = discord.Color.red()
                    )
                )
                return
            await self.client.leave.insert_one(
                {
                    "_id": ctx.guild.id,
                    "channel_id": ctx.channel.id,
                    "message": None,
                    "embed_color": None,
                }
            )
            await ctx.message.reply(
                embed = discord.Embed(
                    title = "Leave Messages Enabled",
                    description = f"""
Leave message have now been **enabled**
Leave channel has been set to {ctx.channel.mention}
In order to customize the settings please use `f!help settings`.
                    """,
                    color = discord.Color.blue()
                )
            )
            return
            
        if choice.lower() == "disable":
            if hmm == None:
                await ctx.message.reply(
                    embed = discord.Embed(
                        title = "Error",
                        description = f"Leave messages are already **disabled**",
                        color = discord.Color.red()
                    )
                )
                return
            await self.client.leave.delete_one(
                {
                    "_id": ctx.guild.id
                }
            )
            await ctx.message.reply(
                embed = discord.Embed(
                    title = "Leave Messages Disabled",
                    description = f"""
Leave message have now been **disabled**
To enable them again you can use `f!leavemessage enable`
                    """,
                    color = discord.Color.blue()
                )
            )

    @commands.has_permissions(manage_guild = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['leavechannel'])
    async def leave_channel(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            await ctx.message.reply(
                embed = discord.Embed(
                    title = "Invalid Usage",
                    description = "Correct Usage: `f!leavechannel <channel>`",
                    color = discord.Color.red()
                )
            )
            return
        hmm = await self.client.leave.find_one({"_id": ctx.guild.id})
        if hmm == None:
            await ctx.message.reply(
                embed = discord.Embed(
                    title = "Error",
                    description = f"Leave message have not been enabled yet.\nUse `f!leavemessage enable` to enable leave messages.",
                    color = discord.Color.red()
                )
            )
            return
        await self.client.leave.update_one(
            {"_id": ctx.guild.id},
            {"$set": {"channel_id": channel.id}}
        )
        await ctx.message.reply(
            embed = discord.Embed(
                title = "Done!",
                description = f"Leave channel has now been updated to {channel.mention}",
                color = discord.Color.blue()
            )
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        hmm = await self.client.leave.find_one({"_id": member.guild.id})
        if hmm == None:
            return
        leave_channel = self.client.get_channel(hmm['channel_id'])

        if hmm['message'] == None:
            embed_description = f"Sad! **{member}** has left us!"
        elif hmm['message'] != None:
            embed_description = hmm['message']

        if hmm['embed_color'] == None:
            embed_color = discord.Color.red()
        elif hmm['embed_color'] != None:
            embed_color = hmm['embed_color']

        leave_embed = discord.Embed(
            title = "Sad!",
            description = embed_description,
            color = embed_color
        )
        leave_embed.set_thumbnail(url=member.avatar_url)

        await leave_channel.send(embed=leave_embed)

def setup(client):
    client.add_cog(Config(client)) 