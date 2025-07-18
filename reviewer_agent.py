import os
import datetime
from ollama import chat
from .reward_system import log_feedback  

VERSION_DIR = 'versions/Chapter_1'
os.makedirs(VERSION_DIR, exist_ok=True)

def get_timestamp():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def get_next_version():
    existing = [f for f in os.listdir(VERSION_DIR) if f.endswith('.txt')]
    versions = [int(f[1:-4]) for f in existing if f.startswith('v') and f[1:-4].isdigit()]
    return f"v{max(versions) + 1 if versions else 2}"  # v2 if only v1 exists

def ai_review_text(text):
    messages = [
        {
            "role": "user",
            "content": f"You're an expert editor. Review the following paragraph for clarity, grammar, and tone. Give suggestions and then provide an improved version.\n\n{text}"
        }
    ]
    
    response = chat(model='llama2:7b', messages=messages)
    return response['message']['content']

if __name__ == "__main__":
    input_file = os.path.join(VERSION_DIR, 'v1.txt')  # Or detect latest version dynamically
    with open(input_file, 'r') as f:
        original_text = f.read()

    reviewed_text = ai_review_text(original_text)

    new_version = get_next_version()
    output_file = os.path.join(VERSION_DIR, f"{new_version}.txt")
    with open(output_file, 'w') as f:
        f.write(reviewed_text)

    print(f"[+] Review complete. Saved as: {output_file}")

    print("\n--- AI REVIEWER OUTPUT ---\n")
    print(reviewed_text)

    accepted = input("\n[?] Do you want to accept this version (Y/n)? ").strip().lower()
    accepted_flag = 'Y' if accepted == 'y' else 'N'

    rating = input("Rate the quality of this version (1-5): ").strip()
    try:
        rating = int(rating)
    except ValueError:
        rating = 3  

  
    log_feedback(
        chapter="Chapter_1",
        version=new_version,
        accepted=accepted_flag,
        rating=rating
    )

    if accepted_flag == 'Y':
        print("Review accepted. Moving to next phase...")
    else:
        print("Review rejected. You may revise manually or rerun the reviewer.")
