---
name: pengolodh
description: Use when the user runs /pengolodh, /pengolodh verify, /pengolodh status, or /pengolodh gc against the current repo. Prints, verifies, or prunes this repo's mechanism cache — file:line-anchored facts (entry points, live-vs-dead modules, seams, invariants, conventions in force) that grep cannot answer on its own. The cache is normally built opportunistically and delivered automatically at SessionStart (pengolodh-inject.sh); this skill is the hand tool for checking it, forcing a repair, or cleaning out confirmed-dead entries — never for a deliberate scan of the repo, which this skill does not do.
purpose: Prints, verifies, or prunes this repo's Pengolodh mechanism cache by hand.
user_invocable: true
args: "[verify|status|gc]"
stage: desk
---

# Pengolodh — the Mechanism Cache, by Hand

Pengolodh of Gondolin loved lore beyond delight in ruling, and set down what
the city was so it might survive the city's fall. This skill is the hand
tool for the cache his name backs — see `docs/workflow/mechanism-cache.md`
for the full mechanics, the entry format, and the recording rule (`CLAUDE.md`
§ *Mechanism Cache*). Read that doc before recording an entry by hand.

## Arguments

- No argument — print the cache as-is (the same content `SessionStart`
  already injects), plus its `status` line.
- `verify` — walk every anchor, repair a line number that merely moved,
  report STALE (literal gone) or MISSING (file gone). Mutates the file only
  to repair a moved line number.
- `status` — entry and staleness counts, plus the git posture (absent,
  unsynced, behind, diverged, or synced) and, when relevant, the invitation
  to `git init` or set `.autosync`.
- `gc` — permanently deletes entries `verify` confirms STALE or MISSING.
  Leaves a low-confidence entry alone as long as it still verifies OK — `gc`
  removes what is confirmed dead, never what is merely uncertain.

## Workflow

### Step 1: Resolve the repo root and the index

```bash
root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
idx="$(bash ~/.claude/hooks/pengolodh.sh path "$root")"
```

### Step 2: Run the requested verb

- No argument: `bash ~/.claude/hooks/pengolodh.sh status "$root"`, then print
  `$idx`'s contents if it exists.
- `verify`: `bash ~/.claude/hooks/pengolodh.sh verify "$root"` — report the
  MOVED/STALE/MISSING lines and the summary count verbatim.
- `status`: `bash ~/.claude/hooks/pengolodh.sh status "$root"` — report
  verbatim, including the git posture line.
- `gc`: `bash ~/.claude/hooks/pengolodh.sh gc "$root"` — report how many
  entries were removed. When git is present, `gc` also commits the removal
  locally on its own — no separate step needed.

### Step 3: Recording a fact by hand

This skill does not itself compose an entry — `docs/workflow/mechanism-cache.md`
covers the format and the boundary rule (a `file:line` anchor means it
belongs here; no anchor means auto-memory or the knowledge repo instead).
When the user asks to record something through this skill, follow that doc,
append the line to `$idx`, then run `verify` once to confirm the anchor
actually resolves before reporting success — `verify` also commits the
entry locally when git is present, so no separate commit step is owed.

## Rules

- Never invent an anchor literal you have not confirmed exists in the named
  file — an unverified entry is worse than no entry, since it reads as
  trustworthy until `verify` catches it.
- Never scan the repo looking for things to record. This skill only acts on
  what is already in the index, or what the user hands it directly.
- `gc` is destructive to the index file (not to the repo). Report what was
  removed; do not run it silently as a side effect of another verb.
