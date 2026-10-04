---
description: Save a preference to CLAUDE.md so it persists across sessions. Triggered by /remember or natural-language phrases like "remember to..." or "from now on, always...".
disable-model-invocation: true
allowed-tools: Read Edit Write
---

You are the `/remember` skill. Save a preference to CLAUDE.md's Preferences section so it persists across future sessions.

## Triggers

- Slash form: `/remember <preference text>`
- Natural language: "remember to...", "from now on, always...", "always X", "never X"

## Step 1: Parse the preference

Extract the user's intended preference. Normalize to one of:
- `Always <verb> <object> [context]`
- `Never <verb> <object> [context]`
- `Prefer <X> over <Y>`
- Or leave verbatim if it doesn't match a pattern.

## Step 2: Personal vs. project disambiguation

If the preference uses first-person singular phrasing ("I prefer", "I like", "my"), ask once:

> "Is this just for you, or should everyone working on this project follow it?"

- "Just me" → write to `~/.claude/CLAUDE.md` under the heading `## Project: <project-name>`.
- "Everyone" / "the project" → continue to Step 3 (write to CLAUDE.md).

## Step 3: Ambiguity check

If the preference is a project-style preference but lacks an engineering, project, or workflow vocabulary (e.g., "remember to call mom"), confirm:

> "Want me to save that as a project preference, or did you mean something else?"

On "something else," abort the skill. On "yes, save it," continue.

## Step 4: Locate the Preferences section in CLAUDE.md

Read CLAUDE.md. Look for the HTML comment marker:

`<!-- managed by /remember and /forget — items added below are remembered across sessions -->`

If the marker is missing, insert a `## Preferences` section with the marker near the end of CLAUDE.md (before any auto-generated trailers, after the Constraints section if present).

## Step 5: Contradiction check

For each existing bullet under the marker, ask: does the new preference directly contradict it? (e.g., new "Never use prettier" vs. existing "Always use prettier.")

If yes, surface to the user:

> "That contradicts an existing preference: '<existing>'. Want me to replace the old one, or keep both?"

On "replace," remove the existing line. On "keep both," continue without removal.

## Step 6: Append the preference

Add a new bullet under the marker:

`- <normalized preference>.`

Preserve any existing bullets. Sort order: append, do not re-order.

## Step 7: Confirm to the user

In plain English:

> "Got it. <repeat the preference>. I've added this to your CLAUDE.md."

## Edge cases

- **Empty input.** Ask: "What should I remember?"
- **Vague preference** (e.g., "be better"). Push back once: "That's a bit broad — could you be specific about when or how?" If the user insists, save verbatim.
- **Preference already present.** Confirm: "I already have that saved. No change needed."
