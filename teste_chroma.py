print("Importando bibliotecas...")
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
print("Importação concluída!")

print("Testando geração de UM embedding...")
embeddings = OllamaEmbeddings(model="nomic-embed-text")
resultado = embeddings.embed_query("teste simples")
print(f"Embedding gerado! Tamanho do vetor: {len(resultado)}")