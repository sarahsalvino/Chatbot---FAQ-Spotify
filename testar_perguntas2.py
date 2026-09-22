from rag_completo import responder_pergunta

perguntas = [
    "O que fazer se o app do Spotify mudou de repente?",
    "Como funciona a Sua Biblioteca no Spotify?",
    "Quais dispositivos são compatíveis com o Spotify?",
    "Quanto custa a assinatura Premium do Spotify?",
    "Como cancelar minha assinatura do Spotify?",
    "Como faço pra embaralhar as músicas da playlist?",
    "Meu Spotify travou e não toca nada, o que fazer?",
    "Não está funcionando, me ajuda",
]

for pergunta in perguntas:
    resultado = responder_pergunta(pergunta)
    print("=" * 60)
    print(f"PERGUNTA: {pergunta}")
    print(f"\nRESPOSTA: {resultado['resposta']}")
    print(f"\nFONTES: {resultado['fontes']}")
    print()