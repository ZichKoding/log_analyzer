from src.models.log_entry import LogEntry
from src.models.log_stats import LogStats

read_log_file_path = 'logs/server.log'

if __name__ == "__main__":
    # Create an instance of LogEntry to read log entries from the file
    log_entry = LogEntry()
    log_data = log_entry.read_log(read_log_file_path)
    
    log_entries = log_data['entries']
    total_entries = log_data['total_entries']
    
    # Create an instance of LogStats to analyze the log entries
    log_stats = LogStats(log_entries, total_entries)
    
    # Get unique user count
    unique_user_count = log_stats.get_unique_user_count()
    print(f"Unique User Count: {unique_user_count}")
    
    # Calculate log type statistics
    log_type_stats = log_stats.calculate_log_type_stats()
    print("Log Type Statistics:")
    for log_type, count in log_type_stats.items():
        print(f"{log_type}: {count}")
