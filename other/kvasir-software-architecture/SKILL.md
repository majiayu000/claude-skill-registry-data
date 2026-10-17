---
name: kvasir-software-architecture
description: Author an arc42 architecture Workfile for a system or a bounded objective in one pass — assess what the architecture is, decide what the objective changes, quality goals first, pruned to sections holding durable content, with a decision record only for each structurally significant decision, a work-package breakdown when implementation follows, and a layout map assigning every heading to its persisted document.
---

# Software Architecture

## Purpose

Produce the architecture of a system, or of one bounded objective against it, as an arc42-structured Workfile — in **one pass** that answers two questions: what the architecture **is**, and what the objective **changes** (nothing, when the objective is to record the system).

**You author the Workfile and touch no project file.** Two facts about the target are yours to resolve before drafting, and only two — whether the folder layout already exists at the briefed location, and the highest decision-record number in use (§ Workflow step 1). Everything else about the target is the persistence step's business. Those two facts fix the **document scope**: **seed** — no layout exists, so you write the in-scope sections from scratch; **update delta** — one exists, so you write only the sections the objective changes, as a delta persistence merges document-by-document. Your single Workfile carries four parts:

- **arc42 §1–§12**, scoped to the sections that hold durable content this objective calls for, every omitted section retained as a heading plus a closed-set marker.
- **Appendix A — Decision Records**, one per structurally significant decision, whether you decided it now or recorded one already in force.
- **Appendix B — Work Packages**, written only when the objective decides a change that implementation will follow; otherwise the single marker `_None — no change decided_`.
- **Appendix C — Layout Map**, every heading → the persisted document that will carry it → its promotion distance.

**Decisions are definite.** Each record names exactly one decision and states it in the indicative, never as a menu. You advise and the requesting agent ratifies, so every record and the document header ship at `Status: Proposed`; ratification is the checkpoint's and promotion to `Accepted` is persistence's. **Your step receives no review** — the checkpoint and the persistence review are its gates, so the quality of this Workfile is yours to own.

## Boundaries

**The long-term-relevance test.** One rule decides what may stand in §1–§12, and it holds in both document scopes and in every one of the twelve sections:

> A statement belongs in §1–§12 only if it would still be true and useful to a reader of the persisted document after the triggering task is complete: it describes a boundary, an interface, a decision and its rationale, a quality goal, a stable mechanism, or a risk to the system. A statement about how this run was performed, what one work package does inside a block, a temporary measure, or anything that resolves only inside the task's workspace is task-scoped: it belongs in Appendix B, in the report, or nowhere.

**Tell-tales of task-scoped content** — the patterns that fail the test: workspace paths of the form `.yggdrasil-workspace/<yyyymmdd>-…`, task directory names, and Workfile filenames; a review verdict or a reviewer cited as this document's provenance; revision, contradiction, and inputs logs; run provenance phrased as time ("at the time of writing", "in this run"); work-package names or sequencing; feature flags, rollout steps, temporary workarounds, and task-specific test-harness setup; internal helper structure, local control flow, naming inside a block, test-case selection; run-local identifiers not defined in §1.1.

A statement that fails the test is **relocated, not lost**: into Appendix B, into the report, or — when it genuinely constrains future work — into a decision record or a §11 risk stated in durable terms.

**The significance test.** A decision gets a record only if it (a) constrains structure, contracts, technology, or external dependencies; (b) affects a §1.2 quality goal; or (c) is expensive to reverse. Anything else — naming, internal structure, test selection, sequencing, a temporary measure — is never recorded: it may shape a package's done criterion in Appendix B or, when it leaves a durable debt, a §11 entry stated in durable terms.

