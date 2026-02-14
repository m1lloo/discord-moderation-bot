import discord
from discord.ext import commands
import asyncio
import os
from collections import defaultdict, deque
from utils.config import *
from utils.checks import is_immune, is_automod_exempt
from utils.duration import parse_duration
from utils.embeds import create_modlog_embed
from services.db import db
from utils.logger import get_logger

logger = get_logger()

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_tracker = defaultdict(lambda: deque())
        self.banned_words = set()
        self.load_banned_words()
    
    def load_banned_words(self):
        try:
            with open("data/banned_words.txt", "r", encoding="utf-8") as f:
                self.banned_words = set(word.strip().lower() for word in f if word.strip())
            logger.info(f"Loaded {len(self.banned_words)} banned words")
        except FileNotFoundError:
            logger.warning("banned_words.txt not found")
    
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
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if not ENABLE_ANTISPAM and not ENABLE_WORD_FILTER:
            return
        
        if is_automod_exempt(message.author):
            return
        
        guild = message.guild
        if not guild:
            return
        
        if ENABLE_ANTISPAM:
            await self.check_spam(message)
        
        if ENABLE_WORD_FILTER:
            await self.check_word_filter(message)
    
    async def check_spam(self, message):
        user_id = message.author.id
        now = discord.utils.utcnow()
        
        self.spam_tracker[user_id].append(now)
        
        while self.spam_tracker[user_id] and self.spam_tracker[user_id][0] < now - discord.timedelta(seconds=SPAM_SECONDS):
            self.spam_tracker[user_id].popleft()
        
        if len(self.spam_tracker[user_id]) >= SPAM_MSG_COUNT:
            await self.handle_spam(message)
    
    async def handle_spam(self, message):
        guild = message.guild
        author = message.author
        
        if SPAM_ACTION == "warn":
            await db.create_case(guild.id, "warn", author.id, self.bot.user.id, "Auto-mod: Spam detection")
            
            embed = create_modlog_embed("warn", self.bot.user, author, "Auto-mod: Spam detection")
            await self.send_modlog(guild, embed)
            
            try:
                await author.send(f"You have been warned in {guild.name} for spamming")
            except:
                pass
        
        elif SPAM_ACTION == "timeout":
            duration = parse_duration(SPAM_TIMEOUT_DURATION)
            await author.timeout(discord.utils.utcnow() + discord.timedelta(seconds=duration), reason="Auto-mod: Spam detection")
            
            await db.create_case(guild.id, "timeout", author.id, self.bot.user.id, "Auto-mod: Spam detection", duration)
            
            embed = create_modlog_embed("timeout", self.bot.user, author, "Auto-mod: Spam detection", SPAM_TIMEOUT_DURATION)
            await self.send_modlog(guild, embed)
        
        try:
            await message.delete()
        except:
            pass
        
        self.spam_tracker[author.id].clear()
    
    async def check_word_filter(self, message):
        content = message.content.lower()
        
        for word in self.banned_words:
            if word in content:
                await self.handle_word_violation(message, word)
                break
    
    async def handle_word_violation(self, message, word):
        guild = message.guild
        author = message.author
        
        try:
            await message.delete()
        except:
            pass
        
        if WORD_FILTER_ACTION == "delete":
            embed = create_modlog_embed("delete", self.bot.user, author, f"Auto-mod: Banned word '{word}'")
            await self.send_modlog(guild, embed)
        
        elif WORD_FILTER_ACTION == "delete_warn":
            await db.create_case(guild.id, "warn", author.id, self.bot.user.id, f"Auto-mod: Banned word '{word}'")
            
            embed = create_modlog_embed("warn", self.bot.user, author, f"Auto-mod: Banned word '{word}'")
            await self.send_modlog(guild, embed)
            
            try:
                await author.send(f"You have been warned in {guild.name} for using a banned word")
            except:
                pass
        
        elif WORD_FILTER_ACTION == "delete_timeout":
            duration = parse_duration(WORD_FILTER_TIMEOUT_DURATION)
            await author.timeout(discord.utils.utcnow() + discord.timedelta(seconds=duration), reason=f"Auto-mod: Banned word '{word}'")
            
            await db.create_case(guild.id, "timeout", author.id, self.bot.user.id, f"Auto-mod: Banned word '{word}'", duration)
            
            embed = create_modlog_embed("timeout", self.bot.user, author, f"Auto-mod: Banned word '{word}'", WORD_FILTER_TIMEOUT_DURATION)
            await self.send_modlog(guild, embed)
    
    @commands.hybrid_group(name="automod", description="Automod management commands")
    async def automod(self, ctx):
        if not has_command_permission(ctx.author, AUTOMOD_MANAGE_ROLES):
            return await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="AutoMod Status",
                color=DEFAULT_EMBED_COLOR
            )
            embed.add_field(name="Anti-Spam", value="Enabled" if ENABLE_ANTISPAM else "Disabled", inline=True)
            embed.add_field(name="Word Filter", value="Enabled" if ENABLE_WORD_FILTER else "Disabled", inline=True)
            embed.add_field(name="Join Log", value="Enabled" if ENABLE_JOIN_LOG else "Disabled", inline=True)
            
            if ENABLE_ANTISPAM:
                embed.add_field(name="Spam Threshold", value=f"{SPAM_MSG_COUNT} messages in {SPAM_SECONDS}s", inline=True)
                embed.add_field(name="Spam Action", value=SPAM_ACTION, inline=True)
            
            if ENABLE_WORD_FILTER:
                embed.add_field(name="Word Filter Action", value=WORD_FILTER_ACTION, inline=True)
                embed.add_field(name="Banned Words", value=str(len(self.banned_words)), inline=True)
            
            await ctx.respond(embed=embed, ephemeral=True)
    
    @automod.command(name="reloadwords", description="Reload banned words list")
    async def reloadwords(self, ctx):
        if not has_command_permission(ctx.author, AUTOMOD_MANAGE_ROLES):
            return await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        
        self.load_banned_words()
        await ctx.respond(f"Reloaded {len(self.banned_words)} banned words", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
