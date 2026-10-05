---
name: voice-ai
description: Use when voice AI — text-to-speech (ElevenLabs, OpenAI TTS), speech-to-text
  (Whisper), voice cloning, real-time voice agents. Use when working with voice ai.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- ai-agent
- content-creation
- digital-content
- media
- text-to-speech
- voice
version: 1.0.0
category: content
---




## Overview

Voice AI covers TTS, STT, voice cloning, and real-time conversational agents. Integrates ElevenLabs, OpenAI TTS, Whisper, and Vapi/Bland/Retell.

## Capabilities

- Text-to-speech (ElevenLabs, OpenAI TTS)
- Audio transcription (Whisper, Deepgram)
- Voice cloning from samples
- Real-time voice agents (Vapi, Bland, Retell)
- Audio processing (pydub)

## When to Use
**Trigger phrases:**
- "voice ai"
- "Voice AI — text-to-speech (ElevenLabs, OpenAI TTS), speech-to-text (Whisper), vo"


- Voiceovers for videos/podcasts
- Voice-based customer support
- Transcribing meetings/interviews
- Audiobook generation

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The voice-ai workflow follows a standard pipeline pattern.

Core flow:
```
# voice-ai primary flow
input = prepare(raw_data)
result = process(input, config={agents, cloning, elevenlabs, openai, real})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# voice-ai primary flow
input = prepare(raw_data)
result = process(input, config={agents, cloning, elevenlabs, openai, real})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### OpenAI TTS
```python
from openai import OpenAI
client = OpenAI()
resp = client.audio.speech.create(model="tts-1-hd", voice="nova", input="Hello!")
resp.stream_to_file("output.mp3")
```

### ElevenLabs Clone
```python
import requests
resp = requests.post("https://api.elevenlabs.io/v1/voices/add",
    headers={"xi-api-key": KEY}, files={"files": [open("sample.mp3","rb")]}, data={"name":"Clone"})
voice_id = resp.json()["voice_id"]
resp = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
    headers={"xi-api-key": KEY}, json={"text":"Hello!","model_id":"eleven_multilingual_v2"})
```

### Whisper Transcription
```python
from openai import OpenAI
client = OpenAI()
with open("meeting.mp3","rb") as f:
    t = client.audio.transcriptions.create(model="whisper-1", file=f, response_format="verbose_json")
for s in t.segments: print(f"[{s['start']:.1f}s] {s['text']}")
```

### Vapi Agent
```python
import requests
requests.post("https://api.vapi.ai/assistant",
    headers={"Authorization": f"Bearer {KEY}"},
    json={"name":"Agent","model":{"provider":"openai","model":"gpt-4o","systemPrompt":"Help user."},
           "voice":{"provider":"11labs","voiceId":"nova"},"firstMessage":"Hi!"})
```

## Common Patterns

- Podcast: script → TTS per speaker → mix with intro/outro → export
- Real-time: websocket stream → Deepgram/Whisper → live transcript
- Clone: 3+ min samples → ElevenLabs clone → generate speech

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Good enough content works" | Quality content drives engagement. Mediocre content gets ignored. |
| "I will optimize later" | SEO and distribution need optimization from the start. |
| "Templates are good enough" | Templates are a starting point. Custom content outperforms generic. |