- Never write `Status: Accepted` on the document or on any record.
- **Never create or modify a project file.** Your only written output is the single Workfile the brief names, in the workspace; you read the target and never touch it.
- Never overwrite a file that already exists at the Workfile path. Ask the requesting agent, and write nothing until it answers.
- **Never derive more about the target than the two facts of step 1** — no reading of folder contents beyond what the existing document itself says, no second opinion on the layout.
- Never renumber, rename, or delete a heading § Document Shape fixes. A section this objective does not reach keeps its heading and gets a marker.
- Never run a substantive investigation to close a knowledge gap. Spot-check the codebase to confirm structure you build on, then **report the gap** — an unreported gap becomes an invented building block.
- Never put a building block, an interface, or a file path in §5 that you did not verify against the codebase or an input Workfile. Cite the path.
- Never present a decision with one option as `Kind: decided`. If no second option survives a sentence of analysis, the decision is a constraint — record it in §2 and say so. Never reconstruct an options table on a decision already in force: a deliberation nobody held is fiction.
- Never decide implementation minutiae the implementation phase owns: internal helper structure, local control flow, naming inside a building block, test-case selection.
- **Never put a run-local reference in §1–§12** — the tell-tales above, and the inputs' `AC-n` tokens. A persisted section cites only document-stable references: repository paths, this document's section numbers, decision-record IDs, and requirement IDs §1.1 defines.
- Never fill a section because § Document Shape lists it. An improvement you *conclude* but the objective did not ask you to decide belongs in §11, not in §4 or in a record.

## When to Use

- Dispatched as the drafting step of the architecture workflow, with the objective, the architecture location, the path of the Workfile to **create**, and the input Workfile paths (requirements, context) the run produced.
- **Not without a stated location.** The default is `docs/architecture/`; if the brief names none, ask.
- **Not for** writing anything into the target project. You map the layout in Appendix C; the persistence step is what writes it.

## Document Shape

The Workfile's headings are fixed. You write them all, at these levels, in this order — you decide what goes under a heading, never whether the heading exists.

The title is `# <System / Subsystem> — Architecture (arc42)`, followed by the header block:

```text
- **Status:** Proposed
- **Date:** <YYYY-MM-DD>
- **Target:** <location>
- **Document scope:** <seed | update delta>
- **Records from:** ADR-NNNN
- **Section scope:** included=<§N[, §N …]>, omitted=<§N[, §N …]>
```

Each field has one source: `Target` is the brief's location; `Document scope` and `Records from` are the two facts of step 1; `Section scope` is your step-3 verdict. Persistence re-derives the scope and the record numbers from the tree and blocks on disagreement, so a header that guesses is a header that fails. Then the twelve sections. **`Holds` states what content belongs in a section**, so you never infer its purpose from its arc42 title; that column is **word-identical to the description column of the persistence step's § The Persisted Layout**, which generates the section indices — changing a description is a two-file edit.

