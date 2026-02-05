---
name: court-record-transcriber
description: |
  Development skill for CaseMark's Court Recording Transcriber - an AI-powered 
  application for transcribing court recordings with speaker identification, 
  synchronized playback, search, and legal document exports. Built with Next.js 16, 
  PostgreSQL, Drizzle ORM, wavesurfer.js, and Case.dev APIs. Use this skill when: 
  (1) Working on or extending the court-record-transcriber codebase, (2) Integrating 
  with Case.dev transcription APIs, (3) Working with audio playback/waveforms, 
  (4) Building transcript export features, or (5) Adding speaker identification logic.
---

# Court Recording Transcriber Development Guide

An AI-powered application for transcribing court recordings with speaker identification, synchronized playback, search functionality, and professional legal document exports.

**Live site**: https://court-record-transcriber.casedev.app

## Architecture

```
src/
├── app/
│   ├── api/recordings/         # API routes for recordings
│   │   ├── route.ts            # List, create recordings
│   │   └── [id]/
│   │       ├── route.ts        # Get, update, delete
│   │       ├── transcribe/     # Start transcription
│   │       └── export/         # Export endpoints
│   ├── upload/                 # Upload page
│   └── recording/[id]/         # Transcript viewer page
├── components/
│   ├── ui/                     # shadcn/ui components
│   ├── AudioPlayer.tsx         # Waveform + playback
│   ├── TranscriptView.tsx      # Transcript display
│   ├── SpeakerEditor.tsx       # Label speakers
│   └── ExportDialog.tsx        # Export options
└── lib/
    ├── db/
    │   ├── index.ts            # Database connection
    │   └── schema.ts           # Drizzle schema
    ├── casedev/                # Case.dev API client
    └── legal-vocabulary.ts     # Word boosting config
```

## Core Workflow

```
Upload Audio → Transcribe → Identify Speakers → Review/Edit → Export
     ↓             ↓              ↓                ↓            ↓
  MP3/WAV     Case.dev API    Auto-detect      Sync playback   PDF/Word/
  M4A/etc     with legal      Judge, Atty,    click-to-seek   Plain text
              vocabulary      Witness, etc
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, React 19, Tailwind CSS |
| Backend | Next.js API Routes |
| Database | PostgreSQL + Drizzle ORM |
| Audio | wavesurfer.js |
| Transcription | Case.dev Speech-to-Text API |
| Export | React PDF, docx library |

## Key Features

| Feature | Description |
|---------|-------------|
| Audio Upload | Drag-drop MP3, WAV, M4A, FLAC, OGG |
| AI Transcription | Case.dev API with legal vocabulary boosting |
| Speaker ID | Auto-detect speakers, customizable labels |
| Synced Playback | Click transcript line to jump to timestamp |
| Search | Find words/phrases with highlighting |
| Export | PDF, Word (.docx), plain text with legal formatting |

## Database Operations

PostgreSQL with Drizzle ORM. See [references/database-schema.md](references/database-schema.md).

### Commands
```bash
npm run db:push      # Push schema (dev)
npm run db:generate  # Generate migrations
npm run db:studio    # Open Drizzle Studio
```

### Core Tables
- **recordings**: id, filename, duration, status, audioUrl
- **transcripts**: id, recordingId, content (JSON), speakerMap
- **utterances**: id, transcriptId, speaker, text, startTime, endTime

## Case.dev Integration

See [references/casedev-transcription-api.md](references/casedev-transcription-api.md) for API patterns.

### Transcription Flow
```typescript
// 1. Upload audio to Case.dev
const { audioId } = await uploadAudio(file);

// 2. Start transcription with legal vocabulary
const { jobId } = await startTranscription(audioId, {
  vocabulary: legalVocabulary,
  speakerDiarization: true,
});

// 3. Poll for completion
const transcript = await pollTranscriptionStatus(jobId);

// 4. Store results
await saveTranscript(recordingId, transcript);
```

## Audio Playback

See [references/audio-playback.md](references/audio-playback.md) for wavesurfer.js patterns.

### Key Features
- Waveform visualization
- Click-to-seek from transcript
- Playback speed control
- Keyboard shortcuts (space, arrows)

## Development

### Setup
```bash
npm install
cp .env.example .env.local
# Add CASEDEV_API_KEY and DATABASE_URL
npm run db:push
npm run dev
```

### Environment
```
CASEDEV_API_KEY=sk_case_...       # Case.dev API key
DATABASE_URL=postgresql://...     # PostgreSQL connection
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Common Tasks

### Adding a New Export Format
1. Create export function in `lib/export/`
2. Add endpoint in `app/api/recordings/[id]/export/`
3. Add option to `ExportDialog.tsx`

### Customizing Speaker Labels
```typescript
// Default labels
const speakerLabels = ['Judge', 'Plaintiff Attorney', 'Defense Attorney', 
                       'Witness', 'Clerk', 'Unknown'];

// In SpeakerEditor component, allow custom labels
```

### Adding Legal Vocabulary
```typescript
// lib/legal-vocabulary.ts
export const legalVocabulary = [
  'objection', 'sustained', 'overruled', 'plaintiff', 'defendant',
  'voir dire', 'habeas corpus', 'pro bono', 'amicus curiae',
  // Add more terms
];
```

## Export Formats

| Format | Use Case |
|--------|----------|
| PDF | Official court filing, archive |
| Word (.docx) | Editing, annotations |
| Plain Text | Processing, search indexing |
| SRT | Subtitles for video recordings |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Transcription stuck | Check Case.dev API status, verify audio format |
| Audio won't play | Verify audio URL accessible, check CORS |
| Speaker labels wrong | Use SpeakerEditor to reassign |
| Export fails | Check transcript exists, verify format support |
| Waveform not showing | Ensure wavesurfer.js loaded, check audio src |
