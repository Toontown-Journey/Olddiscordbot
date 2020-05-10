#  Copyright (c) 2020. Toontown Journey. All rights reserved

import io
import textwrap
import traceback
from contextlib import redirect_stdout

from discord.ext import commands

from core import Checks
from core.Config import get_config


class Admin(commands.Cog):

    def __init__(self, bot: commands.bot, config):
        self.bot = bot
        self.config = config

    def validify_cog(self, cog: str):
        if not cog.startswith(self.config.cog_dir_name.strip("/")):
            return f'{self.config.cog_dir_name.strip("/")}.{cog.capitalize()}'
        return cog

    @commands.command(aliases=["reload", "reloadcog", "rload"])
    @commands.check_any(Checks.is_owner(), commands.has_permissions(administrator=True))
    async def reload_cog(self, ctx, cog: str = "all"):
        msg = await ctx.send('Reloading Cogs. . .')
        failed_to_reload = ""

        def rlcog(cog_name):
            try:
                self.bot.reload_extension(cog_name)
            except commands.ExtensionError as e:
                return f'\nError: {e}'

        if cog.lower() == "all":
            for ex in self.bot.extensions:
                print(ex)
                error = rlcog(ex)
                if error is not None:
                    failed_to_reload += error
        else:
            cog = self.validify_cog(cog)
            failed_to_reload = rlcog(cog)

        reloaded_message = "Reload Complete!"
        if failed_to_reload is not None and len(failed_to_reload) > 0:
            reloaded_message = "Reload Complete, but Errored:" + failed_to_reload

        await msg.edit(content=reloaded_message)

    @commands.command(aliases=["close", "quit"])
    @Checks.is_owner()
    async def shutdown(self, ctx):
        await ctx.send('Shutting down. . .')
        # appropriately shutdown the bot.
        if not self.bot.is_closed():
            await self.bot.close()

    @commands.command(aliases=["unloadcog", "uload"])
    @Checks.is_owner()
    async def unload(self, ctx, cog):
        msg = await ctx.send("Attempting to unload cog. . .")
        cog = self.validify_cog(cog)
        try:
            self.bot.unload_extension(cog)
        except commands.ExtensionError as e:
            await msg.edit(content=f"Failed to unload : {e}")
            return
        await msg.edit(content=f"Successfully unloaded `{cog}`")

    @commands.command(aliases=["loadcog"])
    @Checks.is_owner()
    async def load(self, ctx, cog):
        msg = await ctx.send("Attempting to load cog. . .")
        cog = self.validify_cog(cog)
        try:
            self.bot.load_extension(cog)
        except commands.ExtensionError as e:
            await msg.edit(content=f"Failed to load : {e}")
            return
        await msg.edit(content=f"Successfully loaded `{cog}`")

    @commands.command(aliases=["disablecog", "dcog"])
    @commands.check_any(Checks.is_owner(), commands.has_permissions(administrator=True))
    async def disable(self, ctx, cog):
        msg = await ctx.send("Attempting to disable cog. . .")
        cog = self.validify_cog(cog)
        if cog.split('.')[-1] in list(self.bot.cogs):
            await self.unload(ctx, cog)
            self.config.disable_cog(cog)
            await msg.edit(content=f"`{cog}` was successfully disabled.")
        else:
            await msg.edit(content=f"`{cog}` was not disabled, the cog is either invalid, or not running.")

    @commands.command(aliases=["enablecog", "ecog"])
    @commands.check_any(Checks.is_owner(), commands.has_permissions(administrator=True))
    async def enable(self, ctx, cog):
        msg = await ctx.send("Attempting to enable cog. . .")
        cog = self.validify_cog(cog)
        self.config.enable_cog(cog)
        await self.load(ctx, cog)
        if cog.split('.')[-1] in list(self.bot.cogs):
            await msg.edit(content=f"`{cog}` was successfully enabled.")
        else:
            await msg.edit(content=f"`{cog}` was not enabled, the cog is either invalid, or could not be started.")

    @commands.command(name="eval")
    @Checks.is_owner()
    async def _eval(self, ctx, *, code: str):
        # Strip off any code block formatting
        code = code.replace('```py', '')
        code = code.replace('```', '')
        # Place where the stdout will be stored
        stdout = io.StringIO()
        # setup env
        env = {
            'bot': self.bot,
            'config': self.config,
            'ctx': ctx,
            'message': ctx.message,
            'author': ctx.author,
            'guild': ctx.guild,
            'channel': ctx.channel
        }

        env.update(globals())  # add any globals

        # In order to support async, we put the code into a method
        # and run that.
        code = f'async def func():\n{textwrap.indent(code, "  ")}'
        print(code)
        try:
            # Covert the code to python bytecode
            exec(code, env)

        # Something is wrong with the code itself [failed to compile]
        except Exception as error:
            await ctx.send(f"```py\n{type(error).__name__}: {error}```")
            await ctx.message.add_reaction("⁉")
            return

        # finally, we run the function.
        try:
            with redirect_stdout(stdout):  # prevent the output from going to console
                returns = await env['func']()  # place where the compiled function was stored

        except Exception:
            await ctx.send(f"```py\n{stdout.getvalue()}{traceback.format_exc()}```")
            await ctx.message.add_reaction("⁉")
            return

        # send back returns or output.
        if returns is None:
            if len(stdout.getvalue()) > 0:
                await ctx.send(f"```py\n{stdout.getvalue()}\n```")
        else:
            if len(stdout.getvalue()) > 0:
                await ctx.send(f"```py\n{stdout.getvalue()}{returns}\n```")
            else:
                await ctx.send(f"```py\n{returns}\n```")

        # eval completed successfully
        await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Admin(bot, get_config()))
