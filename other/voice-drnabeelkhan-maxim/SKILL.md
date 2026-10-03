---
skill_id: voice
name: Voice Mode
description: "Voice-driven invocation of Maxim — voice command, hands-free request, /mxm-voice, spoken \"Maxim, ...\" or \"Hey Maxim\". Wraps voicemode for Whisper STT and Kokoro TTS."
version: 1.0.0
category: interface
type: input-output
frameworks: []
triggers:
  - voice command
  - hands-free request
  - "/mxm-voice"
  - audio input from voicemode
  - utterance contains "Maxim, ..." or "Hey Maxim"
collaborates_with:
  - executive-router
  - session-memory
  - operator-profile
  - wiki-query
  - wiki-ingest
ethics_required: false
priority: medium
tags: [voice, stt, tts, whisper, kokoro, voicemode, accessibility]
created: 2026-04-16
updated: 2026-04-16
---

# Voice Mode

## Purpose

Voice-driven invocation of Maxim's full capability surface. Wraps [mbailey/voicemode](https://github.com/mbailey/voicemode) for STT (Whisper) + TTS (Kokoro) and adds office-aware intent routing, hotword config, and decision capture.

**Maxim is the only multi-agent framework with native voice-driven executive office routing.**

## When To Invoke

- User runs `/mxm-voice`
- User uploads audio that needs transcription + dispatch
- Voice utterance contains "Maxim, ..." or "Hey Maxim, ..." trigger phrase
- Hands-free workflows (commute, accessibility, eyes-free debugging)

## Architecture

This skill DOES NOT do STT or TTS itself. It depends on two layers:

1. **mbailey/voicemode MCP** — handles Whisper transcription + Kokoro speech synthesis
2. **mxm-voice MCP** — Maxim's hotword config + intent routing + decision capture

The flow:

```
[User speaks] → [voicemode Whisper STT]
                      ↓
              [transcribed text]
                      ↓
       [mxm-voice.voice_invoke_command]
                      ↓
       Hotword match? ─── YES ──→ [dispatch slash command]
              ↓
              NO
              ↓
       [/mxm-route <utterance>]  → [executive-router classifies intent]
                      ↓
              [skill execution]
                      ↓
              [text response]
                      ↓
       [mxm-voice.voice_brief_office or formatted response]
                      ↓
              [voicemode Kokoro TTS]
                      ↓
       [User hears response]
```

## When VoiceMode Is Not Installed

`/mxm-voice` prints install instructions and exits gracefully:

```
🗣️ VoiceMode not detected. Install with:
   claude plugin marketplace add mbailey/voicemode
   claude plugin install voicemode@voicemode
   /voicemode:install
```

The `mxm-voice` MCP server still runs (provides `voice_status`, hotword config validation, decision capture from typed transcripts) — only the actual STT/TTS requires voicemode.

## Hotword Configuration

User-editable file: `config/voice-phrases.yml`

```yaml
phrases:
  - pattern: "maxim run my project health check"
    dispatch: "/mxm-health"
  - pattern: "maxim draft a landing page *"
    dispatch: "/mxm-design landing page $1"
  - pattern: "maxim research * tell me how it improves *"
    dispatch: "/mxm-cino research $1 for $2"
```

Pattern types: plain string (substring match), wildcards (`*` captured as `$1`, `$2`), regex (`regex:<pattern>`).

User adds/removes/renames phrases freely. Config reloads on every voice invocation — no restart.

## Default Hotwords (ship with Maxim)

| Spoken | Dispatched |
|---|---|
| "Maxim, morning CEO cycle" | `/mxm-ceo-morning` |
| "Maxim, overnight CEO cycle" | `/mxm-ceo-overnight` |
| "Maxim, portfolio status" | `/mxm-portfolio` |
| "Maxim, project status" | `/mxm-status` |
| "Maxim, run project health check" | `/mxm-health` |
| "Maxim, run wiki ingest" | `/mxm-wiki ingest` |
| "Maxim, query wiki *" | `/mxm-wiki query $1` |
| "Maxim, audit the wiki" | `/mxm-wiki lint` |
| "Maxim, review unverified pages" | `/mxm-wiki explore` |
| "Maxim, recall *" | `/mxm-recall $1` |
| "Maxim, remember *" | `/mxm-remember $1` |
| "Maxim, brief me on the *" | `voice_brief_office($1)` |
| "Maxim, draft a landing page *" | `/mxm-design landing page $1` |
| "Maxim, research * tell me how it improves *" | `/mxm-cino research $1 for $2` |

## Behavioral Notes

- Voice utterances bypass the typed CLAUDE.md preamble — keep responses concise (TTS-friendly)
- Sensitive operations (security, compliance, payments, regulated projects) STILL fire CSO auto-loop — voice is not a bypass
- Voice-captured decisions go to `.claude-sessions-memory/decision-log.md` with timestamp + transcript
- Operator profile picks up speech patterns over time (preferred command verbs, common requests)

## Output Format

```
Voice Invocation:
Heard: "<transcribed utterance>"
Match: HOTWORD | EXECUTIVE_ROUTER | UNCLASSIFIED
Dispatched: <slash command or fallback>
TTS Response: <spoken text — concise>
Captured to memory: YES (decision tag) | NO
Confidence: 🟢 HIGH (clean transcription, hotword match) | 🟡 MEDIUM (router classified) | 🔴 LOW (unclassified, asked for clarification)
```

## Handoff

- Hotword matched → dispatch slash command directly
- No match → `/mxm-route <utterance>` for intent classification
- Compliance-sensitive utterance → CSO auto-loop fires before any action
- Decision dictation → `voice_capture_decision` writes to session memory

## Maxim Behavioral Layer

- **Confidence tagging**: 🟢 HIGH on hotword match, 🟡 MEDIUM on router classification, 🔴 LOW on unclassified
- **Brevity**: voice responses are SHORTER than typed responses (TTS attention budget)
- **Anti-misfire**: refuses to act on partial/garbled transcriptions (asks for re-utterance)

## Source References

- `mcp/mxm-voice/` — MCP server implementation
- `config/voice-phrases.yml` — user-editable hotword config
- `.claude/commands/mxm-voice.md` — slash command entry point
- [mbailey/voicemode](https://github.com/mbailey/voicemode) — upstream STT/TTS dependency

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
