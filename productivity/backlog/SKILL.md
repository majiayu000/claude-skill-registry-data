---
name: backlog
description: Use when the user wants to defer something for later without losing it — "put a pin in that", "save for later", "defer that", "park this", "come back to it later", "stash that idea", "queue it up", or any equivalent. Creates a placeholder epic spec at `<data_root>/projects/<name>/design/specs/YYYY-MM-DD-<slug>.md` so it appears immediately in the planning queue (surfaced by the disk epic-survey) and is ready to be expanded via `/project <spec-path>` later.
---

# Pin

## Overview

Capture a deferred item as a placeholder epic spec on the status dashboard with one short interaction. The whole point is friction-free — if pinning takes longer than the original aside, the user stops using it.

## When to use

- User says "put a pin in that", "save for later", "defer", "park it", "come back to this later", "queue this up", "stash this idea", or any equivalent
- User is mid-conversation and wants to capture an aside without acting on it now
- User explicitly invokes `/backlog`

## When NOT to use

- User is describing something they want to do **now** — that's a regular task, not a pin
- User says "remember X" — that's a memory write, use the memory system instead (different artifact, different lifecycle)
- User wants to schedule something for a specific time — that's the `schedule` skill, not this
- The thing being deferred is a single trivial chore (rename a var, delete a file) — overhead of a spec card outweighs the benefit. Surface inline as a follow-up note instead. Threshold: if it would take less than 5 minutes to just do, don't pin.

## Procedure

### Step 1: Identify what to pin

Read the recent conversation context. The user's trigger phrase usually points at something specific:
- "Put a pin in that" — "that" is whatever was just discussed; pin THAT.
- "Save for later: <X>" — pin X.
- "Defer the <X> work" — pin X.
- Plain `/backlog-it` with no further input — ASK once: *"What should I pin? One line is fine."*

If the topic is genuinely ambiguous (e.g., the conversation just covered three different things and "save for later" could mean any of them), ASK ONE clarifying question — never more. Don't make pinning a process.

**Also derive the `project:` field** (required in Step 5 frontmatter). Try in order:

1. **Infer from conversation context.** The cwd, the files being discussed, the repo paths in the conversation, and the topic itself almost always pin down the project. Enumerate the installed projects (`~/.agentflow/config/projects/*.md`); for each, match the conversation cues (repo paths, product names, domain words) against that project's `aliases` list. The first project whose aliases match wins. If nothing matches:
   - Anything explicitly personal (personal errands, life admin) → `personal`
   - Anything that genuinely doesn't fit — one-off research, a cross-cutting spike, or a project not yet installed → `other`

2. **If the cue is ambiguous or absent**, fold it into the SAME clarifying question you'd ask about the topic (don't make pinning a two-question process). Example: *"Pinning the connector layer for `<inferred project>` — correct? (Or which project — one of your installed `projects/*.md`, or `personal` / `other`?)"*

3. **If you already asked one clarifying question and still don't know**, default to `other` — the user can fix it later by editing the spec. Do NOT ask a second question.

### Step 2: Derive slug + title

Generate a kebab-case slug from the topic. Rules:
- Lowercase, hyphens only, no special chars
- 3-7 words long
- Specific enough to be findable later (avoid `do-the-thing`)
- No date prefix in the slug itself (filename gets the date prefix)

Title: a one-line description of what the pinned item is. Sentence-case, no trailing period. Example: `Investigate why X happens under Y conditions`.

### Step 3: Capture context

A placeholder is only useful if a future-you can re-orient. Include:
- **What surfaced this** — the discussion / file / commit / decision that prompted the pin
- **Concrete references** — file paths, commit SHAs, line numbers, related slugs, links
- **What's known so far** — the user's current understanding (one paragraph max)
- **What needs deciding** — the open questions that defer-and-think-later is dodging right now
- **Out of scope** — anything the user explicitly said is NOT part of this

Pull these from the conversation context, the relevant memories, and (if needed) a quick `git log` or file read. Do NOT do deep investigation — that would defeat the friction-free goal. If the context is thin, write a thin placeholder; the user can expand it when they `/project <spec-path>`.

