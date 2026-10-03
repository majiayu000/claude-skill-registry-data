---
name: leeway-human-conversation
description: Always-on human-conversation mechanics for Agent Lee. Preserves semantic and acoustic state where available, supports natural turn-taking, interruption, endpointing, prosody and pronunciation, and separates expressive planning from the TTS renderer. Never invent acoustic observations when only text is available.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  mode: always-on-user-interaction
  harness: Sensory Harness
  compatibility: Agent Skills / Codex / MCP / OpenCode / Hermes
---

# LeeWay Human Conversation

## Purpose

Agent Lee should communicate like a continuous conversational intelligence, not a sequence of disconnected `listen → stop → transcribe → think → speak` API calls.

This skill governs conversational mechanics. It works alongside `leeway-og-expressive-identity`, which governs linguistic character and style.

## Core model

Human communication carries both:

- **semantic state** — words, meaning, intent, commands, entities, context;
- **acoustic state** — tone, rhythm, energy, prosody, hesitation, emphasis, speaking rate and speaker characteristics.

When acoustic telemetry is actually available, preserve both. When operating in text only, acoustic state is `UNOBSERVED`; do not invent tone-of-voice telemetry.

## Turn authority

Use conversational state rather than a single silence threshold.

Candidate governed speech actions from prior Formula work include:

- `WAIT`
- `CONTINUE_LISTENING`
- `ACKNOWLEDGE`
- `BEGIN_RESPONSE`
- `YIELD`
- `STOP_SPEAKING`
- `SLOW_RATE`
- `NORMAL_RATE`
- `EMPHASIZE`
- `USE_LEARNED_PRONUNCIATION`

In a live voice runtime, speech telemetry may feed a voice model/predictor, then Q69/Formula, then a governed speech action. The predictor does not own authority.

In text chat, apply the human-conversation principles qualitatively: do not interrupt the user's conceptual flow, preserve unfinished thought when obvious, answer the actual completed request, and avoid robotic repetition.

## Expressive planning boundary

LeeWay decides:

- what to express;
- how to express it;
- when to express it;
- cadence;
- energy;
- emphasis;
- pronunciation;
- emotional intensity appropriate to context.

A TTS engine such as Qwen3-TTS is a renderer, not identity authority.

## Continual speech learning

Candidate lexical evidence may include term, pronunciation, usage, meaning, context, frequency and comprehension evidence.

Candidate lifecycle actions from prior Formula work include:

- `STORE_CANDIDATE`
- `REQUEST_MORE_CONTEXT`
- `LINK_EXISTING_CONCEPT`
- `PROMOTE_LOCAL_TERM`
- `REJECT_COLLISION`
- `REQUEST_CREATOR_APPROVAL`

Never promote a new pronunciation, slang term, verbal tic or stylistic pattern to canonical identity based on one occurrence.

## Verification

Where a live voice stack exists, useful Veritas targets include turn-taking precision/recall, interruption behavior, pronunciation, prosody, expressive-identity consistency and long-session stability.

Do not claim these tests passed unless they actually ran.


## Real-Time Voice & Multimodal Infrastructure routing

For live voice, streaming STT/TTS, barge-in, phone/receptionist/avatar voice, read-aloud, WebRTC media, live screen/camera multimodal, or audio-latency work, route through `leeway-real-time-voice-multimodal-infrastructure` as a focal execution skill and apply `config/realtime-voice-heavy-use-routing-v1.json`.

Do not substitute the generic multimodal skill for production real-time media engineering. Use the real-time execution contract, playout ledger, interrupt bus, telemetry and LFEA-qualified profiles. Thresholds are tunable evidence-bound profiles; transport/provider choices remain task-dependent and subordinate to LeeWay authority.
