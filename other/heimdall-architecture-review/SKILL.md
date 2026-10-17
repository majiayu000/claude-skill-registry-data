---
name: heimdall-architecture-review
description: Review the artifacts of the architecture workflow — the structural context findings an arc42 document is grounded in, and the persisted architecture directory against the ratified Workfile's layout map — selecting the checklist by a Focus line in the brief. The drafted document itself is not reviewed.
---

# Architecture Review

## Purpose

Independent verification of the architecture workflow's artifacts. Two artifact shapes pass through this skill, one per dispatch, selected by the brief's `Focus:` line:

| `Focus:` | Artifact under review | The gate it guards |
| --- | --- | --- |
| `context` | an architecture-context report — the structural evidence base the document is written from | nothing is documented or decided from unproven structure |
| `persistence` | the persisted architecture directory and its decision records, against the layout map and the persistence manifest | no unreviewed structure, unratified status, or run-local reference reaches the repository, and nothing is created over or deleted from an existing document |

**The drafted architecture Workfile is not an artifact of this skill**: the workflow ratifies it at its checkpoint, and this skill checks its persisted form. Every checklist for an artifact that *is* this skill's lives here; a gap in one is a report item to the requesting agent, not license to improvise from another checklist.

**Ground truth, not self-report.** Every verdict rests on files you read at review time, commands you executed yourself, and paths you resolved. A producing session's claim about its own output is the thing under review, never evidence for it.

**Verdict grammar.** One line, the first line of the review Workfile:

```text
Verdict: <PASS | PASS-WITH-NOTES | BLOCKED> — focus=<context|persistence>, artifact=<path>, <one-clause reason>
```

**PASS** — the artifact meets its contract and the spot-checks this Focus names all resolved. **PASS-WITH-NOTES** — it meets its contract with non-blocking gaps, named and located; it may be consumed as it stands. **BLOCKED** — one of this Focus's blocking conditions holds; name it, locate it, and state what re-establishes it.

The verdict is yours. What follows from it — resuming the session or re-dispatching it — belongs to the requesting agent.

## Boundaries

- Never edit the artifact under review. Findings go in the review Workfile; fixes belong to a producing session.
- Never fill in a missing section, header field, marker, or manifest row on the producer's behalf. An absent field is a finding, and supplying it destroys the thing you were dispatched to check.
- Never re-do the producer's work: no re-deciding or re-scoping the architecture, no re-persisting a file. You validate evidence and conformance.
- Never review from session memory; on a re-review after a fix, re-read every changed file live. Never apply more than the one Focus the brief names — and never fewer.
- Never soften a blocking finding to keep a workflow moving, and never trade it for a promise to fix it afterwards.
- Never grant ratification. `Status: Proposed` on an authored document is correct; promotion is the requesting agent's act and the persistence step's write, and your job is to check it happened in that order.

## When to Use

- Dispatched with a `Focus:` line naming exactly one of `context`, `persistence` — as the standing review of an architecture-context session or of a persistence session.
- The brief carries the producing session's brief, the artifact paths, and the **pinned baseline** — the pre-change file state or the commit the session started from, or `new file` for a creation. A brief that omits it is incomplete: ask, rather than diffing against the working tree.
- **Not for** the drafted architecture Workfile — it has no review by design; decline and say so. **Not for** a TDD-context Workfile: route it to `heimdall-tdd-review`.
- **Not for** deciding what the architecture should have been, or pronouncing on a step whose artifact does not exist yet.

## Workflow

**Apply only the subsection the brief's Focus names.** Steps 0, 1, and 2 always run.

**Step 0 — Read the control line and pin the baseline.**

- `Focus: context | persistence`. Missing or ambiguous → ask the requesting agent. Do not guess, and do not hedge by applying both.
- Resolve every artifact path the brief names. A named path that does not exist is a blocking finding by itself.
- Pin the baseline — every byte-identical claim and every diff is measured against it — and re-read the artifacts from disk now. Session memory of an earlier draft is not the artifact.

**Step 1 — Common checks (both Focus values).**

