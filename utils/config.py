import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
OWNER_IDS = [int(id.strip()) for id in os.getenv("OWNER_IDS", "").split(",") if id.strip()]
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/modbot.sqlite3")
MODLOG_CHANNEL_ID = int(os.getenv("MODLOG_CHANNEL_ID", "0")) if os.getenv("MODLOG_CHANNEL_ID") else None
DEFAULT_EMBED_COLOR = int(os.getenv("DEFAULT_EMBED_COLOR", "#2f3136").lstrip("#"), 16)

ENABLE_WARN = os.getenv("ENABLE_WARN", "true").lower() == "true"
ENABLE_TIMEOUT = os.getenv("ENABLE_TIMEOUT", "true").lower() == "true"
ENABLE_KICK = os.getenv("ENABLE_KICK", "true").lower() == "true"
ENABLE_BAN = os.getenv("ENABLE_BAN", "true").lower() == "true"
ENABLE_PURGE = os.getenv("ENABLE_PURGE", "true").lower() == "true"
ENABLE_ANTISPAM = os.getenv("ENABLE_ANTISPAM", "true").lower() == "true"
ENABLE_WORD_FILTER = os.getenv("ENABLE_WORD_FILTER", "true").lower() == "true"
ENABLE_JOIN_LOG = os.getenv("ENABLE_JOIN_LOG", "true").lower() == "true"

def parse_role_ids(env_var):
    return [int(id.strip()) for id in os.getenv(env_var, "").split(",") if id.strip()]

WARN_ROLES = parse_role_ids("WARN_ROLES")
TIMEOUT_ROLES = parse_role_ids("TIMEOUT_ROLES")
KICK_ROLES = parse_role_ids("KICK_ROLES")
BAN_ROLES = parse_role_ids("BAN_ROLES")
PURGE_ROLES = parse_role_ids("PURGE_ROLES")
ADMIN_ROLES = parse_role_ids("ADMIN_ROLES")
AUTOMOD_MANAGE_ROLES = parse_role_ids("AUTOMOD_MANAGE_ROLES")
IMMUNE_ROLES = parse_role_ids("IMMUNE_ROLES")
AUTOMOD_EXEMPT_ROLES = parse_role_ids("AUTOMOD_EXEMPT_ROLES")

SPAM_MSG_COUNT = int(os.getenv("SPAM_MSG_COUNT", "6"))
SPAM_SECONDS = int(os.getenv("SPAM_SECONDS", "8"))
SPAM_ACTION = os.getenv("SPAM_ACTION", "warn")
SPAM_TIMEOUT_DURATION = os.getenv("SPAM_TIMEOUT_DURATION", "10m")

WORD_FILTER_ACTION = os.getenv("WORD_FILTER_ACTION", "delete")
WORD_FILTER_TIMEOUT_DURATION = os.getenv("WORD_FILTER_TIMEOUT_DURATION", "30m")

MIN_ACCOUNT_AGE_DAYS = int(os.getenv("MIN_ACCOUNT_AGE_DAYS", "7"))
ALERT_ON_LOW_ACCOUNT_AGE = os.getenv("ALERT_ON_LOW_ACCOUNT_AGE", "true").lower() == "true"
