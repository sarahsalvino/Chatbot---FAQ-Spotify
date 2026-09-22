from rag_completo import responder_pergunta

perguntas = [
    "Como eu ouço músicas em ordem aleatória?",
    "O que é o Spotify?",
    "Como eu crio uma conta no Spotify?",
    "O Spotify não está tocando, o que eu faço?",
    "Como eu reinstalo o app do Spotify?",
    "O app está offline, como resolver?",
    "Não consigo ouvir nenhum som, o que fazer?",
    "Como eu atualizo o app do Spotify?",
]

for pergunta in perguntas:
    resultado = responder_pergunta(pergunta)
    print("=" * 60)
    print(f"PERGUNTA: {pergunta}")
    print(f"\nRESPOSTA: {resultado['resposta']}")
    print(f"\nFONTES: {resultado['fontes']}")
    print()