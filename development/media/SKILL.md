---
name: media
description: "Maps Puck sound and recording: Puck.Audio mixer and synth, speakers, cues, music director, voice babble, HUD text speech, audio.render, capture.start clips, Puck.Recording (Opus, AV1, Matroska)."
---

# Media

A map of what Puck plays and what it records. Sound and recording share no
code, but both are presentation output that must never feed simulation, and
both reach real hardware only through `Puck.Platform` seams (`platform`).

- **Sound.** `Puck.Audio` holds the deterministic mixer and synth
  (`Puck.Audio.Mixing`) and the music, babble and clock primitives that are
  simulation state (`Puck.Audio.Simulation`). It parses no document.
  `Puck.World` drives it: `WorldAudioDirector` derives the emitter table from
  the delivered world, `WorldAudioRenderService` owns the device, and the
  document intake lives in `src/Puck.World/Audio/`.
- **Recording.** `Puck.Recording` is the platform-neutral recording graph: a
  `RecordingDocument`, a `RecordingSession` that drives it against encoder and
  audio-capture factories, a deterministic Matroska/WebM muxer and an Opus
  lane. Encoders and loopback or microphone capture live in
  `Puck.Platform.Windows`; Linux registers factories that decline.

[Audio](../../../docs/reference/audio.md) and
[recording](../../../docs/reference/recording.md) are the human references;
[the World audio README](../../../src/Puck.World/Audio/README.md) documents
the presentation side. When this file and the code disagree, the code wins and
this file is corrected in the same change.

## Find the owner by what you need

