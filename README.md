# Discord Moderation Bot

A powerful, configurable Discord moderation bot built with discord.py 2.3+.

## Features

- **Warning System** - Warn users, view warnings, clear warnings
- **Timeout Management** - Timeout users with flexible duration parsing
- **Kick/Ban/Unban** - Full moderation actions with role hierarchy
- **Message Purging** - Delete multiple messages at once
- **Anti-Spam** - Automatic spam detection and action
- **Word Filter** - Configurable banned words with multiple actions
- **Join Logging** - Track member joins/leaves with account age alerts
- **Case Management** - SQLite database for all moderation actions
- **Role-Based Permissions** - Granular control via environment variables
- **Modlog Channel** - Detailed embed logs for all actions

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure your settings
4. Run the bot:
   ```bash
   python main.py
   ```

## Configuration

All settings are configured through environment variables in `.env`:

### Required
- `DISCORD_TOKEN` - Your bot token
- `COMMAND_PREFIX` - Command prefix (default: `!`)
- `DATABASE_PATH` - SQLite database path (default: `data/modbot.sqlite3`)
- `MODLOG_CHANNEL_ID` - Channel ID for moderation logs

### Feature Toggles
- `ENABLE_WARN` - Enable warning commands
- `ENABLE_TIMEOUT` - Enable timeout commands
- `ENABLE_KICK` - Enable kick commands
- `ENABLE_BAN` - Enable ban commands
- `ENABLE_PURGE` - Enable purge commands
- `ENABLE_ANTISPAM` - Enable anti-spam
- `ENABLE_WORD_FILTER` - Enable word filter
- `ENABLE_JOIN_LOG` - Enable join/leave logging

### Role Permissions
- `WARN_ROLES` - Role IDs that can use warn commands
- `TIMEOUT_ROLES` - Role IDs that can use timeout commands
- `KICK_ROLES` - Role IDs that can use kick commands
- `BAN_ROLES` - Role IDs that can use ban commands
- `PURGE_ROLES` - Role IDs that can use purge commands
- `ADMIN_ROLES` - Role IDs for admin commands
- `AUTOMOD_MANAGE_ROLES` - Role IDs that can manage automod
- `IMMUNE_ROLES` - Role IDs immune from moderation
- `AUTOMOD_EXEMPT_ROLES` - Role IDs exempt from automod

### Automod Settings
- `SPAM_MSG_COUNT` - Messages threshold for spam detection
- `SPAM_SECONDS` - Time window for spam detection
- `SPAM_ACTION` - Action for spam (warn/timeout)
- `SPAM_TIMEOUT_DURATION` - Duration for spam timeouts
- `WORD_FILTER_ACTION` - Action for banned words (delete/delete_warn/delete_timeout)
- `WORD_FILTER_TIMEOUT_DURATION` - Duration for word filter timeouts
- `MIN_ACCOUNT_AGE_DAYS` - Minimum account age before alert
- `ALERT_ON_LOW_ACCOUNT_AGE` - Alert on young accounts

## Commands

All commands support both slash (`/`) and prefix (`!`) usage.

### Moderation
- `/warn @user [reason]` - Warn a user
- `/warnings [@user]` - View warnings
- `/clearwarnings @user` - Clear all warnings
- `/timeout @user duration [reason]` - Timeout a user
- `/untimeout @user [reason]` - Remove timeout
- `/kick @user [reason]` - Kick a user
- `/ban @user [reason] [delete_days]` - Ban a user
- `/unban user_id [reason]` - Unban a user
- `/purge amount` - Delete messages

### Automod
- `/automod` - View automod status
- `/automod reloadwords` - Reload banned words

## Duration Format

Durations support these formats:
- `10s` - 10 seconds
- `10m` - 10 minutes
- `2h` - 2 hours
- `3d` - 3 days
- `1w` - 1 week

## File Structure

```
├── main.py              # Bot entry point
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore file
├── README.md           # This file
├── cogs/               # Bot modules
│   ├── moderation.py   # Moderation commands
│   ├── automod.py      # Auto-mod features
│   └── events.py       # Event handlers
├── utils/              # Utility modules
│   ├── config.py       # Configuration management
│   ├── logger.py       # Logging setup
│   ├── duration.py     # Duration parsing
│   ├── checks.py       # Permission checks
│   └── embeds.py       # Embed creation
├── services/           # Core services
│   └── db.py           # Database wrapper
├── data/               # Data files
│   └── banned_words.txt # Banned words list
└── logs/               # Log files (created automatically)
```

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.

### What this means:

**You are free to:**
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

**Under the following terms:**
- **Attribution** — You must give appropriate credit to the original author (usxer), provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **NonCommercial** — You may not use the material for commercial purposes. Commercial use is any use primarily intended for or directed toward commercial advantage or monetary compensation.

**No additional restrictions** — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

### Attribution Example
If you use this code in your project, please include credit like:
```
Discord Moderation Bot by m1lloo
Original: https://github.com/m1lloo/discord-moderation-bot
Licensed under CC BY-NC 4.0
```

### Full License
For the full license text, see: https://creativecommons.org/licenses/by-nc/4.0/