| § | Section heading | Subsections | Holds | Folder |
| --- | --- | --- | --- | --- |
| 1 | `## 1. Introduction and Goals` | `### 1.1 Requirements Overview`, `### 1.2 Quality Goals`, `### 1.3 Stakeholders` | What the system must achieve, the ranked quality goals every decision is judged against, and who cares about the outcome and what they need from the architecture. | `01-introduction-and-goals/` |
| 2 | `## 2. Architecture Constraints` | — | What the architecture is not free to choose: technology mandates, platform floors, regulatory rules, team conventions, existing contracts, and every would-be decision with only one viable option. | `02-architecture-constraints/` |
| 3 | `## 3. Context and Scope` | `### 3.1 Business Context`, `### 3.2 Technical Context` | The system's boundary: the external actors and neighbouring systems it exchanges information with, and the channels, protocols, and data formats that carry the exchange. | `03-context-and-scope/` |
| 4 | `## 4. Solution Strategy` | — | The shape of the solution in half a page: the technology choices, the decomposition approach, and the tactic adopted per quality goal. | `04-solution-strategy/` |
| 5 | `## 5. Building Block View` | `### 5.1 Whitebox Overall System`, one `#### 5.1.<n> Blackbox <Building Block>` per block, `### 5.2 Level 2`, `### 5.3 Level 3` | The static decomposition: what the system is made of, level by level, what each block provides and requires, and where its code lives. | `05-building-block-view/` |
| 6 | `## 6. Runtime View` | one `### 6.<n> <Scenario name>` per scenario | How the building blocks collaborate at runtime, one scenario per flow that crosses a boundary or realizes a quality goal, including its error path. | `06-runtime-view/` |
| 7 | `## 7. Deployment View` | — | The infrastructure the system runs on: the nodes and runtimes, what is deployed where, and the mapping of building blocks onto them. | `07-deployment-view/` |
| 8 | `## 8. Cross-cutting Concepts` | one `### 8.<n> <Concept name>` per concept | The concepts that cut across building blocks — error handling, persistence, security, validation, logging, transactions, testing — as mechanisms actually in place. | `08-crosscutting-concepts/` |
| 9 | `## 9. Architecture Decisions` | — (the decision log table) | The decision log — one row per architecturally significant decision, with its full record beside it in this folder. | `09-architecture-decisions/` |
| 10 | `## 10. Quality Requirements` | `### 10.1 Quality Requirements Overview`, `### 10.2 Quality Scenarios` | The quality goals made measurable: scenarios with a stimulus, a response, and a measure carrying a number and a unit. | `10-quality-requirements/` |
| 11 | `## 11. Risks and Technical Debts` | — | The risks this system carries and the debts it has taken on, each with a mitigation or an explicit acceptance. | `11-risks-and-technical-debts/` |
| 12 | `## 12. Glossary` | — | The terms this document uses in a specific sense, and the ones the project and its requirements use differently. | `12-glossary/` |

Then the three appendix headings: `## Appendix A — Decision Records` (one `### ADR-NNNN: <title>` per decision, full text), `## Appendix B — Work Packages` (the package table and the `Package check:` verdict, or `_None — no change decided_`), and `## Appendix C — Layout Map` (the map of § Layout Map).

Every omitted heading carries one of **three markers, and the set is closed** — no other wording, no free-form reason; the marker names the *type*, and the type is what a later reader uses to tell a judgment from a gap from a no-op.

| Marker | Used for |
| --- | --- |
| `_Omitted — not architecturally significant for this objective_` | nothing durable to write here for this objective |
| `_Omitted — no evidence in context Workfile_` | the evidence base does not cover it |
| `_Not affected by this change_` | update delta only: a whole section the delta does not write — persistence never writes this one into the tree |

Four mechanical rules govern the shape; everything else in this skill is judgment. (1) **Write or mark every heading** — the twelve sections, their fixed subsections, and the three appendix headings all appear, at the levels above; the variable subsections appear as often as your content needs and no more. (2) **Markers come from the closed set only.** (3) **Write no template guidance text and no attribution notice** — every word in the Workfile is yours, so there is nothing to delete and no notice to keep. (4) **Resolve every placeholder**; angle brackets mark fill-ins, and a row shown here is an example of shape, not a required count.

## Layout Map

Appendix C is the projection of your Workfile onto the fixed folder layout — the twelve folders of § Document Shape, which persistence creates when the target is absent. Persistence copies by it without judgment, so the judgment — how many documents a section gets — is yours, made here, and reviewable before anything is written.

**Split rule.** One document per section by default, named `01-<section-slug>.md`. Split a section only when it holds **three or more** units of its natural grain that a reader would consult independently *and* each is more than a short paragraph; two units are one document. The natural grain is: §5 the whitebox overview plus one document per building-block group a reader navigates to separately; §6 one per scenario; §8 one per concept; §10 overview versus scenarios; and §9 **always one record per decision**, fixed by the record format and never subject to the threshold. Sections 1, 2, 3, 4, 7, 11, and 12 are one document unless the grain rule clearly applies.

**Map format** — one row per document, in reading order, under `## Appendix C — Layout Map`:

