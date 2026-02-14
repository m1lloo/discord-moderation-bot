import re

def parse_duration(duration_str):
    pattern = r'^(\d+)([smhdw])$'
    match = re.match(pattern, duration_str.lower())
    
    if not match:
        return None
    
    amount, unit = match.groups()
    amount = int(amount)
    
    multipliers = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'w': 604800
    }
    
    return amount * multipliers[unit]

def format_duration(seconds):
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours}h"
    elif seconds < 604800:
        days = seconds // 86400
        return f"{days}d"
    else:
        weeks = seconds // 604800
        return f"{weeks}w"
