#  Copyright (c) 2020. Toontown Journey. All rights reserved

import os

from discord.ext import commands

from core import Config

# grabs any configuration data
config = Config.get_config()
# Sets up the bot object, forcing case_insensitivity on
bot = commands.Bot(command_prefix=commands.when_mentioned_or(config.prefix), description=config.bot_description,
                   case_insensitive=True)


@bot.event
async def on_ready():  # Actions to occur once the bot has connected and logged in
    # Stop storing the token in config
    # for security reasons.
    del config.token
    print(f'Connected! \nUsername: {bot.user}\nClient ID: {bot.user.id}')
    load_cogs()


@bot.event  # process any valid message as a command
async def on_message(message):
    ctx = await bot.get_context(message)
    if ctx.valid:
        await bot.process_commands(message)


def update_avatar(filename):
    if os.path.isfile(filename):
        with open(filename, 'rb') as avatar:
            bot.user.edit(avatar=avatar.read())


def load_cogs():  # load all files located in the cogs directory and attempt to load them as a cog
    for cog in [i.strip(".py") for i in os.listdir(config.cog_dir) if os.path.isfile(config.cog_dir + i)]:
        try:
            if 'cogs.{}'.format(cog) not in config.disabled_cogs:
                bot.load_extension('cogs.{}'.format(cog))
        except Exception as error:
            exception = '{0}: {1}'.format(type(error).__name__, error)
            print('Failed to load {}: {}'.format(cog, exception))
    print('Loaded Cogs: {}'.format(list(bot.cogs)).strip("'"))


@bot.event
async def on_message_edit(old, new):  # allow running commands on edit
    ctx = await bot.get_context(new)
    if ctx.valid:
        await bot.process_commands(new)


# prepares the bot to be started
def start_bot():
    if not hasattr(config, 'token') or config.token is None:
        raise Config.InvalidConfigError("Token not defined in config!")
    try:
        bot.run(config.token)
    except RuntimeError:
        raise Config.InvalidConfigError("Token is invalid")


# Make sure this file is being ran,
# and not being imported.
if __name__ == '__main__':
    start_bot()
