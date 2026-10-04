---
name: transcription-voice-system
description: Guide for working on the Transcription, Voice, and Wake Word system spanning Rust (Tauri), Python (FastAPI), and React layers. Use when editing Voice.tsx, use-transcription.ts, use-wake-word.ts, use-transcription-sessions.ts, TranscriptionContext, WakeWordContext, wake_word_routes, transcription/ Rust module, session persistence, or any audio/whisper/wake-word related code. Also use when adding new AI tools that interact with voice/transcription data.
---

# Transcription & Voice System

## Mandatory: Keep This Skill Current

**Any agent that makes significant modifications to this system MUST update this skill file before finishing.** If you discover that the code has drifted from what this skill describes — fix the skill. Outdated guidance here causes real bugs (infinite render loops, state divergence, SIGABRT on quit). Treat this file as a living specification.

## Architecture (4 Layers)

```
RUST (Tauri IPC)          — Whisper inference, audio capture, wake word (whisper-tiny)
PYTHON (FastAPI :22140)   — OpenWakeWord ONNX, AI audio tools, wake word settings
REACT (Vite :1420)        — Hooks, contexts, UI, session persistence
STORAGE                   — localStorage, SQLite, filesystem, Supabase (settings only)
```

## Critical Rules — Read Before Touching Anything

### 1. Singleton Context Pattern (NEVER violate)

`useTranscription()` runs **once** inside `TranscriptionProvider` at the app root. All consumers use `useTranscriptionApp()` from `TranscriptionContext.tsx`. **Never** call `useTranscription()` directly in a page or component — the Rust side only allows one active audio stream; multiple hook instances cause state divergence.

```tsx
// WRONG — creates independent state instance
const [state, actions] = useTranscription();

// CORRECT — reads from singleton context
const { state, actions } = useTranscriptionApp();
```

Same pattern applies: `useLlmApp()`, `useTtsApp()`. `useWakeWord()` is the one exception — it's called only in `Voice.tsx` and published to `WakeWordContext` via `usePublishWakeWord()`.

### 2. useMemo on ALL Return Objects

Every hook returning `[state, actions]` **must** wrap both in `useMemo`. A plain object literal is a new reference every render, causing infinite loops through any `useEffect` or context consumer.

```tsx
// Both state AND actions must be memoized
const state = useMemo(() => ({ ... }), [deps]);
const actions = useMemo(() => ({ ... }), [deps]);
```

Hooks that follow this pattern: `useTranscription`, `useWakeWord`, `useTranscriptionSessions`. Parity tests enforce this — see `tests/parity/test_transcription_parity.py`.

### 3. Never Use `actions` as a useEffect Dependency

Even with `useMemo`, always list the specific callback you call, never the entire `actions` object.

### 4. Session Writes Are Debounced

`appendSegments()` in `sessions.ts` buffers segments in memory and flushes to localStorage every 1s. Call `flushNow()` before `finalizeSession()` or component unmount. The `useTranscriptionSessions` hook registers a flush callback automatically.

### 5. Rust Shutdown Order Matters

`graceful_shutdown_sync()` in `lib.rs` must: stop wake word → join (2s) → stop recording → join (5s) → kill llama-server → drop TranscriptionState → kill sidecar. Dropping WhisperContext before joining threads causes SIGABRT from GGML's `atexit` handler.

### 6. Wake Word Keyword Is Read Dynamically

The wake word thread reads `state.keyword` from the Mutex on each detection window (not captured once at start). `configure_wake_word` persists to `TranscriptionConfig.wake_keyword` on disk.

## File Map

### Rust (desktop/src-tauri/src/transcription/)
| File | Purpose |
|------|---------|
| `commands.rs` | 26+ Tauri commands, state types, transcription loop |
| `manager.rs` | WhisperContext wrapper (model load + inference) |
| `audio_capture.rs` | CPAL mic → rubato 16kHz mono resampling |
| `config.rs` | `TranscriptionConfig` persistence (JSON) — includes `wake_keyword` |
| `downloader.rs` | HuggingFace model download with cancel support |
| `hardware.rs` | RAM/CPU/GPU/Metal/CUDA detection (platform-specific) |
| `model_selector.rs` | 3-tier model recommendation |
| `wake_word.rs` | Whisper-tiny 2s window KWS thread |

