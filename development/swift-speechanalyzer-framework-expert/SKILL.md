---
name: SpeechAnalyzer Framework Expert
description: Implement, migrate, debug, and review on-device transcription with Apple SpeechAnalyzer, SpeechTranscriber, DictationTranscriber, AssetInventory, AnalyzerInput, live microphone audio, and audio-file analysis on iOS 26, macOS 26, visionOS 26, and tvOS 26 where supported. Use for SpeechAnalyzer setup, locale assets and reservations, volatile/final results, AttributedString transcripts, audio conversion, permissions, lifecycle, and migration from SFSpeechRecognizer or Whisper-based solutions. Do not invent beta or later-SDK APIs, assume locale/device support, iterate Foundation Progress as an AsyncSequence, or use SpeechAnalyzer on watchOS.
---

# SpeechAnalyzer Framework

Use the API surface in the project’s installed SDK. This guide is compatibility-first for the stable Xcode 26.6 / iOS 26.5 SDK and does not substitute later beta conveniences into a 26-target implementation.

## Compatibility baseline

- `SpeechAnalyzer`, `SpeechTranscriber`, `AssetInventory`, and `AnalyzerInput` require iOS 26, macOS 26, visionOS 26, or tvOS 26. They are unavailable on watchOS.
- `DictationTranscriber` is available on iOS 26, macOS 26, and visionOS 26, but not tvOS/watchOS.
- Build these APIs with Xcode 26 or newer. A lower deployment target requires an availability gate and a legacy or disabled-feature path.
- `SpeechTranscriber.isAvailable` is hardware-sensitive. An OS version check alone is insufficient.
- The live microphone example is iOS-only because it configures `AVAudioSession` and requests record permission.
- If an SDK 27 beta offers helpers such as capture/input providers or converter types, keep those declarations in a beta-SDK-only source path, add the relevant `#available(iOS 27, macOS 27, ...)` runtime gate, and retain the 26 implementation. A stable 26 compiler cannot resolve an unknown symbol merely because it appears inside `#available`.

Do not hardcode a language count. Query locale support on the running device.

## Stable setup sequence

1. Check `SpeechTranscriber.isAvailable`.
2. Resolve user input with `SpeechTranscriber.supportedLocale(equivalentTo:)`; exact `Locale` equality can reject a usable regional equivalent.
3. Reserve the resolved locale with `AssetInventory.reserve(locale:)` when the app owns that reservation.
4. Create a transcriber for the resolved locale.
5. Obtain `AssetInventory.assetInstallationRequest(supporting:)` and await `downloadAndInstall()` when it returns a request.
6. Guard the optional result of `SpeechAnalyzer.bestAvailableAudioFormat(compatibleWith:)` before installing an audio path.
7. Create `SpeechAnalyzer`, supply `AnalyzerInput` values, and consume `transcriber.results` in tracked structured work.
8. End input and await an analyzer finish method. Finishing an `AsyncStream` alone does not finish analysis.
9. Await the result consumer, then release only the locale reservation this operation created.

There is no `SpeechTranscriber.allocate(locale:)` in the stable 26 SDK. Locale reservation is an `AssetInventory` responsibility.

Read [examples/basic_setup.swift](examples/basic_setup.swift) for a scoped preparation helper that releases its reservation on success and failure.

## Assets and progress

`AssetInventory.reserve(locale:)` returns `true` when it created a new app reservation and `false` when that locale was already reserved. Release only reservations the current owner created; do not tear down another feature’s reservation. Respect `maximumReservedLocales` and expose an explicit release action.

`AssetInstallationRequest` conforms to `ProgressReporting`. Its `progress` property is Foundation `Progress`, not an `AsyncSequence`. Pass the object to UI/observation code or inspect `fractionCompleted`; never write `for try await` over it.

Read [examples/locale_manager.swift](examples/locale_manager.swift) for equivalence lookup, explicit reservation ownership, installation, Foundation Progress handoff, and release.

## Results

The element type is `SpeechTranscriber.Result`. Use:

- `result.text` for the most likely `AttributedString`;
- `String(result.text.characters)` when plain text is required;
- `result.alternatives` only when alternative reporting was configured;
- `result.isFinal` to distinguish final from volatile output;
- `result.range` and configured attributes when reconciling time-indexed text.

There is no `SpeechTranscriptionResult` type and no `result.transcription` property in the stable 26 SDK.

