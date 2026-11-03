---
name: development-audit
description: |
  Independent fresh-eyes audit of a development-* step's output for FLOW-quality issues — coverage gaps, altitude leaks, unrecorded divergences, classification-propagation slips, contracts realized by coincidence, new logic outside the part that owns it. One skill for every audited step (the step is a parameter). Produces flow_findings/<step>.md, one file per audited step; audits only, never fixes.
  Use when: a development-* step (development-specs / development-design / development-plan / development-content / development-implementation) has just produced its artifact and you want to audit that output for issues about the flow before the next step runs.
  Do not use for: product-correctness review (that is acceptance / QA), redesigning the artifact, or fixing anything.
  Trigger phrases: "run development-audit", "audit the flow output", "audit the change_spec / change_design / tl_instruction", "development-auditing", "check this step's output for flow issues".
license: MIT
metadata:
  version: "1.14.4"
  category: quality
  risk: safe
---

# Development Audit

## Purpose

After a development-* step produces its artifact, audit that output for **flow-quality issues** — the failure shapes the pipeline itself produces: coverage gaps, altitude leaks, unrecorded divergences, classification-propagation slips, stated contracts realized only by coincidence, new logic left outside the part that owns it, and step-specific contract breaches. The findings are **observability signal**, not a gate: they accumulate in a per-change ledger and feed both this change's record and (for generalizable defects) the kaizen queue.

**One skill, every audited step** — the step audited is a parameter, never a per-step fork (the audit *stage shape* is identical; only the artifact and its contract differ).

**Produces:** `flow_findings/<step>.md` — one file per audited step, under the per-change `flow_findings/` directory.

## Posture

- **Fresh, role-neutral eyes.** You did **not** produce this artifact; do not defend it. Read it as a skeptic receiving it cold.
- **Audit, do not fix.** Never edit the audited artifact, any decision file, or any skill body. You emit findings only — the producing skill or a follow-up change acts on them.
- **Flow-issues only.** You judge the *pipeline's output quality*, attributable to the producing step. Out of scope: product bugs (acceptance/QA owns those), design taste, and anything the step was correct to defer downstream.

## This is NOT

- **Not acceptance / QA.** Acceptance is a pass/fail gate against the contract (`development-acceptance-*` / the orchestrator own that). development-audit produces findings; it does not pass or block.
- **Not a fix or a redesign.** Findings only.
- **Not product-correctness review.**

## Input

The invocation must supply:
- **change key** — `<YYYY-MM-DD>_<slug>` (the worktree-branch name).
- **project name** `<project>` — the `system/projects/<project>/` folder (passed by the orchestrator); the change-work folder is `$WORKTREE/system/projects/<project>/journey/tobiishi/<key>/`.
- **step audited** — one of `development-specs` | `development-design` | `development-plan` | `development-content` | `development-implementation`. If omitted, infer from the newest produced artifact in the change folder.

Derive `$WORKTREE` exactly as the development-* skills do — `$WORKTREE = $(git rev-parse --show-toplevel)/.worktrees/<key>`. If `$WORKTREE` does not exist, **STOP**: the step has not run for this change. `$WORKTREE` is used only to confirm the change branch's tip and as the `PROJECT_DOCS` resolution anchor below — this skill never writes into it (Step 0 opens a **second**, this-auditor-only worktree, and every read and the one write happen there instead). For any `docs/` cross-check, **resolve `PROJECT_DOCS`** the same way development-design / development-plan do — never from a header (the `Project:` header is retired), but from the path tool's contract, which reads `project.md` `Product path:` (`python3 "<CORE>/tools/development_path.py" resolve --format json --worktree "$WORKTREE" --project <project> --key <key>`), never composed by hand. `<sub>` is the contract's `product_path` when it is relative, else `product_path` relative to `product_repo` (`.` when the same). In-repo (`product_worktree` is `$WORKTREE`) → `$AUDIT_WORKTREE/<sub>/docs`, with `$AUDIT_WORKTREE` (Step 0) standing where `$WORKTREE` stands; external → `<product_worktree>/<sub>/docs`, the product worktree opened for this change, by `create_change_worktree.py`, on the chain path and under `ad-hoc-plan` alike, never the primary checkout. For any **product-code** cross-check, anchor the same way — `PROJECT_ROOT=$(dirname "$PROJECT_DOCS")` — and read product source strictly under `$PROJECT_ROOT`, never by scanning `$WORKTREE` for a product folder (a sibling in-repo product is the wrong one — the external-product split-brain).

