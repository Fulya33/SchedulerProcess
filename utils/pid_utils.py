"""Process ID utility functions"""
import re
from typing import Tuple


def pid_key(pid: str) -> Tuple[int, int]:
    """
    Extract numeric part of PID for proper sorting (P10 > P2, not P10 < P2)
    Returns a tuple for sorting that handles both numeric and non-numeric PIDs:
    - (0, int_value) for numeric PIDs (sorted first, by number)
    - (1, pid_string) for non-numeric PIDs (sorted after, alphabetically)
    """
    m = re.search(r'\d+', pid)
    if m:
        return (0, int(m.group()))  # Numeric PIDs come first
    else:
        return (1, pid)  # Non-numeric PIDs come after, sorted alphabetically


