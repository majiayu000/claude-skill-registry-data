---
name: product-sdd
description: CTO-posture skill that authors a project's SDD — the architecture-and-cut document, written off the settled SRS and UXD. Requires CTO posture (writes nothing and stops, saying "product-sdd requires CTO posture", if invoked outside a cto session or the cto subagent). Non-interactive by design — every run drafts the whole SDD best-effort, including the parts the CPO or the CDO decides, and writes whatever it cannot settle into a companion open-issues file whose items carry the answering seat's Seat field. On the next round it folds the owner's answered companion into the SDD, retires the answered file whole to a permanent trail, re-raises what stays unsettled, and removes the companion when nothing is left — its absence means the SDD is done. The skill resolves where the files land from the project's Product path. Use when authoring, continuing or revising a product's SDD — write the SDD, cut the architecture into slices, station 5 of the definition sequence. Do not use for upstream documents (product-prd / product-srs / product-uxd / product-design / product-content), the Agari (project-agari), per-change specs (development-specs), or anything downstream (Delivery Plan / FDR / ADR / NFDR).
license: MIT
metadata:
  author: Eyal Golan
  version: "1.0.4"
  created: "2026-10-03"
  category: product-definition
  tags: sdd, cto, product-definition, architecture-cut, upstream-chain
  risk: safe
---

# product-sdd

## Purpose

Author a project's **SDD**: the technical *how*, ending in a **cut** — the architecture the rest of the
system builds against, derived from the settled SRS and UXD and the PRD, then cut into ordered slices
that each deliver something on their own. It is station 5 of the definition sequence
(`<CORE>/doctrine/setup/setting_up_a_project.md`, which owns the sequence and is not restated here).

This file is the **orchestrator**: posture, the file loop, path resolution, staging and the commit.
**How to author** — the weighing of the shape, the parts and seams, the cut, and how each part the CPO
or the CDO decides is drafted and routed — is the authoring prompt
**`prompts/rich.md`**, applied at Step 2; a rule referenced below by name lives there.
The document's **section shape** and the table of who decides each part are the template
**`<CORE>/templates/product-templates/sdd_template.md`**; the companion's shape is
**`sdd_open_issues_template.md`** beside it. None of them is restated here.

**Non-interactive, one CTO run.** The CTO writes the whole SDD in one run, best-effort, and never blocks
on the owner. A part the template gives to the CPO or the CDO to decide is drafted too, and a call the
inputs leave unsettled — or a draft that needs that seat's confirmation — becomes an item in the
companion carrying `- **Seat:** cpo` or `- **Seat:** cdo`. The owner answers on their own time and
re-runs the skill, and **the run folds the answered companion on its next round** (Step 2).

---

## Posture

**CTO role required.** If invoked outside CTO posture (neither a `cto:` session nor the `cto`
subagent), **write nothing** and stop, saying: *"product-sdd requires CTO posture. Switch? (Open a
session with the `cto:` prefix, or run the `cto` subagent.)"* Make this check before any read that
leads to a write. Do not shed the role.

---

## The files and the loop

