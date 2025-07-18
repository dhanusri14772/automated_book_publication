import os
import csv
from datetime import datetime

LOG_FILE = "logs/rewards.csv"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_feedback(chapter, version, accepted, rating):
    """
    Logs human feedback for rewritten versions (for RL training).
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['chapter', 'version', 'accepted', 'rating', 'timestamp'])
        writer.writerow([chapter, version, accepted, rating, timestamp])

    print(f"[+] Feedback logged to {LOG_FILE}")

SEARCH_LOG_FILE = "logs/search_feedback.csv"
os.makedirs(os.path.dirname(SEARCH_LOG_FILE), exist_ok=True)

def log_search_feedback(chapter, chunk_id, query, rating):
    """
    Logs user feedback on semantic search results (chunk-level).
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_exists = os.path.isfile(SEARCH_LOG_FILE)

    with open(SEARCH_LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['chapter', 'chunk_id', 'query', 'rating', 'timestamp'])
        writer.writerow([chapter, chunk_id, query, rating, timestamp])

    print(f"[+] Search feedback logged to {SEARCH_LOG_FILE}")

