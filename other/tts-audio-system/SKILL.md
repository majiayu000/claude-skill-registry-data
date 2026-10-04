---
name: tts-audio-system
description: "The TTS/STT/audio-playback system behind the one `speak()` entry point. Use when working on read-aloud, the Listen panel, voice/speed settings, transcription, mic capture, SpeakerButton, iOS playing silence, audio API routes, or files in features/audio/, features/tts/, hooks/tts/, app/api/audio/."
---

# TTS / Audio System

## 🚨 Start here — the four things that are easy to get wrong

1. **`speak()` is the ONE entry point** (`features/audio/service/speak.ts`). Never
   hand-roll a TTS call, never construct a player, never read a voice preference
   yourself. React surfaces use `useSpeech()` on top of it. To let someone HEAR
   a catalog model's voice (e.g. a speech-script speaker), call
   `speak({ text, sample: { model, voice } })` — the catalog lane plays the
   vendor's own sample (ElevenLabs) or a line the server renders once per
   (model, voice) via `POST /audio/voice-preview`.
2. **Voice / speed / language come from the tiered `listening` config**
   (`features/audio/service/listeningConfig.ts`) — system → org → user, user wins.
   **Never read `userPreferences.voice.*` for playback**; those fields survive
   only as the pre-fetch boot fallback. See the tiered-config section below.
3. **Audio output must be unlocked inside a user gesture** or iOS plays silence.
   Call `primeAudioOutput()` (`features/audio/unlock.ts`) synchronously in any
   handler that will later start audio. See the iOS section below.
4. **One voice at a time, app-wide.** `playbackLock` arbitrates; the
   `playbackQueue` + `audioSessionRegistry` own what is playing and its history.
   Producing audio without a session trips the runtime bypass guard.

## Architecture Overview

Two independent TTS engines, one STT engine, and a voice assistant pipeline.

### TTS Engines

| Engine | Provider | Transport | Primary Hook | API Route |
|--------|----------|-----------|-------------|-----------|
| **Cartesia** | Cartesia API | WebSocket (PCM F32LE, 44.1kHz) | `useCartesiaSpeaker` | `GET /api/cartesia` |
| **Groq/PlayAI** | Groq SDK | REST → WAV blob | `useTextToSpeech` | `POST /api/audio/text-to-speech` |

### STT Engine

| Route | Provider | Auth | Max Size |
|-------|----------|------|----------|
| `POST /api/audio/transcribe` | Groq Whisper | Supabase cookie/Bearer | 4.5 MB |
| `POST /api/audio/transcribe-url` | Groq Whisper | Supabase cookie/Bearer | 100 MB (URL) |
| `POST /api/audio/log-error` | Supabase | Supabase cookie/Bearer | N/A |

### Auth

All audio API routes use `resolveUser` from `utils/supabase/resolveUser.ts` — dual-mode: Supabase session cookie OR Bearer token. Both TTS routes (`/api/cartesia`, `/api/audio/text-to-speech`) require authentication.

---

## Directory Map

