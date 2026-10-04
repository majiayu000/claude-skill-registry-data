---
name: food-deep-research
description: "General-purpose deep research that produces a fully written, source-validated literature review on any question: scope it, design the method, discover and screen sources by journal ranking, validate every source, extract and verify evidence, synthesize, stress-test, then write and format the review (APA 7.0 by default, or a target journal's style) and polish it through an editorial + integrity review loop. Use standalone for a deep dive or literature review, or as the deep-dive engine called by food-research. Runs a 12-subagent team with iterate-to-saturation and compile↔review loops. Triggers: deep research, research this in depth, write a literature review, investigate thoroughly, comprehensive review, state of the evidence, briefing on, dig into, deep dive."
metadata:
  version: "2.1.0"
  verified: "2026-07"
  related_skills: [food-research, journal-selector, food-paper, food-pipeline]
  subagents: [research_scope, research_architect, investigator, source_screener, source_verifier, bibliography, claim_verifier, synthesizer, critic, compiler, editor, ethics_reviewer]
  references:
    - references/reasoning-and-fallacies.md
---

# Deep-Research — Source-Validated Literature Review Engine

Answer a hard question properly and hand back a **written, formatted, integrity-
checked literature review** — not just notes. Scope → design → discover → screen
by journal ranking → validate sources → extract & verify evidence → synthesize →
stress-test → write → review-loop → final report. Original work; architecture
informed by open community food-deep-research skills (see the repo README
Acknowledgements). Usable standalone, or as the deep-dive engine called by
`food-research`.

## Modes
- **quick brief** — scope → discover → screen (Tier 1) → light synthesis → short sourced answer. Skips the full validation/compile/review loop.
- **full** — the default: the complete 12-subagent pipeline below with the iterate-to-saturation and compile↔review loops, ending in a finished review.

## Subagent team (dispatch via the Agent tool)
| # | Subagent | Job |
|---|---|---|
| 1 | `research_scope` | Comprehensive scope brief: background, problem, significance, central + sub-questions, concepts, boundaries, success criteria. |
| 2 | `research_architect` | Methodology blueprint: review type, search strategy, inclusion criteria, analytical framework, reporting standard, stopping criteria. |
| 3 | `investigator` | Pass 1 discover candidate sources; Pass 2 extract evidence **from validated sources only** (parallel per sub-question). |
| 4 | `source_screener` | Prioritize candidates by **journal ranking** (Tier 1 Q1/Q2 + Nature/Science/Cell + other-discipline Q1/Q2; Tier 2 Q3; avoid Tier 4). |
| 5 | `source_verifier` | Validate each prioritized source (existence/DOI, venue legitimacy, retraction, predatory, methodology, COI) → Source Quality Matrix. |
| 6 | `bibliography` | Deduplicate + format references (APA 7.0 default, or target-journal style via `journal-selector`); build the citation map + `.bib/.ris`. |
| 7 | `claim_verifier` | Verify each load-bearing claim against its validated source; classify fact/hypothesis/contested/speculation. |
| 8 | `synthesizer` | Evidence matrix, thematic synthesis, conflict reconciliation, evidence grading, coverage advisory, gap agenda, narrative arc. |
| 9 | `critic` | Devil's advocate on the **synthesis**; loop back to investigate if gaps. |
| 10 | `compiler` | Write & format the **literature-review draft** (APA 7.0 / target journal); cite by key only; no fabrication. |
| 11 | `editor` | Editorial review of the draft (5 weighted dimensions, verdict + prioritized feedback). |
| 12 | `ethics_reviewer` | Integrity/ethics review of the draft (citation integrity, faithful representation, bias, COI, disclosure). |

## Workflow

```mermaid
flowchart TD
    A[research_scope<br/>scope brief] --> B[research_architect<br/>methodology blueprint]
    B --> C[investigator Pass 1<br/>discover candidate sources]
    C --> D[source_screener<br/>journal-ranking tiers]
    D --> E[source_verifier<br/>validate → Source Quality Matrix]
    E --> F[bibliography<br/>dedupe + format + citation map]
    E --> G[investigator Pass 2<br/>extract evidence from validated sources]
    G --> H[claim_verifier<br/>verify claims vs validated sources]
    H --> I[synthesizer<br/>matrix, themes, conflicts, grading, gaps]
    I --> J[critic<br/>stress-test synthesis]
    J -- gaps --> C
    J -- sound --> K[compiler<br/>write + format review<br/>APA 7.0 / target journal]
    F --> K
    K --> L[editor + ethics_reviewer<br/>editorial + integrity review]
    L -- minor/major revision --> K
    L -- accept --> M[Final literature review]
```

