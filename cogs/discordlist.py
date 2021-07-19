from discord.ext import commands
import discordlists


class DiscordListsPost(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api = discordlists.Client(self.client)  # Create a Client instance
        self.api.set_auth("bladebotlist.xyz", "U7RUFhtzY0f18Zx.wKZB8zvJ0xdXAAC.vxIfcICRVssUrlp")
        self.api.set_auth("space-bot-list.xyz", "7X-OoJ7alP9JoF-RFVRObjviMEngmnEMSBVoqdd9idovIBphtp")
        self.api.set_auth("discordbotlist.com", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0IjoxLCJpZCI6Ijc5MDUyNTk4NTI2NjU5NzkxOCIsImlhdCI6MTYyMjMwNjIwMn0.UJkW-4MXehH30o2Qn4pOXZlI702cGi1GQ-ZH6KCd9SU")
        self.api.set_auth("botsfordiscord.com", "a95af6049919ec81f2ce4442a2e44d5a5dca411e93ca01a3577f6c5856adff6480065b97c2e41892fbbf0b9883b20e98516c39742072f26a1bb57e4ec73c5157")
        self.api.set_auth("discord.bots.gg", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGkiOnRydWUsImlkIjoiNDg5NjgyNjc2MTU3MTIwNTEzIiwiaWF0IjoxNjIyMzA2NDU0fQ.AWdiq_6yJYIrA6FyqZYQxijOIMe5e6u0UZhg10m3K1w")
        self.api.set_auth("infinitybotlist.com", "dQRUj3HYDxsHssTI4WrBtTikMcD1wOghuubGhAwPmB4DuTORuQz8Ub7u2Le7ko4EzbpGTK92nf28Z5ZUL71rd7zr3ms7icq9QZZw")
        #self.api.set_auth("discordlist.space", "942292990d0fe954c70e539429ee8ac6e3cb55100bcfb798acb6b3046120c233f243b2417b6fe49e21303c2cac30860a")
        self.api.set_auth("disforge.com", "f53e565beed654b2de49151a082dc9a3bbd146aef30efb81226089740b97f02e")
        self.api.start_loop()

    @commands.command()
    @commands.is_owner()
    async def post(self, ctx: commands.Context):
        """
        Manually posts guild count using discordlists.py (BotBlock)
        """
        try:
            result = await self.api.post_count()
        except Exception as e:
            await ctx.send("Request failed: `{}`".format(e))
            return

        await ctx.send("Successfully manually posted server count ({:,}) to {:,} lists."
                       "\nFailed to post server count to {:,} lists.".format(self.api.server_count,
                                                                             len(result["success"].keys()),
                                                                             len(result["failure"].keys())))

    @commands.command()
    @commands.is_owner()
    async def get(self, ctx: commands.Context, bot_id: int = None):
        """
        Gets a bot using discordlists.py (BotBlock)
        """
        if bot_id is None:
            bot_id = self.client.user.id
        try:
            result = (await self.api.get_bot_info(bot_id))[1]
        except Exception as e:
            await ctx.send("Request failed: `{}`".format(e))
            return

        await ctx.send("Bot: {}#{} ({})\nOwners: {}\nServer Count: {}".format(
            result['username'], result['discriminator'], result['id'],
            ", ".join(result['owners']) if result['owners'] else "Unknown",
            "{:,}".format(result['server_count']) if result['server_count'] else "Unknown"
        ))



def setup(client):
    client.add_cog(DiscordListsPost(client))