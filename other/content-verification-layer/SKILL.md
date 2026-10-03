---
name: content-verification-layer
description: Phase 4 Turn 2 of disease-market-sizing-orchestration (A6' upgrade). Audits compose output via Cite-or-Block strict — every anchor must reverse-resolve to an actual file in sources/, every fact claim must have an anchor. Returns verdict (ok/blocked) + violations list. Use AFTER cite-bound-content-generator (Turn 1), BEFORE report-bundle-builder (phase 5).
license: Cite-or-Block strict (P0 iron law, see ../../CLAUDE.md)
---

# Content Verification Layer (Phase 4 Turn 2)

## Strict Audits

1. `enforce_citations_in_text(html)` — flag fact-bearing claims without anchors
2. anchor existence reverse-lookup — every anchor source_id must have a backing file in sources/
3. numeric support gate — every market/statistical number in a claim must appear in the cited source/model evidence after normalization; derived numbers must be saved in and cited from a model/evidence file
4. report substance gate — block source inventory/process filler, deferred worker/model language, and toy Mermaid diagrams even when anchors resolve
5. drug-bearing sections route to A5' citation verifier; unsupported drug mentions are critical
6. strict locator gate — production anchors must include locator context; a numeric claim anchored only as `[guideline:ID]` or `[evidence:path]` is not strict evidence.
7. claim-level audit output — `verify_full_report()` must return enough detail for downstream gates to audit total claims, total anchors, strict locator coverage, verified count, anchors without locator, and violation reasons. A tiny `{"verdict":"ok"}` file is not an acceptable production audit.
   When semantic Tier 2 is enabled, `verification_report.json` must also record `semantic_audit.audit_log_path`, `audit_log_entries`, `calls_remaining`, and `call_budget`; the referenced JSONL log must exist and line counts must match.
8. Mermaid numeric-source audit — when rendered Mermaid sources are present, numeric labels must be checked against their nearest/declared anchors with the same numeric support rule used for visible body claims.
9. source-channel utilization audit — when production recall fetched required channels such as ClinicalTrials.gov or PubTator/entity evidence, `verify_full_report(..., required_source_channels=...)` must block if the channel has saved source files but no matching body anchors.
10. formula/model dominance audit — saved formula/model evidence can support derived numbers, but it cannot dominate body citations. If formula anchors are the main citation class, the output is a model dump, not a V25-level report.

## Report Substance Gate

Verification must reject HTML that is only report-shaped. These are critical blockers:

- visible body dominated by "已保存于 sources" rows, source-index tables, or repeated `附录证据说明`
- final report language that says work remains for a worker or later quant model
- shallow Mermaid blocks such as `A-->B` diagrams without real pathway logic
- Mermaid blocks must be audited even when the `<div class="mermaid">` tag carries extra attributes such as `data-chart`; raw HTML attributes cannot bypass shallow-diagram checks
- repeated `证据消化矩阵` blocks in the report body instead of narrative synthesis
- formula/model evidence anchors accounting for a dominant share of body citations
- numbered template padding such as `场景1/场景2/...` or `Block 1/Block 2/...` with the same sentence body; normalize the numbering before repetition checks

Passing Cite-or-Block syntax is necessary but not sufficient for a production smoke pass.

## Source Channel Utilization Gate

Production runs may pass `required_source_channels=("clinical_trials", "pubtator")` or equivalent. If files exist under the corresponding current-run source folders, the final report must use matching anchors in body analysis:

- ClinicalTrials.gov / AACT → `[nct:...]` or `[aact:...]`
- PubTator/entity recall → `[pubtator:...]`

Appending a source list is not enough. If a channel was fetched but excluded from analysis, the exclusion must happen before verification with a recorded reason, not by silently ignoring the saved sources.

## Numeric Evidence Gate

Do not accept "数字 + existing anchor" as proof. For every numeric fact such as percentage, patient count, currency, incidence, time window, or market size, verify:

- the cited source text contains the same number after comma/whitespace normalization, or
- the claim cites a saved model/evidence file that contains the formula, input anchors, units, and derived result.
- the anchor includes locator context that points at the relevant abstract, section, line, or evidence-file line.

If the number is absent from the cited source/model evidence, return a critical violation with `numeric token miss`.

For long captured sources, the semantic fallback excerpt must be built around the matched locator, numeric tokens, or nearby claim terms. Do not pass only the first page/header of a guideline or HTML capture to semantic verification; website navigation text is not the evidence window.

## Audit Output Contract

`verification_report.json` must keep the audit trail needed by the production smoke gate:

- `verified_count`
- `anchor_audit.total_claims`
- `anchor_audit.total_anchors`
- `anchor_audit.verified_count`
- `anchor_audit.anchors_without_locator`
- `anchor_audit.violations_by_reason`
- `semantic_audit.audit_log_path` / `audit_log_entries` / `calls_remaining` / `call_budget` when semantic verification writes a JSONL log

Schema lint must fail if these fields are written but not declared in `schemas/verification_report.schema.json`.

## Functions

- `verify_section(section_html, sources_dir) -> Verdict`
- `verify_full_report(html, sources_dir) -> Verdict`
- `enforce_citations_in_text(html) -> list[Violation]`

## P0 守门

Tests grep skill source for hardcoded drug names / disease names — CI blocks on hit.
