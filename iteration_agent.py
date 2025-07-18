import os
import datetime
import subprocess
import sys 

VERSION_DIR = 'versions/Chapter_1'
REVIEW_LOG = os.path.join(VERSION_DIR, 'review_log.txt')
os.makedirs(VERSION_DIR, exist_ok=True)

def get_timestamp():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def get_latest_version_number():
    versions = sorted([f for f in os.listdir(VERSION_DIR) if f.startswith('v') and f.endswith('.txt')])
    if not versions:
        return 0
    return int(versions[-1].replace('v', '').replace('.txt', ''))

def edit_file(filepath):
    print(f" Opening file for manual editing: {filepath}")
    subprocess.call(['notepad', filepath])  
    print("Manual edit complete.")

if __name__ == "__main__":
    latest_version = get_latest_version_number()
    latest_file = os.path.join(VERSION_DIR, f'v{latest_version}.txt')

    print(f" Latest version is: v{latest_version}")
    with open(latest_file, 'r') as f:
        print("\n--- Current Version Preview ---\n")
        print(f.read())
        print("\n-------------------------------\n")

    response = input("[?] Do you want to edit this version manually? (Y/n): ")
    if response.lower() == 'y':
        new_version_number = latest_version + 1
        new_file = os.path.join(VERSION_DIR, f'v{new_version_number}.txt')
        with open(new_file, 'w') as f:
            f.write(open(latest_file).read()) 
        edit_file(new_file)

        review_again = input("[?] Send edited version to AI reviewer? (Y/n): ")
        if review_again.lower() == 'y':
            print(" Reviewing your edited content...")
            subprocess.call([sys.executable, "agents/reviewer_agent.py"])

        with open(REVIEW_LOG, 'a') as log:
            log.write(f"{get_timestamp()} - Manual edit: v{new_version_number}.txt\n")

        print(f" Saved new version: v{new_version_number}.txt")
    else:
        print("Edit skipped.")

