from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="bge-m3")
vectorstore = Chroma(persist_directory="vectorstore_teste", embedding_function=embeddings)

pergunta = "Não consigo ouvir nenhum som, o que fazer?"
resultados = vectorstore.similarity_search_with_score(pergunta, k=5)

for i, (doc, score) in enumerate(resultados, 1):
    print(f"{i}º - distância: {score:.4f} - fonte: {doc.metadata['fonte']}")