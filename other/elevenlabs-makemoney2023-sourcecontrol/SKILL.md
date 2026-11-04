---
name: elevenlabs
description: >-
  Use when generating speech or voiceovers via ElevenLabs API or MCP for video/audio production.
---

# ElevenLabs

Thin adapter for digital workers. See `skills/org/TOOL-REGISTRY.md`.

## Preferred access
ElevenLabs API / MCP if connected; OpenMontage audio path

## Env / secrets
`ELEVENLABS_API_KEY`

Resolve via `skills/integrations/obsidian-secrets/` then `.env.local`.

## MCP
ElevenLabs MCP if present

## Primary ops
1. Use for Plane B audio on video-producer / paid creatives
2. Keep scripts short; store asset paths under write_lease
3. Fallback to local OmniVoice / OpenMontage TTS when allowed

## Fallback
OmniVoice / local TTS in tools/

## Common failures
Quota errors → shorter script or local fallback