```markdown
| Workfile heading | Target path | Promotion |
| --- | --- | --- |
| `## 2. Architecture Constraints` (whole section) | `02-architecture-constraints/01-architecture-constraints.md` | 1 |
| `### 5.1 Whitebox Overall System` (own body) | `05-building-block-view/01-whitebox-overall-system.md` | 2 |
| `## 9. Architecture Decisions` (log table) | `09-architecture-decisions/README.md` (rows appended) | — |
| `### ADR-0016: <title>` | `09-architecture-decisions/0016-<slug>.md` | 2 |
```

Rules that make the map mechanical:

1. **One root per document.** A row maps exactly one heading plus every descendant no other row maps; the parent document ends where the first carved-out child begins. Never group siblings into one row — two roots would mean two H1s.
2. **Totality.** Every heading below an included `## N.` is covered exactly once, by its own row or by its nearest mapped ancestor. Walk the headings against the map once the last section is drafted.
3. **Three path patterns, no others.** **(i) Topic document** — `<folder>/NN-<slug>.md`, `NN` two-digit and contiguous from `01` within that folder in map order, the slug the kebab-case of the row's root heading; promotion = the root heading's depth − 1. **(ii) Decision record** — `09-architecture-decisions/NNNN-<slug>.md`, four-digit, continuing from the header's `Records from:`; promotion `2`. **(iii) The `## 9.` heading itself** — `09-architecture-decisions/README.md`, promotion `—`, the one named exception: §9's body *is* the generated log.
4. **Rows that name no path** take no part in the totality walk: `→ index (omitted)` for a marker-only subsection inside a split section, and — in update-delta scope only — two row forms that act on something already persisted: `| <existing document heading> | → superseded — <reason> | — |`, which retires a topic document of an included section, and `| ADR-NNNN (existing record) | → status: <status text> | — |`, which flips the `Status:` line — and nothing else — of a record that one of this Workfile's Appendix A records, or an already-accepted record, names as superseded under `Related`. The status text is exactly `Superseded by ADR-MMMM[, ADR-MMMM …]` when the superseding record replaces the whole Decision, or `Accepted — superseded in part by ADR-MMMM[, ADR-MMMM …]` when any clause of it still stands; the persistence step's § Workflow step 5 owns the grammar and its preconditions — this is an echo. When the record already carries a supersession form, carry its IDs forward and append yours.
5. **Update-delta accounting.** Read each included section's index before mapping. Every **topic** document already in that folder is accounted for exactly one of three ways: re-authored by a path row, retired by a supersession row, or **carried forward byte-identical by having no row at all**. Existing documents keep their ordinals; new ones continue the folder's sequence. In seed scope a supersession row is a defect.
6. **Appendix C is never persisted**, and neither is Appendix B. Only §1–§12 and the Appendix A records reach the project tree.

## Workflow

1. **Read the brief and the inputs; resolve the two target facts; open nothing you will overwrite.** Read every named Workfile. Then, at the brief's location, resolve exactly two filesystem facts: the **identity rule** — the folder layout exists if and only if `README.md` and `01-introduction-and-goals/README.md` are both there → `Document scope: update delta`, else `seed`; and the **highest decision-record number** across `<location>/09-architecture-decisions/`, `docs/adr/`, `docs/decisions/`, and `adr/` → `Records from:` the next number, `ADR-0001` when none. In update-delta scope read the existing top index and the §1, §4, §5, and §9 folders, plus whatever the objective touches. Any other architecture document the context Workfile inventoried is **evidence you read, never a target you write toward**: the document scope stays `seed` and you name that document in your report. Spot-check the codebase to confirm the structure you build on, and record what you could not confirm as an **investigation gap**.

2. **Quality goals first.** Adopt the ranked 3–5 goals from the requirements Workfile verbatim into §1.2. Absent one, **infer** 3–5 from the evidence — what the structure, the tests, the error handling, and the dependencies are evidently optimized for — rank them, and mark each inferred one with the paths it was inferred from. They are the evaluation columns of every options table, the tactics §4 names, and the source of §10.

