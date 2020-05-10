#  Copyright (c) 2020. Toontown Journey. All rights reserved

import discord
import discord.ext
from discord.ext import commands

from core.Config import get_config

config = get_config()


def is_owner():
    def predicate(ctx):
        if ctx.author.id not in get_config().owners:
            raise discord.ext.commands.errors.NotOwner('You are not a Bot Owner')
        return True

    return commands.check(predicate)
