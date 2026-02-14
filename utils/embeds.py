import discord
from utils.config import DEFAULT_EMBED_COLOR

def create_embed(title=None, description=None, color=None):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color or DEFAULT_EMBED_COLOR
    )
    embed.set_footer(text="Moderation Bot")
    embed.timestamp = discord.utils.utcnow()
    return embed

def create_modlog_embed(action, moderator, target, reason=None, duration=None):
    embed = create_embed(
        title=f"Case: {action.upper()}",
        color=discord.Color.red()
    )
    
    embed.add_field(name="Target", value=f"{target.mention} ({target.id})", inline=False)
    embed.add_field(name="Moderator", value=f"{moderator.mention} ({moderator.id})", inline=False)
    
    if reason:
        embed.add_field(name="Reason", value=reason, inline=False)
    
    if duration:
        embed.add_field(name="Duration", value=duration, inline=False)
    
    embed.set_thumbnail(url=target.display_avatar.url)
    return embed

def create_success_embed(message):
    return create_embed(
        title="Success",
        description=message,
        color=discord.Color.green()
    )

def create_error_embed(message):
    return create_embed(
        title="Error",
        description=message,
        color=discord.Color.red()
    )