```
features/tts/              ← Production TTS feature (Cartesia + Groq)
  hooks/
    useCartesiaSpeaker.ts   ← PRIMARY Cartesia hook (lazy, self-contained)
    useTextToSpeech.ts      ← Groq/PlayAI hook (REST, WAV blob)
  components/
    SpeakerButton.tsx       ← Single play/pause toggle (lazy-loads core)
    SpeakerButtonCore.tsx   ← Dynamically imported Cartesia logic
    SpeakerGroup.tsx        ← 3-button group shell (Play, Pause, Stop)
    SpeakerGroupCore.tsx    ← Dynamically imported 3-button core
    SpeakerCompactGroup.tsx ← 2-button group shell (Play/Pause, Stop)
    SpeakerCompactGroupCore.tsx
    AudioPlayerButton.tsx   ← Groq/PlayAI button (uses useTextToSpeech)
  types.ts                  ← Shared types (EnglishVoice, SpeakerVariant, etc.)

hooks/tts/                  ← Legacy/specialized hooks
  simple/
    useCartesiaControls.ts  ← Full controls (connect-on-mount, script state)
    useCartesiaWithPreferences.ts ← Redux voice prefs + connect-on-mount
    useSimpleCartesia.ts    ← Minimal Cartesia (connect-on-mount)
  useCartesia.ts            ← Legacy full-featured (direct API key, eager)
  usePlayer.ts              ← Raw PCM stream player (Web Audio API, 24kHz)
  usePlayerSafe.ts          ← Enhanced usePlayer with explicit init
  useVoiceChat.ts           ← Voice assistant pipeline (VAD + STT + AI + TTS)
  useVoiceChatCdn.ts        ← CDN variant of voice chat
  useVoiceChatWithAutoSleep.ts ← Auto-sleep extension

features/audio/             ← THE modern audio system (start here, not features/tts/)
  service/
    speak.ts                ← 🚨 THE app-wide "turn text into audio" entry point
    useSpeech.ts            ← React face of speak() (per-surface status)
    listeningConfig.ts      ← 🚨 tiered voice/speed/language (system→org→user)
    useListeningSettings.ts ← settings-pane face; update() writes MY tier
    engines.ts              ← AV engine registry (voice lists live here ONCE)
  unlock.ts                 ← 🚨 iOS/WebKit gesture unlock (see iOS section)
  activation.ts             ← one-way latch that mounts the lazy audio system
  playback/
    playbackQueue.ts        ← the single app-wide queue (one at a time)
    playbackLock.ts         ← app-wide single-output arbiter (start-always-wins)
    AudioPlaybackHost.tsx   ← queue → Redux mirror; installs unlock listeners
    adapters/cartesiaAdapter.ts  ← streaming PCM lane (SinkAwarePlayer)
    adapters/catalogAdapter.ts   ← server-catalog lane (HTMLAudioElement)
  session/
    audioSessionRegistry.ts ← ALL audio activity (in + out, live + history)
    usePlaybackSessionController.ts / useMediaElementPlaybackSession.ts
    bypassGuard.ts          ← screams when audio is produced with no session
  sinkAwarePlayer.ts        ← our WebPlayer fork; output-device routing
  hooks/ components/ services/ voice/   ← recording, mic UI, voice selection UI

features/window-panels/windows/listen/
  ListenSummaryWindow.tsx   ← the Listen panel (summarize-for-listening player)

providers/AudioSystemHost.tsx        ← the ONE ssr:false boundary (lazy mount)
providers/AudioOutputHostImpl.tsx    ← app-root streaming speaker owner

lib/cartesia/               ← Low-level Cartesia client & types
  client.ts                 ← LEGACY: direct NEXT_PUBLIC_CARTESIA_API_KEY
  cartesia.types.ts         ← Full Cartesia type definitions
  voices.ts / voices.json   ← Voice catalog

app/api/cartesia/route.ts   ← Token endpoint (authenticated)
app/api/audio/              ← TTS + STT API routes

utils/supabase/resolveUser.ts  ← Shared auth resolution
utils/markdown-processors/parse-markdown-for-speech.ts ← MD → plain text
```

---

## Hook Selection Guide

**Adding TTS to a new component?** Use `useCartesiaSpeaker` or a Speaker* component.

| Need | Solution |
|------|----------|
| Single play/pause button | `<SpeakerButton text={content} />` |
| 3-button group (Play/Pause/Stop) | `<SpeakerGroup text={content} />` |
| 2-button group (toggle + Stop) | `<SpeakerCompactGroup text={content} />` |
| Programmatic TTS with Redux prefs | `useCartesiaSpeaker({ processMarkdown: true })` |
| Groq/PlayAI TTS (non-Cartesia) | `useTextToSpeech()` or `<AudioPlayerButton text={content} />` |
| Full voice config UI (demo/playground) | `useCartesiaControls()` or `useSimpleCartesia()` |
| Voice assistant with VAD | `useVoiceChat()` or `useVoiceChatWithAutoSleep()` |

### Why multiple hooks exist

The legacy hooks (`useCartesiaControls`, `useSimpleCartesia`, `useCartesia`) connect eagerly on mount and manage their own voice/emotion/speed state. They exist for playground and demo pages where the user needs full control over Cartesia parameters.

`useCartesiaSpeaker` is the production hook: lazy (does nothing until `speak()` is called), reads voice preferences from Redux, and has proper error handling. Always prefer it for new features.

---

## Speaker Component Contracts

All Speaker* components follow the same pattern:

1. **Thin shell** renders static disabled buttons (zero JS loaded)
2. **First click** triggers `React.lazy()` → dynamically imports Core
3. **Core** initializes `useCartesiaSpeaker` and begins playback
4. **Shape never changes** — buttons are always rendered, unavailable actions are disabled

### Props (all variants)

