from dotenv import load_dotenv
load_dotenv()

from models import Generation, SessionLocal
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

        # Call GPT-Image-1
        response = openai.Image.create_edit(
            image=base64_image,
            prompt=prompt,
            model="gpt-image-1",
            response_format="url"
        )

        image_url = response["data"][0]["url"]

        # Save to database
        db = SessionLocal()
        entry = Generation(prompt=prompt, image_url=image_url)
        db.add(entry)
        db.commit()
        db.close()

        return jsonify({"image_url": image_url})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/history", methods=["GET"])
def get_history():
    try:
        db = SessionLocal()
        entries = db.query(Generation).order_by(Generation.created_at.desc()).limit(10).all()
        db.close()

        return jsonify([
            {
                "id": entry.id,
                "prompt": entry.prompt,
                "image_url": entry.image_url,
                "created_at": entry.created_at.isoformat()
            }
            for entry in entries
        ])
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500
