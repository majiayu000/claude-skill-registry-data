---
name: explain-brief
description: Speak a neutral explanation in at most 80 words through Kokoro on the primary Mac. Uses the bundled explain-tts transport.
---
Use the shared `../explain-tts` skill instructions and run `../explain-tts/bin/tts-say --preset brief` in the foreground. Write a markdown-free spoken script of at most 80 words from the trailing topic, then invoke the script. Fail-soft rules and options are documented in `../explain-tts/SKILL.md`.
