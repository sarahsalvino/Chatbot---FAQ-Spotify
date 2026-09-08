import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma

with open("data/faq_recursos_app.json", "r", encoding="utf-8") as f:
    artigos = json.load(f)

documentos = []
for artigo in artigos:
    doc = Document(
        page_content=artigo["conteudo"],
        metadata={"titulo": artigo["titulo"], "fonte": artigo["url"]}
    )
    documentos.append(doc)

print(f"Total de artigos carregados: {len(documentos)}")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documentos)

print(f"Total de chunks gerados: {len(chunks)}")

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="vectorstore_teste"
)

print("Indexação concluída!")

pergunta = "Como eu ouço músicas em ordem aleatória?"
resultados = vectorstore.similarity_search(pergunta, k=3)

print(f"\nPergunta: {pergunta}")
print("\nChunks mais relevantes encontrados:")
for i, resultado in enumerate(resultados, 1):
    print(f"\n--- Resultado {i} ---")
    print(f"Fonte: {resultado.metadata['fonte']}")
    print(f"Conteúdo: {resultado.page_content[:200]}...")