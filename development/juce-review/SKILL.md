---
name: juce-review
description: >
  Reviews JUCE audio plugin code for JUCE-specific correctness issues: thread safety,
  APVTS parameter patterns, MessageManager usage, ValueTree, and MIDI handling. Use when
  the user asks to review a JUCE plugin, check a processBlock, audit parameter handling,
  or asks "is this JUCE code safe?". Trigger on phrases like "review my JUCE plugin",
  "check my AudioProcessor", "is this APVTS usage correct?", or when you see
  AudioProcessor, AudioProcessorEditor, or AudioProcessorValueTreeState in the code.
---

# JUCE Audio Plugin Review

JUCE abstractions hide thread boundaries — always trace which thread each piece of code runs on before declaring it safe.

## Step 0 — Run universal checks first

Invoke `audio-dsp-review` and `audio-numerics-review` before this skill. This skill adds JUCE-specific checks on top; it does not replace realtime-safety or numerics reviews.

## Step 1 — Identify plugin structure

Locate the three core classes and their thread ownership:
- `AudioProcessor` — audio thread owns `processBlock`; message thread owns everything else
- `AudioProcessorEditor` — message thread only; never call from audio thread
- `AudioProcessorValueTreeState` — parameter tree lives on message thread; audio thread must use `getRawParameterValue()` raw pointers only

## Step 2 — Scan for JUCE violations

| Violation | Where to look | Risk |
|-----------|--------------|------|
| `juce::String` construction/concatenation | `processBlock`, DSP helpers | May allocate and may touch shared string/logging machinery; realtime unsafe |
| `DBG()` macro | Any audio-thread code | Logger I/O in debug builds; blocks indefinitely |
| `MessageManager::getInstance()` from audio thread | Audio callbacks, DSP helpers | Not thread-safe; undefined behaviour |
| `apvts.getParameter(...)` or `apvts.state` from audio thread | `processBlock` and DSP helpers | APVTS/ValueTree access is not an audio-thread data path; use raw pointer cache instead |
| `ValueTree` listener callbacks assumed on audio thread | Listener overrides | Dispatched via MessageManager; runs on message thread |
| `AudioBuffer::setSize()` inside `processBlock` | Buffer management code | Triggers allocation; causes xrun |
| Modifying MIDI buffer while iterating it | MIDI event loops | Iterator invalidation; undefined behaviour |
| `prepareToPlay` not resetting all state (e.g. filters, envelopes, delay lines) | `prepareToPlay` body | Double-call leaves stale state; causes audio artefacts |
| `juce::CriticalSection::tryEnter()` or `enter()` on audio thread | `processBlock`, DSP helpers | `exit()`/destructor does a syscall to wake waiting threads — not realtime-safe even with `tryEnter()` |
| `juce::SpinLock::enter()` on audio thread | `processBlock`, DSP helpers | Busy-waits on audio thread — use `tryEnter()` + fallback only; non-audio thread should use progressive back-off |

## Step 3 — Write the review

```
## JUCE Plugin Review: `[file / class]`

### Verdict
[Safe | Has critical violations | Warnings only] — [one sentence summary]

### Critical Violations
**[Category]: [description]**
`file:line` — `offending code`
Why: [one sentence on thread / correctness risk]
Fix: [concrete JUCE-idiomatic suggestion]

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
| `juce::String` in `processBlock` | Pre-format on message thread; pass IDs/scalars via `AbstractFifo` or atomics |
| `DBG()` in audio code | Remove entirely or gate behind a lock-free ring buffer drained on message thread |
| `MessageManager` from audio thread | Use `juce::MessageManager::callAsync` from message thread only |
| `apvts.getParameter(id)` in audio thread | Cache `getRawParameterValue(id)` once after APVTS construction; read atomically in `processBlock` |
| `ValueTree` listener on audio thread | Handle listener callbacks on message thread; pass state to audio thread via atomics |
| `AudioBuffer::setSize()` in `processBlock` | Call only in `prepareToPlay`; never resize during playback |
| Mutating MIDI buffer mid-iteration | Collect into a preallocated member buffer or bounded event array, then swap/write back after iteration |
| Missing state reset in `prepareToPlay` | Reset filters, envelopes, delay lines, and position counters unconditionally |
| `CriticalSection::tryEnter()` in audio thread | Replace with `std::atomic<T>` or lock-free SPSC queue; `tryEnter()` + `exit()` is not safe because `exit()` does a syscall |
| `SpinLock::enter()` on audio thread | Use `tryEnter()` + fallback only; non-audio thread should use progressive back-off (see `references/juce-violations.md` Section 4) |

For full code examples (BAD/GOOD patterns, AbstractFifo usage, async dispatch) see
`references/juce-violations.md`.
