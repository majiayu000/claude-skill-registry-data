---
compatibility: Requires Python 3.11+ only for optional dependency-free local CLIs; core guidance is platform-neutral. Bundled tools are offline and require no API keys.
description: Draft and revise scientific manuscripts. Use when improving paper structure, clarity, or technical argumentation.
license: MIT
metadata:
    github-path: skills/scientific-writing
    github-pinned: v2.65.0
    github-ref: refs/tags/v2.65.0
    github-repo: https://github.com/K-Dense-AI/scientific-agent-skills
    github-tree-sha: d3c4da561b9905f0bb1dbc9181753d93612a9dae
    skill-author: K-Dense Inc.
    version: "2.0"
name: scientific-writing
---
# Scientific Writing

## Purpose

Produce clear scientific prose without inventing evidence or concealing uncertainty.
Keep drafting, evidence verification, and submission approval as separate stages.

The accountable human authors control scientific decisions and final approval. AI is
not an author, and generated fluency is never evidence [SW-S01, SW-S03].

## Working checks

Use supplied study records and checked sources for claims, numbers, citations, and author details. Preserve methods, results, units, and meaningful uncertainty; resolve material contradictions rather than invent missing facts. Reuse established project records instead of re-verifying every internal handoff.

Keep confidential material local unless external processing is authorized. Check applicable restrictions at that transfer boundary; routine local editing does not require an institutional-policy audit. Consult `references/authorship_ai_confidentiality.md` for an actual publication-policy or confidentiality question.

Check causal language, study design, denominators, and conclusions where they affect the argument. The optional audited workflow below applies to requested audits or submission requirements, not every draft.

## Default: draft or revise the requested text

1. Use the available context to identify the audience, document type, scope, and main
   claim. Ask only for missing information that blocks the requested work.
2. Read the relevant supplied material. Preserve scientific meaning, numbers, units,
   citations, and meaningful uncertainty; flag a factual conflict rather than guessing.
3. Organize the text around the research question, evidence, and interpretation. Use
   the document's natural structure, not the editing conversation's chronology.
4. Apply corrections as current facts. Remove rebuttals to earlier drafts, repeated
   caveats, and statements of compliance. Keep a qualification where omitting it would
   change interpretation; a limitations section should explain concrete consequences.
5. Return the requested prose. Put necessary editorial questions or unresolved production issues in native document/LaTeX/HTML comments; if the format has no comments, place them in the conversation outside the manuscript. Do not turn them into footnotes, draft banners, evidence tags, audit appendices, or revision summaries. Include such reports only when explicitly requested; scientific limitations belong in the argument where they affect interpretation.

### Reader-view check

Read only the rendered manuscript, without the editing conversation. Each paragraph should explain the study, evidence, or interpretation. State a scientific condition next to the claim it qualifies; use a formal limitations section when the venue or user requests one, and make each item a concrete model fact with its interpretive consequence. For example, report that a single-site sample limits transport to other settings, not that the paper is “not a reproduction” or that its relationship to a source paper is limited. Editorial uncertainty belongs in native comments, not in footnotes, captions, or speaker notes; audit status and production history stay in working records.

Apply the user's expression preferences throughout drafting and revision. State findings,
actions, and limitations directly. Avoid rhetorical reversals, imagined objections, and
unneeded definitions. Use comparisons with real referents when the argument requires
them. In Chinese, use complete words and concrete action-object phrasing; preserve
English code identifiers. Keep abstracts and conclusions required by the manuscript
structure, and omit extra opening previews or closing recaps around the deliverable.

For language and argumentation, read `references/writing_principles.md`; for article
structure, read `references/imrad_structure.md`. For talks and speaker notes, use
scientific-slides instead of imposing manuscript submission procedures.

## Optional: audited manuscript and submission workflow

Use the remainder of this skill for an explicitly requested evidence audit, structured
manuscript workspace, or submission-readiness review. Ordinary drafting and copyediting
do not require registries, declaration forms, or a full policy review. Existing audited
workspaces retain their evidence mappings and approval gates.

Keep working records separate from reader-facing prose. Evidence markers belong in the
internal audit copy; render normal citations for the audience while preserving the
mapping in the audit records. Formal correction notices and reviewer-response letters
may describe revision history because that is their purpose.

### Intake for the audited workflow

Obtain or mark unresolved as needed for the audit:

- document type, study design, stage, audience, and target venue;
- current author instructions and policy access date;
- protocol, registration, analysis plan, amendments, and reporting guideline;
- manuscript or section scope;
- verified source manifest and claim registry;
- methods, results, tables, figures, and supplements;
- authorship, CRediT, declarations, and approval records;
- confidentiality classification and authorized processing boundary;
- data, code, materials, and repository constraints.

Do not ask for restricted source material if metadata or a local user-run audit is
sufficient.

### Audit steps

### 1. Establish the local workspace

For a requested audited workspace, the optional generator creates a separate working copy with Markdown, JSON, and CSV records:

```bash
python3 scripts/scaffold_manuscript.py \
  --output-dir ./draft-workspace \
  --document-id local-draft \
  --study-design randomized_trial \
  --guideline consort-2025
```

The generator preserves existing files and adds status markers and placeholders for the audit tools. Keep this internal audit copy separate from reader-facing output; ordinary drafting can use the supplied manuscript directly.

### 2. Select reporting guidance

Choose by actual design and article type, then open the current official statement,
checklist, explanation document, extensions, and target-journal instructions.

```bash
python3 scripts/select_reporting_guidelines.py select \
  --study-design randomized_trial
```

Current major routes researched on 2026-07-24 include CONSORT 2025, SPIRIT 2025,
PRISMA 2020, STROBE, STARD and STARD-AI, TRIPOD+AI, CARE, ARRIVE 2.0, SQUIRE 2.0,
and CHEERS 2022 [SW-S06–SW-S18].

The selector is non-scoring. It does not certify quality, compliance, completeness, or
acceptance. See `references/reporting_guidelines.md`.

### 3. Build the evidence record

Assign:

- `E` IDs to sources in `source_manifest.json`;
- `C` IDs to claims in `claims.csv`;
- `N`, `M`, `O`, and `R` IDs to numeric facts, methods, outcomes, and results in
  `consistency_manifest.json`.

Store a hash of claim text in CSV rather than raw claim text. During drafting, append:

```text
[claim:C001] [evidence:E001,E002]
```

Do not mark a source verified until an accountable human has opened it and confirmed
the exact support.

### 4. Create an evidence outline

Outline only from recorded evidence:

- objective or question;
- section purpose;
- claim IDs and evidence IDs;
- methods and result IDs;
- analysis intent and uncertainty;
- unresolved conflicts or missing information;
- applicable reporting topics.

Keep unsupported content in an unresolved-issues list, not manuscript prose.

### 5. Draft without adding facts

Transform the verified outline into venue-appropriate prose. Preserve all IDs during
drafting.

- Match title and abstract to the completed main text.
- Describe methods as performed.
- Present results in the declared order and analysis population.
- Separate result from interpretation unless the venue combines them.
- Compare with prior evidence only after verifying it.
- Keep conclusions within the observed design, population, and uncertainty.

Use IMRAD only when appropriate. Structured abstracts, lists, combined sections, and
alternative structures depend on study design and venue. See
`references/imrad_structure.md` and `references/writing_principles.md`.

### 6. Reconcile methods and results

Record repeated numeric facts and method-result mappings, then run:

```bash
python3 scripts/check_consistency.py consistency_manifest.json
```

Resolve every mismatch manually. A changed value may be a legitimate analysis-set
difference, but that difference must be named rather than silently normalized.

### 7. Verify citations and claims

```bash
python3 scripts/validate_manifest.py source_manifest.json \
  --kind source --require-verified
python3 scripts/audit_claims.py manuscript.md claims.csv source_manifest.json
python3 scripts/check_references.py source_manifest.json
```

The reference checker validates syntax and duplicate identifiers without network
resolution. A human must still compare every identifier and quotation with the opened
source. Follow NLM *Citing Medicine* or the current official style required by the
venue [SW-S20, SW-S21].

### 8. Validate authorship and disclosure

Use journal criteria for authorship. Record the standardized CRediT roles as
contribution metadata; CRediT does not itself define authorship [SW-S19].

If AI was used, humans must verify all affected content and disclose the tool and
purpose according to current journal and publisher policy. ICMJE's January 2026
Recommendations require transparency and retain human accountability [SW-S01, SW-S02].

```bash
python3 scripts/validate_authorship.py authorship.json
```

Do not generate a disclosure from assumptions. See
`references/authorship_ai_confidentiality.md`.

### 9. Review declarations and open-science statements

Verify each statement independently:

