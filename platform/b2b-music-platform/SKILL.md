---
name: b2b-music-platform
description: B2B music streaming platform expertise for Cloud Code. Use when discussing features, making architectural decisions, or implementing functionality for commercial venues like restaurants, hotels, retail stores, or gyms. Triggers on mentions of venues, zones, commercial music, background music, or business audio.
---

# Cloud Code B2B Music Platform Knowledge

## Business Context

Cloud Code is a B2B music streaming platform for commercial venues in Asia. It replaces BeatBreeze and competes with Soundtrack Your Brand, Rockbot, and Mood Media.

## Target Users

| User Type | Needs |
|-----------|-------|
| **Venue Managers** | Easy scheduling, quick controls, mobile access |
| **Corporate HQ** | Multi-venue dashboard, brand consistency, reporting |
| **Staff** | Simple override controls, volume adjustment |
| **IT/Technical** | API access, hardware setup, integrations |

## Key Differentiators

1. **Royalty-Free Content** - No licensing fees, predictable costs
2. **Weather Automation** - Automatic playlist switching based on conditions
3. **AI Features** - Voice commands, intelligent playlist generation
4. **Affordable Hardware** - $100 Raspberry Pi vs $649 competitor players
5. **Local File Support** - Play customer's own content alongside library

## Pricing Model

Target: **$20-25/zone/month** (competitors charge $35+)

## Multi-Tenancy Architecture

```
Organization (tenant)
└── Venues (physical locations)
    └── Zones (audio outputs: lobby, restaurant, gym)
        └── Schedules, Now Playing, Messages
```

## Critical Constraints

1. **iOS PWA Limitation**: No background audio → Need native Capacitor app
2. **No Spotify/YouTube**: ToS prohibits commercial use
3. **Gapless Playback**: 45ms browser gaps → Use 35ms crossfades
4. **Offline Required**: Venues need music even during internet outages

## Feature Priorities

### Phase 1 (MVP)
- Content management (upload, organize, playlists)
- Audio player with crossfades and ducking
- Drag-drop scheduling calendar
- Multi-zone dashboard

### Phase 2
- Weather automation
- AI voice commands
- Native iOS/Android apps
- Advanced analytics

### Phase 3
- Generative soundscapes (Mubert integration)
- IoT integrations (lighting, sensors)
- White-label options

## When Making Decisions

Always consider:
- **Reliability** - Music must never stop unexpectedly
- **Simplicity** - Venue staff are not technical
- **Cost** - Keep infrastructure costs low for healthy margins
- **Offline-first** - Assume internet will fail
- **Multi-tenancy** - Data isolation between organizations
