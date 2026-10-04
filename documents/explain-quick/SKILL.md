---
name: explain-quick
description: Speak a headline explanation in at most 25 words through Kokoro on the primary Mac. Uses the bundled explain-tts transport.
---
Use the shared `../explain-tts` skill instructions and run `../explain-tts/bin/tts-say --preset quick` in the foreground. Write a markdown-free headline spoken script of at most 25 words from the trailing topic, then invoke the script. Fail-soft rules and options are documented in `../explain-tts/SKILL.md`.