### Step 4: Determine `depends_on`

Default: `[]`. Add deps only if the conversation context makes it obvious that this work blocks on another epic. Examples:
- "Save for later, after the cutover finishes" → `depends_on: [platform-cutover-pre-flight-blockers]`
- "Park this until the cutover ships" → same
- Plain "save for later" → `[]`

Use existing slugs from the dashboard. Don't invent new ones.

### Step 5: Write the spec

File: `<data_root>/projects/<name>/design/specs/YYYY-MM-DD-<slug>.md` where `<name>` is the routed
project (the `project:` value below) and YYYY-MM-DD is today's date.

Frontmatter (exact shape — the dashboard parses these fields):

```yaml
---
slug: <slug>
title: <one-line title>
current_state: speccing
depends_on: []
project: <an installed project name (the stem of a ~/.agentflow/config/projects/*.md file), or `personal` / `other`>
---
```

**`project:` is required for new pins.** The value is the stem of an installed `~/.agentflow/config/projects/*.md` file (each project's `aliases` supply the cue words used for inference above), or one of the two Forced fallback buckets:

| Value | When to use |
|---|---|
| `<installed project name>` | Work that belongs to an installed project — matched via that project's `aliases`. |
| `personal` | Personal errands, learning goals, life admin. Explicitly personal, not cross-cutting. |
| `other` | Genuinely cross-cutting, one-off, or a project not yet installed. Re-bucket later. |

The `project:` field is consumed by the wiki-mirror system (skills that mirror specs and plans into `wiki/epics/<project>/<slug>/`). Missing `project:` would route a mirror to `_unsorted/` — workable but findability suffers.

**Backward compat — existing specs without `project:` continue to load.** Frontmatter parsers read the field leniently and treat it as optional; legacy specs already on disk load exactly as before. The mirror-routing system feature-detects on the field and falls back to `_unsorted/` when absent. The `project:` field is required for **new** pins written by this skill, not retroactively enforced on the existing corpus.

Body sections (use these headers; skip any that have no content rather than writing "TBD"):

```markdown
# <Title>

**Date:** YYYY-MM-DD
**Slug:** <slug>
**Status:** speccing
**Tier:** <small | medium | large>  (estimate; small = single-function fix, medium = single-file feature, large = multi-file)
**Discovered during:** <brief context — what session, what topic prompted the pin>

## Problem

<What's the thing that needs solving / investigating? Plain language. 2-5 sentences.>

## Goal

<What does "done" look like? One paragraph.>

## Context to recover

<Concrete references the future-you will need: file paths, commit SHAs, related slugs, links. Use bullets.>

## Open questions

<What does deferring let us avoid deciding right now? List them. The expanded spec will resolve these.>

## Out of scope

<What's explicitly NOT this work. Helps a future expansion stay tight.>

## Reference

<Links to memories, prior specs, conversation logs, etc.>
```

Use the Write tool, not Bash heredocs (the file may contain markdown that breaks shell quoting).

### Step 6: Confirm + verify

Verify the spec landed on disk and is picked up by the survey (set-membership + file-exists, no server round-trip):
```python
from agentflow.config import load_environment
from agentflow.epic_survey import survey_epics

env = load_environment()
records = survey_epics(env.data_root, env.mtime_cutoff_iso)
seen = any(r.slug == "<slug>" for r in records)
```

**This call is deliberately PROJECT-WIDE — `project=` is omitted on purpose, not by oversight.** It is a set-membership *confirmation* that the file you just wrote is discoverable at all; scoping it would turn a spec pinned under another project into a false "not surveyed" failure. The builder loops pass `project=<name>` because they select work from their survey; this one never selects anything.

If the file exists at `<path>` but `<slug>` isn't in the survey, the record fell outside the survey's globs or the `mtime_cutoff_iso` floor — surface "spec written at `<path>` but not surveyed; check it sits under `data_root/projects/<name>/design/specs/` and its mtime is past the cutoff." and stop. The spec is already on disk regardless, so never treat this as a hard failure.

If `seen` is true, proceed to mirror step:

**Mirror to wiki (feature-detect):** If `<vault.mirror_helper>` exists AND is executable, invoke:
```bash
# All three come from THIS wake's resolved block. The helper falls back to its own
# literals for every one of them, so omitting any is not a no-op: the vault path decides
# where documents land, the project list decides which projects route by name rather
# than to _unsorted/, and the lock dir keeps the lock out of a synced folder where two
# machines can both believe they hold it.
WIKI_VAULT_PATH="<vault_root>" AGENTFLOW_PROJECTS="<vault_projects>" \
  AGENTFLOW_LOCK_DIR="<lock_dir>" bash <vault.mirror_helper> "<canonical-spec-path>" spec
```

This is one of three mirror-write touchpoints across the skill suite (backlog and project pass a spec, solution passes a plan); see `<vault.root>/CLAUDE.md` "Mirror System" for the vault layout, the `project:` routing rules, and the full touchpoint list.

If the mirror helper doesn't exist or isn't executable, skip silently. If the invocation fails, warn the user but do NOT abort the pin — the canonical spec is already on disk and dashboard-visible.

**Confirmation message:** Send to the user:
> Pinned `<slug>` — surveyed in the planning queue and at `projects/<name>/design/specs/<slug>.md`

If the mirror failed, replace the second clause with: `— visible on dashboard (wiki mirror unavailable).`

## Examples

### Example 1: pin during conversation

User has been discussing why pythonw silently dies on Windows. User says: *"Put a pin in that — I'll fix it after cutover."*

You write `<data_root>/projects/<name>/design/specs/2026-05-10-pythonw-silent-death-fix.md`:
- slug: `pythonw-silent-death-fix`
- depends_on: `[platform-cutover-pre-flight-blockers]` (because of "after cutover")
- Body captures the diagnosis, the workaround used, file path + line number, link to the prior memory entry that documented it last time

Reply: *"Pinned `pythonw-silent-death-fix` — visible on dashboard."*

### Example 2: pin a vague aside

User says: *"Hmm, also I should think about the connector layer eventually. Defer that."*

You ask: *"Connector layer — Slack/Linear/Jira/GitHub-Issues integration (per your memory notes)? Or something else?"*

User confirms.

You write `<data_root>/projects/<name>/design/specs/2026-05-10-connector-layer-pre-launch.md` with the project memory link as primary context.

### Example 3: pin a chore the user wanted "off the table"

User says: *"Save the README rewrite for later, not blocking the release."*

You write a placeholder with `depends_on: []`, body explains the README rewrite was discussed in this session, lists what's currently wrong with it.

If the README rewrite is genuinely a 5-minute chore (e.g., "fix the broken link to the architecture doc"), DON'T pin — surface inline: *"That's small enough to just do. Want me to fix it now?"*

## Constraints

- One pin per invocation. If the user lists 5 things to defer, ask if they want one bundled spec or 5 separate ones — do NOT silently bundle or silently split.
- Never write more than 60 lines into the placeholder body. If a placeholder is getting longer than that, you're doing too much — that's the future spec-expansion's job.
- Do NOT modify any other dashboard specs as part of pinning. The pin is additive only.
- Do NOT auto-launch `/project` on the pin after writing it. Pinning IS the deferral; immediately starting it would defeat the purpose.
- Date prefix on the filename uses TODAY's local date (the date <person.name> is currently working on, per the session context's `currentDate`). Do not use a future or past date.
- If a pin with the same slug already exists on disk, surface that to the user — *"slug `<X>` already exists at `<path>`. Update it, or pick a different slug?"* — do NOT silently overwrite.

## Failure modes

| Failure | Action |
|---|---|
| Topic genuinely ambiguous after one clarifying question | Stop. Ask the user to retry with more specificity. Don't keep asking. |
| Slug collision with existing spec | Surface to user with both paths; let them pick update-or-rename. |
| `<data_root>/projects/<name>/design/specs/` doesn't exist | Surface — something's wrong with the install/scaffold. Don't silently `mkdir -p`. |
| User said "pin" but meant "remember" (e.g., "pin: I prefer X over Y") | Re-route to memory system. The lifecycle is different — preferences belong in `~/.claude/projects/.../memory/`, not as dashboard specs. |
