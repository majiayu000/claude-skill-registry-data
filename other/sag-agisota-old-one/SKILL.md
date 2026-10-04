---
name: sag
description: ElevenLabs text-to-speech with mac-style say UX.
homepage: https://sag.sh
metadata: {"clawdbot":{"emoji":"🗣️","requires":{"bins":["sag"],"env":["ELEVENLABS_API_KEY"]},"primaryEnv":"ELEVENLABS_API_KEY","install":[{"id":"brew","kind":"brew","formula":"steipete/tap/sag","bins":["sag"],"label":"Install sag (brew)"}]}}
triggers:
  keywords: ["sag", "elevenlabs tts", "text to speech", "say command", "voice playback"]
  intent: ["code-change"]
activation: context
priority: 40
packs: []
---