All artifact reads are **read-only**. The only file this skill writes is `flow_findings/<step>.md`.

## Step 0 — open the auditor's own worktree

The chain launches one `development-audit` run per audited step — four, or five when the change
publishes text — one after another, each detached
(`<CORE>/tools/chain_development.py` `_launch_step`), so they are live at once and must never
share a git index — `commit_builder.py` refuses a commit whose staged set another session touched. Each
auditor opens its own worktree, on its own branch, before touching anything else:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
AUDIT_BRANCH="<key>__audit-<step>"
AUDIT_WORKTREE="$REPO_ROOT/.worktrees/$AUDIT_BRANCH"

# Guard — same idempotency rule as create_change_worktree.py: a branch or path that already exists is a
# STOP, not a silent reuse.
git show-ref --verify --quiet "refs/heads/$AUDIT_BRANCH"   # branch exists?
test -e "$AUDIT_WORKTREE"                                    # path exists?
# If either exists, STOP and report — do not recreate.

EXCLUDE="$(git rev-parse --git-path info/exclude)"
grep -qxF '.worktrees/' "$EXCLUDE" 2>/dev/null || echo '.worktrees/' >> "$EXCLUDE"

git worktree add -b "$AUDIT_BRANCH" "$AUDIT_WORKTREE" "<key>"
```

The branch is cut from `<key>`'s **tip** (the change branch), not `main` — the auditor needs the
producer stage's just-committed artifact, which lives only on the change branch so far. `<step>` is
this invocation's own "step audited" parameter (`development-specs` | `development-design` |
`development-plan` | `development-content` | `development-implementation`); the `__audit-` infix keeps a `<key>*` glob from
also matching the change's own worktree.

From here on, every path this skill reads or writes — the audited artifact, `PROJECT_DOCS`'s
standalone fallback, `flow_findings/<step>.md` — resolves under `$AUDIT_WORKTREE`, the exact same
relative layout `$WORKTREE` would have given it (a full checkout of the same branch tip), never under
`$WORKTREE` itself.

## What to read per step

Read the produced artifact **and** the input contract it was supposed to honor:

| Step audited | Primary artifact | Cross-check against |
|---|---|---|
| `development-specs` | `change_spec.md` | `docs/fdr.md` **when present** (else the request + public export surface, or on a product with no code the documents' own statements); the original casual request |
| `development-design` | `change_design.md` | `change_spec.md`; `docs/adr/`, `docs/nfdr.md`, `docs/fdr.md` **when present** |
| `development-plan` | `tl_instruction.md` | `change_design.md` + `change_spec.md`; `docs/adr/`, `docs/nfdr.md`, `docs/fdr.md` **when present** |
| `development-content` | `change_text.md` | `change_spec.md`; `change_design.md` (its `Publishes text:` line names the places); `docs/CONTENT.md` **when present**; `system/doctrine/writing_bar.md`; the product's existing strings under `$PROJECT_ROOT` |
| `development-implementation` | the code + tests + closing commit | `tl_instruction.md`; `change_design.md`; `docs/SDD.md` § 3 **when present**; `code-integrity-report.md`; `system/projects/<project>/project.md` — its `Test command:` and `Execution type:` are the run's commands, and its `Languages:` is what the language resolution must match |

> **FDR-optional.** `development-specs` no longer requires `docs/fdr.md` — a project with no FDR yet is the
> normal starting case, not an error. When it is absent, cross-check the `change_spec.md` against the
> request + the product's public export surface (the same fallback development-specs used), and do **not**
> raise a finding for the missing `fdr.md`.

> **ADR/NFDR-optional.** `development-design` and `development-plan` no longer require `docs/adr/` or
> `docs/nfdr.md` — a project may have none yet, which is normal, not an error. Cross-check the
> `change_design.md` / `tl_instruction.md` against them **only when present and Locked**; when either is
> absent, skip that cross-check column and do **not** raise a finding for the missing `adr/` / `nfdr.md`.
> (Implementation's ADR-optionality — where `development-implementation` reads execution type / test
> command from — does not surface in these cross-checks, so the `development-implementation` row is
> unaffected by it.)

> **SDD-optional.** The `development-implementation` row's `docs/SDD.md` § 3 is optional in the same
> way: a product with no parts table skips lens 9 and raises no finding for the missing table.

## Audit lenses (v1)

Walk each lens against the artifact. Lenses 1–8 are known flow-failure shapes from prior runs, and lenses 9 and 10 come from owner rulings — this list is the v1 set and is meant to grow (future: lenses for other dimensions).

1. **Coverage.** Every spec rule **and every rule-implied edge case** (empty / error / boundary) maps to a downstream row (design test-additions, plan task, test). The Examples table is the floor, not the universe — a dropped rule-implied edge is a finding.
2. **Altitude.** PO altitude held: no mechanism / storage anchor in the rules **or** in the rationale (`## Locked Answers`); any ordering keyed to an output-observable value (the printed `id`), not a hidden property (creation time, insertion order).
3. **Classification propagation.** The header `Category` / `Behaviour` was **copied verbatim**, not re-derived; in-vocabulary. A propagator that re-classified is a finding.
4. **Divergence record.** Every decision that diverged from the step's input is recorded in the step's divergence section (`## Locked Answers` / `## Architect Review Notes` / `## TL Review Notes` / `Developer Review Notes`) **with its reason**. A silent resolution — a load-bearing decision that landed with no entry — is a finding.
5. **Contract realized, not coincidental.** A stated contract (ordering, structure, bound) is realized **by construction**, not by an incidental invariant that merely coincides today.
6. **Step-specific contract.** The audited skill's own Critical Rules held (e.g. worktree-only / never `main`; one-change-per-run; topology binding; `__init__.py` re-export-only).