### Python (app/)
| File | Purpose |
|------|---------|
| `api/wake_word_routes.py` | REST + SSE for OpenWakeWord engine |
| `services/wake_word/service.py` | OWW singleton: sounddevice → ONNX → events |
| `services/wake_word/models.py` | OWW model catalog + HF download |
| `api/settings_routes.py` (lines 124-155) | Wake word settings GET/PUT |
| `tools/tools/audio.py` | 4 AI tools: ListAudioDevices, RecordAudio, PlayAudio, TranscribeAudio |

### React (desktop/src/)
| File | Purpose |
|------|---------|
| `hooks/use-transcription.ts` | Whisper lifecycle, recording, download queue |
| `hooks/use-wake-word.ts` | Dual-engine (whisper/OWW) state machine |
| `hooks/use-transcription-sessions.ts` | Session CRUD over localStorage |
| `contexts/TranscriptionContext.tsx` | **Singleton** — `useTranscriptionApp()` |
| `contexts/WakeWordContext.tsx` | Publish/subscribe from Voice.tsx → toolbar |
| `contexts/TranscriptionSessionsContext.tsx` | Shared session store |
| `contexts/AudioDevicesContext.tsx` | Single source for mic devices |
| `lib/transcription/sessions.ts` | localStorage CRUD with debounced writes |
| `lib/transcription/types.ts` | All TypeScript types |
| `pages/Voice.tsx` | Main page (5 tabs, ~2800 lines) |
| `pages/WakeWord.tsx` | Wake word tab (engine picker, OWW models) |
| `components/TranscriptOverlay.tsx` | Floating Tauri window (`/#/overlay`) |
| `components/CompactRecorderWindow.tsx` | OS-resized compact recorder |
| `components/TranscriptionMiniMode.tsx` | In-page floating panel |
| `components/WakeWordOverlay.tsx` | Ambient glow indicator |
| `components/WakeWordControls.tsx` | Status-bar control strip |
| `components/recording/RecordingMicButton.tsx` | Reusable mic toggle |
| `components/recording/RmsLevelBar.tsx` | Audio level meter |
| `components/quick-actions/QuickTranscriptModal.tsx` | Quick record dialog |
| `components/documents/NoteEditor.tsx` | Inline dictation |

## Provider Nesting Order (App.tsx)

```
DevTerminalProvider > DownloadManagerProvider > TtsProvider > LlmProvider
  > WakeWordProvider > TranscriptionSessionsProvider > PermissionsProvider
    > AudioDevicesProvider > TranscriptionProvider > TooltipProvider
```

`TranscriptionProvider` must be inside `AudioDevicesProvider` (it uses `AudioDevicesContext`).

## State Ownership

| State | Storage | Survives restart? |
|-------|---------|-------------------|
| Transcription recording | `TranscriptionContext` (React) | No |
| Session history (500 max) | `localStorage` key `matrx-transcription-sessions` | Yes |
| Selected audio device | `localStorage` key `matrx-selected-audio-device` | Yes |
| Wake word engine pref | SQLite via `PUT /settings/wake-word` | Yes |
| App-level settings (enabled, auto-init, model, etc.) | `localStorage` + Supabase cloud sync | Yes |
| Whisper model files | `~/{app_data}/models/*.bin` | Yes |
| Rust config (model, setup_complete, wake_keyword) | `~/{app_data}/transcription.json` | Yes |
| OWW models | `~/.matrx/oww_models/` | Yes |

**No cloud sync for session data.** Only settings sync via the generic `AppSettings` pipeline.

## Dual Wake Word Engines

| | Whisper (Rust) | OpenWakeWord (Python) |
|---|---|---|
| Backend | Tauri IPC commands + events | REST + SSE via FastAPI |
| Model | `ggml-tiny.en.bin` (75 MB) | ONNX models (~3 MB each) |
| Latency | ~2s (full ASR on 2s windows) | ~150ms (purpose-built KWS) |
| CPU | High (runs full whisper) | Low (small ONNX model) |
| Events | Tauri: `wake-word-detected`, `-rms`, `-mode`, `-error` | SSE: identical event names |
| Config | Keyword in `TranscriptionConfig` | Model/threshold in SQLite |

