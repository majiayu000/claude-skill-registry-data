---
name: music-discovery
description: "Formulate semantic music search queries, expand genres/moods, and discover music using alx search CLI."
version: 1.0.0
author: agent-lx-music project
license: MIT
metadata:
  hermes:
    tags: [music, discovery, search, mood, genre]
    related_skills: [agent-lx-music]
---

# Music Discovery Skill

## Overview

This skill teaches AI agents how to act as an intelligent music curator. Instead of performing plain literal searches, the agent translates high-level user requests, moods, scenarios, or abstract genres into optimized search queries, using `alx search` to discover and play matching music.

---

## Agent Behavior & Search Expansion

When a user asks for music based on a mood, activity, or vague description, the agent MUST expand it into high-affinity keywords (Artists, Genres, Album keywords, or precise titles) rather than querying the exact phrase.

### Query Expansion Table

| User Request | Key Mood / Genre | Search Term Recommendation | Command Example |
| --- | --- | --- | --- |
| "Play something to help me concentrate" | Lofi / Ambient / Minimalist | "lofi study", "ambient focus", "chillhop" | `alx search "lofi study" --source wy` |
| "I need high energy gym music" | Synthwave / Hardstyle / Phonk | "phonk workout", "synthwave running", "cyberpunk" | `alx search "phonk workout"` |
| "Show me classic Chinese rock" | 90s Chinese Rock / Folk | "崔健", "唐朝乐队", "魔岩三杰" | `alx search "崔健"` |
| "Vibing on a rainy Sunday afternoon" | Acoustic / Indie / Jazz | "acoustic chill", "jazz piano", "indie folk" | `alx search "acoustic chill" --source kw` |

---

## Search Automation Workflow

### Workflow 1: Mood-Based Playlist Generation

1. Receive user mood request (e.g. "feeling nostalgic").
2. Generate 3 distinct related query terms (e.g., "90s classic hits", "retro ballad", "childhood memories").
3. Perform searches for each, fetch the top 2 IDs from each search, and compile a playlist:

```bash
# Create temporary mood playlist
alx playlist create "Nostalgic Vibe"

# Add tracks from distinct searches
alx search "周杰伦 经典" --id-only --limit 2 | xargs -I {} alx playlist add "Nostalgic Vibe" {}
alx search "陈奕迅 怀旧" --id-only --limit 2 | xargs -I {} alx playlist add "Nostalgic Vibe" {}

# Play the playlist
alx playlist play "Nostalgic Vibe" --shuffle
```

### Workflow 2: Platform-Optimized Discovery

Different music platforms excel in different genres. The agent should leverage these strengths:

- **NetEase Music (`wy`)**: Excellent for indie, lofi, electronic, and user-curated playlist matches.
- **Kuwo (`kw`) / Kugou (`kg`)**: Excellent for high-resolution lossless versions and mainstream Mandarin pop.
- **Migu (`mg`) / QQ (`tx`)**: Excellent for high-fidelity master cuts and exclusive license songs.
