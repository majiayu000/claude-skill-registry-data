---
name: zello-messaging
description: Send and receive rich messages (text, image, location, alert) through the Zello SDK in EnforcementMAPS.
---

# Zello Rich Messaging

This skill covers non-voice message types — text, image, location, and alert — which complement PTT voice for situations where voice isn't appropriate or additional context is needed.

## Message Types

| Type | Method | EnforcementMAPS Use Case |
|------|--------|--------------------------|
| Text | `Zello.sendText(contact, text)` | Quick status updates, notes to dispatch |
| Image | `Zello.sendImage(contact, uri)` | Photo evidence, scene documentation |
| Location | `Zello.sendLocation(contact)` | Share GPS position (supplements expo-location) |
| Alert | `Zello.sendAlert(contact, text, level)` | Priority notifications, officer-needs-help pings |

## Sending Messages

```typescript
// Text
await Zello.sendText(contact, 'Proceeding to Section 4B');

// Image (from expo-image-picker or camera)
await Zello.sendImage(contact, 'file:///path/to/photo.jpg');

// Location (uses device GPS internally)
await Zello.sendLocation(contact);

// Alert (level: 1=low, 2=medium, 3=high)
await Zello.sendAlert(contact, 'Officer requires assistance', 3);
```

## Receiving Messages

```typescript
Zello.Listener.on('onIncomingTextMessage', (event) => {
  // event.contact, event.text, event.channel
});

Zello.Listener.on('onIncomingImageMessage', (event) => {
  // event.image, event.contact
});

Zello.Listener.on('onIncomingLocationMessage', (event) => {
  // event.latitude, event.longitude, event.contact
  // Integration: plot on react-native-maps alongside patrol zone markers
});

Zello.Listener.on('onIncomingAlertMessage', (event) => {
  // event.contact, event.text, event.level
});
```

## Messaging Hook

```typescript
// src/features/zello/hooks/useZelloMessaging.ts
import Zello, { ZelloContact } from '@zelloptt/react-native-zello-sdk';

export function useZelloMessaging() {
  const sendText = (contact: ZelloContact, text: string) =>
    Zello.sendText(contact, text);

  const sendImage = (contact: ZelloContact, uri: string) =>
    Zello.sendImage(contact, uri);

  const sendLocation = (contact: ZelloContact) =>
    Zello.sendLocation(contact);

  const sendAlert = (contact: ZelloContact, text: string, level: number) =>
    Zello.sendAlert(contact, text, level);

  return { sendText, sendImage, sendLocation, sendAlert };
}
```

## Integration Opportunities

- **Incoming locations** can be plotted on the existing `react-native-maps` patrol zone map alongside officer markers
- **Image messages** can be saved to the patrol evidence log
- **Alert level 3** should trigger prominent UI (full-screen overlay, alarm sound) similar to Code21 dispatch alerts

## Detailed Documentation

See `docs/dev/zello/07-rich-messaging.md` for the full rich messaging guide.
