import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

CAMINHO_FAQ = "data/faq_recursos_app.json"
CAMINHO_VECTORSTORE = "backend/vectorstore"

def indexar_faq():
    with open(CAMINHO_FAQ, "r", encoding="utf-8") as f:
        artigos = json.load(f)

    documentos = []
    for artigo in artigos:
        doc = Document(
            page_content=artigo["conteudo"],
            metadata={"titulo": artigo["titulo"], "fonte": artigo["url"]}
        )
        documentos.append(doc)

    print(f"Total de artigos carregados: {len(documentos)}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_documents(documentos)
    print(f"Total de chunks gerados: {len(chunks)}")

    embeddings = OllamaEmbeddings(model="bge-m3")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CAMINHO_VECTORSTORE
    )
    print("Indexação concluída!")


if __name__ == "__main__":
    indexar_faq()