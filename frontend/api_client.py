import os
import requests
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
REQUEST_TIMEOUT = 30        # auth calls
SUMMARIZE_TIMEOUT = 60      # LLM call takes longer


def _extract_detail(resp) -> str:
    try:
        data = resp.json()
        return data.get("detail", resp.text)
    except ValueError:
        return resp.text or f"Backend returned status {resp.status_code}."


def _connection_error_message() -> str:
    return (
        f"Couldn't reach the backend at `{BACKEND_URL}`. "
        "Is your FastAPI server running (uvicorn backend.main:app --reload)?"
    )


# ======================================================
# Signup — POST /auth/signup
# ======================================================

def signup_request(email: str, password: str) -> dict:
    try:
        resp = requests.post(
            f"{BACKEND_URL}/auth/signup",
            json={"email": email, "password": password},
            timeout=REQUEST_TIMEOUT,
        )

        if resp.status_code == 200:
            data = resp.json()
            return {"success": True, "message": data.get("message", "Verification email sent.")}

        return {"success": False, "error": _extract_detail(resp)}

    except requests.exceptions.ConnectionError:
        return {"success": False, "error": _connection_error_message()}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "The backend took too long to respond. Try again."}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e}"}


# ======================================================
# Login — POST /auth/login
# ======================================================

def login_request(email: str, password: str) -> dict:
    try:
        resp = requests.post(
            f"{BACKEND_URL}/auth/login",
            json={"email": email, "password": password},
            timeout=REQUEST_TIMEOUT,
        )

        if resp.status_code == 200:
            data = resp.json()
            return {"success": True, "token": data.get("access_token")}

        # covers: 404 user not found / 401 wrong password / 403 not verified
        return {"success": False, "error": _extract_detail(resp)}

    except requests.exceptions.ConnectionError:
        return {"success": False, "error": _connection_error_message()}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "The backend took too long to respond. Try again."}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e}"}


# ======================================================
# Summarize — POST /summarize (threaded, runs alongside the loader)
# ======================================================

def call_summarize_threaded(payload: dict, token: str, result_box: dict):
    """
    Same shape as the old call_backend() from app.py: runs in a background thread so the main thread stays free to animate the typewriter loader.

    Writes into result_box (mutable dict) instead of returning, since threads can't return values directly.
    """
    try:
        response = requests.post(
            f"{BACKEND_URL}/summarize",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
            timeout=SUMMARIZE_TIMEOUT,
        )

        if response.status_code == 401:
            # bad/expired token 
            result_box["success"] = False
            result_box["auth_error"] = True
            result_box["error"] = "Your session expired. Please log in again."
            result_box["done"] = True
            return

        if response.status_code == 429:
            result_box["success"] = False
            result_box["error"] = _extract_detail(response)  # "Daily Application Usage Limit Exceeded"
            result_box["done"] = True
            return

        response.raise_for_status()
        data = response.json()

        result_box["success"] = True
        result_box["summary"] = data.get("summary", "")
        result_box["model"] = data.get("model", "—")
        result_box["response_time"] = f'{data.get("response_time_seconds", "—")} sec'

    except requests.exceptions.ConnectionError:
        result_box["success"] = False
        result_box["error"] = _connection_error_message()
    except requests.exceptions.Timeout:
        result_box["success"] = False
        result_box["error"] = "The backend took too long to respond. Try again."
    except requests.exceptions.HTTPError as e:
        result_box["success"] = False
        result_box["error"] = f"Backend returned an error: {e}"
    except Exception as e:
        result_box["success"] = False
        result_box["error"] = f"Unexpected error: {e}"

    result_box["done"] = True