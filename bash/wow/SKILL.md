---
name: wow
description: "Look up World of Warcraft characters — M+ scores, best runs, raid progression, gear, and more. Uses Raider.io (free), with optional Blizzard API and Warcraft Logs integration for armory data and raid parses."
metadata:
  openclaw:
    emoji: "⚔️"
    requires:
      bins: ["curl", "jq"]
      env_optional: ["BLIZZARD_CLIENT_ID", "BLIZZARD_CLIENT_SECRET", "WCL_CLIENT_ID", "WCL_CLIENT_SECRET"]
    install:
      - id: symlink
        kind: shell
        command: "ln -sf $(pwd)/wow /usr/local/bin/wow"
        label: "Install wow CLI (symlink)"
---

# World of Warcraft

Look up WoW characters, M+ scores, raid progression, and more.

## Quick Start

```bash
# Full character profile — M+ score, best runs, raid progression
wow lookup <name>-<realm>
wow lookup azunazx-hyjal

# Quick one-line summary
wow search azunazx-hyjal

# Current M+ affixes
wow affixes

# Top M+ runs this season
wow top-runs
```

## Character Lookup

The primary command. Shows M+ score, best runs, raid progression, and gear.

```bash
# Default region is US
wow lookup <name>-<realm>

# EU character
wow lookup <name>-<realm> -r eu

# Include recent runs
wow lookup <name>-<realm> --recent

# Raw JSON output (for programmatic use)
wow lookup <name>-<realm> --raw
```

**Output includes:**
- Character info (name, class, spec, race, faction, realm)
- Mythic+ score (overall + per-role breakdown)
- Best M+ runs (dungeon, key level, time, score)
- Raid progression (Normal/Heroic/Mythic kills per raid)
- Equipped item level

## Quick Search

One-line character summary for quick lookups:

```bash
wow search azunazx-hyjal
# → Azunazx | Fire Mage | Hyjal [US] | Alliance | M+ Score: 4002.6
```

## M+ Affixes

```bash
wow affixes           # US affixes
wow affixes -r eu     # EU affixes
```

## Top M+ Runs

```bash
wow top-runs              # Top runs in US
wow top-runs -r eu        # Top runs in EU
wow top-runs --page 1     # Page through results
```

## Raid Info

```bash
wow raids           # List current raids and boss counts
```

## API Sources

### Raider.io (Active — No Auth Required)
- ✅ Character profiles, M+ scores, best/recent runs
- ✅ Raid progression summary
- ✅ Current affixes
- ✅ Top M+ runs / rankings
- ✅ Gear / item level
- Free, no rate limit issues for normal use

### Blizzard API (Optional — OAuth2 Required)
- Armory data: detailed gear, stats, achievements
- M+ rating (Blizzard's own rating system)
- Character media (renders)
- Requires `BLIZZARD_CLIENT_ID` and `BLIZZARD_CLIENT_SECRET`
- Register at: https://develop.battle.net/access/clients

```bash
# When configured:
wow armory <name>-<realm>
```

### Warcraft Logs API v2 (Optional — OAuth2 Required)
- Raid parses and percentiles
- Damage/healing breakdowns per encounter
- Character rankings across difficulties
- GraphQL API
- Requires `WCL_CLIENT_ID` and `WCL_CLIENT_SECRET`
- Register at: https://www.warcraftlogs.com/api/clients

```bash
# When configured:
wow parses <name>-<realm>
```

## Configuration

```bash
# Check what's configured
wow config
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WOW_REGION` | No | Default region: `us`, `eu`, `kr`, `tw` (default: `us`) |
| `WOW_CONFIG` | No | Config file path (default: `~/.config/wow/config.env`) |
| `BLIZZARD_CLIENT_ID` | No | Blizzard API client ID |
| `BLIZZARD_CLIENT_SECRET` | No | Blizzard API client secret |
| `WCL_CLIENT_ID` | No | Warcraft Logs client ID |
| `WCL_CLIENT_SECRET` | No | Warcraft Logs client secret |

### Config File

Create `~/.config/wow/config.env`:

```bash
# Defaults
WOW_REGION=us

# Blizzard API (https://develop.battle.net/access/clients)
BLIZZARD_CLIENT_ID=your_id
BLIZZARD_CLIENT_SECRET=your_secret

# Warcraft Logs (https://www.warcraftlogs.com/api/clients)
WCL_CLIENT_ID=your_id
WCL_CLIENT_SECRET=your_secret
```

## Regions

| Code | Region |
|------|--------|
| `us` | United States & Oceania |
| `eu` | Europe |
| `kr` | Korea |
| `tw` | Taiwan |

## Realm Names

Use hyphenated, lowercase realm names:
- `area-52` (not "Area 52")
- `moon-guard` (not "Moon Guard")
- `tichondrius` (single-word realms work as-is)

The CLI auto-converts spaces to hyphens and strips apostrophes.

## Examples for the Agent

When the user asks about a WoW character:

```bash
# "What's my M+ score?" (if you know their character)
wow lookup charactername-realmname

# "Look up this character on EU"
wow lookup charactername-realmname -r eu

# "What are the affixes this week?"
wow affixes

# "What are the top keys right now?"
wow top-runs

# Quick check
wow search charactername-realmname

# Get raw data for further processing
wow lookup charactername-realmname --raw | jq '.mythic_plus_scores_by_season[0].scores.all'
```
