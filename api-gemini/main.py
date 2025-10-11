from http.client import responses
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#for m in genai.list_models():
#    print(m.name)

MODEL_NAME = "gemini-2.5-flash"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate_text(request: PromptRequest):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(request.prompt)
        return  {"response": response.text}
    except Exception as e:
        return {"error": str(e)}
