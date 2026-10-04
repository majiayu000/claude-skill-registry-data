---
name: webaudio-review
description: >
  Reviews Web Audio API JavaScript/TypeScript code for correctness, thread safety, and deprecated
  patterns. Use when the user asks to review AudioWorklet code, check an AudioWorkletProcessor,
  audit Web Audio graph construction, or diagnose crackling/dropouts in a web audio app.
  Trigger on phrases like "review my Web Audio code", "check my AudioWorklet",
  "is my AudioWorkletProcessor safe", or "why does my web audio crackle".
---

# Web Audio API Safety Review

> **Note — JS realtime model differs from native:**
> JavaScript allocation does not look like `malloc`, but it still creates garbage-collector
> work and can introduce render-thread jitter. The same cardinal rule applies:
> *avoid allocations and blocking operations inside `process()`*.
>
> Invoke `audio-dsp-review` concepts (no allocations, no blocking) adapted for JavaScript:
> replace "mutex" with "GC pause" and "malloc" with "object/array creation".

## Step 1 — Identify the architecture

Determine which Web Audio pattern is in use before scanning:

| Pattern | Where audio runs | Risk level |
|---|---|---|
| `AudioWorkletProcessor` subclass | Dedicated worklet thread | Medium — GC and message overhead |
| `ScriptProcessorNode` | Main thread | High — deprecated; blocks UI |
| Main-thread `AudioContext` only | Main thread | Low — standard graph |
| `OfflineAudioContext` | Offline render | Low — no real-time deadline |

## Step 2 — Scan for violations

| Violation | Location | Risk |
|---|---|---|
| Using `ScriptProcessorNode` | Anywhere | Deprecated; runs on main thread → dropouts under UI load |
| `new Float32Array(...)` inside `process()` | `AudioWorkletProcessor.process()` | GC allocation → potential pause during render |
| Creating objects/arrays/closures inside `process()` | `AudioWorkletProcessor.process()` | GC pressure → jitter |
| `port.postMessage()` every `process()` block | `AudioWorkletProcessor` | High overhead; batch updates or use `SharedArrayBuffer` |
| Accessing `window`, `document`, or DOM from worklet | `process()` or worklet scope | Worklet thread has no DOM access — throws `ReferenceError` |
| Importing non-worklet-safe modules in `addModule()` | Worklet module file | DOM APIs throw; do network/file loading on the main thread and pass data in |
| Not handling autoplay policy | `AudioContext` creation | Context starts `suspended`; must resume on user gesture |
| `SharedArrayBuffer` comms without integer `Atomics` protocol | Worklet ↔ main comms | Race-prone shared state — `Atomics` works on integer typed arrays, not `Float32Array` |
| Changing `AudioNode` graph from worklet thread | `process()` | `connect()`/`disconnect()` are main-thread-only |
| Assuming a hardcoded render quantum in loops/buffers | `process()` | Spec and browsers use 128-frame quanta today, but code should use `output[channel].length` |
| Forgetting `await audioContext.resume()` | After user gesture handler | Stays suspended; no audio output |

## Step 3 — Write the review

```
## Web Audio Safety Review: `[file / component]`

### Verdict
[Safe | Has critical violations | Warnings only] — [one sentence summary]

### Critical Violations
**[Category]: [description]**
`file:line` — `offending code`
Why: [realtime or correctness risk]
Fix: [concrete suggestion]

### Warnings
[same format]

### What's Done Well
[correct patterns observed]

### Recommended Fixes (priority order)
1. ...
```

See `references/webaudio-violations.md` for BAD/GOOD code examples for every violation above.

## Quick fix table

| Violation | Safe alternative |
|---|---|
| `ScriptProcessorNode` | `AudioWorkletProcessor` subclass |
| `new Float32Array()` in `process()` | Pre-allocate in constructor; reuse across calls |
| `port.postMessage()` every block | Batch at lower rate, or use `SharedArrayBuffer` + integer `Atomics` |
| Raw `SharedArrayBuffer` reads | `Atomics.load()` / `Atomics.store()` on `Int32Array` / `Uint32Array` views |
| Graph changes from worklet | Queue a message to main thread; apply in `port.onmessage` |
| Context suspended | `button.addEventListener('click', () => ctx.resume())` |
