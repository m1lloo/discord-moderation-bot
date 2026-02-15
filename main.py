import os
import asyncio
import discord
from discord.ext import commands
from utils.config import *
from utils.logger import *
from cogs import *


logger = get_logger()

intents = discord.Intents.default() # https://discordpy.readthedocs.io/en/latest/api.html#discord.Intents.default
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name} ({bot.user.id})")
    logger.info(f"Connected to {len(bot.guilds)} guilds")
    
    # Wait for ready signal
    await bot.wait_until_ready()

    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} slash commands")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")

@bot.event
async def on_command_error(ctx, error):
    match error: # Python 3.10+
        case commands.CommandNotFound():
            return

        case commands.MissingPermissions():
            await ctx.send(
                "You don't have permission to use this command.",
                ephemeral=True
            )

        case commands.MissingRequiredArgument(param=param):
            await ctx.send(
                f"Missing required argument: {param}",
                ephemeral=True
            )

        case commands.BadArgument():
            await ctx.send(
                f"Invalid argument: {error}",
                ephemeral=True
            )

        case _:
            logger.error(f"Command error: {error}")
            await ctx.send(
                "An error occurred while executing this command.",
                ephemeral=True
            )

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

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("CTRL+C received, shutting down...")
        asyncio.run(bot.close())
    except Exception as e:
        logger.error(f"Unexpected error: {repr(e)}")
