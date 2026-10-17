---
name: brokk-architecture-persistence
description: Persist a ratified arc42 architecture Workfile into the target project by its layout map — creating the fixed folder layout when the target is absent and the document is a seed, otherwise merging into the existing layout document-by-document — topic documents per section, decision records in the decisions folder, every index generated, never deleting and never deciding.
---

# Architecture Persistence

## Purpose

Persist a ratified arc42 architecture Workfile into the target project — topic documents per section, decision records in the decisions folder, every index generated, never deleting.

The Workfile is authored as one document; the split into files is decided in its **Appendix C — Layout Map** (`Workfile heading → target path → promotion`) and executed here. Your transformation is mechanical and fully specified: copy each mapped heading and its unclaimed descendants into the path the map names, promote by the distance the map states, rewrite the decision log's link column, generate the indices. Nothing about the architecture — and nothing about the split — is decided here. A section whose content you would have to invent is a gap to report; a document the map does not name is structure you must not create.

**The existence rule.** You create the folder layout in exactly one case: the target — after the collision rule, when it applies — is **absent** *and* the Workfile header reads `Document scope: seed`. A present layout under a `seed` header would be overwritten; an absent target under an `update delta` header was drafted against a document that does not exist. Both are blocking report items, never something you fix by choosing a scope yourself.

**This section and the two that follow it — § The Persisted Layout and § What Is Not Persisted — are the single source of truth for the persisted layout.** Other steps refer to it by role ("the persisted layout", "the fixed folder table"); the names and formats live here.

### The Persisted Layout

A persisted arc42 document is a **directory of section folders**. Each of the twelve numbered sections is a folder holding a generated `README.md` index and zero or more `NN-<slug>.md` topic documents. Section 9's folder holds the decision records, and its index is the decision log.

```text
docs/architecture/
├── README.md                                  # top index (generated)
├── 01-introduction-and-goals/
│   ├── README.md                              # section index (generated)
│   └── 01-introduction-and-goals.md           # single topic document (default name = section slug)
├── 05-building-block-view/
│   ├── README.md
│   ├── 01-whitebox-overall-system.md          # topic documents: NN-<slug>.md, NN contiguous from 01 in map order
│   └── 02-<building-block-group>.md
├── 07-deployment-view/
│   └── README.md                              # omitted section: index only, marker verbatim in the state line
├── 09-architecture-decisions/
│   ├── README.md                              # the decision log
│   └── 0016-<slug>.md                         # records keep NNNN — global identifiers, append-only
└── 12-glossary/
    ├── README.md
    └── 01-glossary.md
```

**Fixed folder table.** These twelve folder names are the shared vocabulary — no variants, no renumbering, no thirteenth section. The last column is each section index's one-line description, copied verbatim into the index you generate. That column is **word-identical to the `Holds` column of the drafting step's § Document Shape**; changing a description is a two-file edit.