```typescript
interface SpeakerProps {
  text: string;           // Content to speak
  processMarkdown?: boolean; // Strip markdown (default: true)
  className?: string;     // Applied to outer container
  disabled?: boolean;     // Disable all buttons
}

// SpeakerButton also accepts:
variant?: 'glass' | 'transparent' | 'solid' | 'group';
```

### Icon System

Speaker buttons use raw SVG icons from `@ai-matrx/tap-target/buttons`, NOT Lucide. Available: `PlayTapButton`, `PauseTapButton`, `StopTapButton`, `Volume2TapButton`. (Formerly `components/icons/tap-buttons.tsx`, deleted in the 2026-08-30 C9 package adoption.)

### Styling

Uses `TapTargetButton` / `TapTargetButtonGroup` from the `@ai-matrx/tap-target` package (C9 adoption, 2026-08-30 — the old in-repo copy is gone). Glass styling via `matrx-glass` CSS classes (globally available in `app/globals.css`).

---

## API Contracts

### GET /api/cartesia

**Auth:** Required (cookie or Bearer)
**Response:** `{ token: string }` — short-lived Cartesia access token
**Errors:** 401 (no auth), 500 (token generation failed)

### POST /api/audio/text-to-speech

**Auth:** Required (cookie or Bearer)
**Body:** `{ text: string; voice?: EnglishVoice; model?: string }`
**Response:** `audio/wav` binary (Cache-Control: 1 year)
**Limits:** text max 10,000 chars, voice must be valid PlayAI voice
**Errors:** 400 (validation), 401 (no auth), 429 (rate limit), 500

### POST /api/audio/transcribe

**Auth:** Required
**Body:** `multipart/form-data` with `file` (audio), optional `language`, `prompt`
**Response:** `{ success, text, language, duration, segments, _meta: { attempts } }`
**Limits:** 4.5 MB file size, allowed types: flac/mp3/mp4/mpeg/mpga/m4a/ogg/wav/webm
**Retries:** 3 with exponential backoff, logged to `audio_transcription_errors`

### POST /api/audio/transcribe-url

**Auth:** Required
**Body:** `{ url: string; language?; prompt? }` — URL must be on the route's allowlist (Python backend tiers + AWS S3 hostnames; signed cld_files URLs qualify)
**Response:** Same as /transcribe
**Limits:** 100 MB via Groq URL parameter

---

## Voice / speed / language — the tiered listening config (2026-08-28)

🚨 **Cartesia voice, speed, and language NO LONGER live in `userPreferences.voice` for playback.** They resolve through the tiered surface-config `listening` namespace (system → org → user, user wins) via `features/audio/service/listeningConfig.ts`:

- React reads: `selectListeningVoice/Speed/Language` (+ `selectListeningVoiceId(state, purpose)`).
- Imperative reads (`speak()`, playback adapters): `getListeningSettings()` — resolves at START time so replays honor current settings.
- Writes: `useListeningSettings().update(patch)` — ONE row at the user's tier (never a whole-preferences write).
- System default: platform-global row, admin-edited at `/administration/ui/surfaces/matrx-user/assistant-message` (Config namespaces). Org rows override; user rows win.

`userPreferences.voice.{voice,speed,language}` remain ONLY as the pre-fetch boot fallback; `emotion`/`wakeWord`/`microphone`/`speaker` still live there.

## Redux Voice Preferences (legacy fields — see above for voice/speed/language)

```typescript
// state.userPreferences.voice (Cartesia)
interface VoicePreferences {
  voice: string;    // LEGACY for playback — boot fallback only
  language: string; // LEGACY for playback — boot fallback only
  speed: number;    // LEGACY for playback — boot fallback only
  emotion: string;
  microphone: boolean;
  speaker: boolean;
  wakeWord: string;
}

// state.userPreferences.textToSpeech (Groq/PlayAI)
interface TextToSpeechPreferences {
  preferredVoice: GroqTtsVoice; // e.g. "Cheyenne-PlayAI"
  autoPlay: boolean;
  processMarkdown: boolean;
}
```

---

## 🚨 iOS / WebKit — the output-unlock law (2026-08-30)

**Every browser on iPhone is WebKit — Chrome and Firefox included — so these
rules are not "a Safari edge case", they are the whole mobile platform.**

Two WebKit behaviors made all mobile audio silent, with no error:

1. An `AudioContext` created (or resumed) **outside a user gesture** starts
   `suspended` and stays silent. Our TTS starts audio from websocket callbacks
   seconds after the tap, so per-utterance contexts were always suspended.
2. Web Audio is muted by the **ringer/silent switch** unless the page declares
   `navigator.audioSession.type = "playback"` (iOS 16.4+).