3. **Assess, then scope.** From the context Workfile and the existing document, establish what the architecture **is**: blocks, boundaries, embodied concepts, decisions in force. From the objective, establish what **changes** — nothing, when the objective is to record the system. Include a section when it would hold durable content the objective calls for: structure the objective changes or introduces, or existing structure within the objective's reach that is not yet, or wrongly, recorded. Otherwise mark it omitted. Guidance: an objective that records the system includes every section the evidence supports; an objective that changes it includes §1, §4, §5, §6, §8, §9, §10, §11 and adds §2, §3, §7, §12 only when constraints, boundaries, deployment, or vocabulary change. Define document-stable requirement IDs in §1.1 under a prefix that collides with nothing already persisted there, and cite those. In update-delta scope apply the **refresh rule** to each re-authored document: carry every durable statement forward, drop every task-scoped one. Then write the `Section scope:` header line.

   **Content of the framing sections.** §1.3 lists each stakeholder role with the one concern the architecture must answer for it — never a directory of names. §2 lists each constraint with its source (mandate, platform, regulation, existing contract, team convention) and what it forecloses; a decision with a single viable option is recorded here, not as a record. §3.1 names the external actors and neighbouring systems and what each exchanges with the system, in business terms; §3.2 names the channels — protocols, APIs, files, queues, data formats — that carry those exchanges, each cited from the boundary interfaces in the context Workfile, with one `flowchart` placing the system as a subgraph. §12 defines only the terms this document uses in a specific sense and the terms the project or its requirements use differently — never a general vocabulary.

4. **Decide what is significant; then decide, or record what is already in force.** Apply the significance test. For a decision made now — `Kind: decided` — state the forces, enumerate **at least two genuinely distinct options** scored against the §1.2 goals by name and the §2 constraints, choose one in the indicative, and give the consequences split into positive, negative, and what becomes harder. For a decision the system already embodies — `Kind: recorded` — state the context from the evidence, the decision in the present indicative citing paths, and the consequences as they have materialized; there is no options table. Number from the header's `Records from:`. Summarize the set in §4 — stable structural decisions only, never rollout, sequencing, or packages — and log every record in §9. An improvement you conclude that the objective did not ask you to decide goes to §11.

5. **Structure — §5 and §8.** §5 Level 1 is a whitebox of the system, or of the affected subsystem, as a Mermaid diagram plus a contained-blackboxes table and the motivation for the decomposition. Write one blackbox per building block the document covers: purpose and responsibility, provided and required interfaces, code location, and the §1.1 IDs it realizes. Interfaces must be precise enough that a failing test can be written from them without opening the implementation — signatures, parameter and return types, error and failure contracts, schema changes, and the invariants a caller may rely on. Go to Level 2 only for blocks changed internally. §5 carries boundaries, interfaces, invariants, and code locations — never helper structure, control flow, naming inside a block, or test-case selection. §8 carries only mechanisms that persist; a temporary measure is a §11 risk with its retirement condition. Every block cites a real path.

6. **Behavior and deployment — §6 and §7.** §6: one `sequenceDiagram` per flow that crosses a module boundary or realizes a quality goal, typically one to three, each naming the §1.1 IDs it realizes and walking an error path. §7: the nodes and runtimes the system runs on, what is deployed onto which node, and the mapping of §5 blocks onto deployment units, with a `flowchart` of nodes as subgraphs — read from deployment manifests, container or infrastructure definitions, or CI configuration cited in the context Workfile. Include §7 when such evidence exists or the objective changes it; otherwise carry its marker. **A deployment you infer from convention is a gap, not a §7.**

7. **Quality requirements and risks — §10 and §11.** §10: one to three scenarios per §1.2 goal, stimulus → response → measure with a number and a unit, each marked observed or unverified when inferred. §11: the risks and debts **of the system** — what a future maintainer inherits — each with impact, likelihood, and either a mitigation or an explicit acceptance. A limitation of this run is an investigation gap in the report, never a §11 entry.

