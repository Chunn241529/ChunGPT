from flask import Flask, request, Response, jsonify
from openai import OpenAI

app = Flask(__name__)

# AI API Configuration
ollama_api_key = "ollama"
url_local = "http://localhost:11434"


@app.route("/api/chat", methods=["POST"])
def chat_with_ai_stream():
    """Streaming endpoint to interact with AI."""
    data = request.json
    if not data or "messages" not in data:
        return jsonify({"error": "Invalid input, 'messages' is required"}), 400

    messages = data["messages"]
    client = OpenAI(base_url=f"{url_local}/v1", api_key=ollama_api_key)

    def stream_response():
        try:
            # Stream the response from the AI server
            response = client.chat.completions.create(
                model="qwen2.5-coder:7b",
                messages=messages,
                stream=True,  # Enable streaming
            )
            for chunk in response:
                content = (
                    chunk.choices[0].delta.content
                    if hasattr(chunk.choices[0].delta, "content")
                    else ""
                )
                if content:
                    # Stream each chunk as a Server-Sent Event
                    yield f"data: {content}\n\n"
        except Exception as e:
            yield f"data: [Error]: {str(e)}\n\n"

    return Response(
        stream_response(),
        content_type="text/event-stream; charset=utf-8",  # Set UTF-8 in response header
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
