import ollama

response = ollama.chat(model='mistral', messages=[
    {"role": "user", "content": "Rewrite this: I love programming in Python."}
])

print(response['message']['content'])