| You need | Owner | Read |
|---|---|---|
| A sound at a place in the world (a speaker, a machine's audio, a creation's sound) | `speakers` rows (`WorldSpeakerFeed`, `WorldSpeakerAttenuation`) → `WorldAudioDirector` emitters → `AudioSnapshot` → `AudioMixer` | [World audio README](../../../src/Puck.World/Audio/README.md#the-device-worldaudiorenderservicecs) |
| A one-shot sound on an event (a stinger, an edit echo) | an `audio.cues` row (`WorldAudioCue`) naming an event token and a `patches` row; `WorldAudioDirector.SubmitCue` | [audio reference](../../../docs/reference/audio.md) |
| A rule fires a sound, pose, or score condition | `WorldRuleDisclosure` classifies the rule's dependencies from each fact's own `IWorldDisclosedFact`, `WorldTick.PresentCues` (or `PresentLocalCues`, per local seat) admits each cue against the recipient view, and the delivered snapshot drives `WorldCreationInstances.TriggerCue` and the listener's `MusicDirector` | [delivered rule cues](../../../docs/reference/audio.md#delivered-rule-cues) |
| A synthesized instrument voice | a `puck.synthesizer-patch.v1` document, crossed into `VoicePatch` by `WorldVoicePatchFactory.FromDocument`, played by `VoiceSynth` | [World audio README](../../../src/Puck.World/Audio/README.md#document-intake-worldvoicepatchfactorycs) |
| Background music that changes with play: segments, layers, embellishments, a beat clock | `music` rows (`WorldMusicRow`): the authority runs only the `MusicClock` and delivers each tick's boundary (an engaged instrument's beat folded in) and disclosed senses with its cues; each listener compiles the score with `MusicDirectorFactory` into its own `MusicDirector` (`WorldAudioDirector.PresentDeliveredCues`). A rule drives it with `emitCue` and a score's `when: "cue:<name>"`: a transition arms on the cue, a layer plays on the ticks the cue is delivered (a `Level` rule holds it) and joins on its authored `at` grid point (beat or bar; none joins at once), an embellishment fires on it. `music.state` reads the listener's score beside the authority's clock. The press's score (`worlds/debug/score.music.json`) is the live example | [audio reference](../../../docs/reference/audio.md#delivered-rule-cues) |
| What the mixer was last handed: emitters in the mix, triggers, live cues, whether a mixer is attached | `audio.mix` (`WorldAudioDirector.TrySnapshot`, `LiveCueCount`, `MixerAttached`) | [audio reference](../../../docs/reference/audio.md#verifying) |
| A graded press or a phrase on the beat | the standard's `rhythmJudge` (`worlds/standard/rhythm.puck`): authored rules over the clock operands below, with windows, grades and a phrase as data | [rhythm judge](../../../worlds/standard/README.md) |
| A rhythm hit window | a range over a `$clock:<music>` operand; no dedicated grader. `phaseError` is the integer tick distance to the nearest beat at the clock's current position, and `phaseErrorAt:<owner>:<channel>:<kind>:<occurrence>` is the fixed-point seconds distance from a press, at its captured time and calibration, to the nearest beat. `beat`, `bar` and `beatInBar` read the current position's indices, and `beatAt`, `barAt` and `beatInBarAt` read a press's nearest beat | [audio reference](../../../docs/reference/audio.md#clock-operands) |
| A tune or a playable instrument | `tunes` rows (`WorldTune`, `puck.tune.v1`): `TuneMachineSource` for a passive tune, `TuneInstrumentEngine` for an engageable screen machine whose tempo folds into the music clock through `WorldServer.InstrumentClockBoundary` | [World audio README](../../../src/Puck.World/Audio/README.md#the-diegetic-instrument-puckhumblegamingbrickforgetunetuneinstrumentenginetuneinstrumentmachine) |
| An identity that babbles in syllables | `WorldIdentityDefinition.Voice` → `WorldAudioDirector.TriggerBabble` → `VoiceBabbler.ComputeTriggerTicks` | [audio reference](../../../docs/reference/audio.md) |
| A HUD element or sign that reads its text aloud | a HUD `Text` element's `voice` (`patchId` or `sampleSet`), observed by `WorldHudSpeechFeed`, played by `TextSpeechSource` | [text speech](../../../docs/reference/audio.md#text-speech), [samples](../../../docs/reference/audio.md#authored-syllable-samples) |
| A WAV of an utterance without a device | `audio.render <panelId> <elementId> <output.wav>` through `WorldSpeechRenderer` | [text speech](../../../docs/reference/audio.md#text-speech) |
| Speaker gain bound to state | the shared bindable scalar grammar, resolved through the state mirror each publication | [speaker gain](../../../docs/reference/audio.md#speaker-gain) |
| The output device, its faults and rebinds | `WorldAudioRenderService` over `IAudioRenderDeviceFactory` (Windows: `WasapiAudioRenderDeviceFactory`) | [World audio README](../../../src/Puck.World/Audio/README.md#the-device-worldaudiorenderservicecs) |
| A gameplay clip with game audio and microphone | `capture.start/status/stop` (`WorldRecordingCommandModule`) or `--recording`, loading a `RecordingDocument` and arming a `RecordingSession` on the host's `FrameCaptureController` | [recording](../../../docs/reference/recording.md#how-a-session-is-assembled) |
| A run of presented frames kept as images when the world says so (a best score, a finish) | `highlights` rows (`WorldHighlightRow`: a signal, a frame count, a delay) → `WorldHighlightDirector` arms `CaptureSink` on the `FrameCaptureController`; by hand, `capture.start frames <name> [<count>]` | [frame capture](../../../docs/reference/recording.md#frame-capture-and-overlays) |
| One exact still for evidence | `world.screenshot`, or a tick-scheduled `captures` station (`puck-world` console); neither goes through `CaptureSink` | [console](../puck-world/references/console.md) |
| Text, boxes or a timecode burnt into the recording only | `OverlayCompositor` over the document's overlay rows | [frame capture](../../../docs/reference/recording.md#frame-capture-and-overlays) |
| A container, codec or track question | `MatroskaMuxer` and `EbmlWriter`; `OpusAudioLane`, `OpusStreamEncoder`, `LinearResampler`; `Av1TemporalDelimiterFilter` | [muxing and codecs](../../../docs/reference/recording.md#muxing-and-codecs) |
| A deterministic re-run of a session | `replay.*` and the replay tape (`puck-world`), not a recording | [replay](../puck-world/references/replay.md) |

## Contracts that bite

- **The score is the listener's; the clock is the authority's.** There is one
  `MusicDirector` per listener and none on the authority: the audio director
  steps it from each delivered tick (`WorldAudioDirector.PresentLocalCues`,
  `PresentRoutedAudio`) on the cues and senses that listener's seat was told,
  so a remote listener hears what a local one does and a cue a seat may not be
  told never moves its music. The authority owns the `MusicClock` (rules read
  it through `clock(...)`, it is checkpointed and hashed) and delivers the
  boundary it crossed. The server calls out to no audio code: a new music event
  is sounded by teaching that delivered path, never by a callback from the tick.
- **Sound decides nothing.** The mixer, synth, emitter table and score are
  presentation: no simulation read depends on them. `MusicClock` and
  `VoiceBabbler` are the exception, simulation state stepped by the server; they
  never read the wall clock and their seeds fold identity, ordinal and index
  only.
- **The document crosses in one place.** `Puck.Audio` references
  `Puck.Abstractions`, `Puck.Assets`, `Puck.Commands`, `Puck.Hosting` and
  `Puck.Maths` exactly (the architecture gate's closure). A patch becomes a
  `VoicePatch` only through `WorldVoicePatchFactory`.
- **Plays silent, never crashes.** A failed endpoint parks the pump, detaches
  the mixer and retries; a host with no backend (Linux, headless) reports
  `device=unsupported` and machines synthesize at rate zero
  (`MachineAudioRate`).
- **Speech is a function of text and voice.** `TextSpeechSource` schedules
  characters at exact audio-frame boundaries with no wall clock, frame delta
  or history, so two exports of the same text and voice are byte-identical.
- **Capture is a product capability (owner ruling).** Keep the
  `capture.*` surface, `--recording`, the document format, the Windows encoder
  ladder and loopback and microphone capture, and the Linux factories, even
  with no current world caller ([puck-world](../puck-world/SKILL.md#contracts-that-bite)).
  Headless Worlds do not compose the capture verbs.
- **A factory declines with a reason, never throws.** `RecordingSession.TryCreate`
  opens only what the machine can encode and capture and fails whole when
  neither a video encoder nor an audio lane resolves.
- **Capture never blocks rendering.** The render thread copies into a free
  `FrameSlotQueue` slot; a full queue drops the newest frame and counts it.
- **Choose the clock deliberately.** `RecordingClock.Wall` (the default) stamps
  from the wall clock; `RecordingClock.Sim` stamps frames from the tick clock
  for a deterministic offline re-render and forbids audio rows.
- **Container bytes are deterministic** for the same tracks and blocks;
  the live file is crash-safe through a `Void` reservation that a clean
  `Stop` replaces with a `SeekHead`.

## Where each contract is enforced

| Contract | Enforced by |
|---|---|
| `Puck.Audio`'s exact dependency closure | `puck architecture` (`build/Architecture.props`) |
| One document boundary for patches | `WorldVoicePatchFactory.FromDocument`, the only converter |
| A malformed recording document is never half-accepted | `RecordingDocumentValidator`, run by `RecordingDocumentSerialization.TryLoad` |
| Every Matroska element is written one way | `EbmlWriter`'s typed helpers |
| A crash leaves a playable prefix | the `Void` reservation in `MatroskaMuxer`; `MatroskaSeekHeadRecoveryLawTests` |
| Sim-clock sessions carry no audio | `RecordingDocumentValidator`, which refuses audio rows under `RecordingClock.Sim` |

## Open gaps

- **No Linux backends.** No audio render, video encoder or audio capture on
  Linux; the factories decline by name.
- **A babbling identity has no world position.** Every syllable, like every
  embellishment, voices listener-placed.
- **Music embellishment `gainThousandths` does not reach presentation gain**
  (`MusicEmbellishmentDocument.GainThousandths`); a layer's does, at its bed
  emitter.
- **Nothing proves a region crossing's `music.transition` cue end to end.**
- **A listener's score is a function of its delivery history.** A recipient
  that joins mid-run, a routed view whose span is cut, or a history seek starts
  or keeps a score that no delivered tick re-derives: it rests on the first
  segment until a cue moves it (a `Level`-held layer recovers at once, a
  segment does not). Priming a recipient means the authority holding each
  recipient's score, admitted per view, and delivering it in the primer.
- **A layer's tune starts on the grid tick, not phase-locked to the clock.**
  A layer joins on its authored beat or bar (`MusicLayer.At`) and its tune host
  starts from its head when the delivered tick reconciles, so it shares the
  grid within presentation latency; a tune's own tempo is authored to match the
  score, and nothing re-aligns a tune that drifts or starts on a sample frame.
- **Highlights and `capture.start frames` are unproven on a window**: the
  press's row has not been watched writing a file.
- **`LinearResampler` is linear**, not polyphase or anti-aliased.
- **AV1 OBU framing has one home.** `Av1Obu.TryRead` (`Puck.Abstractions`)
  frames a header, extension and size and refuses a set forbidden bit;
  `Av1Bitstream` and `Av1TemporalDelimiterFilter` both walk through it.
- The references' and README's canaries (`voice-babble`,
  `music-conditional-layer-and-embellishment`, `instrument-clock-source`) are
  quarantined under `experimental/`.

## Verify

- Unit laws: `tests/Puck.Audio.Tests` (mixer, synth, `MusicClock`,
  `MusicDirector`, `VoiceBabbler`), `tests/Puck.Recording.Tests`.
- Headless speech: boot the debug world and run the reference's
  `audio.render` recipe ([text speech](../../../docs/reference/audio.md#text-speech))
  twice; two exports of unchanged text and voice are byte-identical. The guide
  and the map sign in `worlds/debug/guide.puck` are the live examples.
- Live sound needs a windowed World with an audio device, which is a GPU leg
  (`verification`): read `audio.state` (device, frames, faults, `peak`),
  `audio.emitters`, `audio.mix`, `speaker.state` (including `lastCue:<token>`)
  and `voice.state` over stdin. A headless World composes none of them.
- The score needs no device: `music.state` and `instrument.state`
  (`WorldMusicCommandModule`) answer in a headless World, and
  `WorldDeliveredScoreLawTests` steps the press's score through
  `WorldAudioDirector.PresentLocalCues` on a real clock.
- A clip: `capture.start`, `capture.status`, `capture.stop` on a windowed
  World, then inspect the file; a lane that declined reports its reason
  rather than failing the session.

## Look-alikes

- `replay.*` records inputs for deterministic re-simulation; `capture.*`
  records pixels and sound. Neither substitutes for the other.
- `world.screenshot` and `world.captures` (scheduled captures in a test) are
  `puck-world` console verbs over the same frame-capture controller.
- A machine's own audio (an emulator's APU) belongs to `gaming-bricks`; the
  mixer only binds its output to a speaker.
- Camera and desktop capture feeds that a screen shows are `platform`
  capture services, not recording.

## Route adjacent work

| Skill | Route there for |
|---|---|
| `puck-world` | `speakers`, `audio.cues`, `music`, `tunes`, `patches` and HUD rows, console verbs, booting and driving a World. |
| `platform` | The WASAPI render device, the Media Foundation encoder ladder, loopback and microphone capture, camera and desktop capture. |
| `gaming-bricks` | An emulated machine's sound hardware and the tune cartridge's core. |
| `rom-forge` | Authoring the `puck.tune.v1` jukebox cartridge chain. |
| `maths-usage` | Fixed-point gains, seeded streams and the music clock's arithmetic. |
| `verification` | GPU legs for windowed Worlds, the private CLI copy. |
