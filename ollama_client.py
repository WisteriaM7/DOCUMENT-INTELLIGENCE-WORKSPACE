import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def call_ollama(prompt: str, model: str = "llama3") -> str:
    """Send a prompt to the local Ollama instance and return the response."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        response.raise_for_status()
        return response.json().get("response", "").strip()

    except requests.exceptions.ConnectionError:
        return (
            "⚠️ **Ollama not running.** "
            "Start it with `ollama serve`, then make sure your model is pulled "
            "(e.g. `ollama pull llama3`)."
        )
    except requests.exceptions.Timeout:
        return "⚠️ **Request timed out.** The document may be too long or the model too slow."
    except Exception as e:
        return f"⚠️ **Ollama error:** {e}"
