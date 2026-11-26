---
name: skill-profiles
description: Keep 100+ skills working - turn groups of skills on or off depending on the type of work (frontend, marketing, video, code, ...) so the skill listing stays within the context budget. Use when the person says what kind of work they'll do ("today is frontend", "let's do video"), asks to see/change/create profiles, or asks why a skill doesn't show up or why the skills listing is truncated. Claude Code only.
author: sant1jmnz
tags:
  - productivity
  - claude-code
  - configuration
---

# Skill profiles

Claude Code loads every skill's description at startup, with a small budget (~1% of the context). With many skills, descriptions get truncated and the agent stops picking them by itself. A profile leaves active only the skills for the current work.

## Catalog

File `~/.claude/skill-profiles.json` (if it doesn't exist, create it with the structure below and ask the person which groups they want based on the skills in `~/.claude/skills/`).

```json
{
  "active": "all",
  "groups": {
    "core": ["handoff", "perfiles", "find-skills", "last30days", "humanizer"],
    "frontend": ["design-taste-frontend", "high-end-visual-design", "emil-design-eng", "apple-design"],
    "marketing": ["copywriting", "content-strategy", "social", "cold-email", "ads", "seo-audit"],
    "video": ["hyperframes", "hyperframes-cli", "media-use"]
  },
  "profiles": {
    "code": { "desc": "Essentials only", "groups": ["core"] },
    "frontend": { "desc": "Interface design", "groups": ["core", "frontend"] },
    "marketing": { "desc": "Marketing and content", "groups": ["core", "marketing"] },
    "video": { "desc": "Video production", "groups": ["core", "video"] },
    "all": { "desc": "Everything on", "groups": ["core", "frontend", "marketing", "video"] }
  }
}
```

## Apply a profile

1. Read `skill-profiles.json` and resolve the active set (union of the profile's groups).
2. In `~/.claude/settings.json`, write `skillOverrides` with `"off"` for **every skill in `~/.claude/skills/` that isn't in the active set**, and no entry for the active ones. Don't touch other keys. Back up first.
3. Update `active` in `skill-profiles.json`.
4. Tell the person: **the change shows after restarting the session.**

Always merge the full JSON with a script or temp file; never interpolate skill names inside a shell command.

## Rules

- Only skills in `~/.claude/skills/`. Don't touch plugin or built-in ones.
- Never delete files: a profile only writes `skillOverrides`. Going back to `all` turns everything on.
- If the work doesn't fit a profile, propose the closest one and offer to create a new one.
- If they ask to enable a single skill that's off, remove its entry from `skillOverrides` without changing the rest.
- Limitation: only one profile at a time for the whole machine.
