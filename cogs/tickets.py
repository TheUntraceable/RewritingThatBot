import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json
import asyncio

class Tickets(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Tickets are ready!")

    @commands.command(aliases = ['createticket', 'ticketnew', 'newticket'])
    @cooldown(1, 10, BucketType.user)
    async def new(self, ctx, *, reason = None):
        em = discord.Embed(title = "Confirm New Ticket", color =  ctx.author.color)
        em.add_field(name = "Reason:", value = "We don't want people to spam!")
        em.add_field(name = "Steps to do:", value = "Type `confirm` (case sensetive) in the chat to confirm this ticket!")
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        msg = await ctx.send(embed = em)

        def msg_check(m):
            return m.author == ctx.author and m.channel  == ctx.channel

        try:
            msg = await self.client.wait_for('message', timeout = 15.0, check= msg_check)
        except:
            em = discord.Embed(title = "<a:crossno:842290118436847666> New Ticket Failed!", color = ctx.author.color)
            em.add_field(name = "Reason:", value = "You took too long!")
            em.add_field(name = "Cooldown", value = "1 minute more!")
            em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)
        else:
            if msg.content != "confirm":
                em = discord.Embed(title = "<a:crossno:842290118436847666> New Ticket Failed!", color = ctx.author.color)
                em.add_field(name = "Reason:", value = "You did not want to create one!")
                em.add_field(name = "Cooldown", value = "1 minute more!")
                em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = em)

            else:
                channelname = "ticket-{}".format(ctx.author.name)
                for _channel in ctx.guild.channels:
                    if _channel.name == channelname:
                        return await ctx.channel.send(f"You already have a ticket! Please contact staff in {_channel.mention}!")

                warning = f"""{ctx.author.mention} it is good to provide a reason for your inquires with the mods \nNext time try `{ctx.prefix}new <reason>`"""
                tickets = await self.client.tickets.find_one({'guildID' : ctx.guild.id})
                # Logic
                if not tickets:
                    em = discord.Embed(title = "<a:crossno:842290118436847666> New Failed",color = ctx.author.color)
                    em.add_field(name = "Reason:", value = "Tickets are not setup!")
                    em.add_field(name ="Usage:", value = f"Usage for an admin:\n```diff\n+ {ctx.prefix}addticketrole <@role> [reason]\n- f!new [reason]\n```")
                    await ctx.send(embed = em)
                    return
                # Getting the role made!
                ticketrole = tickets['TicketRole']
                helper_role = ctx.guild.get_role(ticketrole)
                # Setting up the Channel
                channel = await ctx.guild.create_text_channel(f'ticket-{ctx.author.name}')
                # Creating the embed
                em = discord.Embed(title = f"<a:fiber_yesiltik:736571879283884064> New ticket", color = ctx.author.color)
                em.add_field(name = "Ticket Channel:", value= f"{channel.mention}")
                em.add_field(name = "Description:", value = "Staff will be with your shortly")
                em.add_field(name = "Member:", value = f"{ctx.author.mention}")
                em.add_field(name = "Reason:", value = f"`{reason}`")
                # Perms
                # Make sure the author can type!
                await channel.set_permissions(ctx.author, read_messages = True, send_messages = True)
                # Make sure everyone else should not be able to see anything, cause it should be private
                await channel.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False)
                # And now make sure the helper_role should see this, incase the owner is busy
                await channel.set_permissions(helper_role, read_messages = True, send_messages = True)
                """
                and before you ask, how are we gonna set our Perms
                if we can manage_channels (create a channel), then hell ye
                we can speak, we dont need to actually set perms for ourselves
                """
                # Sending the embed
                await channel.send(embed = em)
                if reason == None:
                    await channel.send(warning)
                await ctx.send(f"Created the ticket! Check {channel.mention}")

                # send the mod log
                try:
                    channelId = tickets['TicketChannel']
                    for channel_ in ctx.guild.channels:
                        if channel_.id == channelId:
                            em = discord.Embed(title = "<a:fiber_yesiltik:736571879283884064> Ticket Opened!", color = ctx.author.color)
                            em.add_field(name = "Member:", value = f"{ctx.author.mention}")
                            em.add_field(name ="Reason:", value = f"`{reason}`")
                            em.add_field(name= "Channel / Access Point", value = f'{channel.mention}')
                            em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                            await channel_.send(embed = em)
                            break
                except:
                    pass

    @new.error
    async def new_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title = "<a:crossno:842290118436847666> New Error", color = ctx.author.color)
            em.add_field(name = "Reason:", value = "If your trying to spam then you will get blacklisted from using tickets!")
            em.add_field(name = "Try again in:", value = "`{:.2f}s`".format(error.retry_after))
            em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)
        if isinstance(error, commands.BotMissingPermissions):
            em = discord.Embed(title = f'<a:crossno:842290118436847666> {ctx.command.name} Failed!', color = discord.Color.random(), description = "<:pepeHammer:669760300374949908> Ladies and gentlemen we created uhhhhhhhhh yeahhhhhh")
            em.add_field(name = 'Reason', value = 'I don\'t have the perms to do that')
            em.add_field(name = 'What to do:', value = "Say `f!invite` and accept **all** the perms I ask for")
            em.set_footer(text = "-_-", icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)

    @commands.command(aliases = ['setticketrole', 'ticketrole'])
    @commands.has_permissions(manage_guild = True)
    async def addticketrole(self, ctx, role : discord.Role = None, *,reason = None):
        if role == None:
            await ctx.send("You need to provide a valid role!")
            return

        em = discord.Embed(title= "<a:fiber_yesiltik:736571879283884064> Added ticketrole", color = ctx.author.color)
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        check = await self.client.tickets.find_one({
            "guildID" : ctx.guild.id
        })
        if not check:
            await self.client.tickets.insert_one({
                'guildID' : ctx.guild.id,
                'TicketChannel' : None,
                'TicketRole' : role.id
            })
        else:
            await self.client.tickets.update_one(
                {
                    "guildID" : ctx.guild.id 
                },{
                'TicketRole' : role.id
            })

        em.add_field(name = "Role:", value = f"{role.mention}")
        em.add_field(name = "Features:", value = "Users can now type `f!new <reason>`")
        em.add_field(name = "Reason:", value = f"`{reason}`")
        await ctx.send(embed = em)

        try:
            channelId = check["TicketChannel"]
            for channel_ in ctx.guild.channels:
                if channel_.id == channelId:
                    em = discord.Embed(title = "<a:fiber_yesiltik:736571879283884064> Ticket Role Set!", color = ctx.author.color)
                    em.add_field(name = "Moderator:", value = f"{ctx.author.mention}")
                    em.add_field(name ="Reason:", value = f"`{reason}`")
                    em.add_field(name= "Ticket Role", value = f'{role.mention}')
                    em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                    em.set_thumbnail(url = ctx.author.avatar_url)
                    await channel_.send(embed = em)
                    break
        except:
            pass
    @addticketrole.error
    async def addticketrole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title = "<a:crossno:842290118436847666> Ticket Error", color = ctx.author.color)
            em.add_field(name = "Reason:", value = "You don't have the perms")
            em.add_field(name = "Perms:", value = "`Manage Server permission missing!`")
            em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)
        if isinstance(error, commands.BadArgument):
            em = discord.Embed(title=  "<a:crossno:842290118436847666> Ticket Error", color = ctx.author.color)
            em.add_field(name ="Reason:", value = f"{ctx.author.mention}, you need to provide a valid role!")
            em.add_field(name = "Usage:", value = '```diff\n+ f!addticketrole <@role> [reason]\n- f!addticketrole bruh\n```')
            em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            em.set_footer(text = "Read the docs, heheboi!")
            await ctx.send(embed = em)
        if isinstance(error, commands.BotMissingPermissions):
            em = discord.Embed(title = f'<a:crossno:842290118436847666> {ctx.command.name} Failed!', color = discord.Color.random(), description = "<:Coder_Hammer:826315685142462474> Ladies and gentlemen we got ||a dummy!||")
            em.add_field(name = 'Reason', value = 'I don\'t have the perms to do that')
            em.add_field(name = 'What to do:', value = "Say `f!invite` and accept **all** the perms I ask for")
            em.set_footer(text = "-_-", icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)

    @commands.command(aliases = ['addticketlogs', 'atl', 'stl'])
    @commands.has_permissions(manage_guild = True)
    async def setticketlogs(self, ctx, channel : discord.TextChannel = None, *, reason = None):
        if channel is None:
            return await ctx.send("You need to provide a valid channel!")

        em = discord.Embed(title ="<a:fiber_yesiltik:736571879283884064> Ticket Logs Set", color = ctx.author.color)
        em.add_field(name = "Moderator:", value = f"{ctx.author.mention}")
        em.add_field(name = "Channel:", value = f"{channel.mention}")
        em.add_field(name = "Reason:", value = f"`{reason}`", inline = False)
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        em.set_footer(text = "Invite me with f!invite ;)")
        await ctx.send(embed = em)

        tickets = await self.client.tickets.find_one({'guildID' : ctx.guild.id})

        if not tickets:
            await self.client.tickets.insert_one({'guildID' : ctx.guild.id,"TicketChannel" : channel.id,"TicketRole" : None})
        else:
            await self.client.tickets.update_one(
                {
                    "guildID" : ctx.guild.id 
                },{
                'TicketChannel' : channel.id
            })

    @setticketlogs.error
    async def setticketlogs_error(self,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title = '<a:crossno:842290118436847666> Setticketlogs Failed', color = ctx.author.color)
            em.add_field(name = "Reason:", value = "`Manage Server permission is missing!`")
            em.set_thumbnail(url = ctx.author.avatar_url)
            em.set_footer(text="Smh, imagine thinking you have the perms!")
            em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)
        if isinstance(error, commands.BadArgument):
            em = discord.Embed(title = '<a:crossno:842290118436847666> Setticketlogs Failed', color = ctx.author.color)
            em.add_field(name = "Reason:", value = "Mention a channel properly, like {}".format(ctx.channel.mention))
            em.add_field(name= "Usage:", value = "```diff\n+  f!setticketlogs #ticket-logs better ticket logs\n-  f!setticketlogs <member> setting a member as logs\n```")
            em.set_thumbnail(url = ctx.author.avatar_url)
            em.set_footer(text="Smh, imagine being that bad!")
            em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)
        if isinstance(error, commands.BotMissingPermissions):
            em = discord.Embed(title = f'<a:crossno:842290118436847666> {ctx.command.name} Failed!', color = discord.Color.random(), description = "<:Coder_Hammer:826315685142462474> Ladies and gentlemen we got ||...||")
            em.add_field(name = 'Reason', value = 'I don\'t have the perms to do that')
            em.add_field(name = 'What to do:', value = "Say `f!invite` and give me **all** the perms i ask for")
            em.set_footer(text = "-_-", icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)

    @commands.command(aliases = ['closeticket', "ticketclose"])
    @commands.has_permissions(manage_channels = True)
    async def close(self, ctx, *, reason = None):
        channel = ctx.channel
        name = channel.name

        if name.startswith("ticket-"):
            # send mod log
            data = await self.client.tickets.find_one({
                'guildID' : ctx.guild.id
            })
            channelId = data["TicketChannel"]
            for ticketChannel in ctx.guild.channels:
                if ticketChannel.id == channelId:
                    em = discord.Embed(title = "<a:fiber_yesiltik:736571879283884064> Ticket Closed!", color = ctx.author.color)
                    em.add_field(name = "Moderator:", value = f"{ctx.author.mention}")
                    em.add_field(name ="Reason:", value = f"`{reason}`")
                    em.add_field(name = "Member who's ticket it was:", value = f"{name}")
                    em.set_thumbnail(url = ctx.author.avatar_url)
                    await ticketChannel.send(embed = em)
                    break

            messageEmbed = discord.Embed(title = "<a:fiber_yesiltik:736571879283884064> Ticket Will Close!", color = ctx.author.color,
            description = "This ticket will close in ten seconds. Thanks for your time!")
            messageEmbed.add_field(name = "Moderator:", value = f"{ctx.author.mention}")
            messageEmbed.add_field(name = "Reason:", value = f"`{reason}`")
            messageEmbed.add_field(name = "Mod Logs:", value = "Sending logs in 10 seconds!")
            messageEmbed.set_footer(text = f"Invite me to your server! {ctx.prefix}invite)")
            await ctx.send(embed = messageEmbed)
            await asyncio.sleep(10)
            await channel.delete()
        else:
            em = discord.Embed(title = "<a:crossno:842290118436847666> Closing Failed!", color= ctx.author.color)
            em.add_field(name = "Reason:", value = f'This channel ({ctx.channel.mention}) is not a ticket channel!')
            em.add_field(name = "Try again later!", value = "Only a channel which has been a ticket can be closed!")
            em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)

    @close.error
    async def close_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title = '<a:crossno:842290118436847666> Close Failed', color = ctx.author.color)
            em.add_field(name = "Reason:", value = "`Manage Channels permission is missing!`")
            em.set_thumbnail(url = ctx.author.avatar_url)
            em.set_footer(text="Smh, imagine thinking you have the perms!")
            await ctx.send(embed = em)
        if isinstance(error, commands.BotMissingPermissions):
            em = discord.Embed(title = f'<a:crossno:842290118436847666> {ctx.command.name} Failed!', color = discord.Color.random(), description = "<:Coder_Hammer:826315685142462474> Ladies and gentlemen we got ||...||")
            em.add_field(name = 'Reason', value = 'I don\'t have the perms to do that-')
            em.add_field(name = 'What to do:', value = "Give me perms when?")
            em.set_footer(text = "Bruh", icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)

    """
    @param guild : discord.Guild object!
    @param ticketrole : discord.Role object
    @param ticketchannel : discord.Channel object
    """
    async def open_guild(self, guild, ticketrole : discord.Role, ticketchannel: discord.TextChannel):
        check = await self.client.tickets.find_one({
            'guildID' : guild.id
        })
        if check:
            await self.client.tickets.update_one({ 
                'guildID' : guild.id,},
                {'TicketChannel' : ticketchannel.id,
                 'TicketRole' : ticketrole.id},upsert=False)
        else:

            await self.client.tickets.insert_one({
                'guildID' : guild.id,
                'TicketChannel' : ticketchannel.id,
                'TicketRole' : ticketrole.id
            })
def setup(client):
    client.add_cog(Tickets(client))