- **The producing session wrote only in the medium its role may write.** Run this first, and run it mechanically: `git status --short` in the target project, plus `git diff --name-status <baseline>` when the baseline is a commit; and a listing of the task directory in the workspace. A persistence session writes project files and **no Workfile at all**; a context session writes **only** Workfiles and no project file. A violation is **blocking in either Focus**, whatever the artifact's own quality — an artifact can match its specification exactly and still break a standing rule of the framework.
- The named artifacts exist, are complete against their own output contract, and are the version the brief points at.
- The originating brief was honored: its inputs were used, its scope was not exceeded, and gaps were reported rather than invented.
- Every claim your verdict rests on is verified against ground truth — a resolved path, an executed command, or a line quoted from the live file.
- **Mermaid diagrams are cleared by a named method, never by impression.** Prefer a parser: invoke a Mermaid CLI when one is already available (`command -v mmdc` or equivalent) — never install one, and never invoke it in a way that could fetch over the network. When none is available, run a deterministic scan for the reserved and terminator characters of each block's own diagram type, alongside the manual read: a bare `;` terminates a `sequenceDiagram` statement and `#` opens a comment there, with no quoting to escape either, while `flowchart` protects label text inside quoted brackets. Record `parser-verified`, `deterministic-scan`, or `manual-only` with its reason in the verification method. This applies to a context Workfile's diagram and, under `Focus: persistence`, to **every persisted topic document carrying a Mermaid block** — the drafting step is unreviewed, so this is where a broken diagram is caught.
- Every finding carries a location (`path:line`, section number, criterion ID), the evidence that establishes it, and the change that would clear it.

### Focus: context

The artifact is the architecture-context Workfile: the structural evidence base the arc42 document is written from. Judge it as evidence; whether the structure it reports is *good* structure is not this review's question.

- **Scope declaration.** A preamble names what was investigated and what was deliberately excluded, with a reason per exclusion. Its absence is blocking, not a finding: without it you cannot distinguish a thin report from a narrow one.
- **Output contract complete.** Scope; area map; entry points and call paths; boundary interfaces; cross-cutting concepts as embodied; existing architecture and decision records; dependencies; a current-state view or the explicit line saying why none was earned; a not-examined list. A missing part is a finding.
- **Boundary interfaces quoted, not summarized.** Each provided and required surface is reproduced verbatim in a fenced block with its `path:line`. A summarized load-bearing interface is blocking — a paraphrase cannot be written against.
- **Every finding proven** by `path:line`, or by a command plus its captured output. "The service layer", "errors bubble up somewhere" are vague citations, not proofs.
- **Fact-rich, framing-poor.** No recommendation, no prioritization, no "should", no target-state description. Framing content is blocking.
- **Resolve at least two proofs yourself** — one module boundary and one boundary interface, the two findings the building-block view rests on. The path exists, the line numbers are accurate, and the quoted interface matches the live file character for character.
- **Documentation facts resolve.** Every named architecture-document and decision-record path exists, and the reported structure matches what you find when you look.
- **`[UNVERIFIED]` discipline.** Each carries the reason verification was not possible, and they are at most a quarter of the findings.
- **Diagrams.** Every element of a current-state view traces to a stated finding. A proposed or target-state element inside it is framing.
- **No task-scoped facts gathered** — the runner and its commands, the conventions new code must imitate, implementation-phase test infrastructure, what the touched paths do today. Check § Scope names them as exclusions when the brief named a change, then read the findings for one that slipped in anyway. **This is a note, never a blocker**, and the asymmetry is deliberate: a context Workfile is never persisted, so a task-scoped fact here costs one filtering decision, whereas the same fact inside §1–§12 is permanent.
- **Not checked here:** test infrastructure, a baseline test run, current-behavior characterization. This shape carries none of them by contract; their absence is never a finding.
- **BLOCKED on:** a proof that does not resolve or names a nonexistent path; recommendation, prioritization, or target-state content; a missing scope declaration; a load-bearing boundary interface summarized rather than quoted; unverified findings above a quarter of the total.

### Focus: persistence

Inputs are the persistence manifest, the ratified architecture Workfile **with its Appendix C layout map**, the `Ratification:` line, and the pinned baseline. There is no test-suite item here. The persisted form is a folder per section holding a generated `README.md` index plus `NN-<slug>.md` topic documents, `09-architecture-decisions/` holding the decision log as its `README.md` beside the `NNNN-<slug>.md` records, and a generated top `README.md`.

