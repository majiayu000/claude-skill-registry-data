---
name: synthesis/dialogue-dramatizer
description: Convert dense source-grounded content into a two-speaker dramatized script with persona roles, prosody cues, and interruptions. Use for audio-friendly overviews that stay faithful to cited material.
---

# Dialogue Dramatizer

Capabilities
- identify_key_themes from scoped sources.
- assign_persona_roles (Host vs. Expert/Skeptic).
- generate_banter_turn with interruptions, metaphors, and clarifications.
- insert_prosody_markers (<break>, <emphasis>, <laugh>) for TTS engines.

Dependencies
- hybrid-orchestrator (flow)
- memory-linker (carry context across turns)
- citation-verifier (optional downstream grounding)

Inputs
- grounded notes or summary + persona config.

Outputs
- scripted dialogue turns with optional prosody tags and inline citations.

Usage
- Feed grounded notes (post-boundary + citation) to produce a lively two-voice script ready for TTS.
