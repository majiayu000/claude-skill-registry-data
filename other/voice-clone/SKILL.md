---
name: voice-clone
description: Clone a voice for use in TTS generation. Covers voice sample upload, cloning workflow, and integration with ElevenLabs.
---

## Purpose

Clone a custom voice from audio samples using ElevenLabs, then use it for TTS generation throughout the app. The cloned voice appears in the voice library alongside built-in voices and can be selected for any character dialogue.

## Steps

1. **Collect audio samples.** The user uploads audio files through the drag-and-drop zone in `VoiceClonePanel.tsx`. Requirements:
   - Supported formats: WAV, MP3, M4A, WebM, OGG (checked by extension regex)
   - Max 25 files total (`MAX_FILES`)
   - Max 10MB per file (`MAX_FILE_SIZE`)
   - Minimum 60 seconds total duration recommended (`MIN_TOTAL_DURATION`)
   - 5+ minutes total duration is ideal for best quality

2. **Validate samples.** The panel automatically decodes each file using `AudioContext.decodeAudioData()` to measure duration. A quality indicator bar shows:
   - Red: under 60s total duration
   - Yellow: 60s-300s (meets minimum but not ideal)
   - Green: 300s+ (good quality expected)
   - Warnings for oversized files or unsupported formats

3. **Provide voice metadata.** The user enters:
   - **Voice Name** (required): A label for the cloned voice
   - **Description** (optional): Characteristics of the voice

4. **Submit clone request.** Call `getElevenLabsService().cloneVoice(name, description, files)` which:
   - Builds a `FormData` with name, description, and all audio files
   - Posts to `/api/proxy/elevenlabs/voices/add` (server-side proxy to avoid CORS)
   - Returns `{ voice_id: string }` on success

5. **Preview the cloned voice.** After successful cloning, the panel offers a preview button that generates speech for the phrase "Hello, this is my cloned voice. How does it sound?" using the new voice ID via `getElevenLabsService().generateSpeech()`.

6. **Use the cloned voice.** The cloned voice becomes available in `useVoiceStore.clonedVoices` and can be selected like any built-in voice for dialogue generation. Use it with `generateWithAlignment()` by passing the new `voice_id`.

7. **Delete a cloned voice.** Call `getElevenLabsService().deleteVoice(voiceId)` which sends a DELETE to `/api/proxy/elevenlabs/voices/{voiceId}`. The voice is removed from both ElevenLabs and the local store.

## Key Files

- `src/components/panels/VoiceClonePanel.tsx` -- Full voice cloning UI with upload, quality indicator, metadata form, progress, preview
- `src/services/elevenlabs.ts` -- `cloneVoice(name, description, files)`, `deleteVoice(voiceId)`, `generateSpeech(text, voiceId)`
- `src/stores/useVoiceStore.ts` -- `clonedVoices` array, `isCloning` flag, `cloneError` state, `cloneVoice()` action, `deleteClonedVoice()` action
- `src/components/ui/AudioSampleCard.tsx` -- Individual audio sample display card
- `src/components/credits/CreditCostTag.tsx` -- Credit cost indicator for the clone operation

## Common Issues

- **Insufficient sample duration**: Voice quality degrades significantly below 60 seconds. The UI warns but does not block cloning. Recommend at least 1 minute, ideally 5 minutes.
- **File size limits**: Individual files over 10MB may be rejected by ElevenLabs. The panel warns but does not prevent upload.
- **Server proxy required**: Voice cloning goes through `/api/proxy/elevenlabs/voices/add` to inject the API key server-side and avoid exposing it in the browser.
- **Credit cost**: Voice cloning consumes credits. The `CreditCostTag` component shows the cost. Check with `creditGate` before proceeding.
- **Cloning takes time**: The ElevenLabs API processes samples asynchronously. The UI shows a loading spinner during the operation.

## Examples

```typescript
// Clone a voice
const service = getElevenLabsService()
const result = await service.cloneVoice(
  'My Custom Voice',
  'Warm male voice with slight British accent',
  [file1, file2, file3] // File objects from input
)
console.log('New voice ID:', result.voice_id)

// Use the cloned voice for TTS
const { audioUrl, alignment } = await service.generateWithAlignment(
  'Hello world, this is my cloned voice!',
  result.voice_id,
  { stability: 0.5, similarityBoost: 0.75 }
)

// Delete the voice
await service.deleteVoice(result.voice_id)
```
