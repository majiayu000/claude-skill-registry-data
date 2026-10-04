---
name: audit-orchestrator
description: Marketplace entrypoint for a complete brand AI-readiness audit. Use for a website audit, GEO or AI-visibility check, missing or incorrect AI citations, or poor engagement from AI referrals. Composes all seven stages and emits one evidence-backed JSON, Markdown, HTML, or PDF report with findings and actions.
license: MIT
---

# Audit Orchestrator (entrypoint)

Runs the pipeline, composes the findings, emits one report.

## When to use

This is the entrypoint. Invoke it for any request of the form "audit this site
for AI visibility", "why isn't this brand cited by ChatGPT", "why do visitors
bounce", or "give me a brand AI-readiness report".

## Inputs

| Input | Required | Default | Notes |
|---|---|---|---|
| `url` | yes | — | Bare domain or full URL. |
| `--max-pages` | no | 20 | Page budget for the whole run. |
| `--max-seconds` | no | 150 | Detection budget: the crawl and analysis stages. |
| `--max-total-seconds` | no | 240 | Hard ceiling for the entire run -- detection, advisory, render and the review loop. Every subprocess timeout is derived from what is left of it, so total runtime stays under the 5-minute limit. Raised automatically if `--max-seconds` is set higher. |
| `--strictness` | no | `balanced` | `lenient`, `balanced`, `strict`. Shifts derived thresholds only. |
| `--formats` | no | `json,md` | Any of `json`, `md`, `html`, `pdf`. |
| `--out` | no | `./audit-report` | Output path stem. |
| `--skip` | no | — | Comma-separated layers to skip. |

## Procedure

The pipeline is ordered because the gates are ordered: a page that cannot be
retrieved cannot be assessed for structure, and a page with no content cannot
be assessed for evidence density. Running the stages out of order would
produce findings that are artefacts of the missing upstream stage.

1. **`url-validation`** — preflight gate. Hard stop on failure; nothing else runs.
2. **`crawl-reachability`** — discovery, fetching, sitemap audit, render faults.
   Writes the page inventory every later stage reads.
3. **`structured-data-identity`** — selection-layer eligibility.
4. **`evidence-density`** — absorption-layer readiness.
5. **`freshness-corroboration`** — trust signals.
6. **`engagement-audit`** — the on-site half.
7. **`advisory-review`** — the deterministic critic gate. Drops, downgrades,
   merges, aligns action priority to downgraded severity, and adds the
   proactive layer.
8. **Compose** — merge, prioritise, validate against the schema, render, then
   verify every requested artefact (present, non-trivial size, HTML contains
   `</html>` and the site name plus every advisory title verbatim, PDF starts
   with `%PDF-` and ends with `%%EOF`). A missing or broken artefact fails the
   run — a promised format is never silently absent.
9. **Review loop** — after compose, the independent reviewer
   (`scripts/review_report.py`) re-checks the draft JSON against the report
   schema and the stage artefacts (`07-advisory-review.json` plus the
   detection-layer files) and returns `VERDICT: ACCEPT` or
   `VERDICT: REGENERATE` with numbered issues and concrete repairs. On
   `REGENERATE` the orchestrator applies the repairs (`--apply`: removal,
   demotion, priority capping, id reallocation, summary recompute, re-render),
   re-renders, re-verifies, and re-reviews — bounded by `--max-review-passes`
   (default 3), then ships the best draft with residuals recorded. The reviewer
   may only demand removal, demotion, rewording or re-rendering — never a new
   finding. The critic gate in step 7 stays authoritative: the reviewer cannot
   reinstate a dropped finding, and any draft finding outside the advisory
   `reviewed_findings` is itself removed. Every pass is recorded in the
   workspace (`08-review.json`, `09-review-summary.json`).

```
python3 scripts/review_report.py --report ./audit-report.json \
  --workspace .audit/<run-id> --formats json,md,html,pdf
```

Stages 3 through 6 are independent of one another and all read the same
inventory, so a failure in one does not invalidate the others; the orchestrator
records the failure and continues with a documented gap rather than aborting.

Run it:

```
python3 scripts/run_audit.py https://example.com --formats json,md,html,pdf
```

## Composition

The orchestrator's job is composition, not detection. It contributes no checks
of its own. Specifically it:

- **Sequences** the stages and enforces the shared budget across all of them.
- **Isolates failures** — a stage that errors is recorded in `limitations`
  rather than aborting the run, so a partial audit is still a usable audit.
- **Takes findings from the advisory layer, not from the detectors.** This is
  the important one: if the advisor dropped a finding, it does not appear in
  the report. There is no path around the critic.
- **Prioritises globally** by severity, then pipeline order, then confidence.
  Pipeline order matters because an upstream cause should be read before its
  downstream symptoms.
- **Validates** the assembled report against the required schema and refuses to
  emit an invalid one.
- **Renders** to the requested formats from one composed object.

## Output

`site`, `audited_at`, `summary` and `findings` exactly as required, plus
`scope`, `scores`, `proactive_recommendations`, `advisory` (the audit trail of
what the critic removed and why), `limitations`, and `generator`.

Formats:

- **JSON** — the canonical artefact.
- **Markdown** — for a pull request or a ticket.
- **HTML** — self-contained, inline SVG charts, no external assets.
- **PDF** — vector charts, generated with the standard library alone.

## Guardrails

Recommend-only. No skill in this marketplace modifies a live site. Read-only,
unauthenticated, `robots.txt` respected, rate-limited, scope-confined to the
registrable domain, hard page and time budgets. Every suggested action is a
recommendation for a human to apply.

## Grounding

The pipeline shape is the two-stage framework of arXiv:2604.25707 — citation
selection and citation absorption as separate outcomes — extended at the front
with reachability (the paper's measured 76.44% fetch success rate) and at the
back with on-site engagement (the handout's second half). `references/composition.md`
documents the ordering rationale and the failure-isolation policy;
`references/severity-model.md` documents severity and claim-level assignment;
`references/report-schema.json` is the validated schema.
