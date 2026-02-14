import discord
from utils.config import OWNER_IDS, IMMUNE_ROLES, AUTOMOD_EXEMPT_ROLES
import json

def is_owner(user_id):
    return user_id in OWNER_IDS

def has_role(user, role_ids):
    if not role_ids:
        return False
    user_role_ids = [role.id for role in user.roles]
    return any(role_id in user_role_ids for role_id in role_ids)

def is_immune(user):
    if is_owner(user.id):
        return True
    if has_role(user, IMMUNE_ROLES):
        return True
    return False

def is_automod_exempt(user):
    if is_owner(user.id):
        return True
    if has_role(user, AUTOMOD_EXEMPT_ROLES):
        return True
    return False

async def check_role_hierarchy(ctx, target_user):
    if is_owner(ctx.author.id):
        return True
    
    if is_immune(target_user):
        await ctx.respond("You cannot moderate this user.", ephemeral=True)
        return False
    
    author_top_role = ctx.author.top_role
    target_top_role = target_user.top_role
    
    if target_top_role >= author_top_role and ctx.author.id != ctx.guild.owner_id:
        await ctx.respond("You cannot moderate someone with an equal or higher role.", ephemeral=True)
        return False
    
    return True

def has_command_permission(user, required_roles):
    if is_owner(user.id):
        return True
    return has_role(user, required_roles)
