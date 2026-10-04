---
name: kickoff-prompt
description: Format and quality bar for the `## Kickoff` section that lives in every spec. Defines a paste-ready cold-start prompt the user can drop into a fresh session.
compatibility: opencode
metadata:
  audience: any-agent
  purpose: cold-session-start
---

## What I do

Define the shape of the `## Kickoff` section in `spec.md` — a terse,
model-optimized cold-start prompt the user pastes into a fresh session
when they want to pick this spec back up after a context break.

A kickoff prompt is **not** a documentation summary. It's a *prompt*:
- 60–120 tokens (hard cap 200).
- Tells a fresh model what this spec is, where it stands, where to pick
  up, and which 2–5 files to open first.
- Aggressive on signal-to-noise. The spec body has the documentation;
  the kickoff has only what gets you productive in 30 seconds.

The kickoff is **part of the spec**, not a projection. Skills (`/design`,
`/deliver`, `/diagnose`) write it inline as they author or mutate the
spec. There is no auto-refresh hook. If a kickoff goes stale, the fix
is to re-run the workflow or hand-edit — same as any other spec content.

## When to write or update me

- **`/design`** — write a fresh `## Kickoff` as part of scaffolding the
  new spec, between `## Goal` and `## Problem`.
- **`/deliver`** — rewrite `## Kickoff` when the spec's status flips
  (planning → delivering, delivering → completed) or when a meaningful
  chunk lands. The "Pick up at:" line should always reflect *now*, not
  "two commits ago."
- **`/diagnose`** — same pattern when bug specs flip from `triaging` →
  `delivering`.
- **Hand-edit** — anytime the user changes direction or wants to tune
  the opener. The spec is source of truth; edit it like any other
  section.

A kickoff that says *"pick up at X"* when X already shipped is misleading.
A kickoff that's still accurate doesn't need refreshing for refresh's sake.

## Format

```markdown
## Kickoff

<1 line: what this spec is, in the user's vocabulary. Avoid jargon
the user wouldn't say themselves.>

**Status:** <planning|delivering|blocked|in-review> — <last meaningful
turn, 1 line>

**Pick up at:** <concrete next step, 1–2 lines. Specific enough that
a fresh model can act without re-reading the whole spec.>

→ <runnable pointer: spec path, slash command, or shell command>

**Files:** <2–5 path:line refs the model will need to open first>
**Skip:** <1 line of approaches already rejected — only if non-empty>
```

Sections after `Files:` are omitted entirely when empty. Don't write
`Skip: (none)`; just leave the line out.

## Section guidance

- **First line (the what)** — phrase as the user would say it aloud, not
  as the spec title. Example: *"Adds `## Kickoff` sections to every spec
  and a `hero queue` command for the ranked backlog."* — the spec title
  is more formal; the kickoff line is the elevator-blurb.
- **Status** — one of `planning`, `delivering`, `blocked`, `in-review`.
  Append a half-sentence on the *last meaningful turn* — what just
  happened that a fresh session needs to know. Don't describe everything
  done so far; the spec body has that.
- **Pick up at** — the *one specific thing* a fresh session should
  attempt. Don't list options. If there are forks, pick the highest-leverage
  next step and name only that. The user can re-tune the kickoff if they
  pivot.
- **→ pointer** — must be runnable as-is. A spec path (`.hero/specs/foo/spec.md`),
  a slash command (`/deliver foo`), or a shell command. Not a sentence.
- **Files** — 2–5 file paths with optional `:line` markers. These are the
  files the fresh session will need to open first. Pick load-bearing
  ones, not every file in `## Changes`.
- **Skip** — gold when present. One line per approach already rejected,
  so the next session doesn't re-suggest it. Omit the heading entirely
  when there's nothing to skip.

## Quality bar

A good kickoff is one a fresh session can paste and immediately be
productive — no follow-up "what's the spec?" or "where are the files?"
questions.

