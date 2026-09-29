from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.app.rag_chain import responder_pergunta

app = FastAPI(title="Spotify FAQ Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def aquecer_modelos():
    print("Aquecendo modelos (pode levar alguns minutos na primeira vez)...")
    responder_pergunta("teste de aquecimento")
    print("Modelos aquecidos e prontos!")


class PerguntaRequest(BaseModel):
    pergunta: str


class RespostaResponse(BaseModel):
    resposta: str
    fontes: list[str]


@app.post("/perguntar", response_model=RespostaResponse)
def perguntar(request: PerguntaRequest):
    resultado = responder_pergunta(request.pergunta)
    return RespostaResponse(resposta=resultado["resposta"], fontes=resultado["fontes"])


@app.get("/")
def raiz():
    return {"status": "API do chatbot Spotify FAQ está rodando"}