import discord
from discord.ext import commands
import asyncio
import os
import config

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description='discord bot')

@bot.event
async def on_ready():
    print('Logging in...')
    print('username: ' + str(bot.user.name))
    print('id: ' + str(bot.user.id))
    load_cogs()

@bot.event
async def on_message(message):
    if message.channel.id == 708507541784494111:
        await message.add_reaction('✅')
        await message.add_reaction('❌')

def update_avatar(filename):
    if os.path.isfile(filename):
        with open(filename, 'rb') as avatar:
            bot.edit_profile(avatar=avatar.read())
def load_cogs():
    for subdir in next(os.walk(config.cog_dir))[1]:
        try:
            bot.load_extension('cogs.{}.cog'.format(subdir))
            print('loaded plugin: {}'.format(subdir))
        except Exception as error:
            exception = '{0}: {1}'.format(type(error).__name__, error)
            print('Failed to load {}: {}'.format(subdir, exception))

@bot.event
async def on_message_edit(old, new):
    await bot.process_commands(new)

@bot.command(pass_context=True)
@commands.has_role("Toontown Journey Staff")
async def quit(ctx):
    await ctx.send('bye')
    os._exit(0)

try:
    bot.run(config.token)
except OSError:
    os._exit(0)


