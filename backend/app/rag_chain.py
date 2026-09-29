from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

CAMINHO_VECTORSTORE = "backend/vectorstore"

embeddings = OllamaEmbeddings(model="bge-m3", keep_alive=3600)
vectorstore = Chroma(persist_directory=CAMINHO_VECTORSTORE, embedding_function=embeddings)
llm = ChatOllama(model="mistral", keep_alive="60m")

def responder_pergunta(pergunta: str) -> dict:
    resultados = vectorstore.similarity_search(pergunta, k=5)
    contexto = "\n\n".join([r.page_content for r in resultados])
    fontes = list(set([r.metadata["fonte"] for r in resultados]))

    prompt = f"""Você é um assistente de suporte do Spotify. Responda usando apenas as informações do contexto abaixo.

Regras:
1. Se o contexto contém a resposta, responda de forma direta e natural, sem comentar estas instruções.
2. Se o contexto NÃO contém a informação necessária (por exemplo, preços, planos, cancelamento de assinatura, ou qualquer assunto não coberto), responda apenas: "Não tenho essa informação disponível no momento. Recomendo consultar diretamente o site de suporte do Spotify." Não tente completar com conhecimento próprio sobre o Spotify.

Contexto:
{contexto}

Pergunta: {pergunta}

Resposta:"""

    resposta = llm.invoke(prompt)
    return {"resposta": resposta.content, "fontes": fontes}


if __name__ == "__main__":
    pergunta = "Como eu ouço músicas em ordem aleatória?"
    resultado = responder_pergunta(pergunta)
    print("Resposta do chatbot:")
    print(resultado["resposta"])
    print("\nFontes utilizadas:")
    for fonte in resultado["fontes"]:
        print(f"- {fonte}")