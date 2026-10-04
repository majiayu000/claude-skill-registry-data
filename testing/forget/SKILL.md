---
description: Remove a saved preference from CLAUDE.md. Triggered by /forget or phrases like "forget about..." or "stop remembering...".
disable-model-invocation: true
allowed-tools: Read Edit
---

You are the `/forget` skill. Remove a preference from CLAUDE.md's Preferences section.

## Triggers

- Slash form: `/forget` (no arg) or `/forget <text>`
- Natural language: "forget about...", "stop remembering...", "drop the preference about..."

## Step 1: Locate the Preferences section

Read CLAUDE.md. Find the HTML comment marker:

`<!-- managed by /remember and /forget — items added below are remembered across sessions -->`

If the section is missing or empty, tell the user: "There are no saved preferences yet."

## Step 2: List and pick

**If no argument** is provided:

Number each existing preference and present:

> "Here's what I'm currently remembering:
> 1. Always run prettier before committing.
> 2. Never push to main directly.
> 3. Prefer integration tests over mocks.
>
> Which would you like me to forget? (number or short phrase)"

Wait for response.

**If an argument** is provided:

Find the best-matching line via case-insensitive substring match. If multiple match, list them and ask which.

## Step 3: Confirm

Show the matched line and ask:

> "Remove this? '<line>'  (yes/no)"

On "no," abort.

## Step 4: Remove

Edit CLAUDE.md to delete the matched bullet. Preserve all other bullets and the marker.

## Step 5: Confirm to the user

> "Done — I've forgotten '<line>'."

## Edge cases

- **No match.** Tell the user: "I couldn't find a preference matching that. Want me to list them all?"
- **Multiple matches.** List numbered options; ask which.
- **User says 'all' or 'everything'.** Ask twice: "Remove ALL preferences? This will clear the section entirely. (yes/no)" — require a second yes.
