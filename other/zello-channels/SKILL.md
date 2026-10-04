---
name: zello-channels
description: Manage Zello channels, contacts, group conversations, user provisioning, and presence integration for patrol zone communications in EnforcementMAPS.
---

# Zello Channels, Contacts & Groups

This skill covers how EnforcementMAPS organises Zello communication around patrol zones, manages contacts, and integrates with the existing presence system.

## Channel Strategy

Map Zello channels to the patrol zone structure:

| Zello Channel | Purpose |
|---------------|---------|
| `dispatch` | Central dispatch — all officers monitor |
| `zone-north` | North patrol zone officers |
| `zone-south` | South patrol zone officers |
| `zone-east` | East patrol zone officers |
| `zone-west` | West patrol zone officers |
| `supervisors` | Supervisor-only channel |

Channels are created in the **Zello Work admin console**, not programmatically via the SDK.

## Connecting to Channels

Auto-connect on login based on the officer's assignment:

```typescript
// Auto-connect to dispatch (all officers)
Zello.connectChannel('dispatch');

// Connect to assigned zone channel
const zoneChannel = `zone-${user.assignedZone.toLowerCase()}`;
Zello.connectChannel(zoneChannel);
```

## Channel and Contact Events

```typescript
Zello.Listener.on('onChannelsChanged', (channels) => {
  // channels: ZelloChannel[] — name, status, usersOnline
});

Zello.Listener.on('onContactsChanged', (contacts) => {
  // contacts: ZelloContact[] — name, displayName, status, isMuted
});
```

## Muting

Officers can mute channels they monitor but aren't actively using:

```typescript
Zello.muteContact(channel);   // Mute
Zello.unmuteContact(channel); // Unmute
```

## Group Conversations

Ad-hoc groups for multi-officer operations (coordinated enforcement):

```typescript
const group = await Zello.createGroupConversation([
  officer_101, officer_205, officer_629,
]);
Zello.send(group); // PTT to the group
```

## User Provisioning

Officers must exist in the Zello Work network before connecting. Two approaches:

1. **Manual** — Admin creates users in Zello Work console
2. **API provisioning** — Backend (`maps-api`) calls the Zello provisioning API when officers are registered in CIVIC MAPS

See: https://sdk.zello.com/core-concepts/user-+-channel-provisioning

## Presence Integration

The existing `src/features/presence/presence.api.ts` tracks officer online status via heartbeats. Zello contact status can augment this:

```typescript
Zello.Listener.on('onContactsChanged', (contacts) => {
  // Cross-reference with app's officer roster
  // Update presence indicators on the patrol map
  // A Zello "online" status confirms the officer's radio is active
});
```

This creates a dual presence signal: app heartbeat + Zello radio status — more reliable than either alone.

## Detailed Documentation

See `docs/dev/zello/08-channels-contacts.md` for the full channel and provisioning guide.
