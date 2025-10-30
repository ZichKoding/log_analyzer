import re
from .log_entry import LogEntry

class LogStats:
    def __init__(self, log_entries: list, total_entries: int):
        self.log_entries = log_entries
        self.total_entries = total_entries
        self.stats = {}

    def get_unique_user_count(self) -> int:
        '''
        Calculate the number of unique users in the log entries. For this to work,
        the log entries must have a format that includes user identification.
        Example: "2025-10-20 10:23:45 INFO User <action>: <user_email>", user: <user_email>
        regex pattern: r'User (?:login|registration|changed for user): (\S+@\S+\.\S+)', r'user: (\S+@\S+\.\S+)'
        :return: Count of unique users.
        '''
        users = set()
        # Regex pattern to extract user emails from log entries, which looks for lines indicating user actions and captures the email.
        user_pattern1 = re.compile(r'User (?:[A-Za-z ]+): (\S+@\S+\.\S+)', re.IGNORECASE)
        user_pattern2 = re.compile(r'user: (\S+@\S+\.\S+)')
        # Iterate through log entries and extract user emails
        for entry in self.log_entries:
            match = user_pattern1.search(entry)
            if not match:
                match = user_pattern2.search(entry)
            if match:
                print(f"Found user: {match.group(1)} in entry: {entry}")
                users.add(match.group(1))
        # Return the count of unique users
        return len(users)
    
    def calculate_log_type_stats(self) -> dict:
        '''
        Calculate statistics for different log types (INFO, WARNING, ERROR).
        :return: Dictionary with counts of each log type.
        '''
        # Initialize log type statistics
        log_types = ['INFO', 'WARNING', 'ERROR']
        # Create a dictionary to hold the count of each log type
        stats = {log_type: 0 for log_type in log_types}
        # Count occurrences of each log type in the log entries
        for entry in self.log_entries:
            for log_type in log_types:
                if f' {log_type} ' in entry:
                    stats[log_type] += 1
        # Store and return the statistics
        self.stats = stats
        return stats