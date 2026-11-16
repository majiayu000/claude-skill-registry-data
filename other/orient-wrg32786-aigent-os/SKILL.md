---
name: orient
description: "Provide orientation. Use when asking to orient or needing an initial orientation."
---

# orient

When the user (or an agent) is confused about where something lives, who owns what, what the rules are, or what to do next, run this to load the canonical map.

## What it does

Reads `vault/concepts/MAP.md`. If the user has named what they're confused about, surface only the section of the MAP most relevant to their question:

- "where does X live" → Geography section
- "who handles Y" → Roster section
- "what's the rule for Z" → Standing Rules section
- "whether to delegate or ship inline" → Compass row on routing
- "what build pattern to use" → Compass row on Lego Arsenal Doctrine

If the user has not named a confusion, give them the MAP table of contents and ask which area they need.

## Voice

Tight. Don't restate the MAP — point to the section. The MAP is the source of truth.

## Triggered by

Use on confusion patterns: "where does X live", "which repo", "who handles", "I'm lost", "where do I start", "how do I find", "what's the rule for".
