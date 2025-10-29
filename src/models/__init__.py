"""
Models package for log analyzer.
Contains data structures for representing log entries and statistics.
"""

from .log_entry import LogEntry
from .log_stats import LogStats

# This makes LogEntry available when doing: from models import LogEntry
__all__ = ['LogEntry', 'LogStats']
