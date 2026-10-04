---
name: standup
description: Generate a tweetable build-in-public update from recent git activity, written for a music community audience
disable-model-invocation: true
---

# Standup — Tweetable Build-in-Public Update

Generate a single short update from git history. The audience is ZAO — a music community of artists, not engineers. Write like you are telling a fellow musician what you built today.

## Context to Gather

```
Recent commits: !`git log --oneline --since="yesterday" -20`
Weekly commits: !`git log --oneline --since="7 days ago" -30`
Files changed today: !`git diff --stat HEAD~5`
Commit count today: !`git rev-list --count --since="yesterday" HEAD`
Files changed count: !`git diff --shortstat HEAD~5`
```

## How to Process

1. Read the commit messages and changed file paths from the context above.
2. Extract the **specific feature names** mentioned in commits (e.g., "screen share for Spaces", "broadcast to YouTube Live", "music player queue"). Always name the actual feature — never say "various improvements".
3. Count commits and files changed — you MUST include at least one number in the output.
4. Translate everything into plain language a musician would understand:
   - "ControlsPanel.tsx" -> "room controls"
   - "RoomMusicPanel" -> "the music panel in Spaces"
   - "RTMP modal" -> "live-streaming setup"
   - "API route" -> skip or say "backend work"
   - "component" -> "screen" or "feature" or just name what it does
   - "refactor" -> "cleaned up" or "improved"
   - "bug fix" -> "fixed [the thing that was broken]"
5. Pick the 1-2 most interesting features to highlight. Drop the rest.

## Output Format

One single update. HARD LIMIT: 280 characters (must fit in a tweet/cast).

Template:
```
[What shipped, in plain language] — [1 metric]. Building ZAO OS in public.
```

Examples (all under 280 chars):
```
Added screen sharing to Spaces so artists can share visuals during listening sessions — 6 commits across 12 files today. Building ZAO OS in public.
```
```
You can now broadcast your room to YouTube and Twitch at the same time. Multi-streaming is live — 4 commits today. Building ZAO OS in public.
```
```
New provider picker in Spaces lets hosts choose their audio engine before going live — shipped in 3 commits. Building ZAO OS in public.
```

## Rules

- HARD LIMIT: 280 characters. Count before outputting. If over, cut words until it fits.
- MUST include at least one number (commits, files, days, etc.).
- MUST name the specific feature from the commits — never be vague.
- NO developer jargon: no "components", "routes", "API", "refactor", "merge", "PR", "deploy", "endpoints", "middleware", "hooks", "state management", "database migrations".
- Write for artists: use words like "rooms", "music", "listening", "streaming", "sharing", "voting", "community".
- Always say "Farcaster" not "Warpcast".
- One update only. No bullet lists, no sections, no headers.
- End with "Building ZAO OS in public." (or a variation) when space permits.
