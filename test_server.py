import httpx
import json

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
OLLAMA_CONFIG = {
    "model": "mistral:latest",
    "keep_alive": "5m",
    "stream": False
}

PROMPT_TEMPLATE = """Corrija todos los errores tipográficos, mayúsculas y minúsculas y signos de puntuación en este texto, pero conserve todos los caracteres de línea nuevos:

$text

Devuelve solo el texto corregido, no incluyas un preámbulo.
"""

def test_server(text):
    prompt = PROMPT_TEMPLATE.replace("$text", text)
    print(f"🔹 Enviando solicitud a {OLLAMA_ENDPOINT} con modelo {OLLAMA_CONFIG['model']} y el siguiente texto:\n{text}")

    try:
        response = httpx.post(
            OLLAMA_ENDPOINT,
            json={"prompt": prompt, **OLLAMA_CONFIG},
            headers={"Content-Type": "application/json"},
            timeout=120
        )
        print("✅ Respuesta recibida del servidor")

        if response.status_code == 404:
            print("❌ Error 404: El endpoint no se encuentra.")
            return
        elif response.status_code != 200:
            print(f"❌ Error {response.status_code}: {response.text}")
            return

        response_text = response.text.strip()
        print(f"🔸 Respuesta completa del servidor: {response_text}")

        # Asegurarse de que la respuesta no es un log de depuración del servidor
        if "llama_model_loader" in response_text:
            print("❌ Respuesta parece ser un log de depuración del servidor.")
            return

        # Procesar respuesta NDJSON
        response_lines = response_text.splitlines()
        for line in response_lines:
            print(f"🔹 Línea de respuesta: {line}")
        last_response = json.loads(response_lines[-1])
        result = last_response.get("response", "").strip()
        print(f"🔸 Texto corregido recibido: {result}")
    except json.JSONDecodeError as exc:
        print(f"❌ Error al decodificar JSON: {exc}")
    except httpx.RequestError as exc:
        print(f"❌ Error de solicitud HTTP: {exc}")

# Probar el servidor con un texto de ejemplo
test_text = "Corrija este texto"
test_server(test_text)
