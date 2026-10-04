---
name: explain-mild
description: Speak a measured explanation in at most 150 words through Kokoro on the primary Mac. Uses the bundled explain-tts transport.
---
Use the shared `../explain-tts` skill instructions and run `../explain-tts/bin/tts-say --preset mild` in the foreground. Write a markdown-free measured spoken script of at most 150 words from the trailing topic, then invoke the script. Fail-soft rules and options are documented in `../explain-tts/SKILL.md`.
