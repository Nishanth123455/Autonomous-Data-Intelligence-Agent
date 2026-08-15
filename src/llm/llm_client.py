import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def generate_response(prompt):
    """
    Send a prompt to the local Ollama model
    and return the generated response.
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]


if __name__ == "__main__":

    prompt = """
    Explain what an AI agent is in two sentences.
    """

    answer = generate_response(prompt)

    print("\n===== LLM TEST =====")
    print(answer) 