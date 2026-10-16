import os
from flask import Flask, request, send_file
from flask_cors import CORS
import edge_tts
import asyncio

app = Flask(__name__)
CORS(app)

# Функція генерації аудіо через Edge-TTS
async def generate_audio(text, output_file):
    communicate = edge_tts.Communicate(text, "uk-UA-OstapNeural")
    await communicate.save(output_file)

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return {"error": "No text provided"}, 400

    output_file = "output.mp3"
    
    # Запускаємо асинхронну генерацію аудіо
    asyncio.run(generate_audio(text, output_file))
    
    if os.path.exists(output_file):
        return send_file(output_file, mimetype="audio/mpeg")
    else:
        return {"error": "Audio generation failed"}, 500

if __name__ == '__main__':
    # Отримуємо порт від Render або використовуємо 5000 локально
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
