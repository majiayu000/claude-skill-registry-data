---
name: transcript-edit
description: Edit video by editing its transcript text. Supports multi-provider transcription (Whisper/Deepgram/AssemblyAI) and text-based cutting.
---

## Purpose

Enable Descript-style text-based video editing where users edit a transcript and the timeline automatically adjusts. Transcribe audio/video with word-level timestamps, display the transcript with speaker colors and frame mappings, and support operations like deleting text (removes corresponding frames), rearranging paragraphs (reorders dialogue lines), and modifying text (triggers voice regeneration).

## Steps

1. **Transcribe audio/video.** Call `transcribeAudio(file, options)` from `whisperTranscript.ts`. Options:
   - `provider`: 'whisper' (default), 'deepgram', or 'assemblyai'
   - `language`: language code (e.g., 'en', 'es')
   - `diarize`: enable speaker diarization (boolean)
   - `model`: specific model name
   - Posts to `/api/whisper/transcribe` with the audio file as FormData
   - Returns `WhisperResult` with `text`, `language`, `duration`, `segments[]`, `words[]`

2. **Build the transcript model.** Two approaches:

   **Simple transcript** (`transcriptSync.ts`): Call `buildTranscript()` which reads `useMultiCharacterStore` dialogue lines and returns `TranscriptLine[]` with `lineId`, `characterId`, `characterName`, `text`, `startFrame`, `endFrame`, `emotion`, `color` (per-character color from a 6-color palette).

   **Word-level transcript** (`transcriptEditor.ts`): Call `buildTranscript(dialogueLines, generatedVoices)` which maps word-level alignment data to frames, returning `TranscriptLine[]` with individual `TranscriptWord` entries containing `text`, `startFrame`, `endFrame`, `lineIndex`, `characterName`, `wordIndex`.

3. **Edit operations.** Use functions from `transcriptEditorOps.ts`:

   **Delete selected text**: `deleteSelectedText(lineId, charStart, charEnd)`
   - Removes text from the dialogue line script
   - Estimates frame reduction proportional to deleted text fraction
   - Shifts all subsequent dialogue lines earlier by the removed frame count
   - Reduces total timeline duration

   **Rearrange paragraphs**: `rearrangeParagraphs(fromLineId, afterLineId)`
   - Moves a dialogue line to a new position in the timeline ordering
   - Rebuilds all frame positions sequentially (zero-gap packing)
   - Updates total timeline frames

   **Change character**: `changeCharacterForParagraph(lineId, newCharacterId)` (not shown in snippet but follows the same pattern -- reassigns a dialogue line to a different character)

   **Update line text**: `updateLineText(lineId, newText)` from `transcriptSync.ts`
   - Updates the dialogue line script text
   - Triggers voice regeneration for the modified line

   **Delete line**: `deleteLineAndClose(lineId)` from `transcriptSync.ts`
   - Removes the dialogue line entirely
   - Shifts subsequent lines to close the frame gap
   - Reduces total timeline duration

4. **Sync to timeline.** The transcript editor maintains bidirectional sync:
   - Text changes propagate to `useMultiCharacterStore` dialogue lines
   - Frame changes propagate back to transcript display
   - Word-level click-to-seek: clicking a word in the transcript seeks to its `startFrame`

5. **Import transcribed segments as dialogue.** Use `segmentsToDialogueLines(segments, fps)` from `whisperTranscript.ts` to convert `WhisperSegment[]` into dialogue line objects compatible with `useMultiCharacterStore`. Each segment becomes a line with `script`, `startFrame`, `endFrame`, and `emotion: 'Auto'`.

## Key Files

- `src/services/whisperTranscript.ts` -- transcribeAudio(), transcribeFromUrl(), segmentsToDialogueLines(), WhisperResult, WhisperWord, WhisperSegment types, detectSilences(), detectFillers()
- `src/services/transcriptEditor.ts` -- buildTranscript() (word-level), TranscriptWord, TranscriptLine types, Slate.js integration
- `src/services/transcriptEditorOps.ts` -- deleteSelectedText(), rearrangeParagraphs(), high-level editing operations
- `src/services/transcriptSync.ts` -- buildTranscript() (simple), updateLineText(), deleteLineAndClose(), TranscriptLine type
- `src/stores/useTranscriptStore.ts` -- Transcription state
- `src/stores/useTranscriptImportStore.ts` -- Transcript import state
- `src/components/panels/TranscriptPanel.tsx` -- Transcript display panel
- `src/components/panels/TranscriptEditor.tsx` -- Slate.js-based transcript editor
- `src/components/panels/TranscriptEditorPanel.tsx` -- Transcript editor panel wrapper
- `server/routes/whisper.ts` -- Server-side transcription endpoint

## Common Issues

- **No word-level timestamps**: Some providers or languages may return segment-level only. The word-level transcript falls back gracefully, but text-based cutting precision is reduced.
- **Frame estimation on delete**: When deleting text, frame reduction is estimated proportionally (deleted characters / total characters * frame duration). This is approximate -- for precise editing, regenerate the voice after text changes.
- **Voice regeneration needed**: After modifying transcript text, the corresponding voice audio is stale. Flag the line for regeneration via the voice store.
- **Diarization support**: Speaker diarization (identifying who spoke) requires `diarize: true` in options. Not all providers support it. Deepgram and AssemblyAI have better diarization than Whisper.
- **Credit gating**: `transcribeAudio()` and `transcribeFromUrl()` are wrapped in `withCreditGate('whisper-transcript', ...)`.
- **Large files**: The audio file is uploaded to the server as FormData. Very large files may timeout. Consider chunking or using `transcribeFromUrl()` with a pre-uploaded URL.

## Examples

```typescript
// Transcribe a video file
import { transcribeAudio, segmentsToDialogueLines } from '@/services/whisperTranscript'

const result = await transcribeAudio(videoFile, {
  provider: 'whisper',
  language: 'en',
  diarize: true,
})

// Import as dialogue lines
const lines = segmentsToDialogueLines(result.segments, 30)

// Build editable transcript from existing dialogue
import { buildTranscript } from '@/services/transcriptSync'
const transcript = buildTranscript() // reads from useMultiCharacterStore

// Delete text and adjust timeline
import { deleteSelectedText } from '@/services/transcriptEditorOps'
deleteSelectedText('line-1', 10, 25) // remove characters 10-25

// Rearrange dialogue order
import { rearrangeParagraphs } from '@/services/transcriptEditorOps'
rearrangeParagraphs('line-3', 'line-1') // move line-3 after line-1

// Update text (triggers regeneration need)
import { updateLineText } from '@/services/transcriptSync'
updateLineText('line-1', 'Updated script text here')
```
