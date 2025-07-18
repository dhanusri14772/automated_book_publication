import subprocess
import os
import sys

def human_in_loop_menu(version_text: str) -> str:
    print("\n🔍 --- Human-in-the-Loop Review ---")
    print("AI Output:\n", version_text)
    print("\nOptions:")
    print("1. Accept and continue")
    print("2. Edit manually")
    print("3. Ask AI to revise again")
    print("4. Skip to finalization")
    
    choice = input(" Your choice (1/2/3/4): ").strip()

    if choice == "1":
        return "accept"
    elif choice == "2":
        return "edit"
    elif choice == "3":
        return "revise"
    elif choice == "4":
        return "final"
    else:
        print("Invalid choice. Defaulting to Accept.")
        return "accept"

def open_editor(filepath):
    print(f" Opening {filepath} in notepad...")
    subprocess.call(['notepad', filepath])
    print(" Edit complete.")
