"""Helper utilities for Discord bot extension"""

def format_number(num: int) -> str:
    """Format number with thousands separator"""
    return f"{num:,}"

def format_sats(sats: int) -> str:
    """Format sats as K if over 1000"""
    if sats >= 1000:
        return f"{sats/1000:.1f}K"
    return str(sats)
