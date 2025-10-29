# Challenge 1: Log Analyzer Web Dashboard (30 minutes, Beginner)

## Problem Statement

Build a simple HTTP server that reads server log files, analyzes them, and displays statistics through a web interface. This challenge introduces basic web server concepts, simple data structures, and file processing.

## Specific Requirements

Create a program that:

1. **Reads log files** from a `logs/` directory containing entries like:
   ```
   2025-10-20 14:23:15 INFO User login: john@example.com
   2025-10-20 14:24:03 ERROR Database connection failed
   2025-10-20 14:25:10 INFO User logout: jane@example.com
   ```

2. **Analyzes logs** to extract:
   - Total number of entries
   - Count by log level (INFO, WARNING, ERROR)
   - Most recent 5 log entries
   - Count of unique users mentioned

3. **Serves a simple web interface** with:
   - Homepage displaying statistics as HTML
   - `/api/stats` endpoint returning JSON data
   - Basic error handling for missing files

4. **Uses only standard library**: `http.server`, `pathlib`, `json`, `collections`, `datetime`

## Implementation Requirements

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from collections import Counter
import json

class LogAnalyzerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Implement routing for / and /api/stats
        pass

    def analyze_logs(self) -> dict:
        # Read and analyze log files
        pass
```

## Success Criteria

- ✅ Server starts on port 8000 without errors
- ✅ Homepage displays log statistics in readable HTML
- ✅ `/api/stats` returns valid JSON with all required metrics
- ✅ Handles missing log directory gracefully (no crashes)
- ✅ Uses `pathlib` for all file operations
- ✅ Properly counts log levels using `Counter`
- ✅ Code includes type hints on main functions

## Example Use Cases

**Test Setup:**
```python
# Create logs directory with sample data
Path('logs').mkdir(exist_ok=True)
Path('logs/server.log').write_text("""
2025-10-20 14:23:15 INFO User login: john@example.com
2025-10-20 14:24:03 ERROR Database connection failed
2025-10-20 14:25:10 INFO User logout: jane@example.com
2025-10-20 14:26:22 WARNING High memory usage detected
2025-10-20 14:27:05 INFO User login: alice@example.com
""")
```

**Expected Output at `/api/stats`:**
```json
{
  "total_entries": 5,
  "by_level": {
    "INFO": 3,
    "ERROR": 1,
    "WARNING": 1
  },
  "unique_users": 3,
  "recent_entries": [
    "2025-10-20 14:27:05 INFO User login: alice@example.com",
    "2025-10-20 14:26:22 WARNING High memory usage detected",
    "2025-10-20 14:25:10 INFO User logout: jane@example.com",
    "2025-10-20 14:24:03 ERROR Database connection failed",
    "2025-10-20 14:23:15 INFO User login: john@example.com"
  ]
}
```

## Hints and Guidance

1. **File Reading Pattern**:
   ```python
   log_files = Path('logs').glob('*.log')
   for log_file in log_files:
       content = log_file.read_text()
       lines = content.strip().splitlines()
   ```

2. **Parsing Log Lines**: Use `str.split()` with maxsplit to separate timestamp, level, and message:
   ```python
   parts = line.split(maxsplit=3)  # ['2025-10-20', '14:23:15', 'INFO', 'message...']
   ```

3. **Counting**: Use `collections.Counter` for efficient counting:
   ```python
   from collections import Counter
   levels = Counter()
   levels[log_level] += 1
   ```

4. **HTML Response Template**:
   ```python
   html = f"""
   <!DOCTYPE html>
   <html>
   <head><title>Log Analyzer</title></head>
   <body>
       <h1>Server Log Statistics</h1>
       <p>Total Entries: {stats['total_entries']}</p>
       <h2>By Level:</h2>
       <ul>
           <li>INFO: {stats['by_level'].get('INFO', 0)}</li>
           <li>WARNING: {stats['by_level'].get('WARNING', 0)}</li>
           <li>ERROR: {stats['by_level'].get('ERROR', 0)}</li>
       </ul>
   </body>
   </html>
   """
   ```

5. **JSON Serialization**: Convert Counter to dict for JSON:
   ```python
   json.dumps({'by_level': dict(counter)})
   ```

## Bonus Challenges

1. **Email Extraction** (⭐): Use regex to extract and count all email addresses mentioned in logs
2. **Time Range Filtering** (⭐): Add query parameters like `/api/stats?hours=24` to filter recent logs
3. **Error Rate Alert** (⭐⭐): Display a warning if ERROR count exceeds 10% of total entries
4. **Multiple Files** (⭐⭐): Handle multiple `.log` files in the directory and combine statistics
5. **Live Refresh** (⭐⭐⭐): Add auto-refresh to HTML using `<meta>` tag so page updates every 5 seconds

## Testing Your Solution

```python
# test_challenge1.py
import unittest
from pathlib import Path
import requests
import subprocess
import time

class TestLogAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start server in background
        cls.server_process = subprocess.Popen(['python', 'challenge1.py'])
        time.sleep(2)  # Wait for server to start

    @classmethod
    def tearDownClass(cls):
        cls.server_process.terminate()

    def test_homepage(self):
        response = requests.get('http://localhost:8000/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Log Statistics', response.text)

    def test_api_stats(self):
        response = requests.get('http://localhost:8000/api/stats')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total_entries', data)
        self.assertIn('by_level', data)
```

## Learning Outcomes

- HTTP request/response cycle
- Basic routing concepts
- File I/O with pathlib
- Simple data aggregation
- JSON serialization
