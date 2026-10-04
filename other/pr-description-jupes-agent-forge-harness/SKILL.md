---
name: pr-description
description: Canonical PR description template for every PR shipped from this harness, with a validator that enforces the required sections. Use when opening or editing a PR (the /ship and /forge-ship steps), or when asked for the standard PR format or to check a PR body.
---

# pr-description

The single source of truth for **how every Agent Forge PR body is written**. All ship paths
(`/ship`, `/forge-ship`, `/forgemaster`'s ship phase) compose the PR body from this template and
validate it before `gh pr create`.

The template lives at [references/pr-template.md](references/pr-template.md) — edit that file to
change the standard; everything else references it.

## When to Use

- Any time a PR is opened or its body edited from this harness.
- When the user asks for "the PR format / template" or to check that a PR body conforms.

## Required sections

Every PR body MUST contain these H2 headings, each filled (no leftover placeholders):

| Section | Holds |
|---------|-------|
| `## What Changed` | The change in plain language + concrete edits |
| `## Why It's Needed` | Motivation: the problem, need, or bug it addresses |
| `## How It Was Tested` | Gates run, automated suites, manual steps |
| `## Test Evidence` | Real proof — pasted command output / counts, not a claim |
| `## Risk & Rollback` | Blast radius and the undo path |
| `## Linked Issues & AC Trace` | `Closes <beads-id>` + acceptance-criterion → evidence table |

The first four are the harness baseline (what / why / how-tested / evidence). **Risk & Rollback**
and **Linked Issues & AC Trace** are the harness additions — they make a PR reviewable (knowable
blast radius) and traceable (every acceptance criterion mapped to evidence), matching the
Beads-first, test-evidence rules in `CLAUDE.md`.

## Process

### 1. Start from the template

```bash
cp .claude/skills/pr-description/references/pr-template.md .tmp/work/pr-body.md
```

Fill every section. For a `/forge-ship` run, the ship report (`reports/<slug>-ship.md`) already
contains the narrative and walkthrough — map it into the template sections rather than duplicating
prose. Paste **actual** test output into `## Test Evidence`; never green-wash.

### 2. Validate before creating the PR

```bash
bun run .claude/skills/pr-description/scripts/check-pr-body.ts .tmp/work/pr-body.md
```

The validator emits `{ ok, data: { present, missing, empty }, error }` and exits non-zero if any
required section is missing or left as a placeholder. Fix and re-run until `ok: true`.

### 3. Open or update the PR

```bash
gh pr create --base <base> --title "<title>" --body "$(cat .tmp/work/pr-body.md)"
# or, on an existing PR:
gh pr edit <n> --body "$(cat .tmp/work/pr-body.md)"
```

To check a PR that already exists:

```bash
gh pr view <n> --json body -q .body | bun run .claude/skills/pr-description/scripts/check-pr-body.ts -
```

## Exit Criteria

- [ ] PR body contains all six required sections, each filled.
- [ ] `## Test Evidence` holds real output, not a promise.
- [ ] `check-pr-body.ts` reports `ok: true`.
