import os

class LogEntry:
    def __init__(self):
        self.entries = []
        self.total_entries = 0

    def read_log(self, file_path: str) -> dict:
        '''
        Reads the log file and returns a list of LogEntry instances.
        :param file_path: Path to the log file.
        :return: Dictionary with log total number of entries and list of entries.
        '''
        entries = []

        # Validate parameter type
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string.")

        # Verify file extension is .log or .txt
        if not (file_path.endswith('.log') or file_path.endswith('.txt')):
            print("Invalid file type. Only .log and .txt files are supported.")
            return {"total_entries": 0, "entries": []}
        
        # Check if file exists
        if not os.path.isfile(file_path):
            print(f"Log file {file_path} does not exist.")
            return {"total_entries": 0, "entries": []}

        # Read log file
        try: 
            with open(file_path, 'r') as f:
                for line in f:
                    # Assuming each line is a log entry append it to entries
                    entries.append(line.strip())
        except Exception as e:
            print(f"Error reading log file: {e}")
            return {"total_entries": 0, "entries": []}

        # Update total entries
        self.total_entries = len(entries)
        self.entries = entries

        return {
            "total_entries": self.total_entries,
            "entries": self.entries
        }