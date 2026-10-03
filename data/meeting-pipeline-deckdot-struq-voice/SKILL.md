---
name: meeting-pipeline
description: "The meeting state machine, loopback capture window and transcription worker in Struq Voice. Use whenever a task involves meetings, meeting state (idle/starting/recording/paused/finalizing/error), Ctrl+Shift+M, the meeting hotkey, loopback or getDisplayMedia capture, the meeting window, the struq-meeting utilityProcess, VAD utterances, Silero, speaker clustering, diarization, the CAM++ embedding or pyannote segmentation assets, the opus archive writer, or meeting export. Explains the lane split (mic is me, system is clustered), the dictation-always-wins yield rule, the bounded queue, and why ASR runs out of process. NOT for IPC wiring (use ipc-architecture) or gating (use verification-gates)."
argument-hint: "[state-machine | lanes | worker | loopback | archive]"
---

# Meeting pipeline

## The single authority

`src/main/meeting/meeting-session.ts` owns meeting state. Tray and main
window render from broadcasts of it (`meeting:state-changed` IPC). Nothing
else mutates or owns meeting state.

```
idle ──start──▶ starting ──lanes live──▶ recording ──stop──▶ finalizing ──▶ idle
  ▲                │                        │  ▲                            │
  │                └──fail──────────────────┴──┘pause/resume──────────────┘
  └────────── error ◀────────────────── worker failure / 8s lane timeout ──┘
```

- Refused up front when the database, the support assets or the engine are
  unavailable. The renderer turns each refusal into its own copy, never an
  error toast.
- The support assets ship with the installer (`extraResources`), so in a
  packaged build they are always present and nothing is downloaded. The
  downloader is the repair path for a dev checkout or missing files, and it
  runs on its own without naming a single model to the user.
- The hidden meeting window is created on start, destroyed on stop; the
  `struq-meeting` utilityProcess is forked on start, drained on stop, killed.

## Lifecycle rules (do not relitigate)

`start()` awaits four times: storage, worker start, window load, capture
gesture. Every one of those is a point where the stop hotkey can land.

- **Each start carries a generation token.** `stop()` and `dispose()`
  invalidate it before tearing anything down, and `start()` re-checks after
  every await. A start that has been overtaken unwinds only what *it*
  created and returns; it must never rebuild shared state. Without this the
  losing start rebuilt the window and worker that stop had just destroyed,
  leaving a recorder nobody owned holding the microphone and the loopback
  for the life of the app.
- **A start already in flight refuses a second one.** Two concurrent starts
  would run two full sequences against one set of handles.
- **One finalize per meeting row.** `stop()` claims the id when it cancels a
  start mid-flight so the unwind skips it; otherwise both write and race to
  decide `complete` versus `interrupted`.
- **A meeting that never recorded is `interrupted`.** Cancelled mid-start, a
  failed archive, a dead capture renderer: all `interrupted`, never
  `complete`.
- **Main watches `render-process-gone` on the meeting window.** The
  lane-live timer is cleared the moment a lane goes live, so after that
  nothing else notices a dead renderer and the session would sit in
  `recording` forever with a frozen archive.

## Why ASR runs out of process

`sherpa-onnx-node`'s `recognizer.decode()` is a synchronous blocking native
call. For dictation that is fine; for continuous meeting decoding it would
stall main (tray, IPC, hotkeys, every window pump) for most of the meeting.
The worker (`src/main/meeting/worker/index.ts`) is a utilityProcess with its
own event loop, crash isolation and memory that is genuinely released on
kill. The queue is hard-capped at 600 seconds of backlog; over the cap emits
a `gap` marker instead of growing.

## Speaker clustering

`worker/speaker-clusterer.ts`. A voice is a bounded ring of its recent
embeddings, scored by the mean of the top few similarities. A single running
mean was tried and does not work: one voice split into two clusters whose
means were 0.494 apart while two genuinely different voices sat at 0.391, so
no threshold separates them.

Three rules keep one person from becoming several, which is what the 1.2.x
releases did:

- **Duration is the dominant factor.** CAM++ scores about 0.05 against its own
  voice at 300ms, 0.15 at one second and 0.89 at eight. Anything under
  `minSpeakerAudioMs` (3s) is *provisional*: it takes the nearest speaker's
  label but may never found or define one. Backchannels were minting speakers.
- **Embed the speech, not the utterance.** The VAD hands back padding; embed
  `trimSilence`'d audio or the fingerprint is partly the room.
- **Two thresholds and a merge.** At or above `threshold` the embedding is
  kept, below `createThreshold` it is somebody new, and in between it joins the
  nearest speaker without defining them. Converged speakers merge, which emits
  `speakers-merged` so main can rewrite stored segments.

`speakerMergeThreshold` is *not* on the same scale as `speakerThreshold`: it
averages every pair across two rings, where assignment takes the best few
against one. Scoring a merge with top-k instead of the mean fused a male and a
female voice.

Measure changes, do not guess them: `node scripts/make-two-speaker-fixture.mjs
--speakers 1` then `node scripts/diarization-bench.mjs`. The one-speaker
fixture must yield exactly one speaker and the two-speaker fixture exactly two.

## The lane split (do not relitigate)

- The microphone lane is you by construction: it gets the speaker key `me`
  and no clustering.
- The system lane (Windows loopback) is everyone else: your voice is not in
  it because conferencing apps do not render your own mic back to you. Only
  this lane is clustered.
- Lanes are mixed only into the archive (`recording.webm`), never into the
  transcript pipeline.
- `SpeechSegment.start` from one `Vad` per lane per meeting is the meeting
  timeline directly; no separate clock.

## Dictation always wins

The capture session's state is mirrored into
`meetings.setDictationActive(state.phase !== "idle" && state.phase !== "error")`.
The worker finishes the utterance it is on, then holds until released. Its
queue grows for at most one dictation, then drains.

## Loopback acquisition

`getDisplayMedia` needs transient user activation and a hotkey-started
meeting has none. Main sends `meeting-audio:begin` with the options, the
renderer stores them and exposes `window.__struqBeginMeetingAudio()`, and
main calls it via `webContents.executeJavaScript(code, true)` (the only
supported path). The handler in `src/main/meeting/loopback.ts` grants
`audio: "loopback"` (never `loopbackWithMute`) to the meeting window only.
Never use `loopbackWithMute`: it silences the meeting for the user.

## Worker protocol

The wire format is `src/main/meeting/worker/protocol.ts`, not ipc.ts: these
are private messages over `parentPort`, not renderer channels. Audio frames
are structured-cloned copies (32 KB/s per lane), never SharedArrayBuffer.

## Archive

`src/main/meeting/archive-writer.ts` appends opus chunks to
`userData/meetings/<id>/recording.webm` with an internal queue so the IPC
handler never blocks. Main is the only SQLite writer; the worker never
touches the database.

## Export

`src/main/meeting/export.ts` is pure over records, segments and speakers:
Markdown, plain text and SRT. Speaker labels resolve from the speakers map,
falling back to `defaultSpeakerLabel`; gap rows render as "[not
transcribed]" and are skipped in SRT.
