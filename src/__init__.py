'''
Need to initialize the src package.
This file can be left empty or can include package-level docstrings or imports if necessary.
'''
from .models.log_entry import LogEntry
from .models.log_stats import LogStats

# You can add package-level variables or functions here if needed
__all__ = ['LogEntry', 'LogStats']