7. **Evidence that could have failed.** A step's record carries claims about the run, and each has a shape a wrong run cannot produce. Check each against the artifact rather than reading it for tone.

   **`development-specs`** — the `## Verified Claims` section is present — in **both** modes, since a preserving spec's characterization contract is made of claims about existing code — and every claim about what a command *decides* was run rather than read — in every category, since deriving a verdict by reading the checker is not an `nfdr` failure mode: the command, the tree it ran against, the conditions it ran under, and what it returned. A verdict produced under a harness the rule itself excludes is the finding too — *run, not read* is met and the claim is about a different system. A verdict derived by reasoning about a checker's source is the finding, however correct each quoted fact about that source is. The zero form says so; an absent section is itself the finding.

   **`development-implementation`** — the closing commit's three blocks:
   - **The resolved language matches the project.** Compare the block's language line against `system/projects/<project>/project.md` `Languages:` and the files the change touched. A run that resolves to `none`, or to a language the project does not declare, leaves nothing to count, so a wrong resolution passes every check below it — except on a card whose `Languages:` is blank and whose `Test command:` reads `none`, a product with no code, where `none` is the right resolution and not a finding.
   - **The `Language resolution:` block quotes, never paraphrases.** Every packet clause the implementation turned on carries the concern file, the line, and the clause verbatim. Open the packet and compare. **Open the packet's `README.md` and count its concerns against the block's** — completeness is the packet's list, not the run's. Each concern is accounted for by its own destination's line: a quoted clause or a bore-on-nothing line for any file — a packet file or a named owner outside the packet — and a floor line only where the router sends the concern to the floor. A named owner answered by a summary instead of a quote is the paraphrase this lens exists for. A concern accounted for nowhere is the finding even when every clause quoted is correct. **The roll-call line counts for nothing** — it names the packet's list by design, so a count against it always passes; count the per-concern lines beneath it. **And test every bore-on-nothing line against what the run did, not only what it wrote** — a concern that governs the run's own commands (the toolchain its gate commands ran under, the formatter and linter it was bound to) bore on the change whether or not any written line touched it. The run's commands are `system/projects/<project>/project.md`'s `Test command:`, a cross-check input above. A summary that reads as compliance while the packet says something else is the shape this check exists for, and it is invisible to a reader holding only the commit. **Then check the verdict against the quote it sits beside.** A correct citation carrying a correct quote can still reach a false conclusion, and nothing above reaches that: read the quoted words for any exception the verdict claims — a clause that does not contain one makes the verdict a divergence, however it is worded — and check that the site the line names is code this change wrote. Where the change wrote code bearing on the clause and the line cites a pre-existing site instead, that is a finding even when the clause is satisfied at both.
   - **The Step 1b block is present and says what it derived.** A run that adds no case and logs no divergence is indistinguishable from one that skipped the pass; the block's zero case has to say something, and a missing block is itself the finding. Both of its counts are present — cases added beyond the instruction **and** instruction cases not delivered — since a count that can only rise cannot show a case the instruction named and the run dropped. **Check the not-delivered count against the instruction's stated assertions, not its case names** — open each task's `#### Behaviours to verify` and confirm each named case asserts what it lists. A case under its right name with an assertion missing is a case not delivered.
   - **A task landing more than one rule behind one entry point proves them one at a time.** A red phase answers *did the task's cases go red* and never *because of which rule*, so for such a task the notes name which case goes red when each rule alone is reverted. Its absence means the suite may be green over a rule that could be deleted.

