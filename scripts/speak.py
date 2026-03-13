#!/usr/bin/env python3
"""Generate speech via ElevenLabs API. Usage: speak.py "text" [output.mp3] [voice_id]"""
import sys, os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from script directory
load_dotenv(Path(__file__).parent / '.env')

from elevenlabs import ElevenLabs

def speak(text, output_path=None, voice_id=None):
    api_key = os.environ.get('ELEVENLABS_API_KEY')
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    
    voice = voice_id or os.environ.get('ELEVENLABS_VOICE_ID', 'EXAVITQu4vr4xnSDxMaL')
    output = output_path or '/tmp/sales-coach-voice.mp3'
    
    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice,
        model_id="eleven_turbo_v2_5",
        output_format="mp3_44100_128"
    )
    
    with open(output, 'wb') as f:
        for chunk in audio:
            f.write(chunk)
    
    print(output)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: speak.py 'text' [output.mp3] [voice_id]")
        sys.exit(1)
    speak(
        sys.argv[1],
        sys.argv[2] if len(sys.argv) > 2 else None,
        sys.argv[3] if len(sys.argv) > 3 else None
    )
