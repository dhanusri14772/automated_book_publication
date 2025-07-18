import ollama
import os

def spin_paragraph(paragraph):
    prompt = f"Please rewrite the following paragraph with variation: {paragraph}"
    response = ollama.chat(model='llama2:7b', messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']

if __name__ == "__main__":
    input_path = "data/chapter_1.txt"
    output_dir = "versions/Chapter_1"
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as f:
        paragraph = f.read()

    spun = spin_paragraph(paragraph)

    output_path = os.path.join(output_dir, "v1.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(spun)

    print("[+] Spun text saved to:", output_path)

