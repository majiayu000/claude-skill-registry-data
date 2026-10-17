---
name: read-aloud
description: Read text aloud using the reader-core chunked speech engine.
version: 1
triggers: read aloud, read this to me, speak this, text to speech, read it out
category: Writing & documents
blurb: Prepares text to be read aloud by your phone's own voice — cleaned, chunked, and paced for listening instead of reading.
example: Read this summary aloud, cleaned up for listening.
---
# Read Aloud

The user wants text read aloud. The phone's own text-to-speech reads Milo's
replies (that's the standing setup — no AI-generated audio).

## How to handle

1. If the user pasted text and said "read this", format it for clean reading:
   strip markdown, expand abbreviations, one idea per line.
2. Keep the reply itself short — the reading happens on their device.
3. For long documents, offer to chunk it: "I've split it into 3 parts —
   say 'next' after each."

## Rules

- Never generate audio files; the device reads Milo's text replies.
- Clean the text for speech: no URLs read aloud, no markdown symbols.
