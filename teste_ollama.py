import ollama

resposta = ollama.chat(
    model="mistral",
    messages=[
        {"role": "user", "content": "Qual a capital do Brasil?"}
    ]
)

print(resposta["message"]["content"])