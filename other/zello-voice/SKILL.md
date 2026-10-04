---
name: zello-voice
description: Implement push-to-talk voice messaging including the PTT button component, send/receive hooks, history playback, and audio UX patterns for EnforcementMAPS.
---

# Zello Voice (PTT)

This skill covers the core push-to-talk voice feature — the heart of the Zello integration.

## Core PTT Flow

1. Officer presses and **holds** the PTT button → `Zello.send(contact)`
2. SDK captures audio from microphone → streams to Zello servers in real time
3. Officer **releases** → `Zello.stopSending()`
4. Recipients hear audio as it streams (near-zero latency)

PTT is **half-duplex** — an officer cannot send and receive simultaneously.

## PTT Hook

```typescript
// src/features/zello/hooks/useZelloPTT.ts
import { useState, useCallback } from 'react';
import Zello, { ZelloContact } from '@zelloptt/react-native-zello-sdk';
import { requestZelloPermissions } from './useZelloPermissions';

export function useZelloPTT() {
  const [isSending, setIsSending] = useState(false);
  const [isReceiving, setIsReceiving] = useState(false);

  const startSending = useCallback(async (contact: ZelloContact) => {
    const granted = await requestZelloPermissions();
    if (!granted) return;
    Zello.send(contact);
    setIsSending(true);
  }, []);

  const stopSending = useCallback(() => {
    Zello.stopSending();
    setIsSending(false);
  }, []);

  return { isSending, isReceiving, startSending, stopSending };
}
```

## PTT Button Component

Use `onPressIn`/`onPressOut` for press-and-hold behaviour. The app already uses `expo-haptics` — provide tactile feedback on transmit:

```tsx
// src/features/zello/components/PTTButton.tsx
import { Pressable, Text, StyleSheet } from 'react-native';
import * as Haptics from 'expo-haptics';
import { ZelloContact } from '@zelloptt/react-native-zello-sdk';

interface PTTButtonProps {
  contact: ZelloContact;
  isSending: boolean;
  onPressIn: () => void;
  onPressOut: () => void;
}

export function PTTButton({ isSending, onPressIn, onPressOut }: PTTButtonProps) {
  return (
    <Pressable
      onPressIn={() => {
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
        onPressIn();
      }}
      onPressOut={onPressOut}
      style={[styles.button, isSending && styles.active]}
    >
      <Text style={styles.label}>
        {isSending ? 'TRANSMITTING' : 'PUSH TO TALK'}
      </Text>
    </Pressable>
  );
}
```

## Receiving Voice Messages

Register event listeners via `Zello.Listener`:

```typescript
Zello.Listener.on('onIncomingVoiceMessage', (message) => {
  // message.contact — who is speaking
  // message.channel — which channel (if channel message)
  setIsReceiving(true);
});

Zello.Listener.on('onIncomingVoiceMessageStopped', () => {
  setIsReceiving(false);
});
```

## History Playback

Replay missed transmissions:

```typescript
Zello.playHistory(historyMessage);
Zello.stopPlayback(); // Cancel playback
```

Listen for playback events: `onHistoryPlaybackStarted`, `onHistoryPlaybackStopped`.

## UX Guidelines

These patterns matter for officer safety and usability:

- **Visual + haptic feedback** during transmit — the button must feel responsive
- **Receiving indicator** showing the sender's identity (officer name/number)
- **Disable PTT** when `isReceiving === true` — half-duplex enforcement
- **Transmission timer** — display elapsed time for officer awareness
- **Audio focus** — the SDK manages audio focus, but avoid playing other sounds during PTT

## Detailed Documentation

See `docs/dev/zello/06-voice-messaging.md` for the full voice implementation guide. For event details, load `references/events-catalog.md`.
