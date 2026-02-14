import discord
from discord.ext import commands
import os
from utils.config import *
from utils.logger import get_logger
from cogs.moderation import Moderation
from cogs.automod import AutoMod
from cogs.events import Events

logger = get_logger()

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True
intents.bans = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name} ({bot.user.id})")
    logger.info(f"Connected to {len(bot.guilds)} guilds")
    
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} slash commands")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.", ephemeral=True)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param}", ephemeral=True)
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Invalid argument: {error}", ephemeral=True)
    else:
        logger.error(f"Command error: {error}")
        await ctx.send("An error occurred while executing this command.", ephemeral=True)

async def load_cogs():
    await bot.add_cog(Moderation(bot))
    await bot.add_cog(AutoMod(bot))
    await bot.add_cog(Events(bot))

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN not found in environment variables")
        exit(1)
    
    async def main():
        await load_cogs()
        await bot.start(DISCORD_TOKEN)
    
    import asyncio
    asyncio.run(main())
