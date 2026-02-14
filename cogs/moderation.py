import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from utils.config import *
from utils.checks import has_command_permission, check_role_hierarchy
from utils.duration import parse_duration, format_duration
from utils.embeds import create_success_embed, create_error_embed, create_modlog_embed
from services.db import db
from utils.logger import get_logger

logger = get_logger()

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def cog_load(self):
        await db.init()
    
    async def send_modlog(self, guild, embed):
        if MODLOG_CHANNEL_ID:
            channel = guild.get_channel(MODLOG_CHANNEL_ID)
            if channel:
                try:
                    await channel.send(embed=embed)
                except Exception as e:
                    logger.error(f"Failed to send modlog: {e}")
    
    @commands.hybrid_command(name="warn", description="Warn a user")
    @app_commands.describe(user="User to warn", reason="Reason for warning")
    async def warn(self, ctx, user: discord.Member, *, reason: str = "No reason provided"):
        if not ENABLE_WARN:
            return await ctx.respond("Warn commands are disabled.", ephemeral=True)
        
        if not has_command_permission(ctx.author, WARN_ROLES):
            return await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        
        if not await check_role_hierarchy(ctx, user):
            return
        
        case_id = await db.create_case(ctx.guild.id, "warn", user.id, ctx.author.id, reason)
        
        embed = create_modlog_embed("warn", ctx.author, user, reason)
        await self.send_modlog(ctx.guild, embed)
        
        await ctx.send(embed=create_success_embed(f"Warned {user.mention} (Case #{case_id})"))
        
        try:
            await user.send(f"You have been warned in {ctx.guild.name}: {reason}")
        except:
            pass
    
    @commands.hybrid_command(name="warnings", description="View warnings for a user")
    @app_commands.describe(user="User to check")
    async def warnings(self, ctx, user: discord.Member = None):
        if not ENABLE_WARN:
            return await ctx.respond("Warn commands are disabled.", ephemeral=True)
        
        if not has_command_permission(ctx.author, WARN_ROLES):
            return await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        
        target = user or ctx.author
        cases = await db.get_cases(ctx.guild.id, target.id)
        
        if not cases:
            return await ctx.respond(f"No warnings found for {target.mention}.", ephemeral=True)
        
        embed = discord.Embed(
            title=f"Warnings for {target.display_name}",
            color=DEFAULT_EMBED_COLOR
        )
        
        for case in cases[:10]:
            embed.add_field(
                name=f"Case #{case[0]} - {case[2].upper()}",
                value=f"Reason: {case[5] or 'No reason'}\nDate: {case[7][:10]}",
                inline=False
            )
        
        await ctx.respond(embed=embed, ephemeral=True)
    
    @commands.hybrid_command(name="clearwarnings", description="Clear all warnings for a user")
    @app_commands.describe(user="User to clear warnings for")
    async def clearwarnings(self, ctx, user: discord.Member):
        if not ENABLE_WARN:
            return await ctx.respond("Warn commands are disabled.", ephemeral=True)
        
        if not has_command_permission(ctx.author, WARN_ROLES):
            return await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        
        await db.clear_cases(ctx.guild.id, user.id)
        await ctx.send(embed=create_success_embed(f"Cleared all warnings for {user.mention}"))
    
    @commands.hybrid_command(name="timeout", description="Timeout a user")
    @app_commands.describe(user="User to timeout", duration="Duration (e.g., 10m, 2h, 1d)", reason="Reason for timeout")
    async def timeout(self, ctx, user: discord.Member, duration: str, *, reason: str = "No reason provided"):
        if not ENABLE_TIMEOUT:
            return await ctx.respond("Timeout commands are disabled.", ephemeral=True)
        
        if not has_command_permission(ctx.author, TIMEOUT_ROLES):
            return await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        
        if not await check_role_hierarchy(ctx, user):
            return
        
        seconds = parse_duration(duration)
        if not seconds:
            return await ctx.respond("Invalid duration format. Use formats like 10s, 10m, 2h, 3d, 1w", ephemeral=True)
        
        if seconds > 2419200:
            return await ctx.respond("Duration cannot exceed 28 days.", ephemeral=True)
        
        await user.timeout(discord.utils.utcnow() + discord.timedelta(seconds=seconds), reason=reason)
        
        case_id = await db.create_case(ctx.guild.id, "timeout", user.id, ctx.author.id, reason, seconds)
        
        embed = create_modlog_embed("timeout", ctx.author, user, reason, format_duration(seconds))
        await self.send_modlog(ctx.guild, embed)
        
        await ctx.send(embed=create_success_embed(f"Timed out {user.mention} for {format_duration(seconds)} (Case #{case_id})"))
    
    @commands.hybrid_command(name="untimeout", description="Remove timeout from a user")
    @app_commands.describe(user="User to untimeout", reason="Reason for untimeout")
    async def untimeout(self, ctx, user: discord.Member, *, reason: str = "No reason provided"):
        if not ENABLE_TIMEOUT:
            return await ctx.respond("Timeout commands are disabled.", ephemeral=True)
        
        if not has_command_permission(ctx.author, TIMEOUT_ROLES):
            return await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        
        if not user.is_timed_out():
            return await ctx.respond("This user is not timed out.", ephemeral=True)
        
        await user.timeout(None, reason=reason)
        
        case_id = await db.create_case(ctx.guild.id, "untimeout", user.id, ctx.author.id, reason)
        
        embed = create_modlog_embed("untimeout", ctx.author, user, reason)
        await self.send_modlog(ctx.guild, embed)
        
        await ctx.send(embed=create_success_embed(f"Removed timeout from {user.mention} (Case #{case_id})"))
    
    @commands.hybrid_command(name="kick", description="Kick a user")
    @app_commands.describe(user="User to kick", reason="Reason for kick")
    async def kick(self, ctx, user: discord.Member, *, reason: str = "No reason provided"):
        if not ENABLE_KICK:
            return await ctx.respond("Kick commands are disabled.", ephemeral=True)
        
        if not has_command_permission(ctx.author, KICK_ROLES):
            return await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        
        if not await check_role_hierarchy(ctx, user):
            return
        
        case_id = await db.create_case(ctx.guild.id, "kick", user.id, ctx.author.id, reason)
        
        embed = create_modlog_embed("kick", ctx.author, user, reason)
        await self.send_modlog(ctx.guild, embed)
        
        await user.kick(reason=reason)
        await ctx.send(embed=create_success_embed(f"Kicked {user.mention} (Case #{case_id})"))
    
    @commands.hybrid_command(name="ban", description="Ban a user")
    @app_commands.describe(user="User to ban", reason="Reason for ban", delete_days="Days of messages to delete (0-7)")
    async def ban(self, ctx, user: discord.User, *, reason: str = "No reason provided", delete_days: int = 0):
        if not ENABLE_BAN:
            return await ctx.respond("Ban commands are disabled.", ephemeral=True)
        
        if not has_command_permission(ctx.author, BAN_ROLES):
            return await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        
        if delete_days < 0 or delete_days > 7:
            return await ctx.respond("Delete days must be between 0 and 7.", ephemeral=True)
        
        member = ctx.guild.get_member(user.id)
        if member and not await check_role_hierarchy(ctx, member):
            return
        
        case_id = await db.create_case(ctx.guild.id, "ban", user.id, ctx.author.id, reason)
        
        embed = create_modlog_embed("ban", ctx.author, user, reason, f"{delete_days} days of messages deleted")
        await self.send_modlog(ctx.guild, embed)
        
        await ctx.guild.ban(user, reason=reason, delete_message_days=delete_days)
        await ctx.send(embed=create_success_embed(f"Banned {user.mention} (Case #{case_id})"))
    
    @commands.hybrid_command(name="unban", description="Unban a user")
    @app_commands.describe(user_id="User ID to unban", reason="Reason for unban")
    async def unban(self, ctx, user_id: str, *, reason: str = "No reason provided"):
        if not ENABLE_BAN:
            return await ctx.respond("Ban commands are disabled.", ephemeral=True)
        
        if not has_command_permission(ctx.author, BAN_ROLES):
            return await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        
        try:
            user_id_int = int(user_id)
        except ValueError:
            return await ctx.respond("Invalid user ID.", ephemeral=True)
        
        try:
            ban_entry = await ctx.guild.fetch_ban(discord.Object(user_id_int))
            user = ban_entry.user
        except discord.NotFound:
            return await ctx.respond("This user is not banned.", ephemeral=True)
        
        case_id = await db.create_case(ctx.guild.id, "unban", user.id, ctx.author.id, reason)
        
        embed = create_modlog_embed("unban", ctx.author, user, reason)
        await self.send_modlog(ctx.guild, embed)
        
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(embed=create_success_embed(f"Unbanned {user.mention} (Case #{case_id})"))
    
    @commands.hybrid_command(name="purge", description="Delete messages")
    @app_commands.describe(amount="Number of messages to delete (1-100)")
    async def purge(self, ctx, amount: int):
        if not ENABLE_PURGE:
            return await ctx.respond("Purge commands are disabled.", ephemeral=True)
        
        if not has_command_permission(ctx.author, PURGE_ROLES):
            return await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        
        if amount < 1 or amount > 100:
            return await ctx.respond("Amount must be between 1 and 100.", ephemeral=True)
        
        deleted = await ctx.channel.purge(limit=amount)
        
        case_id = await db.create_case(ctx.guild.id, "purge", ctx.channel.id, ctx.author.id, f"Deleted {len(deleted)} messages")
        
        embed = create_modlog_embed("purge", ctx.author, ctx.channel, f"Deleted {len(deleted)} messages")
        await self.send_modlog(ctx.guild, embed)
        
        await ctx.send(embed=create_success_embed(f"Deleted {len(deleted)} messages (Case #{case_id})"), delete_after=5)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
