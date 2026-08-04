from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai
from enum import Enum
import logging
import os
import time

# ======================================================
# Configuration
# ======================================================

APP_NAME = "Dhvani"
APP_VERSION = "1.0.0"
MODEL_NAME = "gemini-3.6-flash"

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in environment variables."
    )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ======================================================
# FastAPI Application
# ======================================================

app = FastAPI()

# ======================================================
# Gemini Client
# ======================================================

#create connection with google like we do in sql:
client = genai.Client(api_key=GEMINI_API_KEY)

logger.info(f"{APP_NAME} backend started.")
logger.info(f"Using Model: {MODEL_NAME}")

# ======================================================
# Enums
# ======================================================

class SummaryType(str, Enum):
    SHORT = "short"
    MEDIUM = "medium"
    DETAILED = "detailed"


class Audience(str, Enum):
    STUDENT = "student"
    INTERVIEW = "interview"
    RESEARCH = "research"

# ======================================================
# Request & Response Models
# ======================================================

class SummaryRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=20,
        max_length=25000,
        description="Notes to summarize"
    )

    summary_type: SummaryType

    audience: Audience

    additional_instructions: str = Field(
        default="",
        max_length=500
    )


class SummaryResponse(BaseModel):

    success: bool
    summary: str
    model: str
    response_time_seconds: float

# ======================================================
# Prompt Configuration
# ======================================================

AUDIENCE_PROMPTS = {

    Audience.STUDENT:
    """
    Easy language + Definitions included + analogies can be used
    """,

    Audience.INTERVIEW:
    """
    Short + Keywords + Definitions + Revision
    """,

    Audience.RESEARCH:
    """
    Formal + Detailed + Technical aspect included
    """
}

SUMMARY_LENGTH = {

    SummaryType.SHORT: 180,
    SummaryType.MEDIUM: 330,
    SummaryType.DETAILED: 480
}

# ======================================================
# Prompt Builder Helpers
# ======================================================

def build_prompt_type(option: Audience):
    return AUDIENCE_PROMPTS[option]


def build_prompt_length(option: SummaryType):
    return SUMMARY_LENGTH[option]

# ======================================================
# Prompt Builder
# ======================================================

def build_prompt(request: SummaryRequest):

    response_length = build_prompt_length(request.summary_type)
    audience = build_prompt_type(request.audience)

    return f"""
You are an expert study assistant.

## Primary Task
Summarize the provided notes accurately.

## Audience
{audience}

## Summary Constraints
- Use bullet points.
- Preserve important technical terms.
- Keep the summary within approximately {response_length} words.
- Do not omit important concepts.

## Additional User Instructions
Follow these instructions whenever possible,
provided they do not conflict with the primary task.

{request.additional_instructions}

## Notes
{request.text}
"""

# ======================================================
# Routes
# ======================================================

@app.get("/")
def HomePage():

    return {
        "application": APP_NAME,
        "status": "running",
        "model": MODEL_NAME,
        "version": APP_VERSION
    }


@app.post("/summarize", response_model=SummaryResponse)
async def summarize(request: SummaryRequest):

    start = time.perf_counter()  # End-to-End API Latency

    logger.info("Generating summary...")

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=build_prompt(request)
        )

        end = time.perf_counter()

        logger.info(
            f"Summary generated successfully in {round(end-start,2)} seconds."
        )

    except Exception as e:

        logger.error(e)

        raise HTTPException(
            status_code=500,
            detail="Unable to generate summary at the moment. Please try again."
        )

    return {
        "success": True,
        "summary": response.text,
        "model": MODEL_NAME,
        "response_time_seconds": round(end-start, 2)
    }