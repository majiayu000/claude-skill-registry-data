---
name: zello-emergency
description: Implement Zello emergency mode with Code21 dispatch dual-trigger, emergency button UX, dispatch calls, and emergency event handling for officer safety in EnforcementMAPS.
---

# Zello Emergency & Dispatch

This skill covers the highest-stakes feature in the Zello integration — emergency mode and its integration with the existing Code21 dispatch system.

## Zello Emergency Mode

When activated, emergency mode:
- Opens a **priority audio channel** to dispatch (overrides all mute settings)
- Sends the officer's **location automatically**
- Triggers a **prominent alert** on the dispatch console
- Remains active until explicitly deactivated

```typescript
Zello.startEmergency();  // Activate
Zello.stopEmergency();   // Deactivate
```

## Code21 Dual-Trigger Pattern

Zello emergency **complements** Code21 — it does not replace it. When an officer triggers emergency, fire both systems:

| Scenario | Code21 | Zello Emergency |
|----------|--------|----------------|
| Dispatch sends job to officer | ✅ Push notification | — |
| Officer acknowledges dispatch | ✅ API call | — |
| Officer needs immediate help | — | ✅ Live voice + location |
| Officer sends status update | ✅ API status change | ✅ PTT voice |

### Emergency Hook

```typescript
// src/features/zello/hooks/useZelloEmergency.ts
import Zello from '@zelloptt/react-native-zello-sdk';
import api from '@/shared/infra/api';

export function useZelloEmergency() {
  const startEmergency = async () => {
    // 1. Activate Zello emergency (live voice + location)
    Zello.startEmergency();

    // 2. Notify MAPS API (creates Code21 record, alerts supervisors)
    try {
      await api.post('/code21/emergency', {
        type: 'OFFICER_EMERGENCY',
        source: 'zello',
      });
    } catch {
      // Zello emergency is already active — API failure is non-blocking
      console.error('[EMERGENCY] Failed to notify MAPS API');
    }
  };

  const stopEmergency = () => {
    Zello.stopEmergency();
  };

  return { startEmergency, stopEmergency };
}
```

The Zello emergency takes priority — even if the MAPS API call fails, the officer has live voice and location streaming to dispatch.

## Receiving Emergency Events

For dispatch/supervisor app:

```typescript
Zello.Listener.on('onEmergencyStarted', (event) => {
  // event.contact — officer in emergency
  // Highlight on patrol map, sound alarm, bring to front
});

Zello.Listener.on('onEmergencyStopped', (event) => {
  // Clear emergency state
});
```

## Emergency Button UX

Officer safety requirements:
- Place in a **persistent, accessible location** — not buried in a menu
- Use a **long-press gesture** (3-second hold) to prevent accidental activation
- Provide strong **visual + haptic + audio** feedback on activation
- Make deactivation equally clear but not accidentally triggerable

## Dispatch Calls

For non-emergency priority communications:

```typescript
await Zello.sendDispatchCall(dispatchChannel);
```

This requests attention from dispatch without triggering full emergency mode.

## Detailed Documentation

See `docs/dev/zello/10-emergency-dispatch.md` for the full emergency and dispatch guide.
