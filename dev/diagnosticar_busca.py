from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="bge-m3")
vectorstore = Chroma(
    persist_directory="vectorstore_teste",
    embedding_function=embeddings
)

pergunta = "Como eu crio uma conta no Spotify?"
resultados = vectorstore.similarity_search_with_score(pergunta, k=10)

print(f"Pergunta: {pergunta}\n")
for i, (doc, score) in enumerate(resultados, 1):
    print(f"{i}º lugar (distância: {score:.4f}) - Fonte: {doc.metadata['fonte']}")
    print(f"    {doc.page_content[:100]}...")
    print()