`useWakeWord` abstracts both behind the same `WakeWordHookState` / `WakeWordHookActions` interface.

## Recording Pipeline

```
1. startRecording() → Tauri IPC "start_transcription"
2. Rust: Opens AudioCapture (CPAL) → 16kHz mono via rubato
3. Rust: 2s silence calibration → emits "whisper-calibrated"
4. Rust: 5s chunk accumulation → ctx.transcribe_with_params()
5. Rust: Emits "whisper-segment" per segment (filtered for hallucinations)
6. React: useTranscription accumulates segments in state
7. React: sessionsActions.append() → debounced localStorage write
8. stopRecording() → sets flag → Rust flushes remaining audio
9. Rust: emits "whisper-stopped" → React tears down listeners
```

## AI Polish Pipeline

Uses **local LLM** (llama-server sidecar), not cloud:
1. `useLlmPipeline.run("polish_transcript", { transcript })`
2. Structured output: `{ title, description, tags, cleaned }`
3. `sessionsActions.applyPolish()` preserves `rawText` on first run

## Adding a New Feature — Checklist

- [ ] New hook state → wrap `state` and `actions` in `useMemo`
- [ ] New context → add provider to `App.tsx` in correct nesting order
- [ ] New Tauri command → add to `lib.rs` `generate_handler![]`, verify `cargo check`
- [ ] New settings key → add to TS `AppSettings`, Python `DEFAULT_SETTINGS`, `SECTION_KEYS`
- [ ] New AI tool → register in `dispatcher.py` + `tool_schemas.py`
- [ ] Run `uv run pytest tests/parity/test_transcription_parity.py` to verify
- [ ] Update this skill file if architecture changed

## Common Pitfalls

| Mistake | Consequence | Prevention |
|---------|-------------|------------|
| Call `useTranscription()` in a page | Duplicate instance, state divergence | Always `useTranscriptionApp()` |
| Plain object `actions` return | Infinite render loops, API polling floods | `useMemo` wrap — parity tests catch this |
| `[actions]` in useEffect dep | Re-fires every render | Use specific callback: `[refreshStatus]` |
| Use `ReturnType<typeof useTranscription>` for prop types | TS2552 / TS2448 — name no longer in scope after context migration | Import `TranscriptionState`, `TranscriptionActions` from `@/hooks/use-transcription` |
| `useCallback` declared after `useEffect` that references it | TS2448 "used before declaration" — blocks release | Always declare `useCallback` functions **above** any `useEffect` that references them |
| Drop WhisperContext before joining thread | SIGABRT / macOS crash report | `graceful_shutdown_sync()` joins first |
| Read localStorage on every render | UI jank with 500 sessions | Derive from React state; debounced writes |
| Forget `flushNow()` before finalize | Up to 1s of segments lost | `finalizeSession()` calls it internally |

## Tests

| File | Category | What it verifies |
|------|----------|-----------------|
| `tests/parity/test_transcription_parity.py` | Parity (fast) | Context exists, IPC names match, `useMemo` wrapping, defaults match, cancel command |
| `tests/smoke/test_wake_word.py` | Smoke (needs engine) | Wake word routes, settings round-trip, model list, lifecycle |

Run parity tests after any change: `uv run pytest tests/parity/test_transcription_parity.py -v`

## Platform-Specific Notes

- **macOS**: TCC microphone permission checked before audio stream opens (`check_microphone_permission`). Metal acceleration for whisper.
- **Windows**: nvidia-smi path probing (`C:\Windows\System32\`, `C:\Program Files\NVIDIA Corporation\NVSMI\`). wmic fallback for GPU detection. No mic permission check needed.
- **Linux/WSL**: WSL nvidia-smi bridge (`/usr/lib/wsl/lib/nvidia-smi`). DRM sysfs for AMD/Intel VRAM. ALSA/PulseAudio via CPAL.

## Known Gaps (as of 2026-03-26)

- `Voice.tsx` is ~2800 lines — tabs should be extracted to `components/voice/*.tsx`
- English-only (`language("en")` hardcoded in Rust)
- No partial/streaming results (full 5s chunks)
- No cloud sync for session data
- Wake word: whisper-tiny is CPU-expensive; sherpa-onnx KWS planned when Rust bindings ship
