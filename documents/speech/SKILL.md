---
name: speech
description: Generate speech audio from text with an already configured local or approved text-to-speech capability, using current supported voices/models verified at.
license: MIT
---

# Speech Generation

## Plan

Confirm script, language, pronunciation, audience, tone, pace, pauses, file format, sample rate, channel layout, loudness target, clip boundaries, and whether disclosure of synthetic audio is required. Normalize dates, numbers, abbreviations, URLs, and domain terms without changing meaning.

## Capability and consent

Use the active host's existing TTS tool, configured API, or installed local engine. Verify supported voices, formats, limits, and current model identifiers from installed/current official documentation. Do not hard-code a dated default or route to a different provider. A paid/network call, dependency install, or new credential requires authorization.

Do not imitate or clone a real person's voice without clear permission and a supported consent process. Never use synthetic speech for deception, impersonation, bypassing authentication, or undisclosed high-stakes communication.

## Generate

Start with a short pronunciation/style sample before a long render. Keep chunks at natural sentence/paragraph boundaries and preserve deterministic settings when the engine supports them. Use a pronunciation glossary or supported markup rather than spelling hacks that damage captions.

## Validate

Listen to or inspect every produced clip. Check exact words, names/numbers, truncation, repeated/missing phrases, clipping, silence, artifacts, loudness consistency, duration, format, and join seams. Preserve the source script and generation settings. Provide captions/transcript where useful.

Report engine/provider used, whether data left the device, voice/model configuration source, output paths, duration/format, validation, and any disclosure/consent requirement.
