import discord
from discord.ext import commands
from datetime import datetime, timedelta
from utils.config import *
from utils.embeds import create_modlog_embed
from services.db import db
from utils.logger import get_logger

logger = get_logger()

class Events(commands.Cog):
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
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not ENABLE_JOIN_LOG:
            return
        
        guild = member.guild
        
        embed = discord.Embed(
            title="Member Joined",
            color=discord.Color.green()
        )
        
        embed.add_field(name="Member", value=f"{member.mention} ({member.id})", inline=False)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"), inline=False)
        
        account_age = datetime.utcnow() - member.created_at
        embed.add_field(name="Account Age", value=f"{account_age.days} days", inline=False)
        
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Member #{len(guild.members)}")
        embed.timestamp = datetime.utcnow()
        
        await self.send_modlog(guild, embed)
        
        if ALERT_ON_LOW_ACCOUNT_AGE and account_age.days < MIN_ACCOUNT_AGE_DAYS:
            alert_embed = discord.Embed(
                title="⚠️ Young Account Alert",
                description=f"{member.mention} joined with an account younger than {MIN_ACCOUNT_AGE_DAYS} days!",
                color=discord.Color.orange()
            )
            alert_embed.add_field(name="Account Age", value=f"{account_age.days} days", inline=False)
            alert_embed.add_field(name="Threshold", value=f"{MIN_ACCOUNT_AGE_DAYS} days", inline=False)
            alert_embed.set_thumbnail(url=member.display_avatar.url)
            alert_embed.timestamp = datetime.utcnow()
            
            await self.send_modlog(guild, alert_embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not ENABLE_JOIN_LOG:
            return
        
        guild = member.guild
        
        embed = discord.Embed(
            title="Member Left",
            color=discord.Color.red()
        )
        
        embed.add_field(name="Member", value=f"{member.mention} ({member.id})", inline=False)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S UTC") if member.joined_at else "Unknown", inline=False)
        
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        if roles:
            embed.add_field(name="Roles", value=", ".join(roles), inline=False)
        
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Members remaining: {len(guild.members)}")
        embed.timestamp = datetime.utcnow()
        
        await self.send_modlog(guild, embed)
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if not ENABLE_JOIN_LOG:
            return
        
        embed = discord.Embed(
            title="Member Banned",
            color=discord.Color.dark_red()
        )
        
        embed.add_field(name="User", value=f"{user.name} ({user.id})", inline=False)
        embed.set_thumbnail(url=user.display_avatar.url if hasattr(user, 'display_avatar') else None)
        embed.timestamp = datetime.utcnow()
        
        await self.send_modlog(guild, embed)
    
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        if not ENABLE_JOIN_LOG:
            return
        
        embed = discord.Embed(
            title="Member Unbanned",
            color=discord.Color.green()
        )
        
        embed.add_field(name="User", value=f"{user.name} ({user.id})", inline=False)
        embed.set_thumbnail(url=user.display_avatar.url if hasattr(user, 'display_avatar') else None)
        embed.timestamp = datetime.utcnow()
        
        await self.send_modlog(guild, embed)

async def setup(bot):
    await bot.add_cog(Events(bot))