**Two loops:** (1) *evidence loop* — `critic` sends gaps back to `investigator`
(cap ~2–3); (2) *writing loop* — `editor`/`ethics_reviewer` send revisions back
to `compiler` until Accept (cap ~2–3), then deliver.

## First move — set up full-text access (once)
The evidence loop reads **actual articles**, not abstracts. At the start, run the
**`food-fetch` first-run setup** (`python3 scripts/food_fetch_setup.py status`): if the
user hasn't set up access, surface the one-time highlighted request to provide their
**EndNote `.Data` folder** (or Zotero/Mendeley / a PDF folder) or **institutional
access**, warning that **without non-open-access access the accuracy is substantially
limited**; save the choice so it isn't re-asked. If they chose "open-access only",
**remind** briefly of that accuracy limit each run. Don't block — proceed at
open-access + abstract level and flag paywalled sources. Full rules: `food-fetch/SKILL.md`
and `food-research/references/full-text-access.md`.

## Source discipline (non-negotiable)
- **Investigation and claim-checking operate only on validated sources** — those that passed `source_screener` (ranking) **and** `source_verifier` (validity). Retracted/unresolvable sources are excluded and logged.
- **Journal ranking** favors Tier 1 (Q1/Q2 food-science & nutrition, Nature/Science/Cell families, Q1/Q2 in any other discipline); Tier 2 (Q3) only to fill gaps; Tier 4 avoided.
- Every claim carries a source and locator; inference is labelled as inference.

## Formatting — resolve the target journal once
At the start, load **`journal-selector/SKILL.md`** (a shared procedure, not an
installed skill), which **asks which journal the review
targets** (they may answer 'generic' → **APA 7.0**). Ask **once**: record the
choice and reuse it in `bibliography` and `compiler` to format the review to that
journal's structure, limits, and reference style — don't ask again. Reuse a
journal already resolved by `food-research`/`food-pipeline`; re-resolve only if the
user asks to switch journals.

## Principles
Every claim sourced; fact separated from interpretation; disagreement shown, not
averaged; uncertainty surfaced. Upstream evidence beats parametric knowledge —
mark missing evidence `[EVIDENCE GAP]`, never fabricate.

## References (load as needed)
- `references/reasoning-and-fallacies.md` — `synthesizer`/`critic`: sound argument + fallacies.
- `food-research/references/literature-sources.md` — databases/APIs for `investigator`.
- `food-research/references/full-text-access.md` — reading the **actual full text** for `investigator`/`source_verifier` (open access → connected tool → user PDFs → library session, legitimate access only); mark anything unread rather than summarizing.
- `food-research/references/source-quality-hierarchy.md` — evidence grading for `source_verifier`/`synthesizer`.
- `food-research/references/reporting-guidelines.md` — EQUATOR/PRISMA/CONSORT/STROBE.
- `food-paper/references/apa7-quickref.md` — APA 7.0 for `bibliography`/`compiler` (default style).
- `food-paper/references/writing-style.md` + `food-paper/references/human-writing.md` — **`compiler`: academic style + remove AI tells, applied together** — academic register as a human scientist, machine tells stripped, calibrated hedging and journal form kept.
- `food-review/references/ethics-integrity-checklist.md` — for `ethics_reviewer`.
- `food-paper/references/faithfulness-and-citation.md` — **grounding + four-gate citation check** for `bibliography`, `source_verifier`, `claim_verifier`, `compiler`. Never invent sources/data; run `scripts/verify_citations.py`.
- `food-paper/references/privacy-and-confidentiality.md` — **privacy scan before delivering the report** (no local paths/secrets); `scripts/privacy_scan.py`.

## Handoff
Standalone → deliver the final review. Called by `food-research` → return the
validated synthesis (or the finished review) to fold into the evidence brief.
