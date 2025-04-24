from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import base64
import os

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key here or from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/generate", methods=["POST"])
def generate_image():
    try:
        data = request.form
        image_file = request.files["image"]
        prompt = data.get("prompt")

        if not image_file or not prompt:
            return jsonify({"error": "Missing image or prompt"}), 400

        # Read and encode image
        image_bytes = image_file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        # Call GPT-Image-1 (replace with actual API call once available)
        response = openai.Image.create_edit(
            image=base64_image,
            prompt=prompt,
            model="gpt-image-1",
            response_format="url"
        )

        return jsonify({"image_url": response["data"][0]["url"]})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
