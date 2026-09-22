from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

embeddings = OllamaEmbeddings(model="bge-m3")
vectorstore = Chroma(persist_directory="vectorstore_teste", embedding_function=embeddings)
llm = ChatOllama(model="mistral")

LIMITE_DISTANCIA = 0.75  # ajustável, baseado no que observamos nos testes anteriores

perguntas = [
    "Quanto custa a assinatura Premium do Spotify?",
    "Como cancelar minha assinatura do Spotify?",
]

for pergunta in perguntas:
    resultados_com_score = vectorstore.similarity_search_with_score(pergunta, k=5)
    melhor_distancia = resultados_com_score[0][1]

    print("=" * 60)
    print(f"PERGUNTA: {pergunta}")
    print(f"Melhor distância encontrada: {melhor_distancia:.4f}")

    if melhor_distancia > LIMITE_DISTANCIA:
        print("\nRESPOSTA: Não tenho essa informação disponível no momento. Recomendo consultar diretamente o site de suporte do Spotify.")
        print("(resposta bloqueada automaticamente por baixa relevância, sem chamar o LLM)")
        continue

    resultados = [r for r, score in resultados_com_score]
    contexto = "\n\n".join([r.page_content for r in resultados])
    fontes = list(set([r.metadata["fonte"] for r in resultados]))

    prompt = f"""Você é um assistente de suporte do Spotify. Use APENAS as informações do contexto abaixo para responder.

REGRAS OBRIGATÓRIAS:
- Se a resposta não estiver EXPLICITAMENTE no contexto, responda exatamente: "Não tenho essa informação disponível no momento. Recomendo consultar diretamente o site de suporte do Spotify."
- NUNCA invente preços, valores, links, URLs ou procedimentos que não estejam escritos no contexto.
- Não complete informações usando conhecimento geral seu sobre o Spotify.

Contexto:
{contexto}

Pergunta: {pergunta}

Resposta:"""

    resposta = llm.invoke(prompt)
    print(f"\nRESPOSTA: {resposta.content}")
    print(f"\nFONTES: {fontes}")