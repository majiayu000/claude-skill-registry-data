---
name: handoff
category: orchestration
description: |
  Fresh-session handoff doc drafting. Produces a stable, single-file
  human-readable narrative state for the NEXT agent context (fresh
  session, after `/clear`, after persist iteration, after a tab close).
  The artifact lives at `docs/handoffs/YYYY-MM-DD-<arc>.md` and follows
  a stable shape: TL;DR + State-of-the-world (P15 snapshot) +
  What-was-delivered (PR table with SHAs) + First action + Pickup state.
  Distinct from P12 persist's `PROMPT.md` (machine-state for
  cross-context loop) and the P1 Bridge session log (raw transcript) —
  the handoff is the narrative bridge a human reads in ten seconds and
  a fresh agent reads in thirty.
  Use when: (1) ending a substantive session that another agent will
  continue, (2) preparing a fresh-session pickup point mid-arc,
  (3) needing to compress a multi-PR arc into a single resumable
  document, (4) the user says "write a handoff" / "fresh-session
  handoff" / "let me come back to this tomorrow".
  Triggers on "handoff", "fresh-session", "fresh session", "pickup",
  "where we are", "leave off", "for the next session", "resume tomorrow",
  "stage continuation", "for the next agent".
---

# handoff — Fresh-session handoff doc skill

**Compress a substantive arc into a single resumable doc the next agent
loads cold.**

## Why this skill exists

Across the 7-day window 2026-05-18 → 2026-05-24, **nine fresh-session
handoff docs** were drafted by hand. Six landed in `docs/handoffs/`
(Houston substrate completion, BRO-1208 streaming hang, Houston
advanced-settings wave, Life-Houston H1 runner refactor, Stage 1
fresh-session, etc.) and three landed in `docs/conversations/HANDOFF-*`
(substrate completion arc, BRO-1180 four pillars, Spec J real-Anthropic
smoke). All shared the same shape — the recurrence met rule-of-three
(P16) ~3× over.

Before this skill, the writer rebuilt the structure each time: which
sections appear, what order, what level of detail per section, which
git SHAs to cite, how to phrase the "first action". The skill captures
the canonical shape so subsequent handoffs are produced consistently
in a single pass.

## What this skill provides

1. **Template** (`references/handoff-template.md`) — the canonical
   section structure, with annotations explaining each section's
   purpose and stop condition.
2. **Anti-patterns** below — what NOT to include (the failure modes
   that produce unusable handoffs).
3. **Composition rules** — when to use this skill alone vs. compose
   with `persist` (P12), `bookkeeping`, or `make-spec`.

## When to invoke

- **End of substantive in-session work** that another agent (or the
  same user in a fresh context) will resume.
- **Mid-arc snapshot** when the user wants to break before
  continuing in a fresh context (this
  is the *handoff* half of P12 — `PROMPT.md` is the *state-replay* half).
- **Stage boundary** in a multi-stage arc (Stage 0 → Stage 1 →
  Stage 2 pattern that appeared 4× in the Houston/Life-Houston work).
- **Before merging the last PR of a substantial arc** so the next
  agent inherits the arc's lessons and remaining loose ends.

## Carve-outs (do not invoke)

- Single-PR work that's fully self-contained → just the PR description suffices.
- Pure read questions → no handoff needed.
- Continuation of work in the same context → no fresh-context boundary.
- Personal-life retrospective → use the Telos surface, not this.

## The canonical shape (mirrors `references/handoff-template.md`)

```
---
arc: <slug>                 # stable queue slug (== broomva handoff push --as)
specs: []                   # related spec handles → /d/<handle>
ticket: BRO-NNNN
priority: 0
# queue_id / queue_slug / queue_version / queue_status / queue_url / pushed_at
# are written back by `broomva handoff push` — do not hand-edit.
---

# <Arc name> — <Stage / Phase>

**TL;DR.** <One-sentence summary of where we are; ends with the FIRST ACTION.>

## State of the world (P15 snapshot YYYY-MM-DD)

- **<Repo 1>** — <branch>, ahead N / behind M vs origin/main. Last commits …
- **<Repo 2>** — <branch>, last merged PRs with SHAs.
- **<Running services / dev daemons>** — STILL RUNNING / DEAD; restart command if dead.

## What <arc> delivered (so the next agent doesn't redo it)

| PR | Crate(s) / files | What it gave |
|----|------------------|--------------|
| #N | … | … |

## E2E proof (re-runnable any time the prereqs hold)

```bash
<exact command>
# Expected: <observable output>
```

## First action

<The single next step the fresh agent should take, with the exact command
or file path. NO ambiguity. NO "consider X or Y" — pick one.>

## Pickup state (what's open)

- [ ] <open thread 1>
- [ ] <open thread 2>

## Related context

- Lessons doc: `docs/<...>.md`
- Linear: BRO-NNNN
- Prior handoff: `docs/handoffs/<earlier>.md`
```

