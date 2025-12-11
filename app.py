from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_KEY}",
    "Content-Type": "application/json"
}


def generate_blog(prompt):
    full_prompt = (
        f"Write a detailed, well-structured blog article of around 900–1000 words "
        f"on the topic: {prompt}. Use headings, subheadings, bullet points, and a conclusion."
    )

    url = "https://openrouter.ai/api/v1/chat/completions"

    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct",  # ⚡ FASTEST FREE MODEL
        "messages": [
            {"role": "user", "content": full_prompt}
        ],
        "max_tokens": 950,      # ⚡ Faster but still long blog
        "temperature": 0.7
    }

    try:
        import time
        start = time.time()

        response = requests.post(url, headers=HEADERS, json=payload)
        data = response.json()

        print("API Response Time:", time.time() - start, "seconds")
        print("RAW RESPONSE:", data)

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        if "error" in data:
            return f"OpenRouter Error: {data['error']}"

        return f"Unexpected Response: {data}"

    except Exception as e:
        return f"Error: {str(e)}"



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    output = generate_blog(prompt)
    return jsonify({"blog": output})


if __name__ == "__main__":
    app.run(debug=True)