| File | What it is | Lifecycle |
|---|---|---|
| `<Product path>/docs/SDD.md` | The SDD — best-effort complete on every run, every part drafted. | Permanent; one document, revised and versioned in place (the template's bump-on-material-change note), never forked. |
| `<Product path>/docs/SDD_open_issues.md` | The companion, holding what the run could not settle, in the buckets `sdd_open_issues_template.md` defines. Each item names the seat that answers it. | Transient — exists only while something is unresolved. **Its absence is the done signal.** |
| `<Product path>/docs/trail/sdd/cycle-<N>.md` | Each answered companion, retired whole. | Permanent. |

**Cycle numbering:** `N` is one higher than the **highest** `cycle-<N>.md` already in `trail/sdd/`.
List the directory and match names of exactly the form `cycle-<N>.md`; every other file in that folder
(`run-…`, `self_answer-…`, anything else) is ignored, and a gap in the numbering does not matter. With
none matching, `N` is `1`; create `trail/sdd/` if it is not there. Never overwrite an existing cycle.

**The loop, repeated until clean:**

1. The run drafts the SDD and writes the companion with what it could not settle.
2. The **owner answers inline** — filling the answer slots whose names and shape are
   `sdd_open_issues_template.md`'s — and re-runs the skill.
3. The run **copies the answered companion whole to the next trail cycle**, folds the answers into the
   SDD, and rewrites the companion with only what is still unresolved. An answer the fold leaves
   unsettled still drops, and its residue is re-raised as a fresh item with an empty answer slot.
4. When the answers resolve everything, the run is the close: it folds, copies the answered companion
   to the trail, and **removes** the companion through the builder's `--rm`, never a hand-`rm`.
   **No open-issues file = the SDD is done.** The close needs the owner's answers already committed
   (Step 3 owns the rule); when they are not, the run changes nothing at all and asks for that commit.

---

## Inputs and where the files land

Read each of these in full; the run is entitled to nothing it did not open.

- **The SRS and the UXD** — `<Product path>/docs/SRS.md` and `<Product path>/docs/UXD.md`, status line
  included, plus **`<Product path>/docs/PRD.md`**. A missing one is not a halt: draft best-effort
  without it and raise it as an item for the seat that owns that document. What a `Draft` or unreadable
  status means for the derivation is `<CORE>/doctrine/governance/unsettled_inputs.md`'s rule.
- **`system/projects/<name>/agari.md`** — the declared terminus, the scope boundary. Its absence does
  not halt the run.
- **`system/projects/<name>/doctrine/`** — `<name>_doctrine.md` and `ai_responsibility.md`, when present.
- **`<Product path>/docs/definition_brief.md`** — when present.
- **`system/doctrine/writing_bar.md`** — the writing bar every document this instance authors follows.
- **`<Product path>/docs/adr/` and `nfdr.md`** — when present; the lens says why.
- **`<CORE>/templates/product-templates/sdd_template.md`** — the shape and the table of who decides what.
- **`system/projects/<name>/project.md`** — the card. Its `Product path:` resolves where every output
  lands; the field is the card template's (`<CORE>/templates/project_template.md`).
- The existing `SDD.md`, `SDD_open_issues.md` and `trail/sdd/` — the loop's state (Step 1).

**Path resolution.** A relative `Product path:` is inside the instance repo; an absolute one is outside
it, in whatever repo holds the product. Every instance-relative path resolves from the instance repo
root, the directory the session opened in; no step `cd`s away from it. If `Product path:` is a
placeholder or awaits an owner value, halt and report — nothing can be filed. Never invent one.

---

## Workflow

### Step 1 — Identify the project, read current state

Identify the target project; if more than one exists and the target is ambiguous, halt and report the
candidates. Read the inputs above, and resolve **`<repo>`** from `Product path:` — the instance repo
(`.`) for a relative path; for an absolute one, `git -C "<Product path>" rev-parse --show-toplevel`.
Then read the loop's state: the existing SDD (the settled baseline a re-run holds stable), the
companion if one exists, and `trail/sdd/` — a value the owner set in an earlier cycle is authorized,
and changing it needs a fresh authorization. A first run has none of the three.

### Step 2 — Draft or revise the SDD, fold the answers, write the companion (no interview)

**Gate first — detect the first closing touch before you write anything.** When a companion existed
at intake, its inline answers would resolve everything unresolved, and the file is uncommitted
(check its git cleanliness in `<repo>`), this run is the first closing touch and **writes nothing**:
no draft or fold, no trail copy, no companion rewrite. Skip the rest of this step and Step 3, and
report CLOSING at Step 4.

Draft or revise `<Product path>/docs/SDD.md` by applying **`prompts/rich.md`** and
the template. **Draft every part**, the ones the table gives to the CPO or the CDO included, from the
inputs and any answer already in hand. For each such call the inputs leave unsettled, or that the draft
needs the seat to confirm, raise an item in the companion carrying `- **Seat:** cpo` or
`- **Seat:** cdo` — the seat the table names, not the seat that raised it. An item whose call is the
CTO's carries `- **Seat:** cto` or no `Seat:` field. Write the companion from
`sdd_open_issues_template.md`.

**Consuming an answered companion.** A companion that existed at intake with at least one answer slot
filled is **consumed**; what counts as an answer slot is the companion template's, read from its
current shape. Three moves, in this order: copy the companion whole (an ordinary `cp`) to
`trail/sdd/cycle-<N>.md` *before* the fold rewrites it; fold the answers into the SDD; then drop every
**answered** item from the companion. An answer the fold leaves unsettled drops with its item and
**re-enters as a fresh item with an empty answer slot**, never the old one surviving, so a filled slot
in a surviving companion is always the owner's writing. A companion with no slot filled is not
consumed: no trail cycle, nothing to fold, and a first run with no companion at intake makes no cycle.
When the drop resolves **every** item, leave the companion as intake read it and let Step 3's `--rm`
remove it; no state of this run leaves an empty companion behind.

Set the template's `Status:` from Step 4's DONE condition, never from your tally of answers:
**Settled** only when this run ends with no companion on disk, **Draft** otherwise, so the companion's
absence and `Status: Settled` agree. Leave **Locked** alone — ratification is the owner's act. Bump
the `Version:` line on any run that changes the SDD's content.

### Step 3 — Commit through the builder

Commit through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and
supply its variables (`<repo>` from Step 1, the `--add`/`--rm` paths, the actor, subject and body, the
directional). The builder stages, derives `Role:` and lays the trailer block; this step never
hand-writes a `git commit`, spells a trailer, or `cd`s into the repo.

**A run that changes nothing builds no commit and touches no disk.** If it folded no answer, changed no
SDD content and has nothing to stage, make no file change at all, report (Step 4) and stop.

**The stage list — compose it from what this run did.** Pass every path in **one** `--add`, and the
companion as the one `--rm` path when removed. `<D>` is `<Product path>/docs` relative to `<repo>`.

- `--add <D>/SDD.md` — always, on any run that builds a commit.
- The companion, exactly one of: `--add <D>/SDD_open_issues.md` (something is unresolved) ·
  `--rm <D>/SDD_open_issues.md` (nothing unresolved *and* one existed at intake) · **neither** (nothing
  unresolved and none existed). The close needs the owner's answers already committed: git will not
  remove a dirty file, and their words are not this run's to commit. That is Step 2's gate.
- `--add <D>/trail/sdd/cycle-<N>.md` — only if this run consumed an answered companion, on the same
  commit as the fold it precedes.

**Actor.** Every commit this run makes — from the `cto` agent or an interactive `cto:` session alike —
names `--actor cto --skill product-sdd`. **And `--prompt product-sdd/rich`**, naming the body this skill
is the carrier for; it takes the bare name, never a path. Subject, body and trailers are the recipe's
variables.

### Step 4 — Close / report

Report:

- the SDD path, and the commit SHA (or that the run changed nothing and built no commit);
- on a run that consumed an answered companion, the **trail cycle path**,
  `<Product path>/docs/trail/sdd/cycle-<N>.md`;
- the SDD's **version, status and the number of items open for the owner**; and
- the **loop status**, exactly one of:
  - **DONE** — no open-issues file remains; the SDD is complete.
  - **CLOSING** — the owner's answers resolve everything but the companion is uncommitted, so this run
    changed nothing. The one ask: commit the companion, then re-run — that re-run is the close.
  - **OPEN** — something is still unanswered. Give a count per bucket under the names the companion
    on disk carries, name where they live, and name the next move: the owner answers inline, commits,
    and re-runs product-sdd.

Do not enumerate downstream steps; authoring the SDD is this skill's whole job.
