import os
from .functions import parse_role_ids
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

config_path = Path("../config/config.json")
config = open(config_path.resolve(), "r", encoding="utf-8")
config_data = json.load(config)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") or ""
COMMAND_PREFIX = config_data.get("COMMAND_PREFIX", "!")
LOG_LEVEL = config_data.get("LOG_LEVEL", "INFO")
OWNER_IDS = [int(id.strip()) for id in config_data.get("OWNER_IDS", "").split(",") if id.strip()]
DATABASE_PATH = os.getenv("DATABASE_PATH") or ""
MODLOG_CHANNEL_ID = int(config_data.get("MODLOG_CHANNEL_ID", "0")) if config_data.get("MODLOG_CHANNEL_ID") else None
DEFAULT_EMBED_COLOR = int(config_data.get("DEFAULT_EMBED_COLOR", "#2f3136").lstrip("#"), 16)

ENABLE_WARN = config_data.get("ENABLE_WARN", "true").lower() == "true"
ENABLE_TIMEOUT = config_data.get("ENABLE_TIMEOUT", "true").lower() == "true"
ENABLE_KICK = config_data.get("ENABLE_KICK", "true").lower() == "true"
ENABLE_BAN = config_data.get("ENABLE_BAN", "true").lower() == "true"
ENABLE_PURGE = config_data.get("ENABLE_PURGE", "true").lower() == "true"
ENABLE_ANTISPAM = config_data.get("ENABLE_ANTISPAM", "true").lower() == "true"
ENABLE_WORD_FILTER = config_data.get("ENABLE_WORD_FILTER", "true").lower() == "true"
ENABLE_JOIN_LOG = config_data.get("ENABLE_JOIN_LOG", "true").lower() == "true"



WARN_ROLES = parse_role_ids("WARN_ROLES")
TIMEOUT_ROLES = parse_role_ids("TIMEOUT_ROLES")
KICK_ROLES = parse_role_ids("KICK_ROLES")
BAN_ROLES = parse_role_ids("BAN_ROLES")
PURGE_ROLES = parse_role_ids("PURGE_ROLES")
ADMIN_ROLES = parse_role_ids("ADMIN_ROLES")
AUTOMOD_MANAGE_ROLES = parse_role_ids("AUTOMOD_MANAGE_ROLES")
IMMUNE_ROLES = parse_role_ids("IMMUNE_ROLES")
AUTOMOD_EXEMPT_ROLES = parse_role_ids("AUTOMOD_EXEMPT_ROLES")

SPAM_MSG_COUNT = int(config_data.get("SPAM_MSG_COUNT", "6"))
SPAM_SECONDS = int(config_data.get("SPAM_SECONDS", "8"))
SPAM_ACTION = config_data.get("SPAM_ACTION", "warn")
SPAM_TIMEOUT_DURATION = config_data.get("SPAM_TIMEOUT_DURATION", "10m")

WORD_FILTER_ACTION = config_data.get("WORD_FILTER_ACTION", "delete")
WORD_FILTER_TIMEOUT_DURATION = config_data.get("WORD_FILTER_TIMEOUT_DURATION", "30m")

MIN_ACCOUNT_AGE_DAYS = int(config_data.get("MIN_ACCOUNT_AGE_DAYS", "7"))
ALERT_ON_LOW_ACCOUNT_AGE = config_data.get("ALERT_ON_LOW_ACCOUNT_AGE", "true").lower() == "true"