`features/audio/unlock.ts` is the fix and the only place this logic lives:

- `installAudioUnlockListeners()` — capture-phase `pointerdown`/`keydown`/
  `touchend` listeners; mounted ONCE by `AudioPlaybackHost`. Unlocks on the
  user's first interaction anywhere, so the page is usually already unlocked
  before any audio is requested.
- `primeAudioOutput()` — **call this synchronously in every handler that will
  later start audio.** Idempotent and cheap. Already called by
  `enqueuePlayback` / `resumePlayback` / `playPlaybackItem`, both Listen
  actions, and the Listen panel transport.
- `getUnlockedAudioContext()` / `getPrimedMediaElement()` — the shared,
  gesture-unlocked handles. `SinkAwarePlayer` schedules into the shared
  context when it exists (per-utterance `GainNode`; **never closes it**);
  `catalogAdapter` plays through the shared element.

**Rules when you touch audio:**
- Adding a new "start audio" button? Call `primeAudioOutput()` in the handler.
- Never mint a bare `new AudioContext()` for playback — go through the queue.
- Never close the shared context (`stop()` in shared mode tears down the
  utterance only).
- A context that will not reach `running` **throws a user-facing error**
  ("The browser blocked audio output — tap the play button to start sound").
  Keep it that way: silence with no error is the bug this replaced.

---

## The Listen panel — summarize-for-listening

`features/window-panels/windows/listen/ListenSummaryWindow.tsx` (overlay
`listenSummaryWindow`). Two entry points, both in one "Listen" context-menu
submenu and in the assistant action bar's ⋯ menu:

- **Summarize without playing** — summary streams in as text; user presses Play.
- **Summarize & listen** — stream-to-stream: the summary is spoken as it is
  written, via the app-root speaker (`voicePlaybackBus` request with
  `includeActive: true`).

The summarizing agent is resolved from the `spoken_summary` surface role,
falling back to the platform home surface (`LISTENING_HOME_SURFACE`) whose
`ambient.spoken_summary` mandate holds the default agent — so it works on
every surface for every user with no personal binding. **Never put an agent
UUID in code here.** Menu wiring: `features/context-menu-v3/` (`listen`
submenu role) + `messageActionRegistry.listeningItems`.

---

## Known Deferred Issues

These are documented design decisions, not bugs:

1. **Five Cartesia hook variants** — Consolidation into one hook requires updating ~15 consumer files. Deferred as separate effort. Use `useCartesiaSpeaker` for all new code.
2. **`lib/cartesia/client.ts` leaks API key** — Uses `NEXT_PUBLIC_CARTESIA_API_KEY`. Legacy hook `useCartesia` depends on it. Will be removed when legacy hook is consolidated.
3. **No connection health monitoring** — No heartbeat/ping. Silent WebSocket drops discovered only on next `speak()`.
4. **No playback progress for Cartesia** — the catalog (element) lane tracks duration/currentTime; the streaming PCM lane does not.
5. **Token expiry** — Cartesia token fetched once, no refresh. If it expires mid-session, `connectCartesiaTts` refreshes and retries once automatically.

**Two entries were REMOVED on 2026-09-08 because they became false** — do not
reinstate them from an old copy of this file: *"no global TTS instance
management"* (the `playbackQueue` + `playbackLock` + `audioSessionRegistry`
trio has been the single owner since the unified-audio work) and *"no abort
for in-flight TTS"* (`skipPlayback` / `clearPlayback` / a session's `stop`
control all abort; `playbackLock` preempts across paths).

---

## Adding a New Speaker Variant

1. Create `SpeakerNewVariant.tsx` (thin shell) in `features/tts/components/`
2. Create `SpeakerNewVariantCore.tsx` (default export, uses `useCartesiaSpeaker`)
3. Use `React.lazy()` in shell to import core
4. Use `TapTargetButton*` from `@ai-matrx/tap-target` (icons: `@ai-matrx/tap-target/buttons`)
5. Export from `features/tts/components/index.ts`
6. Never hide buttons — disable unavailable actions
7. Never change component shape during state transitions

## Modifying API Routes

All audio API routes use `resolveUser` from `utils/supabase/resolveUser.ts`. When adding new routes:
1. Import and call `resolveUser(request)` first
2. Return 401 if `!user`
3. Use structured error responses with `code` field
4. For Groq routes: implement retry with exponential backoff
5. Log errors to `audio_transcription_errors` via `logTranscriptionError()`
