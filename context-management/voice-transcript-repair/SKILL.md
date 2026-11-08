---
name: voice-transcript-repair
description: Repair low-risk recognition mistakes while preventing wrong recipients, dates, commands, and accidental language switches.
---

# Voice Transcript Repair

1. Treat received text as a transcript, not verified original audio. You cannot hear the microphone or determine precisely what speech recognition heard.
2. Correct obvious contextual typos for harmless questions without a tedious confirmation ritual.
3. If uncertainty affects the target, recipient, amount, location, reminder date, medication, or permission, repeat the likely interpretation and ask one narrow question.
4. Resolve 'that', 'it', and 'her' using clear conversation referents; do not guess when an external action would result.
5. Default to English. Never switch languages because a noisy English transcript mentions a language name; switch only for clear user intent.
6. Do not interpret duplicate transcripts as authority to repeat potentially consequential actions. Use event IDs if the transport supplies them; model memory alone cannot guarantee exactly once.
7. Distinguish speech recognition, language generation, text encoding/display, and speech playback failures. This skill cannot fix microphone or speaker hardware.
