---
name: pre-reading-briefing
version: 1.1.0
description: Use when entering the review/revision phase of a draft. Generates a pre-reading briefing for each section—prerequisites, main claims, and anticipated objections—before the author or reviewers read through, reducing comprehension cost. Addresses the asymmetry between production (writing) and comprehension (reading) as reading-phase cognitive scaffolding.
---

# Pre-Reading Briefing Skill

## Purpose
"Writing" a draft and "reading & verifying" it impose different cognitive loads. Even when drafting is accelerated, the author or reviewers need separate effort to read the finished manuscript and understand its terminology, assumptions, and line of argument. This skill generates a per-section **"how to read this" guide** before entering the review phase (PH-REV), providing reading-side scaffolding.

In cognitive-scaffolding terms, this skill primarily extends **M1 (Mirroring) to the comprehension side** together with **M4 (ZPD prompting)**: it reflects the reader's current position and incrementally presents the prerequisites for the next section to be read.

## Trigger Conditions
- A chapter or section draft is complete, **before the author's own read-through/verification**
- As a **reader's guide** before sharing a draft with reviewers or collaborators
- After a long writing hiatus, when one's own draft reads like someone else's text
- Before post-hoc audits such as claim-evidence-gate, to **narrow the scope of human verification**

## Prerequisites
- The target draft files (chapter/section) exist
- Ideally, domain concept definitions (glossary) exist under `design/` (used for concept grounding)

## Workflow

### Step 1: Determine scope
1. Agree with the user on the briefing target (chapter, sections, paragraph groups).
2. Confirm the reader model (Step 2 below).

### Step 2: Select the reader model
Depth of explanation and handling of assumed knowledge depend on the reader role.

| Reader model | Assumption | Briefing policy |
| :--- | :--- | :--- |
| **Author (re-reading)** | Time has passed since writing; details forgotten | Re-present "why this structure" and "original intent" |
| **First-time reviewer** | Domain expert, but unfamiliar with this paper's setup | State definitions and argument structure upfront |
| **Novice / practitioner** | Limited background knowledge | Explain prerequisites plainly; mark expert sections as "skippable" |

If the reader model is unclear, always ask the user one question before generating (do not guess).

### Step 3: Generate per-section briefing
For each section, present the following **before** reading:

| Element | Content |
| :--- | :--- |
| **Purpose of this section** | One sentence; show the mapping to the research question (RQ) |
| **Prerequisite concepts & definitions** | Up to 3 technical terms used in the text; reference domain concept definitions if available |
| **Main claim** | The single most important point of the section, in 1–2 sentences |
| **Anticipated objection / caveat** | One point a reader is likely to question; indicate whether a counter-argument exists |
| **Comprehension check question** | Typed (see below). Do not repeat what the Purpose/Claim lines already say. |

Target **5–10 lines per section**. Do not produce a detailed summary (this is a reading scaffold, not a copy of the text).

### Question types and who answers (v1.1.0)

The agent tags questions at generation time. **If ambiguous, default to TERM.** The author may retag at any time; do not treat retagging as an extra decision. Typed questions apply only when the reader model is **Author (re-reading)**.

| Tag | Asks | Who fills it |
| :--- | :--- | :--- |
| **TERM** | Meaning of a term or concept | Author; one question at a time (Capture→Mirror→Confirm) |
| **VALID** | Manuscript vs an external source of truth (version, protocol) | Agent drafts; author adopt/rejects |
| **MAP** | Alignment between internal artifacts (table↔section, definition↔observation) | Same |
| **GAP** | Optional MAP subtype: gap vs chapter/observation | Same |

Intent questions ("why cite this source?") are not a fourth type. If the answer is in a design doc, tag MAP; otherwise TERM.

**VALID / MAP draft rules (P0)**

- Drafts may be generated in one pass. **Confirm 2–3 rows per turn. Do not offer accept-all.**
- Every cell must cite the join evidence (table row, section number, short excerpt). Do not emit a draft without evidence.
- MAP values: **match / mismatch / unmatched** (missing from table or section).

**TERM cap**: 3 questions per session. Prefer concepts the author marked unknown. Park the rest via `session-research-handoff`. Not answering every question is not a failure. Unknown TERM → explain; unknown MAP → draft.

### Step 4: Placement & delivery
- Confirm with the user whether to insert the briefing as a **"Pre-Reading Briefing"** block at the head of the chapter, or to output it as a separate file (e.g., `docs/<paper-id>/design/reading-brief-chapterN.md`).
- If inserted into the manuscript, mark it clearly as a **temporary review artifact**; recommended practice is to remove it from the final/submission version.

### Step 5: Post-reading feedback
Do not ask the user to answer every question. Route by type.

- **TERM**: at most 3 unknowns the author named; explain then Confirm.
- **VALID / MAP**: emit evidenced drafts; adopt/reject 2–3 rows per turn.
- Record outcomes (answered / explained / draft-adopted / rejected) in the briefing answer column.
- Feed adopt/reject and remaining unknowns into the next revision. Exhaustive audit belongs to `claim-evidence-gate` (this skill's VALID is an author-facing prompt, not a gate).

## Separating production/comprehension metrics (recommended)
When operating this skill, record **writing time (production side)** and **briefing generation + read-through + check-question time (comprehension side)** as **separate metrics**. This makes the "writable but not readable" asymmetry quantitatively observable.

## Outputs
- `docs/<paper-id>/design/reading-brief-chapterN.md` (when managed as a separate file)
- Or a temporary block inserted at the chapter head (removed from the final manuscript)

## Output template

```markdown
## Pre-Reading Briefing: Chapter N — Title
**Target reader**: Author (re-reading)
**Estimated read time**: ~X minutes

### §N.1 Section title
- **Purpose**: For RQ1, establishes that ...
- **Prerequisites**: Term A (= definition ...), Term B
- **Main claim**: ...
- **Anticipated objection**: "But what about ...?" → addressed in §N.2
- **Check question** `[TERM]`: Can you state this section's conclusion in one sentence?
```

## Relations to other skills
- **session-research-handoff**: Combines well with warm-up questions when resuming a session
- **claim-evidence-gate**: VALID here is an author-facing reading aid. The gate is the exhaustive machine audit. Do not make the author fill the same table twice.
- **scholarly-concept-modeling**: Source of prerequisite concept definitions
- **academic-paper-translation**: Applicable as comprehension support for foreign-language literature

## Cognitive scaffolding
All interactions under this skill follow the [Cognitive Scaffolding Principles](../../../rules/en/cognitive-scaffolding-rule.md) (S1–S4). In particular, S1 (mirroring) is extended to the comprehension side: always reflect where the reader is now and what prerequisites they need next.

## Disclaimer
The generated briefing is a secondary artifact for comprehension support; it does not guarantee the correctness of the paper. Final verification of content must always be performed by the author against the manuscript itself.
