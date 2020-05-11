#  Copyright (c) 2020. Toontown Journey. All rights reserved

import discord
from discord.ext import commands

from core.Config import get_config


class Welcome(commands.Cog):

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        await ctx.send(f'pong! `[Client ping: {int(self.bot.latency * 1000)}ms]`')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        msg = 'Welcome to the discord, {0}! Please read the rules and enjoy your stay!'
        await channel.send(msg.format(member))
        await member.add_roles(discord.utils.get(member.guild.roles, name='Toons'))

    # future implementation
    '''@commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        msg = 'RIP. {0} has left the server.'
        await channel.send(msg.format(member))
    '''


def setup(bot):
    bot.add_cog(Welcome(bot, get_config()))
