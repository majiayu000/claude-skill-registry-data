---
name: paper-writing-onboarding
version: 1.3.0
description: Use when writing an academic paper for the first time or starting a new research project, to get guided through repository structure, initial setup, the phase-based writing workflow, and core scholarly conventions such as citation practice and research ethics
---

# Paper Writing Onboarding Skill

## Purpose
Guide users who are writing their first academic paper (or using this skill set for the first time) through the software-engineering-driven writing workflow, from environment setup to first-draft completion. Prevents the most common beginner failures upfront: unsourced numerical claims, ambiguous concept usage, and oversized scope.

## Trigger Conditions
- When starting a new paper or research project
- When the user is identified as a first-time or inexperienced academic writer
- When the user asks "where do I start?"

## Pre-Writing Setup Checklist

Before drafting, verify the following environment prerequisites:

1. **Skills installed**: This repository is available as a submodule (`.scholarly-agent-skills/`) or via symbolic link (see root `AGENTS.md` for setup).
2. **Language configured**: [`config/user_preferences.json`](../../../config/user_preferences.json) is set to the user's writing language.
3. **AI Ignore configured**: If handling raw or confidential data, `scripts/setup_ai_ignore.py` has been run to exclude them from AI indexing.
4. **Directory structure**: Create the five-category artifact structure (when managing multiple papers, place under `docs/<paper-id>/`):

```text
docs/
├── manuscript/  # Final paper outputs & rendered formats (.md, .html, .pdf)
├── chapters/    # Manuscript body (one Markdown file per chapter)
├── design/      # Internal design docs (concept inventory, objection lists, audit reports)
├── literature/  # Literature artifacts (matrix, gap report, paper notes)
└── data/        # Primary data (statistics, survey datasets)
```

5. **Commit cadence decided (v1.3.0)**: At project start, agree with the author on a minimum commit frequency/timing for artifacts, and record it in the research plan or an operations design doc. Recommended minimum: "per chapter, when the human check completes." Uncommitted artifacts can be lost to editor accidents or sync failures, so deciding cadence upfront is a risk control. The agent still never commits on its own at the agreed times — commits run only on the author's explicit instruction (the no-auto-commit rule is unchanged)

## Phase-Based Writing Workflow

Each phase hands off to a dedicated skill. Following this order avoids the single most common beginner mistake: jumping straight into writing the manuscript.

### Phase 0: Articulate the Research Plan
→ Invoke [`research-plan-workshop`](../research-plan-workshop/SKILL.md) and, through dialogue, write `docs/design/research-plan.md` (one page maximum):
- The research question in a single sentence
- Target audience and venue (conference, journal, preprint server)
- Definition of done (chapter outline, target length, deadline)

### Phase 1: Establish Conceptual Foundations
→ Invoke [`scholarly-concept-modeling`](../scholarly-concept-modeling/SKILL.md) to define and bound core concepts. Starting to write with polysemous terms guarantees a full rewrite later.

### Phase 2: Literature Research
→ For diachronic papers, type claims first with [`diachronic-claim-typing`](../diachronic-claim-typing/SKILL.md).
→ Use [`literature-search`](../literature-search/SKILL.md) to collect sources, [`pdf-paper-ingestion`](../pdf-paper-ingestion/SKILL.md) to convert papers to Markdown, and [`academic-paper-translation`](../academic-paper-translation/SKILL.md) for foreign-language sources.
→ Filter citation candidates through [`source-criticism-gate`](../source-criticism-gate/SKILL.md) (Tier 1/2 only).

### Phase 3: Establish Novelty
→ Use [`literature-gap-analysis`](../literature-gap-analysis/SKILL.md) to structure the gap between prior work (AS-IS) and your contribution (TO-BE), forming the core of the Introduction.

