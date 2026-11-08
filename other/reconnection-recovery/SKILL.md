---
name: reconnection-recovery
description: Diagnose disconnected, stuck-sending, stale-session and silent-playback reports without blind retries.
---

# Reconnection Recovery

1. Identify the likely failing layer: watch mic/STT, transport, auth, backend acceptance, Hermes inference/tool execution, response transport, TTS, device playback.
2. Treat a 'Sending' spinner as UI state, not proof that the backend never accepted a task.
3. On reconnect, ask the supported API for session or run state when an identifier is available. Never blindly resubmit a consequential action.
4. If the status cannot be queried, label it unknown and suggest one non-destructive verification step.
5. If text appears but speech is silent, separate inference from voice generation and speaker routing. A TTS callback is not proof that audible playback occurred.
6. Strange glyphs may be STT language, model output, font or transport encoding; don't assume one cause from text alone.
7. Keep the response short: what is known, what remains uncertain, and one recovery step. Never change auth keys, deploy code, or alter provider configuration based on inference alone.
