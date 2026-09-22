import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

with open("data/faq_recursos_app.json", "r", encoding="utf-8") as f:
    artigos = json.load(f)

# Filtra só o artigo getting-started
artigo_alvo = [a for a in artigos if "getting-started" in a["url"]][0]

doc = Document(page_content=artigo_alvo["conteudo"], metadata={"fonte": artigo_alvo["url"]})

splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents([doc])

print(f"Total de chunks gerados para este artigo: {len(chunks)}\n")
for i, chunk in enumerate(chunks, 1):
    print(f"--- Chunk {i} ({len(chunk.page_content)} caracteres) ---")
    print(chunk.page_content)
    print()