8. **A handed-down constraint is stated, not enacted.** Where the artifact carries a property its successor is bound by — an atomic-landing edge, a probabilistic red, a value set closed by its domain — it states the property and stops there. Two findings live here, and they are the two ways out the blackboard model closes (`<CORE>/doctrine/flow/folder_state_handoff.md` § *A constraint handed down is stated as a property*):
   - **Enacted.** The artifact names a downstream role, or decides something that role owns — task granularity, the member names of a set, the shape of a test, the commits a task lands as. Wording like *development-plan must …* is the visible form; prescribing the decision without naming the role is the same finding.
   - **Dropped.** The step's own input demanded a property its output does not carry, and the successor is left to invent it. Only visible by reading the input beside the output, which is why it survives every read of the artifact alone.

9. **New logic in the part that owns it** — `development-implementation` only. This lens comes from the owner's ruling of 2026-10-01, not from a leak seen in an earlier run. Each piece of logic the change added that some part owns sits in that part's code, as `<CORE>/doctrine/flow/development_flow.md` § *Code goes where the parts table puts it* defines it from `docs/SDD.md` § 3 (`Owns` and `Must not own` both). Read the table, not the import graph: on that section's reading, misplaced logic usually needs no forbidden import. Code-integrity ran before this audit and moved what it found. Its report, `system/projects/<project>/journey/tobiishi/<key>/code-integrity-report.md`, lists each move under **Placement**. A misplacement still in the code is a **`blocking`** finding, and so is a **Placement** entry the code contradicts. The audit does not block the seal — the owner's call, 2026-10-01. The finding reaches the PM through `shukuba-refine`, which takes `blocking` findings first. When the product has no § 3 parts table, say so and skip the lens.

10. **Words the product can keep** — `development-content` only. The owner's ruling of 2026-10-04, after a content step wrote a word the product's `CONTENT.md` bans and the Developer, bound to place it verbatim, could only defer the task. Each string in `change_text.md` is checked against `CONTENT.md`'s banned lexicon and rejected names, in every inflection, and against any word the writing bar bans; a hit is **`blocking`**. Each place the design's `Publishes text:` line names has a block and no block names a place the line does not. Each string is whole (no fragment a runtime joins), names no identifier or file, and claims no cause, state or guarantee the change's spec does not establish. When the product has no `CONTENT.md`, check against the writing bar alone and say so.

## Each finding records

