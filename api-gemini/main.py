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

chat_sessions = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class GenerateResponse(BaseModel):
    response: str
    session_id: str

def get_or_create_chat(session_id: str):
    if session_id in chat_sessions:
        return chat_sessions[session_id]

    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction="Você é um assistente de recomendação de relaxamento. Conduza um questionário em etapas para sugerir a melhor mídia para o descanso do usuário. Com um limte de uma pergunta por vez"
    )
    new_chat = model.start_chat()
    chat_sessions[session_id] = new_chat
    return new_chat

@app.post("/generate", response_model=GenerateResponse)
def generate_text(request: PromptRequest):
    session_id = request.session_id

    try:
        session_id = request.session_id
        chat = get_or_create_chat(session_id)
        response = chat.send_message(request.prompt)
        print(response.text)
        return GenerateResponse(response=response.text, session_id=session_id)
    except Exception as e:
        error_message = str(e)

        # Sugestão de erro mais amigável se for bloqueio de segurança
        if "was blocked" in error_message or "valid `Part`" in error_message:
            error_message = "A resposta do modelo foi bloqueada pelas regras de segurança. Por favor, reformule sua pergunta."

        raise HTTPException(
            status_code=500,
            detail=f"Erro na API Gemini: {error_message}"
        )