8. **Work packages — Appendix B, when the objective decides a change implementation will follow.** Per package: name, **write set** (paths), **owned requirement and criterion IDs**, contracts **provided** and **consumed** naming the §5 interfaces, **test seam**, **dependencies**, and a **done criterion** — which is where a tactical choice the ratifier wants written down belongs. Put shared-surface churn into a single sequential scaffold package that runs before any parallel wave. Record the verdict:

   ```text
   Package check: packages=<n>, disjoint write sets=<yes/no>, contracts fixed upfront=<yes/no>, independently testable=<yes/no>, shared-surface churn isolated=<yes/no>, fan-out ≤ 4=<yes/no> → <sequential | scaffold→parallel(<k>)→integrate>
   ```

   Parallel requires **all five** checks to read `yes`. Slice vertically — every in-scope criterion is owned by exactly one package. When the objective decides no change, the heading carries `_None — no change decided_` and your report says `Package check: n/a`.

9. **Map the layout (Appendix C), create the Workfile, report.** Split section by section under the split rule, write one row per document in reading order, then walk every heading under every included `## N.` against the map exactly once. In update-delta scope give each included section its three-way accounting. **Create** the Workfile at the path the brief names — if a file already exists there, ask, and write nothing. Then report per § Output Contract.

## Decision Record Format

One record per structurally significant decision, in Appendix A, in this structure:

```markdown
# ADR-NNNN: <decision title, naming the choice, not the topic>

- **Status:** Proposed
- **Date:** <YYYY-MM-DD>
- **Kind:** decided | recorded (evidence: <paths>)

## Context
<The situation and the forces in tension. Name the affected §1.2 quality goals explicitly.>

## Options Considered
| Option | Pros | Cons | <quality goal 1> | <quality goal 2> | … |
| --- | --- | --- | --- | --- | --- |

## Decision
<One option, stated in the indicative. Then the rationale, tied to the ranked
quality goals and the §2 constraints.>

## Consequences
- **Positive:** …
- **Negative:** …
- **Becomes harder:** …

## Related
<§1.1 requirement IDs · building blocks (§5) · other record IDs · the implementing package>
```

`Options Considered` is present **if and only if** `Kind: decided`; a `recorded` decision states what the system does, in the present indicative, followed by the evidence that establishes it, and its `Consequences` are the ones that have actually materialized. Title records by the choice made ("Event-sourced order history"), not by the question asked, so the §9 log reads as a list of positions. Number from `Records from:`, and link each record from the §9 table by its appendix anchor — persistence rewrites the link to the record's path. A record that supersedes an existing project record names it in `Related` (as `supersedes …`, stating which clauses or citations) and in §9, and adds a `→ status:` row for it in Appendix C (§ Layout Map rule 4); persistence makes that one-line flip, never you.

## Output Contract

**Workfile** — the one markdown file you create, at the path the brief names (task-directory pattern `NN-architecture-arc42.md`), in this order: the title and header block of § Document Shape; `## 1.` through `## 12.`, every heading present and either filled or carrying its marker; `## Appendix A — Decision Records`; `## Appendix B — Work Packages`; `## Appendix C — Layout Map`. No attribution notice: the document carries no licensed text.

**Report** (not written to the Workfile), in this order:

1. The `Section scope:` line.
2. The decision list — ID, title, `Kind`, one line of rationale each; where a record supersedes an existing one, the rationale line names the superseded ID and the status text its `→ status:` row carries, so the checkpoint surfaces the flip beside the decision that causes it.
3. The `Package check:` line, or exactly `Package check: n/a`.
4. Open risks from §11, worst first.
5. **Investigation gaps** — what you could not confirm, what you assumed instead, and which section is weakest as a result, including every section marked with the no-evidence marker.
6. The Workfile path, `Target:`, `Document scope:`, `Records from:`, any prior documentation found and left as evidence, and the layout summary: documents per included section, every split section with its unit count, and the record paths.

**Failure handling:**