## The five anti-patterns this skill exists to prevent

| Anti-pattern | Failure mode | Fix |
|---|---|---|
| **Missing P15 snapshot** | Fresh agent reasons against stale state (last-seen instead of current); duplicates work or conflicts with unmerged work. | Always include git status + branch + ahead/behind + open PRs + daemon state. |
| **No "first action" / vague "first action"** | Fresh agent spends 10+ minutes triangulating where to start. | Pick ONE concrete next step with the exact command/file path. If ambiguous, pick anyway and document the alternative as "if blocked, try X". |
| **PR table without SHAs** | Fresh agent can't reproduce the substrate state; doesn't know whether a PR landed or just opened. | Always cite the merge SHA next to each delivered PR. |
| **Lessons buried in prose** | Lessons silently lost because no skim-reader will find them in paragraph 8. | Pull lessons into a labeled section OR link to a separate `<arc>-lessons.md`. |
| **Aspirational scope** | "Next we should also do A, B, C, D, E …" with no priority. Fresh agent thrashes. | List ONLY the next 1–3 actions. Defer A, B, C, D, E to Linear backlog or a separate planning doc. |

## File placement

- **Workspace handoff** (cross-repo or workspace-governance): `docs/handoffs/YYYY-MM-DD-<slug>.md`
- **Project-local handoff** (single repo): `<repo>/docs/handoffs/YYYY-MM-DD-<slug>.md`
- **Legacy location** (still acceptable, gradually migrate): `docs/conversations/HANDOFF-YYYY-MM-DD-<slug>.md`

Filename slug should name the **arc**, not the date. The date is the
mtime, the slug is the identifier.

## Push to the Maestro queue (BRO-1415)

