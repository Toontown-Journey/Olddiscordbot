#  Copyright (c) 2020. Toontown Journey. All rights reserved

from datetime import date

import MySQLdb
from sshtunnel import SSHTunnelForwarder
import discord
from discord.ext import commands
import paramiko 
from core.Config import get_config

def calculate_time(join_time):
    date1 = date.today()
    date2 = join_time
    weeks = (date1 - date2).days // 7
    return weeks

mypkey = paramiko.RSAKey.from_private_key_file(config.sshKeyFilePath)

class Rolemanager(commands.Cog):

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        with SSHTunnelForwarder( (config.mysqlHost, config.sshPort),
                                 ssh_username=config.sshUsername,
                                 ssh_pkey=mypkey,
                                 remote_bind_address=(config.mysqlHost, 3306)) as tunnel:
             self.db = MySQLdb.connect('localhost', config.mysqlUsername, config.mysqlPassword, "anonuwzz_discord")
             self.cursor = self.db.cursor



    def get_total_messages(self, member):
        sql = 'SELECT * FROM total_messages'
        try:
            cursor.execute(sql)

            results = cursor.fetchall()
            for row in results:
                resultsMember = row[0]
                totalMessages = row[1]
                if member == resultsMember:
                    return totalMessages
                
            return "New user"
        except:
            print('Error: Unable to fetch data')

    def set_total_messages(self, member, totalMessages):
        sql = "INSERT INTO total_messages( " + member  + ','  + " " + totalMessages + ")"
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            db.rollback()

    def update_total_messages(self, member, totalMessages):
        sql = "UPDATE total_messages SET Messages = " + totalMessages + " WHERE Name = " + member
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            db.rollback()
        

    @commands.Cog.listener()
    async def on_message(self, message):
        # wasn't sure where to place this, we can discuss it later
        if message.channel.id == 708507541784494111:
            await message.add_reaction('✅')
            await message.add_reaction('❌')
        member = message.author
        if self.get_total_messages(member) == 'New user':
           #No entry for this member, create a new one
            member.totalMessages = 0
            self.set_total_messages(member, member.totalMessages)
        else:
            member.totalMessages = self.get_total_messages(member)
 
        member.totalMessages += 1

        self.update_total_messages(member, member.totalMessages)
        weeks = calculate_time(member.joined_at)
        if weeks >= 2 and member.totalMessages >= 100:
            await member.add_roles(discord.utils.get(member.guild.roles, name='Toons+'))


def setup(bot):
    bot.add_cog(Rolemanager(bot, get_config()))
