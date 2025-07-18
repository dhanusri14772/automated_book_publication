import os
import shutil
from agents import writer_agent, reviewer_agent, reward_system
from agents.human_loop import human_in_loop_menu, open_editor
from agents import voice  


CHAPTER_ID = "Chapter_1"
DATA_DIR = "data"
VERSION_DIR = f"versions/{CHAPTER_ID}"
LOGS_DIR = "logs"
RAW_INPUT_PATH = os.path.join(DATA_DIR, f"{CHAPTER_ID}.txt")
N_ITERATIONS = 5

os.makedirs(VERSION_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

def get_latest_version_number():
    existing = [f for f in os.listdir(VERSION_DIR) if f.startswith('v') and f.endswith('.txt')]
    numbers = [int(f[1:-4]) for f in existing if f[1:-4].isdigit()]
    return max(numbers) if numbers else 1

def main():
    print("Starting Book Pipeline for:", CHAPTER_ID)

    v1_path = os.path.join(VERSION_DIR, "v1.txt")
    if not os.path.exists(v1_path):
        print("Copying original raw input to v1.txt...")
        shutil.copyfile(RAW_INPUT_PATH, v1_path)

    current_version = 1

    for i in range(N_ITERATIONS):
        print(f"\n Iteration {i+1} — Processing v{current_version}.txt")

        current_path = os.path.join(VERSION_DIR, f"v{current_version}.txt")
        with open(current_path, "r", encoding="utf-8") as f:
            text = f.read()

        print(" Rewriting text with writer agent...")
        rewritten = writer_agent.spin_paragraph(text)

        print("Reviewing text with reviewer agent...")
        reviewed = reviewer_agent.ai_review_text(rewritten)

        next_version = current_version + 1
        next_path = os.path.join(VERSION_DIR, f"v{next_version}.txt")
        with open(next_path, "w", encoding="utf-8") as f:
            f.write(reviewed)
        print(f"Saved reviewed version: v{next_version}.txt")

       
        use_voice = input(" Use voice input? (y/N): ").strip().lower() == 'y'

        if use_voice:
            voice.speak("Do you want to accept, edit, revise or finalize this version?")
            print(" Say: accept / edit / revise / final")
            decision = voice.listen_for_command(["accept", "edit", "revise", "final"])
        else:
            decision = human_in_loop_menu(reviewed)

        if decision == "accept":
            rating = input("Rate this version (1-5): ")
            rating = int(rating.strip()) if rating.isdigit() else 3
            reward_system.log_feedback(CHAPTER_ID, f"v{next_version}", 'Y', rating)
            current_version = next_version
            print("Accepted. Moving forward.")

        elif decision == "edit":
            open_editor(next_path)
            print("Saving edited version.")
            rating = input(" Rate edited version (1-5): ")
            rating = int(rating.strip()) if rating.isdigit() else 4
            reward_system.log_feedback(CHAPTER_ID, f"v{next_version}", 'Y', rating)
            current_version = next_version

        elif decision == "revise":
            print("Triggering re-spin from current version.")
            continue

        elif decision == "final":
            print("Finalization requested. Stopping iterations.")
            break

    print("\n All iterations complete. You may now proceed to indexing with ChromaDB.")

if __name__ == "__main__":
    main()
