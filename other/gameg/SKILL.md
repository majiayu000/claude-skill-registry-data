---
name: gameg
description: Start the game-generalist skill from a slash command, with an optional mode first and then the idea, for example "/gameg prototype a lighthouse keeper who redirects ships with a beam" or "/gameg game a 3-minute browser arcade where you herd fireflies into jars". With no request it shows the menu of modes.
argument-hint: "[prototype|game|polish] <idea>"
disable-model-invocation: true
---

# gameg

The user started `gameg` (`game-generalist`) with this request:

$ARGUMENTS

In tools that do not fill in the line above, the request is the rest of the user's message.

1. If the request is empty or is `help`, show the menu below as it is, then ask one question: what game do you want to
   make? Stop there.
2. Otherwise load the `game-generalist` skill (`../game-generalist/SKILL.md`) and follow it from the start.
3. Read the request from the left: if the first word matches a mode (`prototype`, `game`, `polish`), use that mode and
   drop the word from the idea. Otherwise pick the mode from the idea.
4. Before building, run the intent brief from that skill (`references/intent-brief.md`). A mode and an idea do not say the engine, platform, session length or time box: ask about whichever of those the request leaves open, with options and a recommended default, in one round.

## Menu

| Mode | What it makes | Example |
|---|---|---|
| `prototype` | A playable greybox of the core loop and a go/kill note | `/gameg prototype a lighthouse keeper who redirects ships with a beam` |
| `game` | A complete small original game inside your time box (a jam entry is this mode) | `/gameg game a 3-minute browser arcade where you herd fireflies into jars` |
| `polish` | Feel, readability, audio and QA passes on an existing playable; no new features | `/gameg polish my firefly arcade: jump feel, hit feedback and a softlock check` |