| § | Folder | Section heading it carries | One-line description (the section index's third line) |
| --- | --- | --- | --- |
| 1 | `01-introduction-and-goals/` | `## 1. Introduction and Goals` | What the system must achieve, the ranked quality goals every decision is judged against, and who cares about the outcome and what they need from the architecture. |
| 2 | `02-architecture-constraints/` | `## 2. Architecture Constraints` | What the architecture is not free to choose: technology mandates, platform floors, regulatory rules, team conventions, existing contracts, and every would-be decision with only one viable option. |
| 3 | `03-context-and-scope/` | `## 3. Context and Scope` | The system's boundary: the external actors and neighbouring systems it exchanges information with, and the channels, protocols, and data formats that carry the exchange. |
| 4 | `04-solution-strategy/` | `## 4. Solution Strategy` | The shape of the solution in half a page: the technology choices, the decomposition approach, and the tactic adopted per quality goal. |
| 5 | `05-building-block-view/` | `## 5. Building Block View` | The static decomposition: what the system is made of, level by level, what each block provides and requires, and where its code lives. |
| 6 | `06-runtime-view/` | `## 6. Runtime View` | How the building blocks collaborate at runtime, one scenario per flow that crosses a boundary or realizes a quality goal, including its error path. |
| 7 | `07-deployment-view/` | `## 7. Deployment View` | The infrastructure the system runs on: the nodes and runtimes, what is deployed where, and the mapping of building blocks onto them. |
| 8 | `08-crosscutting-concepts/` | `## 8. Cross-cutting Concepts` | The concepts that cut across building blocks — error handling, persistence, security, validation, logging, transactions, testing — as mechanisms actually in place. |
| 9 | `09-architecture-decisions/` | `## 9. Architecture Decisions` | The decision log — one row per architecturally significant decision, with its full record beside it in this folder. |
| 10 | `10-quality-requirements/` | `## 10. Quality Requirements` | The quality goals made measurable: scenarios with a stimulus, a response, and a measure carrying a number and a unit. |
| 11 | `11-risks-and-technical-debts/` | `## 11. Risks and Technical Debts` | The risks this system carries and the debts it has taken on, each with a mitigation or an explicit acceptance. |
| 12 | `12-glossary/` | `## 12. Glossary` | The terms this document uses in a specific sense, and the ones the project and its requirements use differently. |

The descriptions and the subsection inventory behind them are original content of this repository; the section numbers and titles are arc42's vocabulary, and no arc42 guidance text is reproduced here or anywhere under a target.

**All twelve folders always exist**, each holding at least its index. Git tracks no empty directory, and a missing folder cannot be told apart from one deleted by accident. A fixed folder set makes completeness a listing check.

**Identity rule (one).** Contents decide, never the directory's name: the target is the **folder layout** if and only if it holds `README.md` *and* `01-introduction-and-goals/README.md`. Anything else found at the location — an architecture document in any other structure — is **prior documentation**, not a target: you neither read it as a layout nor touch it.

**Collision rule.** On a seed, if the location holds a `README.md` whose H1 is not this document's, create the layout at `<Target>/arc42/` instead and report the fallback in the manifest. Never write over a `README.md` that is not this document's index.

**Topic document.** `NN-<slug>.md`: `NN` two digits, contiguous from `01` in layout-map order, `<slug>` the kebab-case of the document's root heading title; a section with one document names it `01-<section-slug>.md`. Decision records are `NNNN-<slug>.md`, four digits, continuing the project's record sequence — records are global identifiers and append-only — a record's body is never rewritten, and its one mutable field is the `Status:` line, promoted at its own persistence and later flipped only by a `→ status:` row (§ Workflow step 5) — whereas topic ordinals are folder-local ordering fixed at first fill. **In an update delta a folder's existing ordinals do not move**: a re-authored or carried-forward document keeps its ordinal, and a new document continues the folder's sequence.

**Per-document format.** A document is one root heading plus those of its descendants no other map row claims. Its H1 is the root heading promoted by `depth − 1`, and its body is promoted by that same distance:

```text
## 2. Architecture Constraints   →   # 2. Architecture Constraints          (depth 2 → promote 1)
### 5.1 Whitebox Overall System  →   # 5.1 Whitebox Overall System          (depth 3 → promote 2)
#### 5.1.7 Consumed block …      →   # 5.1.7 Consumed block …               (depth 4 → promote 3)
### ADR-0016: <title>            →   # ADR-0016: <title>                    (depth 3 → promote 2)
```

Promoting by any other distance leaves the document with no H1 or with two. Further rules: the **backlink line** is the second content line, `_Part of [<Title>](../README.md) · [§N](README.md)._`, and records carry none; **markers are copied verbatim**, never reworded or dropped; **carved-out children stop the parent**, which ends where the first carved-out child began; **prose `§N` references stay as written**, because navigation is the index's job; **records** are the Appendix A text verbatim with `Status:` promoted to `Accepted` for exactly the `ratified=` IDs.

**Section index (generated).** `# N. <Title>`, the backlink to the top index, the **one-line description from the fixed folder table**, then a state line — `_Omitted — <marker>_` for an omitted section, or a Documents table (`# · Document · Root heading · Last updated`) listing every live document in the folder in ordinal order, re-authored, new, and carried forward alike. "Omitted subsections" (markers verbatim) and "Superseded documents" (files a map **explicitly supersedes** with a `→ superseded — <reason>` row) follow when either applies. `09-architecture-decisions/README.md` is that section's index and the decision log in one file, its `ID · Title · Status · Date · Link` table holding one row per record, with `Link` rewritten from the Workfile's appendix anchor to the record's path relative to that index.

**Top index.** `README.md` at the directory root: the title, `- **Last updated:** <YYYY-MM-DD>`, `- **Status:** Accepted`, the generated-index note, a Sections table (`§ · Section · State · Docs · Last updated`) whose `State` is `filled` or `omitted — <reason>`, a Decision Records line naming the record directory, and a Change Log table (`Date · Scope · Sections written · Decisions added`) whose rows are **appended, never rewritten**. A top index is `Accepted` from the moment it exists; there is no earlier state.

**Carried-forward document.** In update-delta scope the map is **document-granular**: it names only the documents the delta writes. A topic document of an included section that the map neither names nor supersedes is **carried forward byte-identical** — not opened, not rewritten, not re-ordered — and keeps its Documents-table row at its existing ordinal. Silence in the map means carry forward, never supersede.

**Omitted section = index-only folder.** No topic document; the marker travels verbatim in the index's state line.

**No arc42 guidance text anywhere under the target, ever** — and therefore no attribution notice in any file under it.

### What Is Not Persisted

Appendix B (work packages) and Appendix C (the layout map) are transient and never written. Appendix A is the *source* of the record files, not a document. Workfile header lines and any process metadata — revision logs, contradiction notes, inputs notes — have no home in the layout: invent none, and where their durable substance is missing from a record or from §11, report the gap rather than closing it.

## When to Use

- Dispatched as the persistence step of the architecture workflow, after the decisions have been ratified.
- The brief supplies the architecture Workfile path, the `Ratification:` line, and the pinned baseline.
- Dispatched for a **correction** when a persisted topic document's Workfile source was corrected after persistence — the brief adds a `Re-persist:` line (step 6). Never for correcting a record: that is a superseding record in a delta.
- **Creating the layout is yours only under the existence rule** — never to "repair" a partial or foreign structure at the location.
- **Not for** deciding how a section splits into documents. Appendix C is that decision, already made.
- **Not for** authoring or revising architecture content. You transform and place what was ratified; a content gap is a report item.
- **Not for** persisting Appendix B or C, or for converting prior documentation found beside the target.
- **Not for** writing a Workfile. Your outputs are files in the target project; the workspace gains nothing.
- **Not on your own initiative.** Persisting a document nobody ratified is out of bounds even when the Workfile is sitting there.

## The Ratification Record

The ratification record is the one input that authorizes a status promotion. Its grammar is fixed here and nowhere else:

```text
Ratification: ratified=<ADR-NNNN[, ADR-NNNN …] | none>, withheld=<ADR-NNNN[, ADR-NNNN …] | none>, by=<user | adoption>
```

- **`ratified=`** — the decision IDs you promote to `Status: Accepted`.
- **`withheld=`** — the decision IDs the ratifier declined to promote. Their records persist exactly as authored, at `Status: Proposed`.
- **Totality.** Every `ADR-NNNN` in the Workfile's Appendix A appears in exactly one of the two lists. An ID in neither, in both, or absent from the Workfile makes the record invalid — it was written against a different revision of the document.

A missing or invalid record means no decision may be promoted: report `ratification=missing | invalid — <what fails>` and stop; persist nothing. Never infer a ratification from the fact that the run reached you.

## Workflow

1. **Collect the inputs.** The architecture Workfile path, the `Ratification:` line, the pinned baseline. Read the header's `Target:`, `Document scope:`, `Records from:`, and `Section scope:` lines, and Appendix C. An invalid ratification record stops the run here.

2. **Verify the target against the header; the tree is the fact, the header is a claim.** Apply the identity rule at `Target:`.
   - **Seed** — the target must be absent: no directory, or a directory holding no `README.md`. If it holds a `README.md` whose H1 is not this document's, apply the collision rule, make `<Target>/arc42/` the target, and re-check there.
   - **Update delta** — the target must be the folder layout, all twelve folders and their indices present, top index `Status: Accepted`.
   - **Records** — no Appendix A ID may already exist in any decision directory, and `Records from:` must be one above the highest number in use.

   Any failure → report `precondition failed — <scope mismatch | partial layout | record collision>: <what the tree shows>` and persist nothing. An unresolvable target path is likewise blocking, never an invitation to write elsewhere.

3. **Resolve the record directory.** An existing `docs/adr/`, `docs/decisions/`, or `adr/` always wins, in that order of search; otherwise the records go in `<target>/09-architecture-decisions/`.

4. **Seed scope — create and fill in one act.** Create the top index and the twelve section folders with their indices from the fixed folder table. Then, for every section, write the topic documents Appendix C names at the paths and promotions it states; a section the map leaves unmapped stays index-only with its marker in the state line. Write one record per Appendix A entry, `Accepted` if and only if that ID appears in `ratified=`. Rewrite §9's `Link` column **before** writing `09-architecture-decisions/README.md`. Generate every section index and the top index, `Status: Accepted`, with one Change Log row whose scope reads `seed`. The result is exactly the thirteen indices, the mapped documents, and the records — nothing else.

5. **Update-delta scope.** For each section in `Section scope: included=`, write exactly the documents Appendix C names and regenerate that section's index from the union of three cases — each document of the section falls into exactly one:
   - **Named by a path row** → replaced whole-file, or created there when the row is new, keeping existing ordinals.
   - **Named by a `→ superseded — <reason>` row** → left on disk untouched and listed under "Superseded documents" with that reason.
   - **Named by no row at all** → carried forward byte-identical.

   **§9 and new records.** For `09-architecture-decisions/README.md`, **append** the new rows at the end of the existing table — never reorder an existing row, and never rewrite one except its `Status` cell under a `→ status:` row. Write the new records at the numbers `Records from:` reserved.

   **Status-line supersession — the one exception to "never edit an existing record file."** For each Appendix C row `| ADR-NNNN (existing record) | → status: <status text> | — |`:
   - **Grammar (fixed here and nowhere else):** the status text is exactly one of `Superseded by ADR-MMMM[, ADR-MMMM …]` or `Accepted — superseded in part by ADR-MMMM[, ADR-MMMM …]`.
   - **Preconditions, all checked before any write:** `ADR-NNNN` resolves to exactly one `NNNN-*.md` in the record directory and is not an Appendix A ID of this run; every `ADR-MMMM` is in `ratified=` or already on disk at `Status: Accepted`; each such record names `ADR-NNNN` under its `## Related` heading (in Appendix A when new, in its file when existing); the record's current status line is `- **Status:** Accepted` or a prior supersession form whose every ID the new text also carries — a `Proposed` record is refused. Any failure → `precondition failed — status supersession: <which>`, and nothing is written.
   - **Edit:** replace **exactly the line beginning `- **Status:** `** in the record with `- **Status:** <status text>`, and **exactly the `Status` cell** of that record's row in `09-architecture-decisions/README.md` with the same text; every other byte of both files stays as it was (`git diff --numstat` for the record reads `1 1`) — no body line, `Date:`, `Kind:`, backlink, or `Last updated` changes.

   **Top index and everything else.** Regenerate the top index's header and Sections table and append exactly one Change Log row. **Never delete**, and **never create a folder** — all twelve were verified present in step 2. Every other path — every pre-existing record not named by a `→ status:` row included — stays byte-identical.

6. **Correction scope — named documents only.** When the brief carries `Re-persist: <path>[, <path> …] — <reason>`, a persisted document's Workfile source has been corrected and this run re-persists exactly those documents. It is neither a seed nor a delta, and the header's `Document scope:` is not applied; the grammar is fixed here and nowhere else. Preconditions, replacing step 2's: the target is the folder layout by the identity rule; every named path exists in it and is a topic document — a path under the record directory is refused (`precondition failed — record correction: <path>`; a record's body is corrected only by a superseding record in a delta, and its status line only by that record's `→ status:` row in the same or a later delta — never in correction scope); Appendix A IDs already on disk are expected, and `Records from:` is not checked. The `Ratification:` line is still validated and promotes nothing. Then: replace each named document whole-file from the Workfile heading Appendix C assigns it, at its existing ordinal, with the same promotion and backlink; regenerate each affected section's index and the top index's header and Sections table, so that the `Last updated` of the named documents and of their sections is the run date; append exactly one Change Log row with scope `correction`. Write no record, append no §9 row, and leave every other path byte-identical. The manifest reads `scope=correction`, action `replaced` for each named path.

7. **Report the persistence manifest** in the session's evidence block:

   ```text
   Persistence: target=<path>, scope=<seed | update delta | correction>, layout=<created | existing>, collision-fallback=<none | <path>>
   | Path | Action | Source |
   | --- | --- | --- |
   | README.md | regenerated | top index |
   | 05-building-block-view/README.md | index regenerated | section index |
   | 05-building-block-view/01-whitebox-overall-system.md | created | Workfile §5.1 |
   | 05-building-block-view/02-request-router.md | carried forward | — |
   | 09-architecture-decisions/0016-<slug>.md | created (Accepted) | Appendix A ADR-0016 |
   | 09-architecture-decisions/0014-<slug>.md | status superseded | Appendix C → status: row (ADR-0017) |
   | 01-introduction-and-goals/01-introduction-and-goals.md | untouched | — |
   ```

   **Actions vocabulary — these words and no others:** `created`, `replaced`, `regenerated`, `index regenerated`, `appended <n> rows`, `superseded (kept)`, `status superseded`, `carried forward`, `untouched`. One row per path in the target, including the untouched ones: the manifest is what the review diffs against, so a path you left alone is as much a claim as a path you wrote.

## Quality Criteria

- **The existence rule held**: the layout was created only on an absent target under a `seed` header, and an `update delta` found all twelve folders present at baseline.
- After a seed, every section folder holds exactly the topic documents Appendix C names for it — or only its index when the section is omitted — and the record directory holds one record per Appendix A entry.
- Every document this session wrote equals its Workfile source exactly, modulo the `depth − 1` promotion and the added backlink line; every document has exactly one H1; no document exists that the map does not name.
- Every omitted section is an index-only folder whose index carries the Workfile's marker verbatim, and every section index carries its H1, backlink, and the description from the fixed folder table.
- **No topic document was deleted**, and every "Superseded documents" entry is backed by a `→ superseded — <reason>` row.
- **Carried-forward documents are byte-identical** to the pinned baseline, keep their ordinals, and still hold their rows in the regenerated Documents table.
- Every record equals its Workfile source modulo the two-level promotion and the promoted status; `Status: Accepted` appears for exactly the `ratified=` IDs and every `withheld=` ID reads `Proposed`.
- Every §9 row's link resolves relative to `09-architecture-decisions/README.md` and matches that record's own header; rows are append-only apart from a `→ status:` cell.
- Every `→ status:` row produced exactly one changed line in its record — the `Status:` line, now in one of the two fixed forms — and exactly one changed cell in §9 — that record's `Status`; every superseding ID it names is `Accepted` after this run and names the superseded record under `Related`; every pre-existing record not named by such a row is byte-identical to the baseline.
- In update-delta scope the changed-path set is exactly the mapped documents of the `included=` sections, those sections' indices, §9's index, the new records, the records named by `→ status:` rows, and the top index; everything else is byte-identical.
- In correction scope the changed-path set is exactly the `Re-persist:` paths, their section indices, and the top index; no record was written and no §9 row appended; the `Last updated` of every named document and its section equals the run date.
- The top index's Change Log grew by exactly one row and its prior rows are unchanged.
- No arc42 guidance text and no attribution notice exists anywhere under the target (grep = 0); Appendices B and C were not persisted, and no home was invented for process metadata.
- The task directory gained no file, and the manifest matches what the diff actually shows.

## Anti-Patterns

- **Creating outside the existence rule** — adding folders on an `update delta` because one was missing, or seeding over a present document because the header said `seed`. A tree that disagrees with the header is a drafting defect to report, not a shape to repair.
- **Seeding over a filled document** — treating the header as authority against the tree. The header is a claim; the tree is the fact, and when they disagree you stop.
- **Deleting a superseded document** — removing `01-building-block-view.md` because the new map calls that content `01-whitebox-overall-system.md`. A re-split adds and supersedes; it never removes.
- **Superseding by omission** — treating a document as retired because the map does not name it. Silence means carry forward byte-identical; retirement is the explicit row the ratifier saw.
- **Rewriting a carried-forward document** — re-flowing, renumbering, or tidying a document the map does not name. Carried forward means byte-identical.
- **Splitting below or above the map** — giving §5.1.1 its own document because the layout allows it, or merging two mapped documents because it reads better. Structure you create that the map does not name is unreviewed.
- **Overwriting instead of merging** — writing the delta's documents over every folder in an existing directory deletes content whose removal nobody reviewed.
- **Rewriting existing §9 rows beyond a `→ status:` cell, or regenerating an index without reading it first** — the log is append-only, and the Change Log is the one part of the top index that cannot be reconstructed from the tree.
- **Rewriting prose `§N` references into links**, or **writing `_Not affected by this change_` into the tree** — the first is unreviewable churn, the second is delta bookkeeping that means nothing to a reader.
- **Persisting Appendix B or C, or inventing the missing piece** — planning material goes stale immediately, and a section the Workfile left neither mapped nor marked is a gap to report, not a file to fill.
- **Promoting statuses wholesale, copying guidance into the target, or writing a Workfile** — each substitutes your judgment for a ratification, a license boundary, or a medium that is not yours.
- **Replaying a delta to fix one document, or hand-editing the persisted file** — the first collides on record IDs and duplicates §9 and Change Log rows; the second leaves the document's `Last updated`, its section index, and the top index behind. A correction names its paths in `Re-persist:` and touches nothing else.
- **Touching any line of an existing record other than its `Status:` line, or flipping a status no ratified record claims** — "while I'm in the file": fixing a citation, a date, a typo, a `Related` list. The status line is the one field a superseding record may flip, and only because that record names the superseded one; everything else in a record is answered by a later record, never rewritten.
