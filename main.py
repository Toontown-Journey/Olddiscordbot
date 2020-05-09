import discord
from discord.ext import commands
import asyncio
import os
import config
from datetime import date
import MySQLdb

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description='discord bot')
db = MySQLdb.connect("198.54.125.59","anonuwzz_discord","test123","anonuwzz_discord" )
cursor = db.cursor
@bot.event
async def on_ready():
    print('Logging in...')
    print('username: ' + str(bot.user.name))
    print('id: ' + str(bot.user.id))
    load_cogs()

def calculateTime(join_time):
    date1 = date.today()
    date2 = join_time
    weeks = ( date1- date2).days// 7
    return weeks

def getTotalMessages(member):
    return 

def setTotalMessages(member):
    return 
    data = {
        member: member.totalMessages
    }
    with io.open('data.yaml', w, ecoding='utf8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        
@bot.event
async def on_message(message):
    if message.channel.id == 708507541784494111:
        await message.add_reaction('✅')
        await message.add_reaction('❌')

    return
    member = message.author
    memeber.totalMessages = getTotalMessages(member)
    member.totalMessages += 1

    setTotalMessages(member)
    weeks = calculateTime(member.joined_at)
    if weeks >= 2 and member.totalMessages >= 100:
       await member.add_roles(discord.utils.get(member.guild.roles, name='Toons+'))


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


