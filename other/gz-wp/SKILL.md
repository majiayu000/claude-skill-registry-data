---
name: gz-wp
persona: main-session
description: Use to create, attach issues to, move, change, add evidence to or record an issue close on a work package (WP-<NN>-<slug>) through gz wp.
category: governance-infrastructure
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-28
metadata:
  skill-version: "0.3.0"
model: sonnet
---

# gz-wp

Run a work package through its record, lifecycle and change ladder with `gz wp`
(drydock RO-5, `docs/governance/harbor-ro5-work-packages.md`). This is the lean
wielder the operator ruled for tranche 2 ("New lean gz-wp skill (Recommended)",
2026-10-28); RO-12's contractor kit composes it.

## The record

A work package is `delivery` (it names one outcome) or `repair` (it names one or
more GitHub issues and stores its lane). Its record in
`data/catalog/work_packages.json` holds the formal work package (initial
conditions, procedure, test and inspection, system restoration, each text or
`NA`), its objective quality evidence, its planned alterations and its
departures from specification. Never edit the file by hand (ruling 3):

```bash
uv run gz wp new --kind repair --slug <slug> --issue <n> --lane lite [--alias RO-<n>]
uv run gz wp new --kind delivery --slug <slug> --outcome <code> [--alteration ID:replaced:<text>]
uv run gz wp attach <WP-id> --issue <n>
```

Attaching an issue, by `new` or `attach`, also labels it `repair` and comments
the package id on it, aliases in parentheses (ruling 7); the verb creates the
label when the repository lacks it. If `gh` fails, the verb exits 2 and writes
nothing; fix `gh` and re-run.

## Objective quality evidence

The OQE is required from initiation (amendment 1). Record each receipt, commit
or path as the work produces it, so the record stands without explanation:
`uv run gz wp evidence <WP-id> --oqe "<entry>"`. Entries are append-only.

## An issue's close

`ghi-close` records each fixed issue against its repair package (ruling 10):
`uv run gz wp resolve <WP-id> <n> --commit <fix-sha> --reviewer <reviewer>`.
The last issue's close never closes the package; it closes only through Gate 5.

## The lifecycle

One step at a time: `initiated`, `frozen`, `commenced`, `accepted`, `closed`.

1. **Initiate on the operator's words.** Only the operator initiates a work
   package. Pass their words verbatim; never author them.
   `uv run gz wp initiate <WP-id> --operator-text "<their exact words>"`
2. **Freeze after the independent review.** A reviewer who did not write the
   baseline checks each REQ against the nine criteria; the operator approves
   every planned alteration.
   `uv run gz wp freeze <WP-id> --baseline REQ-<n>@<rev> --risk-note "<note>" --review-receipt <id> --approve-alteration <id> --evidence <id>`
3. **Commence** once every surface the package works has its tag hung:
   `uv run gz wp commence <WP-id> --evidence <what was checked>`.
4. **Accept** at final inspection with no tag still hung:
   `uv run gz wp accept <WP-id> --evidence <inspection>`.
5. **Close through Gate 5.** The attestor is the operator and is never
   defaulted. Account every alteration and name each departure still open.
   `uv run gz wp close <WP-id> --decision proceed --attestor g0 --residual-risk "<risk>" --account <alt-id> --evidence <id>`

## The change ladder

Every change to a live package is one `gz wp change` with its rung:

| Rung | Approver | Must carry |
|------|----------|------------|
| `pen_and_ink` | coordinator | `--superseded` |
| `change_order` | operator | `--superseded`, `--work-stopped` (work stops when the need is found) |
| `attachment` | operator | added work inside the boundary, no new tag-outs |
| `supplement` | operator | `--supplement <WP-id>`; a test change by change order is one |
| `alteration` | operator | `--item <id>` (`--configuration-change` for a new one) |
| `departure` | operator | `--item <id> --form deviation\|waiver --duration temporary\|permanent [--clear-by]` |

Work outside the package's general scope is a new work package, never a change.
A departure from specification is recorded only where the work cannot meet its
own approved specification; a difference from the prior shape is not one.

## Read

`uv run gz wp show <WP-id>` prints the record, the state and the history;
`uv run gz validate --catalog` checks the store against RO-5's rulings.

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "I'll fix the JSON directly, it's one field" | The store is edited only through verbs (ruling 3); a hand edit skips the checks `gz validate --catalog` reads. |
| "The operator clearly wants this started" | Initiation carries the operator's words. Without them there is no initiation. |
| "This scope change is small, pen and ink will do" | Pen and ink is administrative. A change to scope, boundary or test is a change order, and work stops. |
| "The close can default the attestor" | Gate 5 is the operator's own act; `--attestor` is never defaulted. |

## Red Flags

- Writing `data/catalog/work_packages.json` with an editor or a script
- An `--operator-text` the operator did not say
- A change order recorded without `--work-stopped`
- Calling a remodel a departure from specification
