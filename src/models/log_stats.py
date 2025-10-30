import re
import datetime

class LogStats:
    def __init__(self, log_entries: list, total_entries: int):
        self.log_entries = log_entries
        self.total_entries = total_entries

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
    
    def get_most_recent_logs(self, n: int = 5) -> list:
        '''
        Get the most recent n log entries based on their date and time.
        :param n: Number of recent log entries to retrieve.
        :return: List of the most recent log entries.
        :raise ValueError: If n is not a positive integer.
        :raise TypeError: If n is not an integer.
        '''
        if not isinstance(n, int):
            raise TypeError("Parameter n must be an integer.")
        if n <= 0:
            raise ValueError("Parameter n must be a positive integer.")
        # If n is greater than total log entries, adjust n to return all available entries
        if n > self.total_entries:
            n = self.total_entries
        # Return the most recent n log entries based on their date and time
        sorted_entries = sorted(
            self.log_entries,
            key=lambda entry: datetime.datetime.strptime(entry.split(' ')[0] + ' ' + entry.split(' ')[1], '%Y-%m-%d %H:%M:%S'),
            reverse=True
        )
        return sorted_entries[:n]
    
    def compile_default_stats(self) -> dict:
        '''
        Compile default statistics including total entries, by_level, unique user count,
        and recent log entries.
        :return: Dictionary with compiled statistics.
        '''
        return {
            'total_entries': self.total_entries,
            'by_level': self.calculate_log_type_stats(),
            'unique_users': self.get_unique_user_count(),
            'recent_entries': self.get_most_recent_logs()
        }