- **(a) The existence rule, judged at baseline** — not against the tree as it now stands. For `Document scope: seed` the target was **absent** at baseline, or held only a foreign `README.md`, in which case the collision fallback `<target>/arc42/` was used and that foreign file is byte-identical. For `update delta` the target was the folder layout at baseline, with all twelve folders and `Status: Accepted`. Re-derive this yourself by the identity rule (`README.md` *and* `01-introduction-and-goals/README.md`). A seed over a present layout, a delta over an absent one, or a layout created with folders missing is **blocking**. For a correction (`scope=correction`, the brief carrying `Re-persist:`) the target was the folder layout at baseline and every `Re-persist:` path existed in it.
- **(b) Map ⇔ tree, both directions.** Run `git diff --name-status <baseline>` yourself. On a seed the diff is exactly: thirteen indices, the mapped topic documents, and the records. On a delta: exactly the mapped documents of the `included=` sections, those sections' indices, §9's index with rows appended — and, for each `→ status:` row, that record's `Status` cell rewritten and nothing else in its row — the new records, the records named by `→ status:` rows, and the top index. No unmapped topic document was created, and **no `D` line** exists under the target. Carried-forward documents are absent from the diff and present in their section index at their existing ordinal; supersession is row-backed in both directions — every "Superseded documents" entry has its `→ superseded — <reason>` row and every such row has its entry. On a correction: exactly the `Re-persist:` paths, their section indices, and the top index — no record and no §9 row, so (f) is vacuous; (e)'s one new Change Log row reads `correction`.
- **(c) Promotion, sampled.** Open at least two topic documents and one record beside their Workfile sources. Each H1 is its root heading promoted by exactly `depth − 1`, the whole body is promoted by the same distance, and the backlink `_Part of [<Title>](../README.md) · [§N](README.md)._` is the second content line. Records carry no backlink. Compare heading levels directly rather than reading the text.
- **(d) Omitted sections are index-only folders**, the marker verbatim in the state line. **A persisted `_Not affected by this change_` is blocking**: that wording is delta bookkeeping and means nothing to a reader.
- **(e) Indices match the tree.** Every section index carries its H1, its backlink, its description from the fixed folder table, and a state consistent with its folder. The top index reads `Status: Accepted`, its Sections table matches row for row, and its Change Log grew by exactly one row — exactly one on a seed — with every prior row byte-identical.
- **(f) Records.** **Numbering re-derived:** the lowest new record is one above the highest number in use at baseline across every decision directory, matching the header's `Records from:`, and no new record overwrote an existing one. Then open **every** new or replaced record, not a sample — extraction bugs truncate systematically. Its `##` heading set equals its source's heading set promoted (`Options Considered` present if and only if `Kind: decided`), and every heading has real content beneath it; a stub is **blocking**. Statuses follow `ratified=` and `withheld=` decision by decision, every Appendix A ID sits in exactly one list, and the log resolves to the files and the files to the log. **Status supersessions:** for every Appendix C row `| ADR-NNNN (existing record) | → status: <text> | — |`, run `git diff <baseline> --numstat -- <that record's path>` yourself and require `1 1`; the removed line is `- **Status:** Accepted` or a prior supersession form, the added line is `- **Status:** <text>` with text exactly `Superseded by ADR-MMMM[, …]` or `Accepted — superseded in part by ADR-MMMM[, …]`, every `ADR-MMMM` in it reads `Accepted` after this run and names `ADR-NNNN` under its `## Related`, any IDs the removed line carried are still present, and the §9 row for `ADR-NNNN` differs from baseline in its `Status` cell only. Then diff **every** other pre-existing record against the baseline and require zero changes — a record that changed without a `→ status:` row, or a `→ status:` diff that touches any line but the status line, is **blocking**.
- **(g) Greps — three, all expected zero:** `arc42 guidance`, `.yggdrasil-workspace`, and the task-directory name. The second and third catch a run-local reference reaching the repository now that no review precedes persistence. Any hit is blocking.
- **(h) Manifest ⇔ diff**, action for action against the vocabulary `created`, `replaced`, `regenerated`, `index regenerated`, `appended <n> rows`, `superseded (kept)`, `status superseded`, `carried forward`, `untouched`; `layout=` and `collision-fallback=` are consistent with what the baseline showed.
- **(j) Planning material stays transient.** Appendices B and C are not persisted, no file or index field was invented to hold Workfile header metadata, and the durable substance of a changed decision is traceable to a record or to §11 — where it is in neither, the finding is against the Workfile, reported here and not fixed here.
- **BLOCKED on:** a layout created outside the existence rule; any deleted file under the target; a changed path the map does not account for; a topic document the map does not name; a persisted `_Not affected by this change_`; a promotion distance other than `depth − 1`; a persisted record that is a stub; a record number colliding with or skipping past the baseline's highest; any change to a pre-existing record other than its `Status:` line under a `→ status:` row, a status text outside the two fixed forms, or a status text naming a record that is `Proposed`, absent, or does not name the superseded record under `Related`; `Accepted` without a cited ratification, or a ratified record still reading `Proposed`; a log and record set that disagree; a hit on any of the three greps — including a workspace path or task-directory name anywhere under the target.

