---
name: start-thread
description: >-
  Use when opening OR RESUMING a unit of work — a feature, bug, research spike, refactor, an
  experiment — that should survive context loss in its own scratch workspace with a handoff doc.
  Idempotent create-or-resume: a fresh topic gets a scaffolded STATE doc; an existing thread gets a
  resume briefing (STATE + live git/PR deltas) and you keep working — one command, day 1 or day 20.
  Also when asked to "start a thread", "new thread", "continue the thread", "resume", "track this
  work", or "make a workspace for this".
argument-hint: "[topic, e.g. fix-auth-redirect]"
allowed-tools: Bash(git *), Bash(ls *), Bash(mkdir *), Bash(bun *)
---

# Start or resume a thread — scratch workspace with a handoff doc

Topic requested: **$ARGUMENTS**

**Project + config:**
!`bun "${CLAUDE_PLUGIN_ROOT}/scripts/where.ts"`

**Current branch:** !`git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "(not a git repo)"`

**Existing threads:**
!`bun "${CLAUDE_PLUGIN_ROOT}/scripts/threads.ts" --slugs`

## Do this

1. **If `$ARGUMENTS` is empty**, ask for the topic — don't guess.
2. **Normalize** the topic to a slug — run via Bash:
   `bun "${CLAUDE_PLUGIN_ROOT}/scripts/slug.ts" "<topic>"`
   (one shared identity function — never re-implement slugging by hand; if the variable shows as a
   literal, use the `plugin root:` path from the injected block above). With `ticket_system: none`
   a thread is any unit of work; ticket-system adapters may extend this later.
3. **If `<scratch_root>/<slug>/` already has a STATE doc → RESUME.** This is the normal day-2 path,
   not an error: no questions, no "want me to open it?" menu — brief and get to work. Treat slugs
   as the SAME thread when they match ignoring case and separators (`CP-1758` ≡ `cp-1758` ≡
   `cp1758` — the `normalizeForMatch` rule in `scripts/lib/identity.ts`): a near-match in the
   existing-threads list above resumes THAT thread. Never overwrite or re-scaffold an existing
   STATE (skip steps 4–6 entirely). Do all of this:
   1. **Read the whole STATE doc** — Status, the ask, plan, current state, open/deferred.
   2. **Pull live deltas** (parallel; each optional-degrade — an unreachable source gets a one-line
      note, never stalls the resume): current branch; a `git worktree list` / `git branch --list`
      match on the slug; if a matching worktree/branch exists — `git status --porcelain` (dirty
      files) and `gh pr list --head <branch> --state all --json number,state,reviewDecision --limit 1`
      (when `gh` resolves).
   3. **Report a resume briefing** — where the user left off (Status, next plan step, open items),
      then **what changed since** (branch moved / PR merged / dirty files). Explicitly flag any live
      fact that CONTRADICTS the STATE. End ready to work — not with a menu.
   4. Resume is **read-only on the STATE doc** — flag drift in the briefing; the session updates
      STATE as work actually proceeds (the `state-freshness-guard` Stop hook enforces this before
      the session ends).
4. **Seed the ask from the conversation** — there is no ticket system to pull from. If the goal
   isn't clear from context, ask for one line. Mark anything unknown as TODO rather than inventing.
5. **Create** `<scratch_root>/<slug>/` and write the STATE doc from the template below, filling
   the frontmatter (`title: <slug>` · `kind: thread` · `summary:` one-line blurb) and **The ask**.
   Use the `state_basename` from the injected config block (default `STATE.md`).
6. **Version-control check:** if this is a git repo and `<scratch_root>` is not ignored
   (`git check-ignore -q <scratch_root>` fails), ASK whether to add it to `.gitignore` — some
   people want the notebook versioned, some never want notes in PRs. Don't silently do either.
7. **Report** the path created and a one-line summary. (No need to run /ccx:save-state for
   indexing — the `auto-compile-index` hook recompiles the INDEX on every STATE write.)

### STATE template

```markdown
---
title: <slug>
kind: thread
summary: '<one-line INDEX blurb — the live working-state; YAML single-quoted, double any apostrophe>'
---

# <slug> — <short title> · handoff state

**Hub:** [[INDEX]]
**Status:** <one-line live status — done / in-flight / blocked + the key facts, as of <date>>

> **Read this first if context was cleared.** All <slug> work lives in `<scratch_root>/<slug>/` —
> throwaway scripts, probes, and notes stay here, organized per thread, never in the repo or a PR.
> One-off scripts: run from the project root, e.g. `<oneoff_script_runner> <scratch_root>/<slug>/probe.<ext>`.

## The ask (narrowed)
- <one-line goal — from the conversation; TODO if not yet agreed>
- Scope right now = _(TODO: fill when scope is agreed — what's in / explicitly out)_.
- **CORE PRINCIPLE — DATA-DRIVEN.** Derive values/options/categories from real data in this
  project — not from an assumption. If a spec looks like a generated example, confirm it against
  the source before building on it.

## Where things are
- Branch: `<branch>` (based off `<base>`).
- Source data / inputs: <paths, tables, endpoints — whatever this thread feeds on>.

## Plan (in run order)
1. <step> → <output>

## Current state (as of <date>)
- <what exists, what's verified, what's pending>

## Open / deferred (don't start without the user)
- <items, with any deadlines>
```
