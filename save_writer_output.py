import os

os.makedirs("versions/Chapter_1", exist_ok=True)

content = """Once upon a time, in a small village nestled between the hills, lived a young girl named Sarah. Despite her family's meagre means, Sarah dreamed of attending the prestigious school in the neighbouring city. With perseverance and hard work, Sarah managed to secure a scholarship and eventually achieve her dream. She went on to become a successful doctor in the city and eventually returned to her small village to serve the people she had grown up with."""

with open("versions/Chapter_1/v1.txt", "w") as f:
    f.write(content.strip())

print("[+] Saved v1.txt successfully.")