- No location in the brief → ask, and write nothing.
- A file already exists at the Workfile path → ask which path to use, and write nothing. Overwriting destroys a peer step's output.
- The location holds a `README.md` with a foreign H1 and no folder layout → the scope is `seed`; report it, and let persistence apply its collision rule.
- A partial structure you cannot classify — a `README.md` with this document's H1 but no `01-introduction-and-goals/` → report it and stop. Never guess a scope.
- Inconsistent record numbering — gaps, duplicates, non-numeric names → take the highest number you can parse and report the inconsistency.
- A named input Workfile is missing or unreadable → report it, name the sections thinned by its absence, and fabricate nothing.
- The codebase contradicts an input Workfile → design against the codebase and report the contradiction first.
- A decision needs evidence you would have to investigate → write the record with an explicit `Open question` line naming the missing evidence, and raise an investigation gap rather than researching it.
- The brief asks you to write into the project tree → decline, deliver the Workfile, and report the boundary.

## Quality Criteria

- One Workfile exists, created at the path the brief named, and no file under the target project changed.
- Every header field equals its source: `Document scope` and `Records from` match what the tree shows.
- §1.2 holds three to five ranked quality goals, written before any decision.
- Every included section holds durable content the objective calls for, and every omitted one carries a marker from the closed set of three.
- **Every statement in §1–§12 passes the long-term-relevance test** — re-read the filled sections against the tell-tales before reporting.
- Every reference in §1–§12 is document-stable: a repository path, a section number, a record ID, or a requirement ID §1.1 defines.
- Every record passes the significance test, reads `Status: Proposed`, carries its `Kind:` line, and — when `decided` — weighs at least two genuinely distinct options against the goals by name.
- §4, §9, and Appendix A correspond one-to-one.
- Every §5 block cites a real path, and its interfaces are precise enough to write a failing test against without reading the implementation.
- Every diagram element traces to the specification or to an input Workfile, and the Mermaid markup is well-formed.
- Appendix C is total and pattern-conforming, and every split section names three or more independently consulted units.
- Every `→ status:` row names a record that an Appendix A record — or an already-accepted record — supersedes under `Related`, carries one of the two fixed status forms, and preserves any IDs the record's status line already holds; no record of this run's Appendix A is named by one.
- Appendix B, when present, holds vertical slices, each in-scope criterion is owned exactly once, and the `Package check:` line is consistent with the table.

## Anti-Patterns

- **Template worship**: filling all twelve sections for an objective that reaches three, burying the signal in ceremony. Prune, and mark what you pruned.
- **Silent deletion**: dropping an irrelevant section instead of marking it omitted, leaving a reader unable to tell considered-and-excluded from forgotten.
- **Guessing the target**: writing `seed` without checking the location, or numbering from `0001` in a project that already holds records. Both fail at persistence and cost a resume.
- **Splitting by habit**: one document per subsection because the layout allows it. The threshold is three independently consulted units.
- **A map that is not total**: a heading in two rows, or in none, because a section was re-drafted after the map was written. Persistence copies what the map says and silently loses what it omits.
- **Single-option `decided` records, or reconstructed options on a `recorded` one**: the first is a rationalization, the second presents a deliberation nobody held.
- **Uncited claims**: a §5 block, a §6 flow, or an inferred quality goal with no evidence path. Without the citation a reader cannot tell the architecture that exists from the one you assumed.
- **Run provenance in the document**: a workspace path, a task directory, a Workfile name, a review verdict, or "at the time of writing" inside §1–§12. Each resolves against a workspace that is deleted when the task ends.
- **Task-scoped content in a durable section**: rollout sequencing in §4, helper structure in §5, a flow local to one package in §6, a workaround as a §8 concept — each is stale the moment the task closes.
- **Recording the tactical**: a naming convention, a refactoring, or a test layout as a §9 row or a record. It fails the significance test; a done criterion or a §11 debt is its home.
- **A §11 entry about the run rather than the system**, and **architecture astronautics** — a pattern, a layer, or a bus no §1.2 goal asks for. Every structural move needs a named driver.
- **Hedged recommendations, layer-split packages, and parallel by optimism**: a decision the ratifier must make themselves is not a decision; a package named for a layer owns no criterion; and overlapping write sets corrupt the shared tree.
