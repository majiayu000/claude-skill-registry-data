---
name: epic-commands
description: Procedures for `josh epic:audit`, `epic:next`, `epic:bundle`, an epic child in another repository and a `needs-decision` decision. Read it before any of them and when `epic:bundle` places a filed issue.
---

# The `josh epic:*` commands

The workflow keywords themselves — `kickoff`, `fullrun`, `halfrun`, `prrun`, `backlogrun` — live in the
`workflow-commands` skill.

## The order they run in

```
epic:audit → find contradictions across the children, and fix what it finds (Tier A)
backlogrun → which calls epic:next each round
```

Settling every `needs-decision` is `backlogrun`'s job: `backlogrun-steps.md` → "Resolve what
the plan can resolve"; a `推奨なし` park → `backlogrun-park.md` → "A park the driver decides". A `pnpm josh backlogrun <E> --only`'s pre-check is `epic:audit`.

Read `execution-waves.md` only when children need an order between groups (a wave boundary, or a child
that must run alone), and `epic-bundle.md` only when a filing's `epic:bundle` answer places the issue.

## Recording a decision

Record it in both places: the epic's `## Decisions` log, and a comment on each child it applies to.
Recording a decision removes that child's `needs-decision` label (Tier A; `backlogrun-park.md` →
"park and continue").

- **Decided as a child joins the epic**: `pnpm josh epic --add … --decision-file` writes both
  (`epic-bundle.md`).
- **About a child the epic already tracks**: `pnpm josh epic --decide <E> <N...> --decision-file
  <path|->` writes the entry, the comments and the label removal; a rerun writes nothing twice.
- A decision that changes one child's scope → state the new `- 規模見積もり:` line in a record naming
  that child alone; `scripts/epic/epic-decide.ts`.

```md
## Decisions

### <the point that was decided>

- 対象: #<N1>, #<N2>
- 採用: <the option taken>
- 却下: <the option rejected>
- 理由: <why the taken option is clearly better>
- 決定日: <YYYY-MM-DD>
```

## Creating an epic

A split into two or more issues always gets an epic (`prompts/collaboration-workflow/issue-template.md`),
created with the command, never by hand:

```bash
pnpm josh epic "<epic-title>" <N1> <N2> ... --rationale-file .josh/tmp/<dir>/rationale.md   # order-free batch
pnpm josh epic "<epic-title>" A B C --rationale-file <path|-> --chain "#A -> #C" --chain "#B -> #C" \
  --order-reason "#A -> #C: <kind> — <reason>" --order-reason "#B -> #C: <kind> — <reason>"   # a join
pnpm josh epic --add <E> D --chain "#C -> #D" --order-reason "#C -> #D: <reason>"
pnpm josh epic "<epic-title>" A B C --rationale-file <path|-> --ordered --order-reason "#A -> #B -> #C: <kind> — <reason>"
# --ordered: a true series only; one --order-reason per chain (docs/josh-commands-backlog.md → "josh epic")
# <kind> on create / --promote: the refusal lists them (scripts/epic/epic-chain-kind.ts)
# --rationale-file <path|-> is required on create / --promote (fills Split rationale; refused when missing or blank)
# --origin <owner/repo#N> adds the backlink
```

After any hand edit run `pnpm josh epic:check <E>` (exit 1 when the body no longer parses).
The epic closes once every task-list child is closed, whichever path closes the last child
(`pnpm josh followup`, `josh issue:measured`, `josh run:merge`); one whose last child a person
closed (`already-done`) closes at the next of those closes, for any child. One with a child whose
state cannot be read is closed by hand. Without `josh`: `issue-template.md`.

## `josh epic:audit <E>` — contradictions across the children

`epic:check` verifies the format; this verifies the children agree. Run it **without being asked**
when a `backlogrun` starts a named epic's children, and right after a child is added or a dependency
changed. **Only errors fail it** (exit 1); the checks are `docs/josh-commands-backlog.md` →
"`josh epic:audit`".

**Fixing what it finds is Tier A** — fix it and record why on the issue. Park with `needs-decision`
only for a design choice nobody has made.

The two `orphan search` findings are about the search, not the children:

- `✖ orphan search: Could not list the open issues…` — **re-run the audit**; nothing to fix or decide.
  If it keeps failing, check `gh auth status` and the rate limit.
- `⚠ orphan search: The open-issue scan hit its …` — the audit passes. Look further by hand if an
  orphan is expected.

**That a child introducing a new label, command, state or artifact updates the existing code
referencing it is checked at planning**, not here: each plan's `### 影響を受ける既存の利用者` section,
drafted by `pnpm josh plan:consumers` and required by `issue:plan`, names every consumer and which
issue fixes it. Label names live in `scripts/issue/issue-labels.ts`.

## `josh epic:next <E…>` — what is runnable

Returns **every** runnable child, bundled per repository with its local checkout; several epics answer
as one pool, prioritized in the order they were named. How it weighs blockers, lanes and nested epics:
`docs/josh-commands-backlog.md` → "`josh epic:next`".

- **Reorder with `pnpm josh epic --add <E> <N> --order-before <M>`** (or `--order-after <M>`), never a
  hand edit. Moving a row does not free a child a chain still holds — the command prints a ⚠️ line.
- **Order two epics with a native `blocked-by` relation and name both** — `epic:next <E1> <E2>`, or
  `backlog:next`.

Children that are not runnable are sorted by **whether waiting helps**, never by label:

| Bucket | Caller does |
| --- | --- |
| Runnable | Run it |
| Waiting on time | Wait and ask again |
| Waiting on a person | Stop and report |

Two things stop the command: a **circular dependency**, and a **disagreement between the epic body
and the `blocked-by` relations**. Only a line that is *nothing but* a chain is a declaration — a prose
line recommending an execution order is a suggestion, not a dependency.

## Epics that span repositories

Write cross-repository children as `owner/repo#N` or a full issue URL; **no local clone is needed to
learn their state** — only to implement.

- **The owner restriction is inherited unchanged**: a different owner is never a target.
- **An epic in another repository is referenced as `owner/repo#N`** — `backlogrun
  joshuafolkken/kit#<E> --only`, `epic:next joshuafolkken/kit#<E> --repo joshuafolkken/app-kit`. A
  bare `#N` is this repository's issue.
- **A candidate printed `(no local checkout)` is never cloned on its own.**

## `josh epic:bundle <N>` — does this new issue belong with one already filed?

Runs right after any filing; **`pnpm josh issue:file` runs it as its last step** — run it by hand only
when that step printed `⚠`. **It recommends and writes nothing; `--apply` writes every placing answer
— `ask` into its `Recommended:` epic, with the decision recorded.**

| Candidates | Do | Tier |
| --- | --- | --- |
| **The new issue itself already has an epic** | Nothing — an issue belongs to at most one | — |
| Already a child of an epic | Add to **that** epic; do not create a second | A |
| Spread across an epic and its **own parent** | Add to the inner epic — the parent already contains it | A |
| Spread across **different** epics | **The `Recommended:` epic** — most related issues, older on a tie; none on a cycle (`epic-bundle.md`) | **A** |
| In no epic, two or more counting the new issue | Create an epic | A |
| No strong signal | Nothing | — |
| **The epic listing was cut short** | **Nothing** — every placing row above is withheld | — |

**A placing answer is acted on with `epic-bundle.md`**. `Nothing to bundle.` needs no further read.
