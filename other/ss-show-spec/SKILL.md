---
name: ss-show-spec
description: Displays the current source-of-truth OpenSpec for a capability, or lists all capabilities when called without one, and summarizes recent archived changes that touched it. Use this as the entry point before reading or editing anything under openspec/ — do not grep or browse the directory manually first.
---

# Show OpenSpec Capability

Discover and display the authoritative spec for a capability. This is the entry point for
"see what exists, then read it" — don't list or grep `openspec/` blindly before calling
this skill.

## Inputs

Optional: a capability name (matching a directory under `openspec/specs/`) or a keyword to
search for. Omit both to get an index of all capabilities.

## Process

1. **No input given** — enumerate every directory under `openspec/specs/`. For each, read
   the `## Purpose` section (or the first descriptive line) of its `spec.md` and print a
   one-line index entry: `capability-name — <purpose>`. If `openspec/specs/` is empty or
   missing, report that this repository has no OpenSpec baseline yet — suggest running the
   `ss-write-spec` or `ss-reverse-spec` skill. Stop here.
2. **Input matches a capability directory exactly** (`openspec/specs/<capability>/`) — read
   and display that `spec.md` in full.
3. **Input is a keyword** — search every `openspec/specs/*/spec.md` (and, where useful,
   active `openspec/changes/*/specs/*/spec.md`, excluding `archive/`) for the text. Show
   each match with its capability name and the matching line or excerpt. If more than one
   capability matches, list them and ask the user which one to display in full.
4. After displaying a capability, list the 5 most recent archive entries that touched it —
   e.g., by finding files matching `openspec/changes/archive/*/specs/<capability>/spec.md`
   and taking the last 5 in sorted order. For each, show the archive directory name, the
   first proposal heading if available, and a count of delta sections (ADDED / MODIFIED /
   REMOVED / RENAMED).

## Output

Keep the surrounding commentary concise, but always include the full current spec text.
Do not edit any files.