The new session should know after reading it:
1. **What this spec is** — first line.
2. **Where it stands now** — Status line.
3. **What to attempt next** — Pick up at + → pointer.
4. **Which files matter** — Files line.
5. **What not to try** — Skip line, when present.

If you can't picture a fresh session being productive after pasting
the kickoff, add detail. If it's becoming a transcript of everything
done, cut detail.

**Hard cap on kickoff body: 200 tokens. Target: 60–120.** If it's
running over, the spec body is doing the kickoff's job — point at the
spec body and trim.

## Worked examples

### Good — small spec, mid-delivery

```markdown
## Kickoff

<!-- drift-test:ignore (illustrative: this kickoff documents a phantom-command bug — `hero nudge` is intentionally stale) -->
Renames stale docs from `hero nudge` to `hero relevant` so file-aware
context examples match the current CLI.

**Status:** delivering — CLI examples are fixed; MCP docs still need a
note that the tool remains named `hero_nudge`.

<!-- drift-test:ignore (illustrative: same kickoff example as above) -->
**Pick up at:** sweep docs for `hero nudge` and replace user-facing CLI
examples with `hero relevant`, while leaving MCP tool names intact.

→ `rg "hero nudge|hero_nudge" docs README.md GETTING-STARTED.md`

**Files:** README.md, GETTING-STARTED.md, docs/cli/search-and-context.md
**Skip:** renaming `hero_nudge` in MCP docs — that tool name is still real.
```

### Good — large spec, planning

```markdown
## Kickoff

Adds `## Kickoff` sections to every spec and a root-level `hero queue`
command so the user can see all ready-to-work specs at a glance and
copy-paste a session opener for any of them.

**Status:** planning — spec just landed, no code yet.

**Pick up at:** start with the parser change — add `Pinned bool` to
`internal/spec/spec.go` and a `Kickoff()` accessor reading from
`Sections["kickoff"]`. Tests next. Bigger work (selector + commands)
is Phase 2.

→ `.hero/specs/kickoff-prompts-queue/spec.md`

**Files:** `internal/spec/spec.go`, `internal/spec/spec_test.go`, `skills/kickoff-prompt.md`
```

### Anti-pattern — bloated, vague

```markdown
## Kickoff

This spec is about improving developer experience around session
continuity by introducing a structured way to capture the essential
context needed to resume work after a break. It involves several
components including format definitions, command surfaces, integration
with existing workflows, and tooling support. We have considered
several approaches and settled on a hybrid model that balances
flexibility with consistency.

**Status:** in progress

**Pick up at:** various tasks remain. See spec body for full list.

**Files:** see Changes section
```

What's wrong: prose where pointers should be, no concrete next step,
no file paths, no actionable pointer, lists nothing the user can paste
and act on. The spec body should be doing this work; the kickoff has
failed if it just defers to the body.

## Composing with related skills

- **`next-md`** — governs the `.hero/NEXT.md` agent half (this turn's
  status). Different surface: NEXT.md is the *current session* handoff;
  the kickoff is the *cold-start* prompt for any spec in the queue.
  Both can co-exist; both have their own format.
- **`end-of-turn-recap`** — governs the closing message of the current
  turn. When the recap rule's spin-off offer points at a spec, it
  references the spec's kickoff (`hero_kickoff <slug>`) rather than
  reproducing prompt content inline.
- **`hero queue` / `hero list --format kickoff`** — the surfacing
  layer. The selector picks ready specs and renders their `## Kickoff`
  bodies. The kickoff format is what makes the queue useful.

## What not to do

- Don't reproduce the spec body. Reference, don't repeat.
- Don't list every file in `## Changes`. Pick the 2–5 the fresh
  session needs first.
- Don't write a paragraph where one line works.
- Don't leave stale kickoffs around. If `Pick up at:` is wrong, fix it.
- Don't put commit hashes, branch names, or session-specific runtime
  state in the kickoff. That belongs in NEXT.md, not the spec.
- Don't forget the `→ pointer` line — runnable, not prose.