### Phase 4: Draft the Manuscript (Objection-Driven)
→ Follow [`counter-argument-tdd`](../counter-argument-tdd/SKILL.md): enumerate anticipated objections in `docs/design/test-cases.md` before writing each section.
→ When using primary data, run [`primary-data-integration`](../primary-data-integration/SKILL.md) first (PII masking and inventory).
→ **SoT sync check at chapter start (v1.2.0)**: before drafting each chapter, reconcile the relevant section of `paper-outline.md` against the latest state of its input SoTs (`domain-concepts.md`, `literature-gap-report.md`, etc.). Health condition: the outline's last revision date ≥ the last update of its dependent SoTs. If unmet, update the outline first (SoT-first — never fudge a chapter to fit a stale outline). Chapters must reference `domain-concepts.md` rather than redefining concepts. This prevents stale SoTs from cascading into chapter drift.

### Phase 5: Verification & Revision
→ Audit every claim with [`claim-evidence-gate`](../claim-evidence-gate/SKILL.md), then verify 1-to-1 citation correspondence with [`citation-traceability-audit`](../citation-traceability-audit/SKILL.md).

### Phase 6: Submission & Publication
→ Use [`submission-venue-advisor`](../submission-venue-advisor/SKILL.md) to select the venue for your field and language, draft field-level deposit metadata, then follow its submission procedure.

## Common Beginner Failures and Countermeasures

| Failure | Symptom | Countermeasure |
|---|---|---|
| Unsourced figures | Writing "X is 2.3 times Y" without a source | Follow the fact-grounding rule in `rules/`: fetch primary data first, store in `docs/data/`, then reference from the manuscript |
| Oversized scope | Stuffing multiple major claims into one paper | Limit the research question to one sentence in Phase 0; revisit the plan if you drift |
| Ambiguous concepts | Using the same term with different meanings across contexts | Build the concept inventory in Phase 1 before drafting |
| Perfectionist paralysis | Polishing the Introduction forever | Write each chapter as a rough draft that clears the objection list, then verify in Phase 5 |
| Task initiation paralysis | Freezing because you don't know where to start | The agent auto-decomposes Phase 0 into micro-steps and presents them ([Cognitive Scaffolding Rule S1](../../../rules/en/cognitive-scaffolding-rule.md)) |

## Core Scholarly Conventions (For Beginners)

This skill set mechanizes the workflow (how to write), but the conventions of the academic community (what is permitted and what is expected) are often assumed as tacit knowledge. First-time writers should survey the following areas before drafting. Note that these conventions **vary by field and venue** — the table below is a general map, and final decisions must always be grounded in a primary check of the venue's current regulations (submission guidelines, author instructions).

| Area | What beginners should know |
|---|---|
| Citation practice | Distinguish direct quotation (verbatim, page number required) from paraphrase citation. When citing a work you could not read directly via a secondary source, the "as cited in" convention applies. This repository's `manual-stub` (page-anchored verified excerpt notes) is an internal management term and must never appear in the manuscript |
| Source reliability hierarchy | The relative weight of peer-reviewed articles, scholarly books, preprints, grey literature (institutional reports), and web articles. Restrict citations to Tier 1/2 via [`source-criticism-gate`](../source-criticism-gate/SKILL.md) |
| Research ethics | Prohibition of duplicate submission and salami slicing. Definitions of fabrication, falsification, and plagiarism (FFP). Authorship criteria (e.g., ICMJE). AI-tool disclosure policies differ per venue — always check current regulations |
| Peer review culture | Rebuttals to reviewer comments should be evidence-based and courteous. Rejection is a normal part of research; use the comments to strengthen the next submission |
| Data & reproducibility | Retention and disclosure obligations for primary data; privacy (PII) handling follows [`primary-data-integration`](../primary-data-integration/SKILL.md) |

## Working Across Sessions

For long-running projects, invoke [`session-research-handoff`](../session-research-handoff/SKILL.md) at the end of every session from day one, recording context in `docs/session-handoff.md`.

## Cognitive Scaffolding
All interactions in this skill must follow the [Cognitive Scaffolding Rule](../../../rules/en/cognitive-scaffolding-rule.md) (S1–S4). Phase 0 has the highest task initiation barrier, so S1 (Task Initiation Scaffolding) takes priority.

## Outputs
- `docs/design/research-plan.md` (Research plan: question, target venue, definition of done)
- Initialized five-category directory structure