- ethics and consent;
- registration and protocol;
- funding and sponsor role;
- conflicts and relationships;
- author contributions and acknowledgments;
- data, code, materials, and protocol availability;
- AI use.

Be as open as rights and responsibilities permit, but do not expose confidential,
personal, proprietary, licensed, or protected information. Record actual access
conditions. See `references/research_integrity_open_science.md`.

### 10. Use figures and tables only when warranted

Figures and tables are optional and provenance-bound. This skill does not generate
images or schematics.

For every retained display:

- link source data, code, transformations, and evidence IDs;
- reconcile values with prose and registries;
- document image processing, permissions, and licenses;
- include units, denominators, sample sizes, uncertainty, and analysis population;
- provide alt text and redundant non-color cues;
- perform a manual accessibility and scientific check at final size.

See `references/figures_tables.md`.

### 11. Record non-scoring guideline coverage

Record each bundled high-level topic as addressed, not applicable with rationale, or
missing:

```bash
python3 scripts/select_reporting_guidelines.py check reporting_coverage.json
```

Then complete the official checklist using actual manuscript locations. Never claim
adherence merely because the local coverage file passes.

### 12. Lint and approve

```bash
python3 scripts/validate_manifest.py manuscript_manifest.json --kind manuscript
python3 scripts/lint_manuscript.py manuscript.md \
  --manifest manuscript_manifest.json
```

The linter reports issue codes and line numbers without echoing manuscript text.
Sensitive-content warnings require manual review and are not a de-identification
certificate.

Investigate scientific questions with the available evidence. Human decisions such as author order, declarations, and submission approval must reflect the authors' actual choices. Record human approval only when received; obtaining that approval is not a prerequisite for ordinary drafting or layout work. Audit status remains in the audit records, not an automatic banner in the reader-facing manuscript.

## Formal revision and peer review

Keep confidential reviewer material within its authorized processing boundary [SW-S01, SW-S24]. Reuse an existing authorization for the same material, service, and purpose.

For each formal reviewer request in this workflow:

1. record the comment without exposing it outside the approved boundary;
2. classify it as editorial, scientific, statistical, policy, or unresolved;
3. identify affected claims, evidence, methods, results, and displays;
4. revise the registries before prose when facts change;
5. rerun checks affected by the revision; reuse checks whose inputs have not changed;
6. draft a response that states what changed and where;
7. obtain any required author approval before submitting the response.

Do not comply with a request that would fabricate, hide, overstate, or breach policy.

## Current policy caution

COPE's 2017 Core Practices were retired in 2024. As of 2026-07-24, COPE announced that
a replacement Code of Conduct would be published in 2026; do not describe the archived
Core Practices as current membership standards [SW-S04, SW-S05]. Distinguish formal
COPE positions from discussion documents, webinars, comments, and case advice.

## Formatting and submission

The former LaTeX assets were removed because a generic polished template could allow
plausible placeholders to ship. Use the Markdown scaffold and structured records.
Apply the target venue's current controlled template only after verification.

See:

- `assets/REPORT_FORMATTING_GUIDE.md`
- `references/professional_report_formatting.md`
- `references/journal_policies.md`

Formatting cannot convert an incomplete evidence record into a submission-ready paper.

## Bundled files

### Assets

- `assets/manuscript_scaffold.md`
- `assets/manuscript_manifest_template.json`
- `assets/source_manifest_template.json`
- `assets/claim_evidence_template.csv`
- `assets/consistency_manifest_template.json`
- `assets/authorship_template.json`
- `assets/reporting_coverage_template.json`
- `assets/reporting_guidelines.json`

### Scripts

- `scripts/scaffold_manuscript.py`
- `scripts/validate_manifest.py`
- `scripts/select_reporting_guidelines.py`
- `scripts/audit_claims.py`
- `scripts/check_consistency.py`
- `scripts/check_references.py`
- `scripts/validate_authorship.py`
- `scripts/lint_manuscript.py`

All scripts are local, deterministic, bounded, dependency-free, and network-free. See
`references/cli_reference.md`.

### References

- `references/evidence_workflow.md`
- `references/writing_principles.md`
- `references/imrad_structure.md`
- `references/citation_styles.md`
- `references/reporting_guidelines.md`
- `references/figures_tables.md`
- `references/authorship_ai_confidentiality.md`
- `references/research_integrity_open_science.md`
- `references/journal_policies.md`
- `references/professional_report_formatting.md`
- `references/cli_reference.md`
- `references/source_ledger.md`