- **Blocking?** — `blocking` (the next step should not proceed — a grade for the PM's `shukuba-refine`, which takes these first; the audit itself never stops the chain) or `non-blocking` (record-and-proceed).
- **Kind** — `change-local` (about *this* output) or `skill-general` (the skill/development itself is weak — a candidate kaizen item). A `skill-general` finding is **also** raised as a kaizen item (capture, don't fix).
- **Lens** — which lens caught it.
- **What** — the issue in one line.
- **Where** — `<file> §<section>` (or commit / test).
- **Detail** — one line: why it is a flow-issue, and the suggested direction (not a fix).

## Output — write `flow_findings/<step>.md`

Path: `$AUDIT_WORKTREE/system/projects/<project>/journey/tobiishi/<key>/flow_findings/<step>.md`. One file per audited step — a writer that creates its own file cannot reach a sibling step's file, so the isolation this ledger needs is structural rather than a promise to keep. Create the file with the header if absent.

````markdown
# Flow Findings — development-specs  (audited YYYY-MM-DD)

Findings for this step's output only, produced by the `development-audit` skill.
Change-local findings live here; skill-general findings are also raised as kaizen items.

- **[non-blocking · change-local · coverage]** <what>. Where: `change_spec.md §Rules`. <detail / direction>.
- **[blocking · skill-general · altitude]** <what>. Where: `change_spec.md §Locked Answers`. <detail>. → kaizen `<slug>`.

_No findings: state "Clean — no flow-issues found." rather than leaving the file empty._
````

If a lens finds nothing across the whole artifact, say so explicitly (`Clean`) — an empty file reads as "not audited."

## Commit the findings

After writing your file, commit `flow_findings/<step>.md` on **this auditor's own branch** (`$AUDIT_BRANCH`, in `$AUDIT_WORKTREE`) through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply its variables: `<repo>` = `$AUDIT_WORKTREE`, `<staged file(s)>` = `flow_findings/<step>.md` (stage **only** that — never the audited artifact, a decision file, or anything else), plus subject / body / **`--actor kensaiapp-auditor`** (the agent `launcher.md` launches this skill as — name it, never derive it: the builder refuses a token with no `AGENT_ROLE` row, and a run that retries under another seat's token commits under that seat's `Role:`) / `--skill development-audit` (this skill's own name, so `Skill-Version:` records what ran) / directional. Never `$WORKTREE` — that is the change branch's own worktree, and a commit there from a concurrent auditor is exactly the shared-index collision Step 0 exists to avoid. `tobiishi-seal` merges `$AUDIT_BRANCH` into the change branch before the seal's own bookkeeping commit, which is what carries the audit trail into the eventual `--no-ff` merge to `main`. Never hand-write `git commit` or a trailer.

Stage **only** `flow_findings/<step>.md` — never the audited artifact, a decision file, or any other file (audit, never fix). One commit per audited step, on that step's own branch, each one writing its own file under `flow_findings/`; no commit can touch a sibling step's file.

## Critical Rules

- **Audit, never fix.** Emit findings only; never edit the artifact, decision files, or any skill body. The single file you write **and commit** is `flow_findings/<step>.md` — your own output, committed as `--actor kensaiapp-auditor` and no other token.
- **Flow-issues only.** Judge the pipeline's output quality, not product correctness. Tag each finding `change-local` vs `skill-general`; raise every `skill-general` finding as a kaizen item too.
- **One file per step.** Each audited step writes its own `flow_findings/<step>.md`; a step's write cannot reach another step's file.
- **Fresh eyes.** Do not assume the producing step was right; read the artifact cold against its input contract.
- **One skill, all steps.** The step is a parameter — never fork the skill per step.
- **Not a gate.** development-audit never passes/blocks the pipeline; it produces observability signal. Acceptance/QA is a separate concern.
- **This auditor's own worktree, never `$WORKTREE`.** Step 0 opens `$AUDIT_WORKTREE` on branch `<key>__audit-<step>`, cut from the change branch's tip; every read and the one commit happen there. A branch or worktree path that already exists is a STOP, not a silent reuse — the driver runs one of these per audited step concurrently, and reusing another auditor's git index is exactly the collision this convention exists to avoid.

## Improve later

This is v1 — the lens set (above) is the dimensions we have seen leak, plus the two owner rulings added (lenses 9 and 10). The chain invokes this skill as a fresh **`kensaiapp-auditor`** subagent, one per audited step, each detached, after `code-integrity` (Increment 3 — the fan-out layer over the automated half of `flow-findings-production`; still observability, never a gate). That subagent is a thin, tool-scoped agent (`<CORE>/../skills/kensaiapp-auditor/.claude/agents/kensaiapp-auditor.md`) — **not** a pipeline posture (no loader, no inbox); the chain's prompt carries the skill invocation, and `tobiishi-seal` joins each auditor's branch into the change branch before it seals. The accumulated findings are read after the unit lands by `shukuba-refine`, which acts on the project's route. Planned: more lenses, auditors for other output dimensions, and trigger/behaviour evals (`skill-creator` / `skill-evals`).
