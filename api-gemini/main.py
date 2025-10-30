from http.client import responses
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import google.generativeai as genai
import uuid
import os
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"

app = FastAPI()

chat_sessions = {} #Lista com o histórico de conversas

#O que deixa ser possível o frontend conversar com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel): #Classe para controle de histórico
    prompt: str #Mensagens da conversa atual
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    #Id da conversa atual, se alterada, mudará a conversa

class GenerateResponse(BaseModel): #Classe para controle de resposta da IA
    response: str #Respostas da conversa atual
    session_id: str
    #Id da conversa atual, se alterada, mudará a conversa

def get_or_create_chat(session_id: str): #Função para atualizar histórico
    if session_id in chat_sessions: #verifica se o id existe, se não existir, cria conversa nova
        return chat_sessions[session_id] #Se existir, atualiza histório e continua a conversa

    model = genai.GenerativeModel( #Criar Modelo de IA
        model_name=MODEL_NAME, #Modelo da IA
        system_instruction="Você é um assistente de recomendação de relaxamento. Conduza um questionário em etapas para sugerir a melhor mídia para o descanso do usuário. Com um limte de uma pergunta por vez"
        #Instruções para a personalidade da IA
    )
    new_chat = model.start_chat() #começa nova conversa
    chat_sessions[session_id] = new_chat #Cria histórico
    return new_chat #Retorna nova conversa

@app.post("/generate", response_model=GenerateResponse)
def generate_text(request: PromptRequest):
    try:
        session_id = request.session_id #ID da conversa pedida
        chat = get_or_create_chat(session_id) #Busca histórico por id
        response = chat.send_message(request.prompt) #Cria resposta baseado nas conversas anteriores
        return GenerateResponse(response=response.text, session_id=session_id) #Retorna resposta
    except Exception as e:
        error_message = str(e)

        # Sugestão de erro mais amigável se for bloqueio de segurança
        if "was blocked" in error_message or "valid `Part`" in error_message:
            error_message = "A resposta do modelo foi bloqueada pelas regras de segurança. Por favor, reformule sua pergunta."

        #Lançar erro no site
        raise HTTPException(
            status_code=500,
            detail=f"Erro na API Gemini: {error_message}"
        )