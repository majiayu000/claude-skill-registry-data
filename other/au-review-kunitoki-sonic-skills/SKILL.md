---
name: au-review
description: >
  Reviews AudioUnit v2/v3 plugin implementations for spec compliance, thread safety, and
  correctness. Use when the user asks to review an AudioUnit plugin, check an AUv3 app
  extension, audit property or parameter handling, or asks "is my AUComponent thread-safe?"
  or "why does my AU crash in Logic?". Trigger on phrases like "review my AudioUnit",
  "check my AUv3", "is my render block safe?", or when you see AURenderCallback,
  internalRenderBlock, kAudioUnitProperty_*, or AUAudioUnit in the code.
---

# AudioUnit (AUv2 / AUv3) Review

AUv2 runs in-process inside the host; AUv3 runs in a sandboxed XPC extension. Both share
the same realtime-callback constraints, but AUv3 adds ObjC/Swift runtime exposure and
app-extension lifecycle rules that introduce a distinct class of violations.

## Step 0 — Run universal checks first

Invoke `audio-dsp-review` and `audio-numerics-review` before this skill. This skill adds
AU-specific checks on top; it does not replace realtime-safety or numerics reviews.

## Step 1 — Identify AU version and structure

Determine which AU variant is under review:

| Variant | Entry point | Render surface |
|---------|------------|---------------|
| AUv2 (Component Manager) | `AudioComponentRegister` / `AUMIDIEffectFactory` | `AURenderCallback` |
| AUv3 (App Extension) | `AUAudioUnit` subclass, `NSExtensionPrincipalClass` | `internalRenderBlock` |

Locate: the render callback / render block, `allocateRenderResourcesAndReturnError:`,
`deallocateRenderResources`, `supportedViewConfigurations`, and all
`kAudioUnitProperty_*` / `AUParameter` access sites.

## Step 2 — Scan for AU-specific violations

| Violation | Where to look | Risk |
|-----------|--------------|------|
| ObjC message send (`[obj msg]` / `.property`) in render callback | `AURenderCallback` body, `internalRenderBlock` capture body | ObjC runtime uses locks and may allocate; not realtime-safe |
| Render block calls through `self`, weak references, Swift closures, or ObjC properties | AUv3 render block | Runtime calls and weak-reference loads are not realtime-safe |
| `kAudioUnitProperty_*` read/written from render thread | Any render-path property access | `AudioUnitGetProperty` / `SetProperty` are not thread-safe |
| Parameter ramps not applied sample-accurately | `AUParameterEvent` handling, `AUv2 renderProc` | Parameter jumps produce zipper noise on DAW automation |
| Tail time not reported via `kAudioUnitProperty_TailTime` | Reverb, delay, convolution AUs | Host silences the AU before tail has decayed |
| AUv3 extension missing `com.apple.security.app-sandbox` entitlement | Xcode target entitlements | App Store / Notarisation rejection; Logic refuses to load |
| `NSFileManager`, `NSUserDefaults`, or `UserDefaults` accessed from render block | AUv3 internalRenderBlock | Main-thread-only / file-I/O APIs; realtime violation and potential deadlock |
| `AUAudioUnit` subclass not calling `super` in `allocateRenderResources` | `allocateRenderResourcesAndReturnError:` override | Resources for format negotiation never initialised; silent misrender |
| Format negotiation not honouring `outputBusses[n].format` before allocating | `allocateRenderResources` | Mismatch between agreed and actual format; distortion or crash |
| `auval` failures not addressed | Overall AU implementation | Plugin rejected or silently disabled by Logic, GarageBand, and MainStage |

## Step 3 — Write the review

Same format as `audio-dsp-review` / `audio-numerics-review`:
`Verdict` · `Critical Violations` (category, file:line, Why, Fix) · `Warnings` · `What's Done Well` · `Recommended Fixes (priority order)`
Prefix the header with `AudioUnit Review: [file / class]`.

## auval checklist

Run `auval -a` to list registered AUs; validate with type/subtype/manufacturer codes:
`auval -v aufx MYFX MFGR` (effect) · `auval -v aumu MYSY MFGR` (instrument)

| Common auval failure | Cause | Fix |
|----------------------|-------|-----|
| `AU does not support kAudioUnitProperty_CocoaUI` | Missing `NSView`-based UI factory | Implement `AUCocoaViewInfo` + property handler |
| `Render returned error` | Non-zero `OSStatus` from render callback | Validate stream format; guard every render call |
| `TailTime not set` | Reverb/delay returns 0 tail time | Return duration from `kAudioUnitProperty_TailTime` |
| `Latency reported as 0` | Plugin adds latency but reports none | Return correct samples from `kAudioUnitProperty_Latency` |
| `Parameter not in range` | Default value outside `AUParameterInfo` min/max | Clamp default inside declared range |

## Quick fix table

| Violation | Fix |
|-----------|-----|
| ObjC call in render block | Cache plain C/C++ DSP objects, buffers, and atomics before returning the block; call ObjC only outside callback |
| `self` / weak-self use in render block | Capture raw C++ kernel pointers or `__unsafe_unretained` ivars once; do not load weak refs or call properties per render |
| Property access from render thread | Use `std::atomic<>` or lock-free FIFO; read/write properties only from main/audio-graph thread |
| No sample-accurate parameter ramps | Process `AUParameterEvent` list per-sample; use a one-pole smoother for missing events |
| Missing tail time | AUv2: implement `kAudioUnitProperty_TailTime`; AUv3: override `tailTime` in seconds |
| Sandbox entitlement missing | Enable the AUv3 app-extension sandbox; add file/network entitlements only when the extension actually needs them |
| `NSUserDefaults` in render block | Store params via `AUParameter` tree; load defaults only in `init` / `allocateRenderResources` |
