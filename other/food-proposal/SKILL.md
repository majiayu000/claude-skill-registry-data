---
name: food-proposal
description: "Master orchestrator for preparing research proposals and funding-application proposals in food, nutrition & agricultural science. Like food-pipeline, but for proposals: it resolves the target funding scheme's format first (headings, order, page/word limit, font, assessment criteria), then drafts from scratch (food-deep-research for the knowledge base, food-paper to write, food-review to review) or revises an existing draft after first understanding the field. Enforces the scheme's length limit and required headings and aligns content to the assessment criteria. Built-in schemes: ARC Discovery EOI, ARC Discovery Full Application, and the UoM Ag & Food project proposal; if a scheme isn't included it asks the user to upload the guideline and extracts the format. Triggers: write a grant proposal, ARC Discovery application, funding application, research proposal, project proposal, revise my grant, prepare an EOI."
metadata:
  version: "1.0.0"
  verified: "2026-08"
  subagents: [proposal_router, scheme_extractor, compliance_gate]
  related_skills: [food-deep-research, food-research, food-paper, food-review, food-figure, food-pipeline, agri-deep-research, agri-paper, agri-review]
  references:
    - references/proposal-workflow.md
    - references/scheme-selection.md
    - references/format-and-limits.md
    - references/assessment-alignment.md
---

# Food-Proposal — Research & Funding Proposal Orchestrator

The proposal counterpart of `food-pipeline`. It does not research, write, or review
itself — it **routes the proposal to the specialist skills** and enforces the target
funding scheme's **format, length limit, and assessment criteria** at every gate.
Original work; the orchestration mirrors `food-pipeline`.

## Scheme first — the key difference from a paper
A proposal is written to a **funding scheme's format**, the way a manuscript is written
to a journal's. **Before anything else, resolve the target scheme**
(`references/scheme-selection.md`): ask the user which scheme, then load its spec from
`schemes/<id>.md` + `schemes/schemes.json` (required headings in order, page/word limit,
font, assessment criteria). **Built-in:** `arc-discovery-eoi`, `arc-discovery-full`,
`uom-major-minor-project` (see `schemes/INDEX.md`). **If the scheme isn't built in,
don't guess** — ask the user to upload the scheme's guideline / sample form and run
`scheme_extractor` to capture its format into a new `schemes/<id>.md` + `schemes.json`
entry. Every scheme carries a **length limit** — enforce it with
`scripts/proposal_wordcount.py`.

## Own subagents
- **`proposal_router`** — reads what the user has (topic only, or an existing draft),
  resolves the scheme, picks the entry stage, and assembles each downstream skill's
  input. Mirrors `food-pipeline`'s intake router.
- **`scheme_extractor`** — when the scheme isn't built in, extracts its format
  (headings, order, limits, font, criteria) from the user's uploaded guideline/sample
  into a new scheme spec.
- **`compliance_gate`** — the checkpoint between stages: verifies required headings are
  present and in order, the **length limit** is met (`proposal_wordcount.py`), the font/
  format matches, and the content **addresses every assessment criterion**.

## Stages
| Stage | Skill / agent | Deliverable | Gate |
|---|---|---|---|
| 0 · SCHEME | `proposal_router` + scheme resolution | Target scheme spec (headings, limit, criteria) | — |
| 1 · RESEARCH | `food-deep-research` (or `agri-deep-research`; `food-research`) | Knowledge base / evidence for the case | evidence sufficiency |
| 2 · DRAFT | `food-paper` (or `agri-paper`) writing to the scheme's headings | Proposal draft in the scheme format | `compliance_gate`: headings + **length** + criteria |
| 3 · REVIEW | `food-review` (or `agri-review`) as a mock funding panel vs the criteria | Review report + editorial decision | **mandatory** author decision |
| 4 · REVISE | `food-paper` (revise) | Revised proposal (tracked changes; original Word opt-in) | issues resolved + still within limit |
| 5 · FINALIZE | `food-paper` (format-convert) | Submission-ready proposal (`.docx`/PDF) to scheme format | final compliance |

**Slides?** For a proposal pitch, `food-ppt` can turn the finished proposal into a deck.

## From scratch vs revising an existing draft
- **From scratch:** run Stage 1 → 2 → 3, exactly as `food-pipeline` builds a paper, but
  to the scheme's headings and limit.
- **Revising a draft (has one already):** understand the field first (a `food-research`
  quick brief / reuse of any provided library, as `food-pipeline` does before editing),
  then edit to fix gaps and **fit the scheme** — never rewrite blindly.

## Inherited (not optional)
Anti-fabrication grounding + four-gate citations, privacy scan, academic style +
`human-writing.md`, the **mandatory AI-use disclosure** (some schemes, e.g. the UoM
project, require stating the AI model and prompts used — put it in Acknowledgements),
and the full-text-access first move for the research stage. Figures via `food-figure`.
