import ollama

response = ollama.chat(
    model="llama3.1:8b",
    messages=[
        {
            "role": "user",
            "content": "Say hello to Niched in one sentence."
        }
    ]
)

print(response["message"]["content"])