When volatile reporting is enabled, replace the current volatile segment rather than repeatedly appending it. Append finalized text once. For editors that can receive overlapping ranges, reconcile by `result.range` instead of assuming a single volatile phrase.

Read [examples/error_handling.swift](examples/error_handling.swift) for typed validation errors and correct result accumulation.

## Lifecycle and concurrency

- Store any unstructured result-consumer task and cancel/await it during teardown. Prefer `async let` or a task group for finite file transcription.
- After ending input, call `finalizeAndFinishThroughEndOfInput()` to drain and finalize, or `cancelAndFinishNow()` when results are no longer needed.
- Propagate setup and finite-analysis errors to the awaiting caller. Surface later live-stream failures through explicit state/callbacks rather than throwing inside an unobserved task.
- Guard concurrent starts while permission prompts or model installation are pending.
- Keep audio callbacks away from `MainActor` state. Capture a dedicated synchronized feeder and hop to the main actor only for UI/error delivery.
- Do not mark AVFoundation types `@unchecked Sendable` without a concrete synchronization/ownership invariant.

## Live microphone transcription

An iOS host app needs both:

- `NSSpeechRecognitionUsageDescription`
- `NSMicrophoneUsageDescription`

Request speech and microphone authorization before starting the engine. Configure and activate the app’s `AVAudioSession` according to the broader audio policy; the sample owns a record-only measurement session and deactivates it on stop. Apps that mix playback, calls, or other recorders need a central session coordinator.

Install the tap only after obtaining a nonoptional analyzer format. Remove the tap, stop the engine, finish input, finalize/cancel the analyzer, await the result task, deactivate the session, and release the owned reservation on every stop/failure path.

Read these two files together:

- [examples/live_transcription.swift](examples/live_transcription.swift): permissions, audio session, engine, tracked task, finalization, and reservation lifecycle.
- [examples/buffer_converter.swift](examples/buffer_converter.swift): synchronized converter recreation when either input or output format changes.

The sample feeder performs bounded conversion in the audio tap and never touches UI-isolated state. Profile this path on supported devices. A production recorder with stricter real-time requirements should use a preallocated/ring-buffer architecture appropriate to its latency budget.

## Audio-file transcription

File analysis does not need microphone permission or an iOS audio session. Prepare assets, open `AVAudioFile`, start analysis with `finishAfterFile: true`, and consume results with structured concurrency.

Read [examples/file_transcription.swift](examples/file_transcription.swift). Invoke it inside `withPreparedSpeechTranscriber` from the basic example so reservation ownership stays scoped.

## Fallback and migration

- If `SpeechTranscriber.isAvailable` is false, disable the feature or evaluate `DictationTranscriber` on supported platforms and query its locale support separately.
- Keep `SFSpeechRecognizer` only behind a deliberate lower-OS or feature-gap adapter; its authorization, request, result, and network behavior differ.
- Treat migration from Whisper as a product decision: verify supported locale, device hardware, offline behavior, timestamps, custom vocabulary, model/storage policy, latency, and quality on representative audio.
- Out-of-process models reduce model memory in the app process; they do not eliminate the app’s memory limits or the cost of buffers, transcript state, and tasks.

## Review checklist

- Deployment target, SDK, device availability, and locale equivalence are checked.
- Only stable installed APIs are used on the 26 path.
- A created reservation is released; an existing shared reservation is preserved.
- `Progress` is observed as Foundation Progress.
- Optional audio format is guarded.
- Results use `SpeechTranscriber.Result.text` and preserve `AttributedString` when useful.
- Input finish is followed by analyzer finalization/cancellation.
- Result work is stored or structured and all errors have an owner.
- Live capture includes usage descriptions, permission requests, session activation/deactivation, tap removal, and repeated-start protection.
- Audio conversion handles route/input-format changes and does not access main-actor UI state from the tap.

## Supporting material

- [README.md](README.md) summarizes platforms and integration requirements.
- [examples/basic_setup.swift](examples/basic_setup.swift) scopes model preparation and reservation release.
- [examples/locale_manager.swift](examples/locale_manager.swift) manages locale assets and Progress.
- [examples/error_handling.swift](examples/error_handling.swift) handles results and validation failures.
- [examples/file_transcription.swift](examples/file_transcription.swift) performs finite file analysis.
- [examples/live_transcription.swift](examples/live_transcription.swift) and [examples/buffer_converter.swift](examples/buffer_converter.swift) form the live iOS example.
- [examples/prompts.md](examples/prompts.md) contains representative activation prompts.
