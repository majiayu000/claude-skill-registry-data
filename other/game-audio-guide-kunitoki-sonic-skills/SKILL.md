---
name: game-audio-guide
description: >
  Guides implementation of custom Wwise or FMOD DSP plugins from scratch — effect, source,
  and mixer plugin types. Use when the user wants to create a new Wwise plugin, build an FMOD
  DSP effect, or implement a custom game audio middleware plugin. Trigger on phrases like
  "create a Wwise effect plugin", "build an FMOD DSP", "implement custom game audio middleware
  plugin", "how do I write a Wwise source plugin", or "set up an FMOD DSP description".
---

# Game Audio Plugin Implementation Guide

Steps apply to both Wwise and FMOD unless noted.

## Step 1 — Choose middleware and plugin type

| Middleware | Effect plugin | Source plugin | Mixer plugin |
|------------|--------------|---------------|--------------|
| Wwise | `IAkInPlaceEffectPlugin` or `IAkOutOfPlaceEffectPlugin` | `IAkSourcePlugin` | `IAkMixerEffectPlugin` |
| FMOD | `FMOD_DSP_DESCRIPTION` (process callback) | `FMOD_DSP_DESCRIPTION` (generatetone or read) | `FMOD_DSP_DESCRIPTION` on a bus |

- Effect plugins modify an existing signal in place or out of place.
- Source plugins generate audio from scratch (synthesisers, procedural audio).
- Mixer plugins operate on a mix bus and see the summed signal from all inputs.
- Confirm the plugin type before writing any code — changing it later requires reworking the descriptor and callback signatures.

## Step 2 — Set up the plugin descriptor

**Wwise:**
- Declare an `AkPluginInfo` struct with your company ID, plugin ID, and plugin type.
- Implement `GetPluginInfo()` to return it from your plugin class.
- Provide a `CreateXxx` factory function and register it with `AK::SoundEngine::RegisterPlugin`.
- Implement a matching `AkPluginParamBase` subclass for parameter storage.

**FMOD:**
- Declare an `FMOD_DSP_DESCRIPTION` struct with name, version, channel counts, and all callback pointers.
- Fill `FMOD_DSP_PARAMETER_DESC` entries for every parameter the DSP exposes.
- Export a `FMODGetDSPDescription()` function (or pass the struct directly to `FMOD::System::createDSP`).
- Keep the description in static storage — FMOD holds a pointer to it for the lifetime of the DSP.

## Step 3 — Implement the audio callback

**Wwise (`Execute`):**
- Read channel count and frame count from `AkAudioBuffer` at runtime — never hardcode.
- Use `io_pBuffer->GetChannel(ch)` to access per-channel float pointers.
- Allocate during `Init` with the `AK::IAkPluginMemAlloc*` allocator; never allocate inside `Execute`.
- Return early if `uValidFrames == 0` to avoid processing silent tail unnecessarily.

**FMOD (`read` or `process`):**
- Use `inchannels` and `outchannels` from the callback signature — do not assume stereo.
- Allocate during create/reset with `dsp_state->functions->alloc` / `free`; never allocate inside `read` / `process`.
- Never block, lock, or perform I/O; FMOD calls this from a mixer thread with a hard deadline.
- Return `FMOD_OK` after producing valid output; return `FMOD_ERR_DSP_SILENCE` only when the DSP intentionally produces silence.

## Step 4 — Handle parameters

**Wwise RTPC binding:**
- Declare parameter IDs as an enum in your plugin header.
- Implement `SetParam` on your `AkPluginParamBase` subclass to copy incoming values into your struct.
- Wwise copies the parameter struct before calling `Execute` — read from the struct, not from `SetParam` directly.
- Clamp every RTPC value to its valid range before feeding it to DSP computation.

**FMOD parameter system:**
- Define one `FMOD_DSP_PARAMETER_DESC` per parameter in your `FMOD_DSP_DESCRIPTION`.
- Implement `setparameterfloat` / `getparameterfloat` callbacks to read/write from your plugin state.
- Use a fixed enum for parameter indices and keep it in the same order as `paramdesc`; do not rely on magic numbers.
- Use `FMOD_DSP_PARAMETER_DESC` with `FMOD_DSP_PARAMETER_TYPE_FLOAT` and the appropriate float mapping (`LINEAR`, `AUTO`, or piecewise linear) so Studio renders controls correctly.

## Step 5 — Register, test, and package

- Wwise: call `AK::SoundEngine::RegisterPlugin` during engine init before loading banks; ship a `.dll`/`.so` plus a `.xml` authoring descriptor.
- FMOD: pass the `FMOD_DSP_DESCRIPTION` to `createDSP` or load via `loadPlugin`; ship as `.plugin.dll`/`.so`.
- Unit-test with known input buffers outside the engine; cover channel counts 1, 2, and 6.
- Test bypass, all-zeros input, and extreme parameter values.
- Guard debug logging behind `#ifndef AK_OPTIMIZED` (Wwise) or equivalent release flag (FMOD).
