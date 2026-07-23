from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from google import genai
from enum import Enum

MODEL_NAME = "gemini-3.6-flash"

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
app = FastAPI()

#create connection with google like we do in sql:
client = genai.Client(api_key=GEMINI_API_KEY)

class SummaryType(str,Enum):
    SHORT = "short"
    MEDIUM = "medium"
    DETAILED = "detailed"

class Audience(str,Enum):
    STUDENT = "student"
    INTERVIEW = "interview"
    RESEARCH = "research"

class SummaryRequest(BaseModel):
    text: str
    summary_type:SummaryType
    audience:Audience

def build_prompt_type (options:Audience):
    if(options=="student"):
        return """
            Easy language + Definitions included + analogies can be used
        """
    elif(options=="interview"):
        return """
            Short+ Keywords+ Definitions+ Revision
        """        
    return """
        Formal + Detailed + Technical aspect included
    """

def build_prompt_length(options:SummaryType):
    if(options=="short"):
        return 100
    elif(options=="short"):
        return 230
    return 400

def build_prompt(request:SummaryRequest):

    response_length = build_prompt_length(request.summary_type)
    audience = build_prompt_type(request.audience)

    return f"""
You are an expert study assistant.
Summarize these notes.
Requirements:
    - Use bullet points.
    - Preserve important technical terms.
    - Keep the summary within {response_length}.
    - Do not omit important concepts.
Client is a {request.audience} so follow the pattern :'{audience}'
Notes:
    {request.text}
    """

@app.get("/")
def HomePage():
    return {
    "message": "AI Summarizer Backend Running"}

@app.post("/summarize")
async def summarize(request: SummaryRequest):

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=build_prompt(request)
    )

    return {
        "summary": response.text
    }