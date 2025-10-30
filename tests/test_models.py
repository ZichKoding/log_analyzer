'''
Unit tests for the LogEntry model.
Tests the data structure used to represent individual log entries.
'''

import os
import sys
import unittest
import tempfile

from pathlib import Path
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from models.log_entry import LogEntry
from models.log_stats import LogStats


class TestLogEntryModel(unittest.TestCase):
    '''
    Test cases for the LogEntry model. The LogEntry model is only used to format the logs from reading the log files.
    '''
    def setUp(self):
        '''
        Set up test case with a sample LogEntry instance in a file.
        '''
        print("Setting up TestLogEntryModel...")
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, 'test_log.log')

        # Create multiple log entries with variety
        log_lines = [
            "2025-10-20 09:15:42 INFO User registration: sarah.miller@techcorp.com",
            "2025-10-20 10:22:18 WARNING Disk space below 20% on /dev/sda1",
            "2025-10-20 11:45:33 ERROR Failed to send email to admin@company.org",
            "2025-10-20 13:08:55 INFO User login: bob.wilson@startup.io",
            "2025-10-20 14:30:12 CRITICAL System reboot required after update",
            "2025-10-20 15:17:29 WARNING API rate limit exceeded for client 192.168.1.100",
            "2025-10-20 16:42:07 INFO Password changed for user: kate.jones@domain.net"
        ]

        print(f"Creating test log file at {self.log_file} with sample log entries.")
        # Write log lines to a test log file
        with open(self.log_file, 'w') as f:
            f.write('\n'.join(log_lines) + '\n')
        print(f"Test log file created at {self.log_file}")

    def tearDown(self):
        '''Clean up the test log file after tests.'''
        import shutil
        print(f"Cleaning up temporary directory {self.temp_dir}")
        shutil.rmtree(self.temp_dir)
        print(f"Temporary directory {self.temp_dir} cleaned up.")

    def test_log_entry_read_log_file_success(self):
        '''
        Test reading log entries from a file.
        '''
        log_entry = LogEntry()
        result = log_entry.read_log(self.log_file)
        self.assertEqual(result['total_entries'], 7)
        self.assertEqual(len(result['entries']), 7)
        self.assertIn("2025-10-20 09:15:42 INFO User registration: sarah.miller@techcorp.com", result['entries'])

    def test_log_entry_read_log_file_does_not_exist(self):
        '''
        Test reading log entries from a non-existent file.
        '''
        log_entry = LogEntry()
        result = log_entry.read_log("non_existent.log")
        self.assertEqual(result['total_entries'], 0)
        self.assertEqual(len(result['entries']), 0)

    def test_log_entry_read_log_file_not_log_or_txt(self):
        '''
        Test reading log entries that is not a .log or .txt file.
        '''
        log_entry = LogEntry()
        result = log_entry.read_log("invalid_file.pdf")
        self.assertEqual(result['total_entries'], 0)
        self.assertEqual(len(result['entries']), 0)

    def test_log_entry_read_log_file_return_type(self):
        '''
        Test that the read_log method returns the correct types.
        '''
        log_entry = LogEntry()
        result = log_entry.read_log(self.log_file)
        self.assertIsInstance(result['total_entries'], int)
        self.assertIsInstance(result['entries'], list)
        for entry in result['entries']:
            self.assertIsInstance(entry, str)

    def test_log_entry_read_log_file_incorrect_parameter_type(self):
        '''
        Test reading log entries with incorrect parameter type.
        '''
        log_entry = LogEntry()
        with self.assertRaises(TypeError):
            log_entry.read_log(12345)  # Passing an integer instead of a string for file_path
            log_entry.read_log(None)  # Passing None instead of a string for file_path
            log_entry.read_log([])  # Passing a list instead of a string for file_path
            log_entry.read_log({})  # Passing a dict instead of a string for file_path
            log_entry.read_log(object())  # Passing an object instead of a string for file_path


class TestLogStatsModel(unittest.TestCase):
    '''
    Test cases for the LogStats model. The LogStats model is used to generate statistics from log entries.
    '''
    def setUp(self):
        '''
        Set up test case with sample log entries.
        '''
        print("Setting up TestLogStatsModel...")
        self.sample_log_entries = [
            "2025-10-20 09:15:42 INFO User registration: sarah.miller@techcorp.com",
            "2025-10-20 10:22:18 WARNING Disk space below 20% on /dev/sda1",
            "2025-10-20 11:45:33 ERROR Failed to send email to admin@company.org",
            "2025-10-20 13:08:55 INFO User login: bob.wilson@startup.io",
            "2025-10-20 14:30:12 CRITICAL System reboot required after update",
            "2025-10-20 15:17:29 WARNING API rate limit exceeded for client 192.168.1.100",
            "2025-10-20 16:42:07 INFO Password changed for user: kate.jones@domain.net"
        ]
        self.total_entries = len(self.sample_log_entries)
        print(f"Sample log entries set up with total entries: {self.total_entries}")
        self.log_stats = LogStats(self.sample_log_entries, self.total_entries)

    def tearDown(self):
        '''Clean up after tests.'''
        print("Tearing down TestLogStatsModel...")
        del self.log_stats
        print("TestLogStatsModel torn down.")

    def test_get_unique_user_count(self):
        '''
        Test calculating the number of unique users in log entries.
        '''
        unique_user_count = self.log_stats.get_unique_user_count()
        self.assertEqual(unique_user_count, 3)  # sarah.miller, bob.wilson, kate.jones

    def test_get_unique_user_count_no_users(self):
        '''
        Test calculating unique users when there are no user entries.
        '''
        log_stats_no_users = LogStats([
            "2025-10-20 10:22:18 WARNING Disk space below 20% on /dev/sda1",
            "2025-10-20 14:30:12 CRITICAL System reboot required after update",
            "2025-10-20 15:17:29 WARNING API rate limit exceeded for client 192.168.1.100"
        ], 0)
        unique_user_count = log_stats_no_users.get_unique_user_count()
        self.assertEqual(unique_user_count, 0)

    def test_calculate_log_type_stats(self):
        '''
        Test calculating log type statistics.
        '''
        stats = self.log_stats.calculate_log_type_stats()
        expected_stats = {
            'INFO': 3,
            'ERROR': 1,
            'WARNING': 2
        }
        self.assertEqual(stats, expected_stats)

if __name__ == '__main__':
    unittest.main()