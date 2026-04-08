"""
Utility functions for the agents.
"""

from datetime import datetime

# ===== UTILITY FUNCTIONS =====


def get_today_str() -> str:
    """
    Get current date in a human-readable format.
    """
    return datetime.now().strftime("%a %b %-d, %Y")
