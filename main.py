from flask import Flask, request
import requests
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/")
def home_view():
        return "<h1>Maa Chuda Lawde</h1>"

@app.route("/answer", methods=['GET', 'POST'])
def voice():
    response = VoiceResponse()
    response.record(
        max_length=30,
        timeout=0,
        recording_status_callback="/recording-complete",
        recording_status_callback_event="completed"
    )
    return str(response)

@app.route("/recording-complete", methods=['GET', 'POST'])
def recording_complete():
    response = VoiceResponse()

    # The recording url will return a wav file by default, or an mp3 if you add .mp3
    recording_url = request.values['RecordingUrl'] + '.mp3'

    filename = request.values['RecordingSid'] + '.mp3'
    with open('{}/{}'.format("directory/to/download/to", filename), 'wb') as f:
        f.write(requests.get(recording_url).content)

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)