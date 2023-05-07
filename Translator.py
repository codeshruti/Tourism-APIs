from flask import Flask, request, jsonify
from googletrans import Translator
from gtts import gTTS

app = Flask(__name__)

# Create an instance of Translator
translator = Translator()

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data['text']
    target_language = data['target_language']

    if text and target_language:
        translation = translator.translate(text, dest=target_language)
        translated_text = translation.text

        # Generate audio file of translated text
        tts = gTTS(text=translated_text, lang=target_language)
        audio_file = "translation.mp3"
        tts.save(audio_file)

        response = {
            'translated_text': translated_text,
            'audio_file': audio_file
        }

        return jsonify(response)
    else:
        return jsonify({'error': 'Please provide text and target language.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

