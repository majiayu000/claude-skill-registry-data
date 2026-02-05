---
name: speech-recognition
description: iOS speech recognition implementation using @react-native-voice/voice. Use when debugging transcription issues, modifying session handling, or understanding the accumulated text tracking mechanism.
---

# Speech Recognition Implementation

## Overview

The `useSpeechRecognition` hook in `mobile/src/hooks/useSpeechRecognition.ts` handles real-time Japanese speech recognition on iOS.

## Key Concepts

### iOS Voice API Behavior

- `@react-native-voice/voice` wraps iOS Speech Framework
- **Accumulated text**: iOS returns ALL text since `Voice.start()`, not just new words
- `onSpeechEnd` fires when iOS decides speech is complete (unpredictable timing)
- No native "continuous" mode - must manually restart

### Session Management

```
┌─────────────────────────────────────────────────────┐
│  Voice.start()                                      │
│       ↓                                             │
│  onSpeechPartialResults → Update current session    │
│       ↓                                             │
│  [2 sec silence] → Finalize session, track length   │
│       ↓                                             │
│  New speech → Extract only NEW text (subtract old)  │
│       ↓                                             │
│  onSpeechEnd → Reset counter, restart Voice         │
└─────────────────────────────────────────────────────┘
```

## Critical Implementation Details

### 1. Accumulated Text Tracking

```typescript
const lastFinalizedTextLengthRef = useRef(0);

// When session finalizes (silence detected)
lastFinalizedTextLengthRef.current += current.text.length;

// Extract new text from accumulated result
const extractNewText = (fullText: string): string => {
  if (lastFinalizedTextLengthRef.current === 0) return fullText;
  return fullText.substring(lastFinalizedTextLengthRef.current).trim();
};
```

### 2. Silence Detection

```typescript
const SILENCE_TIMEOUT_MS = 2000;

silenceTimerRef.current = setTimeout(() => {
  // Finalize current session
  setTranscripts(prev => prev.map(t =>
    t.id === currentTranscriptIdRef.current
      ? { ...t, isFinal: true }
      : t
  ));
  currentTranscriptIdRef.current = null;
}, SILENCE_TIMEOUT_MS);
```

### 3. Auto-Restart on Speech End

```typescript
const onSpeechEnd = useCallback(() => {
  // Reset counter when iOS naturally ends (buffer cleared)
  lastFinalizedTextLengthRef.current = 0;

  if (isListeningRef.current) {
    restartRecognition(0);
  }
}, [restartRecognition]);
```

## Visual Indicators

In `Transcription.tsx`:
- **Blue border**: Active session (`!entry.isFinal`)
- **"入力中" label**: Speech in progress
- Border disappears when session finalizes

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Previous text in new session | Length not accumulated | Use `+=` not `=` for lastFinalizedTextLengthRef |
| App crash on Voice restart | Double Voice.start() | Don't restart Voice in silence timer - use text tracking |
| "Speech recognition already started" | Multiple start calls | Check isListening before Voice.start() |
| Empty sessions created | Empty text not filtered | Add `if (!transcript.trim()) return` |

## Debug Logging

Key log messages to watch:
```
"Finalized text length (累積): X"  → Length accumulating correctly
"Session finalized, ready for new input" → Session closed
"Auto-restarting speech recognition..." → Voice restarting after onSpeechEnd
```

## Important: Do NOT

- Restart Voice during silence timer (causes crashes)
- Replace lastFinalizedTextLengthRef (must accumulate)
- Ignore empty text results (creates phantom sessions)
