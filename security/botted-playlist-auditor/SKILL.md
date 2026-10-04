---
name: botted-playlist-auditor
description: Use this when auditing Spotify or Apple Music playlists for fake streams, botted networks, or curator red flags. Protects independent artists and labels from streaming strikes and takedowns. Checks stream-to-follower ratio, geographic anomalies, track rotation velocity, and curator payment patterns.
---

# Botted Playlist & Streaming Authenticity Auditor

Protects independent artists, managers, and record labels by identifying artificial streaming farms, fake playlist networks, and botted curator accounts before pitching or purchasing placement.

## 4 Primary Red Flags

### 1. Stream-to-Follower Ratio Anomaly

- **Organic pattern**: 1,000 playlist followers → 50–300 monthly streams per featured track
- **Red flag**: 500 followers generating 50,000+ streams overnight, or 100,000 followers yielding 10 streams

### 2. Geographic Concentration Spikes

- **Organic pattern**: Streams distributed across major music cities matching radio airplay and tour stops
- **Red flag**: 80%+ of streams from one small city known for server farms (Finland, Buffalo, Southeast Asia data centres) with zero local radio or social media engagement

### 3. Track Rotation & Turnover Velocity

- **Organic pattern**: Curators maintain consistent genre themes, rotate 5–10 new tracks per week
- **Red flag**: Playlists wiping 100% of tracks every 48 hours, or mixing completely unrelated genres (death metal next to ambient acoustic) solely to service paid customers

### 4. Curator Contact & Payment Red Flags

- **Organic pattern**: Pitching via official submission forms, email, or verified social profiles
- **Red flag**: Curators requesting direct PayPal/crypto for "guaranteed 50k streams", or using automated Telegram bots

## Audit Output Format

When analyzing a playlist or track trajectory:

1. **Authenticity Score (0–100%)**: Overall safety rating for pitching
2. **Detected Red Flags**: Specific anomaly list (Geography, Followers vs Streams, Rotation)
3. **Verdict & Action**:
   - `SAFE`: Pitch via official channels
   - `CAUTION`: Monitor streams daily via Spotify for Artists
   - `HIGH RISK`: Do NOT pitch or accept placement. Request immediate removal if added (to prevent Spotify artificial streaming flags)

## Example Output

```
Playlist: "Indie Vibes 2026" (15k followers)
- Authenticity Score: 35%
- Red Flags:
  - Stream-to-follower ratio: 200:1 (organic is 0.05–0.3)
  - 78% of streams from Buffalo, NY (server farm hub)
  - Track rotation: 100% wipe every 72 hours
- Verdict: HIGH RISK — do not pitch, request removal if already added
```

## When to audit

- Before pitching any playlist (especially if curator requests payment)
- After track added to unfamiliar playlist (check within 48 hours)
- If Spotify for Artists shows sudden stream spike from one geographic location
- If curator contact is via Telegram bot or requests crypto payment

## Related

- indie-artist-pack (skills/tap/): TAP pack excludes botted playlists
- growth-os brands/spotcheck/: client audit notes and historical red flags
