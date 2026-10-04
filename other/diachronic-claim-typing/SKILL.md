---
name: diachronic-claim-typing
version: 1.0.0
description: Use before literature search and before writing cross-period connection sentences in conceptual history, genealogy, or institutional-history papers, to type claims and audit section selection and over-connection
---

# Diachronic Claim Typing Skill

## Purpose

For papers that connect norms, practices, or institutions across time, **assign a claim type first**, then select sources, design period-sections, and write connecting sentences. If the type outruns the evidence, shrink the claim. This is not a tutorial in writing survey history.

Genealogy here is **selective connection of period-sections**, not a complete chronicle. What is forbidden is presenting that selection as if it were the whole history.

## Trigger Conditions

- When the research plan involves conceptual history, genealogy, intellectual or institutional history, reception history, or a formation/transformation arc
- When classics, critical editions, statutes, examination systems, or journal-primary texts likely sit outside paper APIs such as OpenAlex
- Before writing cross-period connectors ("from…", "adaptation", "continuity", "unique to the present")
- When cherry-picking, anachronism, or missing transmission evidence has been flagged

**Do not invoke** for single-period empirical work or cross-sectional surveys that do not claim temporal connection. Use [`literature-search`](../literature-search/SKILL.md) and [`claim-evidence-gate`](../claim-evidence-gate/SKILL.md) instead.

## Claim Types

Give each diachronic claim **exactly one** type. Split compound sentences.

| Type | What it asserts | Evidence required | Failure | Fallback |
| :--- | :--- | :--- | :--- | :--- |
| **T0 existence** | Source S contains text or record X | Locator (edition, transcript ID, catalogue number) plus a verified excerpt in `literature/papers/` | Invented pages; unread secondary | Do not cite |
| **T1 interpretation** | Inside that text, X can be read as Y | T0 plus acknowledgement of alternative readings | Unique-meaning lock | "a readable cross-section" |
| **T2 institution** | A practice was a branch of an institution or curriculum | Primary statute, textbook, or case | One case as nationwide | Keep it a case claim |
| **T3 transmission** | A was translated, imported, or named as B | Translation bibliography, introduction primary, or named citation | Similarity as causation | T3b |
| **T3b juxtaposition** | Structural similarity of A and B (no causal claim) | T0 on both plus a similarity map | Juxtaposition without similarity | Cut the section or the claim |
| **T4 continuity** | A method or norm persisted through period P | A primary that argues continuity, or primaries at multiple dates | Two classical points as "until…" | Cross-section only |
| **T5 novelty** | Conditions at period P differ in kind | Survives hostile reduction (quantity/time, degree) | The historian already states continuity or a precedent | Degree difference, or making a norm/practice contradiction visible |

**Reception** ("has been received as", "use as reception history") is a claim about someone else's interpretive act. Evidence requirements are **T3**. T1 is text-internal reading only. Without a reception primary, weaken to T1 "readable as".

### Prohibition N1 (non-identification)

Not a type. Applies to every type. Do not write that a historical actor held this paper's coined concept. Exception only when that actor explicitly self-identifies.

## Workflow

### Step 1: Paper type and inventory

Read `research-plan.md`. Stop if the paper is not diachronic.

If it is, **before** literature search create `docs/<paper-id>/design/sot/diachronic-claim-inventory.md` (or `docs/design/sot/` in a single-paper repo). Place intended connections with provisional types.

```markdown
| Section | Claim (one sentence) | Type | Evidence (`papers/` + locator) | Fallback |
```

If `paper-outline.md` exists, copy the type ID as one line in the section note (inventory remains source of truth).

### Step 2: Selection criteria and counter-lineage

Write one paragraph into the inventory **before searching**.

1. **Selection criteria** (canonicity, institutional embedding, OA primary available, etc.)
2. **Counter-lineage**: name the **strongest** line a reviewer would raise, and why it is out of scope (no straw alternatives)
3. **Sense of "formation"**: not encyclopedic origin, but identifying a recurrent starting point, etc.

### Step 3: Primary layer and search channels

1. Keep survey histories as Discovery, not citation grounds. Descend to the classics, statutes, or primary articles they rest on.
2. If a primary is inaccessible, shrink that typed claim or omit the section. Purchase or subscription follows **project policy** (this skill does not order purchases).
3. Channels outside paper APIs (classical digital libraries, J-STAGE, CiNii, institutional repositories) are grounded with WebFetch and manual-stubs. v1.0 adds no new APIs.
4. Then (or in parallel) run [`literature-search`](../literature-search/SKILL.md).

### Step 4: Connection tests (T3 / T3b / T4 / T5)

- **T3**: translation, introduction primary, or named citation? Else T3b.
- **T3b**: T0 on both sides plus a similarity map?
- **T4 / T5**: does the historian already write continuity or a precedent? Survive hostile reduction (speed = quantity/time, necessity = degree, two points ≠ continuity)? If not, record the fallback and make it a start condition for the chapter.

If [`literature-gap-analysis`](../literature-gap-analysis/SKILL.md) novelty is "genealogical connection" and T3 has not passed, change it to juxtaposition/comparison.

### Step 5: Pre-draft checklist

- [ ] Load-bearing claims have types
- [ ] T0 stays inside stub excerpts
- [ ] T3/T4/T5 passed or fell back
- [ ] **N1**: no historical actor = coined concept
- [ ] If the same analysis term (inside, memory, ability) shifts referent across sections, say it is an analytic construct
- [ ] Selection criteria and the strongest counter-lineage are recorded from before the search
- [ ] Teleology style: do fillers such as "thereafter", "thus it developed", "was inherited" hide selection? Does the chapter opening state selectivity?

Then continue to [`counter-argument-tdd`](../counter-argument-tdd/SKILL.md).

## Invariants

- Start the inventory before literature search (no post-hoc criteria)
- `literature-matrix.md` is an index; citation grounds are `literature/papers/`
- Similarity does not satisfy T3
- Do not print T0, N1, or other internal codes in `docs/chapters/`

## Out of scope (v1.0)

No survey-history tutorial, no field-specific historiography textbook, no CiNii/J-STAGE search script, no illegal access. Future lint candidates (teleology connectives, "has been received" with no citation, coined concept co-occurring with a historical actor) stay manual.

## Outputs

- `docs/<paper-id>/design/sot/diachronic-claim-inventory.md` (source of truth; `docs/design/sot/` in a single-paper repo)