**Step 2 — Write the review Workfile.**

Write to the path the brief names, following the pattern for this Focus — `NN-review-context-architecture-<area>.md` for `context`, `NN-review-architecture-persistence.md` for `persistence` — in this order: the verdict line; **blocking findings** worst first, each with its location, evidence, and clearing change; **notes**, explicitly marked as not blocking consumption; and the **verification method** — what you checked by execution with the commands and their results, what you checked by reading, and what you could not verify and why. Record the `git status --short` output and the task-directory listing in every review, and under `Focus: persistence` the diff, the identity-rule result at baseline, and the record numbers you read. Then report the Workfile path and the verdict line to the requesting agent.

## Quality Criteria

- Exactly one Focus was applied, the verdict line names it, and every finding has a location, the evidence that establishes it, and the change that would clear it.
- Ground truth beat self-report: the spot-checks this Focus names were actually executed, and the review distinguishes what was verified by execution from what was verified by reading.
- The medium check was executed, not assumed: the project status and the workspace listing were both run and both appear in the verification method.
- Under `Focus: persistence`, **every** persisted record was opened, **every** pre-existing record was diffed against the baseline (zero changes, or exactly the status line under a `→ status:` row), and the baseline state — the existence rule and the highest record number — was re-derived rather than read off the header.
- The joint to the previous stage was checked rather than assumed: the context report against its scope declaration and the live tree; the persisted directory against the Workfile header, its layout map, and the ratification record.
- Blocking findings are separated from notes, so the requesting agent can tell a re-dispatch from a nicety.
- An artifact that could not be verified is reported as unverifiable with the reason. An unresolved check is never rounded up to PASS.

## Anti-Patterns

- **Rubber-stamping**: passing because the artifact looks complete and the session sounded confident.
- **Reviewing the drafted Workfile anyway** — "while I have it open". It is not this skill's artifact; the checkpoint and the persistence review are its gates.
- **Checking the content and not the medium**: verifying an artifact against its specification without asking whether the session that produced it was permitted to write where it wrote.
- **Trusting the map's self-check**: reading Appendix C's own "every heading covered exactly once" claim instead of walking the tree against the rows.
- **Trusting the header's `Document scope:` or `Records from:`** instead of re-deriving both from the baseline. A wrong scope is a merge turned overwrite; a wrong number corrupts the decision log irreversibly.
- **Waving through a deletion**: accepting that a superseded document disappeared because the new map no longer names it. The map decides what gets written, never what gets removed.
- **Sampling a systematic writer**: opening one record, finding it complete, and passing the other four. A writer that drops bodies drops them the same way every time, while the log, the headers, and the file count all still look right.
- **Clearing a diagram by impression**, or **promoting statuses by inference**: the first passes a `sequenceDiagram` broken by one stray character, the second accepts `Accepted` because the run reached persistence.
- **Reviewing from session memory**, or **applying both checklists at once**: the first judges a file that no longer exists, the second verifies neither properly.
- **Blocking a context report for engineering facts**, **re-doing the producer's work**, or **filling the gap you found**: each demands or supplies what the contract assigns elsewhere.
- **Negotiating a blocker**: downgrading BLOCKED to a note because the run is nearly finished. The cost of an overwritten document or an unratified promotion lands later and larger.
- **Accepting a "tidy-up" in a superseded record**: a corrected citation or date riding along with the status flip. One line changes; a second changed line is a rewrite nobody ratified.
