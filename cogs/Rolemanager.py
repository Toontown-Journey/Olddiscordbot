#  Copyright (c) 2020. Toontown Journey. All rights reserved

from datetime import date

import discord
from discord.ext import commands

from core.Config import get_config


def calculate_time(join_time):
    date1 = date.today()
    date2 = join_time
    weeks = (date1 - date2).days // 7
    return weeks


class Rolemanager(commands.Cog):

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        # self.db = MySQLdb.connect("198.54.125.59", "anonuwzz_discord", "test123", "anonuwzz_discord")
        # self.cursor = self.db.cursor

    def get_total_messages(self, member):
        return

    def set_total_messages(self, member):
        return
        data = {
            member: member.totalMessages
        }
        with io.open('data.yaml', w, ecoding='utf8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        # wasn't sure where to place this, we can discuss it later
        if message.channel.id == 708507541784494111:
            await message.add_reaction('✅')
            await message.add_reaction('❌')
        return
        member = message.author
        member.totalMessages = self.get_total_messages(member)
        member.totalMessages += 1

        self.set_total_messages(member)
        weeks = calculate_time(member.joined_at)
        if weeks >= 2 and member.totalMessages >= 100:
            await member.add_roles(discord.utils.get(member.guild.roles, name='Toons+'))


def setup(bot):
    bot.add_cog(Rolemanager(bot, get_config()))
