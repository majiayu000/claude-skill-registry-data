---
name: game-audio-review
description: >
  Reviews game audio code for Wwise/FMOD integration safety, custom DSP plugin correctness,
  and audio middleware usage. Use when the user asks to review a Wwise plugin, check an FMOD
  DSP effect, audit game audio middleware integration, or asks "is my game audio code safe?".
  Trigger on phrases like "review my Wwise plugin", "check FMOD DSP effect", "is my game
  audio code safe", "review my audio middleware integration", or when you see AkPluginInfo,
  FMOD_DSP_DESCRIPTION, IMetaSoundSource, or Execute/process callbacks in game audio code.
---

# Game Audio Middleware Review

Middleware callbacks share all realtime constraints of native audio, plus middleware-specific
memory, threading, and parameter rules.

## Step 0 — Run universal checks first

Invoke `audio-dsp-review` and `audio-numerics-review` before this skill. This skill adds
middleware-specific checks on top; it does not replace realtime-safety or numerics reviews.

## Step 1 — Identify the integration type

| Type | Entry point | Key concerns |
|------|-------------|--------------|
| Wwise plugin | `AkPluginInfo` + `Execute()` | Memory via `AkAlloc`, thread model per platform |
| FMOD DSP effect | `FMOD_DSP_DESCRIPTION` + `process` callback | `FMOD_MEMORY_ALLOC`, must not block |
| Unreal MetaSounds | `IMetaSoundSource`, `GetNextBuffer` | GameThread vs AudioThread ownership |
| Custom engine integration | Engine audio callback | Platform-specific thread model and priorities |

## Step 2 — Scan for violations

| Violation | Where | Risk |
|-----------|-------|------|
| Allocating from any heap inside the audio callback | plugin `Execute`/`process` | Realtime violation; middleware allocators are for setup/teardown, not per-buffer allocation |
| Blocking I/O from audio callback | `Execute`/`process` | Xrun / dropout |
| Accessing game engine state from audio thread | `Execute`/`process` | Not thread-safe; data race or stale read |
| Event or parameter changes without thread-safe channel | game loop → audio | Data race on shared state |
| DSP plugin not handling bypass correctly | `Execute`/`process` | Incorrect audio output in bypass mode |
| Not respecting channel count negotiation | plugin init | Buffer overread / underwrite |
| Missing `AK_OPTIMIZED` guard around debug code | any plugin code | Debug I/O included in shipping build |
| Wwise RTPC not clamped before use | parameter read | Out-of-range value fed to DSP; clipping or NaN |
| FMOD parameter index used as a magic number | parameter read | Wrong value applied after descriptor edits; use a shared enum tied to `paramdesc` order |
| Unreal: accessing `UAudioComponent` from AudioThread | `GetNextBuffer` | GameThread-only object; crashes on non-GameThread |

## Step 3 — Write the review

```
## Game Audio Review: `[file / plugin class]`

### Verdict
[Safe | Has critical violations | Warnings only] — [one sentence summary]

### Integration Type
[Wwise plugin | FMOD DSP | Unreal MetaSounds | Custom engine]

### Critical Violations
**[Category]: [description]**
`file:line` — `offending code`
Why: [one sentence on the middleware / realtime risk]
Fix: [concrete middleware-idiomatic suggestion]

### Warnings
[same format]

### What's Done Well
[correct patterns observed]

### Recommended Fixes (priority order)
1. ...
```

## Quick fix table

| Violation | Fix |
|-----------|-----|
| Allocation in Wwise `Execute` | Pre-allocate in `Init` with `AK_PLUGIN_ALLOC` / `AK_PLUGIN_FREE` |
| Allocation in FMOD `process` | Pre-allocate in create/reset with `dsp_state->functions->alloc` / `free` |
| Blocking call in callback | Move to game thread; pass result via lock-free queue or atomic |
| Game engine state read on audio thread | Cache a thread-safe copy; update via `std::atomic` or SPSC queue |
| Wwise bypass not handled | Leave buffer untouched and return; do not write to output |
| Channel count assumed constant | Read from `io_pBuffer->NumChannels()` or FMOD `inchannels` at runtime |
| FMOD parameter by magic number | Define enum indices and keep descriptor order in one place |
| Unreal GameThread object on AudioThread | Marshal via `AsyncTask(ENamedThreads::GameThread, ...)` |

For code structure examples (Wwise, FMOD, MetaSounds, thread models, memory patterns)
see `references/game-audio-patterns.md`.
