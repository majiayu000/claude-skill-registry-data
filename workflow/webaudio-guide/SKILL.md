---
name: webaudio-guide
description: >
  Step-by-step guide for building Web Audio processing pipelines — AudioWorklet processors,
  custom nodes, parameter automation, and WebMIDI integration. Use when the user asks how to
  build or wire up Web Audio code from scratch.
  Trigger on phrases like "build an AudioWorklet", "create a custom Web Audio effect",
  "how do I use WebMIDI", "how do I write an AudioWorkletProcessor", or
  "how do I connect AudioNodes".
---

# Web Audio Processing Guide

## Step 1 — Set up AudioContext and load worklet module

- Create `AudioContext` inside a user gesture handler (click, keydown) to satisfy autoplay policy.
- Call `await audioContext.audioWorklet.addModule('path/to/processor.js')` before creating nodes.
- The module path is resolved relative to the page; bundlers may require special config (e.g. Vite's `?worker&url` import).
- Check `audioContext.state` and call `audioContext.resume()` if it is `'suspended'`.

## Step 2 — Write the AudioWorkletProcessor

- Subclass `AudioWorkletProcessor` in a separate file; call `registerProcessor('name', Class)` at module scope.
- Implement `process(inputs, outputs, parameters)` — `inputs[n][channel]` and `outputs[n][channel]` are `Float32Array` views for the current render quantum. Use `.length` in loops instead of hardcoding 128.
- Pre-allocate all working buffers in `constructor()`; never create objects or arrays inside `process()`.
- Declare custom `AudioParam`s via `static get parameterDescriptors()` returning an array of `{ name, defaultValue, minValue, maxValue, automationRate }` descriptors.
- Return `true` from `process()` to keep the processor alive; `false` or no return shuts it down.

## Step 3 — Wire up the node graph

- Instantiate the node on the main thread: `new AudioWorkletNode(ctx, 'name', options)`.
- Use `node.connect(destination)` and `source.connect(node)` to build the signal path; `AudioContext.destination` is the hardware output.
- Access `AudioParam`s via `node.parameters.get('paramName')` — set `.value` for immediate changes.
- Schedule smooth automation with `.linearRampToValueAtTime()`, `.setTargetAtTime()`, or `.setValueCurveAtTime()` on the `AudioParam`.
- Tear down cleanly: `node.disconnect()`, then `source.stop()`, then `audioContext.close()`.

## Step 4 — Worklet ↔ main thread communication

- Use `this.port.postMessage()` / `node.port.onmessage` for low-frequency control (meters, state changes, error reporting).
- Batch postMessage calls; avoid sending one per render quantum (currently ~344/sec at 44.1 kHz with 128-frame quanta).
- For high-frequency or low-latency control (e.g. live gain, pitch), share a `SharedArrayBuffer` and read/write integer views with `Atomics.load()` / `Atomics.store()`. Scale floats to integers or bit-cast through a private buffer; `Atomics` does not operate on `Float32Array`.
- Cross-origin isolation (`COOP: same-origin` + `COEP: require-corp` response headers) is required for `SharedArrayBuffer`.

## Step 5 — WebMIDI integration

- Request access with `await navigator.requestMIDIAccess({ sysex: false })`; handle the `MIDIAccess` object on success.
- Enumerate inputs via `midiAccess.inputs.forEach(input => ...)` and attach `input.onmidimessage = handler`.
- Parse the `MIDIMessageEvent.data` byte array: `data[0] & 0xF0` = status (0x90 = note on, 0xB0 = CC, 0xE0 = pitch bend), `data[1]` = note/CC number, `data[2]` = velocity/value.
- Map MIDI values to `AudioParam` targets: normalize 7-bit CC (0–127) to your parameter range and write via `.setTargetAtTime()` or a `SharedArrayBuffer` cell for real-time feel.
