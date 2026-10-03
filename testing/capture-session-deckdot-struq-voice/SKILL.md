---
name: capture-session
description: "The capture state machine, hotkeys and audio pipeline in Struq Voice. Use whenever a task involves capture state, the session, phases (idle/arming/listening/transcribing/delivering/error), PTT or the keyboard hook, toggle/escape shortcuts, the recorder window, getUserMedia, the AudioWorklet, pre-roll, or live levels. Explains the single-authority rule, the phase transitions, the debounce/watchdog behavior, the warm-mic design, and how tests drive the session. NOT for IPC wiring (use ipc-architecture) or gating (use verification-gates)."
argument-hint: "[state-machine | phase | ptt | recorder | audio-pipeline]"
---

# Capture session, hotkeys and audio

## The single authority

`src/main/session/capture-session.ts` owns capture state. Tray, overlay and
main window all render from broadcasts of it (`captureStateChanged` IPC).
Nothing else mutates or owns capture state. If a new surface needs capture
state, subscribe to it; do not fork a second source.

## Phases

```
idle ──arm──▶ arming ──ready──▶ listening ──stop──▶ transcribing ──ok──▶ delivering
  ▲             │                   │                    │                    │
  │             └──fail─────────────┴───cancel───────────┘                    │
  └────────── error ◀───────────────┴────────fail────────┘                    │
  └──────────────────────── done (auto after 900ms) ◀─────────────────────────┘
```

- `arming` lasts zero frames in the normal path (warm stream already live).
- `cancel` is Escape, registered as a `globalShortcut` only for the duration
  of a capture (the overlay cannot receive key events).
- Captures under `minCaptureMs` (350ms) are discarded silently.
- A `maxCaptureMs` (300s) watchdog force-stops a stuck-key capture.
- Delivering auto-dismisses to idle after 900ms; error after 4s.

## Hotkeys

- PTT: uiohook-napi key-down/up hook (`Ctrl+Space` default, configurable).
  uiohook has no key-repeat handling natively, so the hook tracks
  `active` and ignores repeated key-downs until the matching key-up.
- Toggle: `Ctrl+Shift+Space` via `globalShortcut` (key-down only is fine
  for a toggle).
- Escape: `globalShortcut`, registered only while listening.
- Both PTT and toggle re-register at runtime from Settings without a
  restart (`setHotkeys` on the controller).

## Audio pipeline (recorder renderer)

- `src/renderer/recorder/recorder.ts` + `audio.ts` own a permanently warm
  `getUserMedia` stream feeding an `AudioWorkletNode` (`pcm-collector`).
- `AudioContext({ sampleRate: 16000 })`: the browser resamples, which is
  faster and more correct than doing it by hand.
- A 30s ring buffer in the worklet gives pre-roll (default 250ms): the audio
  before the key press is included, so no first syllable is clipped.
- PCM is transferred to main as a transferable `ArrayBuffer` (never base64).
- The stream watchdog re-acquires a dead/muted mic and reports `arming`;
  a dead mic never silently produces empty transcripts.
- Audio source selection: real recorder source, or a simulated source in
  e2e (`STRUQ_VOICE_E2E=1`).

## Known invariant

uiohook starts only after the recorder stream is live. This is the
structural fix for the uiohook-napi issue where getUserMedia while a window
is focused kills the global hook; verified by `hook.spec.ts`. Do not move
the hook start earlier without re-verifying that spec.
