---
name: evo-tts-audiobook-synth
description: Converts text chunks into speech audio using cascading fallback (OpenAI TTS -> ElevenLabs -> edge-tts -> gTTS). Handles API auth, rate limiting, MP3 chunk generation, and audio concatenation into a single MP3 file.
---

# evo-tts-audiobook-synth

Converts text to speech with cascading API fallback and audio concatenation.

## Key Functions

- `synthesize_with_openai(text, output_path)` - Uses OpenAI TTS API (tts-1, 4096 char limit)
- `synthesize_with_elevenlabs(text, output_path)` - Uses ElevenLabs API (client.text_to_speech.convert)
- `synthesize_with_local_tts(text, output_path)` - Uses edge-tts (async) or gTTS as fallback
- `synthesize_text_to_audio(text, output_path)` - Tries OpenAI -> ElevenLabs -> local, returns bytes
- `concatenate_audio_chunks(chunk_files, output_file)` - Concatenates MP3 files using pydub/ffmpeg

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-tts-audiobook-synth/scripts')
from utils import synthesize_text_to_audio, concatenate_audio_chunks

# Synthesize each chunk
chunk_files = []
for i, chunk in enumerate(chunks):
    path = f'/tmp/chunk_{i}.mp3'
    synthesize_text_to_audio(chunk, path)
    chunk_files.append(path)

# Concatenate all chunks
concatenate_audio_chunks(chunk_files, '/root/audiobook.mp3')
```

## Technical Notes
- OpenAI TTS: `client.audio.speech.create(model="tts-1", voice="onyx", input=text)`, max 4096 chars
- ElevenLabs: `client.text_to_speech.convert(text=text, voice_id="...", model_id="eleven_multilingual_v2")`
- edge-tts: async, uses Microsoft Edge neural voices, no API key needed
- gTTS: Google Translate TTS, no API key needed, lower quality
- Audio concat: use pydub AudioSegment or ffmpeg subprocess
- Always use "wb" mode for writing audio binary data
- Add time.sleep(1) between API calls to avoid rate limiting
