import os
from flask import Flask, request, jsonify
from azure.cognitiveservices.speech import AudioConfig, SpeechConfig, SpeechSynthesizer

app = Flask(__name__)

# Replace these with your actual Azure Speech Service subscription key and region
SPEECH_KEY = os.environ.get('AZURE_SPEECH_API_KEY', None)
SPEECH_REGION = os.environ.get('AZURE_SPEECH_REGION', None)

def get_speech_token():
    if SPEECH_KEY is None or SPEECH_REGION is None:
        return jsonify({"error": "Azure Speech Service subscription key or region is not set."}), 400

    speech_config = SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # Generate the speech token
    speech_token = speech_synthesizer.get_token()

    return speech_token

@app.route('/api/getSpeechToken', methods=['POST'])
def get_speech_token_endpoint():
    token = get_speech_token()
    if isinstance(token, tuple):
        return token  # Return the error response
    else:
        return token

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)