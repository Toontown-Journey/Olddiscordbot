import discord
from discord.ext import commands

class welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context=True)
    async def ping(self, ctx):

        await ctx.send('pong!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel 
        msg = 'Welcome to the discord, {0}! Please read the rules and enjoy your stay!'
        await channel.send(msg.format(member))
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        msg = 'RIP. {0} has left the server.'
        await channel.send(msg.format(member))
    

def setup(bot):
    bot.add_cog(welcome(bot))