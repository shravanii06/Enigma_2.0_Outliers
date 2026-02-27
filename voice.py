import whisper
from gtts import gTTS
import os
import uuid

model = whisper.load_model("base")

AUDIO_OUTPUT_DIR = "audio_outputs"
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

def speech_to_text(audio_path):
    result = model.transcribe(audio_path)
    return result["text"], result["language"]

def text_to_speech(text, lang="en"):
    filename = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join(AUDIO_OUTPUT_DIR, filename)

    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)

    return output_path