A handoff on local disk is invisible to the next session until someone
opens the file. **After writing the `.md`, push it to the Maestro
handoff queue** so it surfaces at
[`broomva.tech/maestro/queue`](https://broomva.tech/maestro/queue) —
the realtime, owner-gated queue that articulates *what to hand off
next*, relates each handoff to its HTML specs, and exposes the
copy-to-continue trigger (the same Copy/Continue a fresh session uses
on the spec board, BRO-1399).

```bash
broomva handoff push docs/handoffs/2026-06-05-<arc>.md \
  --as <arc> \
  --spec <spec-handle> \          # repeatable — the /d/<handle> specs this relates to
  --ticket BRO-NNNN
# → Queue: https://broomva.tech/maestro/queue
```

The CLI auto-extracts the **title** (first `# ` heading), **TL;DR**
(the `**TL;DR.**` lead line), and **first action** (the `## First
action` section → the Copy-button payload), and records git provenance
(repo / branch / commit / path). Re-pushing the same `--as <arc>`
appends a version and supersedes the prior queued entry, so iterating a
handoff is safe. This is a **reflex, not a request** (P6 · Bookkeeping):
push the handoff, then report the queue URL — don't ask permission first.

| Field | Source | Used for |
|---|---|---|
| `title` | first `# ` heading | queue card headline |
| `tldr` | `**TL;DR.**` line | queue card subtitle |
| `firstAction` | `## First action` section | the **Copy** button payload |
| `specRefs` | `--spec <handle>` (repeatable) **or** frontmatter `specs` | related-spec chips → `/d/<handle>` |

### Frontmatter is the control surface (BRO-1418)

The handoff `.md` carries a YAML frontmatter block that is **both the
publish input and the queue reference** (see
`references/handoff-template.md`). You set `arc` / `specs` / `ticket` /
`priority`; `broomva handoff push` reads them (CLI flags override) and
**writes the queue identity back** into the same block:

```yaml
---
arc: maestro-handoff-queue
specs: [maestro, maestro-relay-phase-1b]
ticket: BRO-1415
priority: 0
# --- written back by `broomva handoff push` — do not hand-edit ---
queue_id: a1b2c3d4e5f6
queue_slug: maestro-handoff-queue
queue_version: 2
queue_status: in_progress
queue_url: https://broomva.tech/maestro/queue
pushed_at: 2026-06-06T01:55:00Z
---
```

So the file **references its own queue entry**. Re-pushing the same arc
appends a version and updates the frontmatter in place — iterating a
handoff is safe and traceable. The body sent to the server is the
narrative with the frontmatter stripped. (`--no-write-back` opts out.)

### Managing the lifecycle from the file

The lifecycle verbs accept `<file|id>` — pass the handoff file and the
CLI resolves `queue_id` from its frontmatter and mirrors the new status
back, so the file stays the source of truth:

```bash
broomva handoff pick-up docs/handoffs/<arc>.md   # queued → in_progress
broomva handoff done    docs/handoffs/<arc>.md   # → done   (mirrors queue_status)
broomva handoff archive docs/handoffs/<arc>.md   # set aside, off the active queue
broomva handoff requeue docs/handoffs/<arc>.md   # back to waiting
broomva handoff rm      docs/handoffs/<arc>.md   # delete + clear the queue_* block
broomva handoff list                             # the active queue
```

**When you finish an arc, mark its handoff `done`** — it keeps the queue
honest (the analytics throughput + pickup-latency metrics depend on it).
This too is a reflex, not a request.

> **Prereq:** frontmatter publish + lifecycle ship in the `broomva` CLI
> ≥ the BRO-1418 release (the queue itself is BRO-1415). If `broomva
> handoff` is unknown or lacks the lifecycle verbs, rebuild
> (`cargo install --path crates/broomva-cli` in `broomva.tech`) or fall
> back to opening the queue and pasting — but the canonical path is the
> CLI push.

## Composition rules

| Compose with | When |
|---|---|
| **`persist` (P12)** | When the handoff is the prelude to a fresh-context loop. The handoff is the human-readable narrative; `PROMPT.md` is the machine-readable state. Both exist; they're different artifacts. |
| **`bookkeeping`** | When the handoff cites lessons that should also live as entity pages (`research/entities/pattern/<lesson>.md`). File the lesson via `bookkeeping file` AFTER the handoff is written; reference the entity in the handoff's "Related context" section. |
| **`make-spec`** | When the handoff is dense enough that a separate HTML companion (spec / plan) is warranted. The handoff stays markdown; the companion is HTML. P18 audience rule: handoff is agent-loaded → markdown. |
| **`spec-contract`** | Whenever that companion is a spec / plan / ADR / **RFD** rather than a narrative. Applies to an existing document the handoff merely CITES, not only to one it creates — a handoff can run standalone, and its own checklist checks handoff structure, not the artifact it points at. `make-spec` decides how it looks; `spec-contract` decides what is in it — run `spec_check.py` on the companion before the handoff cites it, or the next agent inherits a document that states decisions without stating what they cost to reverse. |
| **`/p9 watch`** | If the handoff is being written mid-CI (after a push, before merge), include the watch command + PR number so the next agent doesn't restart the wait. |
| **`handback`** | Whenever the arc is stopping on something only a *person* can resolve. The two are siblings with different readers: `handback` is the chat message the **human** acts on (asks first, each with a default); this handoff is what the **next agent** loads. The handback's Detail block links here, and the narrative — the review sagas, the corrections, the what-happened prose — belongs in this document rather than in that message. |

## Validation (handoff self-test)

A well-formed handoff passes all five checks:

- [ ] **TL;DR** is one sentence and names the first action explicitly
- [ ] **P15 snapshot** covers every repo touched in the arc + every long-running daemon
- [ ] **PR table** cites merge SHAs (not just PR numbers)
- [ ] **First action** is a single concrete step with the exact command or file path
- [ ] **Pickup state** lists ≤5 open threads (more than 5 = aspirational scope; split into a separate plan doc)
- [ ] **Pushed to the queue** via `broomva handoff push … --spec <handle>` so the next session sees it at `/maestro/queue` (reflex, not a request)

## References

- Canonical examples: `docs/handoffs/2026-05-24-stage1-fresh-session.md`, `docs/handoffs/2026-05-23-life-houston-h1-runner-refactor.md`, `docs/handoffs/2026-05-22-bro-1208-streaming-hang-handoff.md`
- Template: `references/handoff-template.md`
- Related primitive: P12 persist (cross-context loop); P15 state-snapshot; P18 audience
- Related skills: `persist`, `bookkeeping`, `make-spec`, `autonomous`
