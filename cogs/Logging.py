#  Copyright (c) 2020. Toontown Journey. All rights reserved

import discord
from discord.ext import commands

from core.Config import get_config


# to be implemented
class Logging(commands.Cog):

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    # to be implemented
    @commands.Cog.listener()
    async def on_message(self, message: discord.message):
        # print(f"Info[{self.__class__.__name__}]: on_message called")
        return

    # to be implemented
    @commands.Cog.listener()
    async def on_message_edit(self, previous: discord.message, new: discord.message):
        # print(f"Info[{self.__class__.__name__}]: on_message_edit called")
        return

    # to be implemented
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.message):
        # print(f"Info[{self.__class__.__name__}]: on_message_delete called")
        return

    # to be implemented
    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages: [discord.message]):
        # print(f"Info[{self.__class__.__name__}]: on_bulk_message_delete called")
        return


def setup(bot):
    bot.add_cog(Logging(bot, get_config()))
