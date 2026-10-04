---
name: audio-signal-flow-explainer
description: >
  Traces and documents signal paths, bus/aux architecture, and sidechain connections in audio
  systems. Surfaces hidden coupling between audio components. Use when the user asks to trace a
  signal chain, explain audio routing, understand an audio graph, locate sidechain sources, or
  describe how audio flows through a plugin or engine.
  Trigger on phrases like "trace this signal chain", "explain this audio routing",
  "what calls what in this audio graph", "where does the sidechain come from",
  "how does audio flow through this plugin".
---

# Audio Signal Flow Explainer

> **Core principle:** Audio signal flow is a directed graph. Tracing it reveals hidden coupling,
> latency paths, and places where the signal can be corrupted.

## Step 1 — Map the graph

- [ ] Find all **sources** (oscillators, audio inputs, file readers, generators)
- [ ] Find all **processors** (filters, effects, gain stages, dynamics)
- [ ] Find all **routers** (bus sends, parallel splits, sidechain taps, mixer channels)
- [ ] Find all **sinks** (audio outputs, recorders, meters, analyzers)
- [ ] Note parallel paths — any branch that rejoins a main path
- [ ] Note feedback loops — any path where output feeds back into an earlier node
- [ ] Note sidechain connections — signals that control a processor without passing audio through it

## Step 2 — Identify each node type

| Node type | What to note |
|-----------|-------------|
| Source (oscillator, audio input, file reader) | Sample rate, channel count, sync source |
| Processor (filter, effect, gain) | In/out channel count, latency added, stateful or stateless |
| Router (bus send, parallel split, sidechain tap) | Where signal copies go, gain staging at split |
| Sink (audio output, recorder, meter) | Expected format, callback timing, buffer size |

## Step 3 — Surface issues

- [ ] Latency compensation mismatches on parallel paths
- [ ] Channel count mismatches between connected nodes
- [ ] Sidechain input not wired — processor receives silence as control signal
- [ ] Uninitialized state in feedback loops (DC buildup, NaN propagation)
- [ ] DC leaking into output (missing highpass or DC-blocking filter)
- [ ] Sample rate mismatch between source and downstream processor
- [ ] Gain staging that causes clipping before a later limiter or saturation stage
- [ ] Missing denormal protection in recursive filter paths

## Step 4 — Write the signal flow description

Use this format:

```
## Signal Flow: [component/system]

### Graph
Source → [gain: 1.0] → [Biquad LPF] → [Comp sidechain tap] → [Output]
                                            ↓
                                       [Compressor] → [Output]

### Latency path
Source → LPF (0 samples) → Compressor (64 samples lookahead) → Output
Total: 64 samples

### Issues found
- Parallel path to Output has no latency compensation for the 64-sample compressor delay
```

## Quick reference

| Pattern | What to check |
|---------|--------------|
| Parallel split rejoining | Latency of each branch must match before summing |
| Sidechain compressor | Verify sidechain input is connected and level-matched |
| Send/return bus | Check send gain, return gain, and whether send is pre- or post-fader |
| Feedback loop | Confirm a delay of at least 1 sample exists to break algebraic loop |
| Multi-rate graph | Confirm resampling nodes at every rate boundary |
