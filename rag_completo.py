from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

# 1. Reconectar ao vectorstore que já existe (não reindexar!)
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(
    persist_directory="vectorstore_teste",
    embedding_function=embeddings
)

# 2. Fazer a pergunta e buscar os chunks mais relevantes
pergunta = "Como eu ouço músicas em ordem aleatória?"
resultados = vectorstore.similarity_search(pergunta, k=3)

# 3. Montar o contexto (juntando o texto dos chunks encontrados)
contexto = "\n\n".join([r.page_content for r in resultados])

# 4. Coletar as fontes (sem repetir URLs duplicadas)
fontes = list(set([r.metadata["fonte"] for r in resultados]))

# 5. Montar o prompt final pro LLM
prompt = f"""Você é um assistente de suporte do Spotify. Responda a pergunta do usuário APENAS com base no contexto abaixo. Se a resposta não estiver no contexto, diga que não sabe.

Contexto:
{contexto}

Pergunta: {pergunta}

Resposta:"""

# 6. Chamar o Mistral pra gerar a resposta
llm = ChatOllama(model="mistral")
resposta = llm.invoke(prompt)

# 7. Mostrar o resultado final
print("Resposta do chatbot:")
print(resposta.content)

print("\nFontes utilizadas:")
for fonte in fontes:
    print(f"- {fonte}")