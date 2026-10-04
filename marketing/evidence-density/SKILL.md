---
name: evidence-density
description: Absorption-stage audit for whether cited pages can shape AI answers. Use when a brand is found but not quoted or its pages add little to answers. Measures extractable evidence genres and structural legibility against research anchors, and detects Q&A or FAQ wrappers with no underlying evidence.
license: MIT
---

# Evidence Density (absorption layer)

Selection and absorption are different outcomes. arXiv:2604.25707 measures the
gap directly:

| Platform | Mean citations per prompt | Mean influence of fetched pages |
|---|---|---|
| ChatGPT | 6.88 | 0.2713 |
| Google AIO | 12.06 | 0.0584 |
| Perplexity | 16.35 | 0.0646 |

Perplexity cites nearly two and a half times as many sources as ChatGPT and
absorbs each one roughly a quarter as deeply. Being cited is not the same as
mattering, and this skill measures the second thing.

## When to use

After `crawl-reachability` has built the page inventory. Run it standalone when
a brand is *found* but never *quoted* — the symptom of a selection pass with an
absorption failure.

## Inputs

- **Required** — a run workspace: `preflight.json` for the scope domain and
  `reachability.json` for the page inventory and saved HTML paths.
- **Not consumed** — no network access. This layer re-scores markup that
  `crawl-reachability` already fetched, so it is re-runnable offline.

```
python3 scripts/score_evidence.py [--workspace PATH] [--json]
```

## Procedure

Deterministic, in this order. Text statistics only — no model, no sampling, no
wall-clock input, so the same markup always scores the same.

1. **Load pages and scope.** Read `preflight` and `reachability`; note pages
   whose HTML is missing as a coverage limitation.
2. **Thin content.** Score pages with too little substance to carry an
   absorbable unit.
3. **No evidence genre at all.** Flag pages carrying none of the five measured
   genres (**this is the finding that moves the paper's measured influence**).
4. **The Q&A trap.** Flag Q&A-shaped pages with no evidence genre underneath,
   and *never* recommend adding an FAQ.
5. **Structure.** Measure heading hierarchy, list density and paragraph length
   as legibility proxies.
6. **Genre gaps across the site.** Roll per-page genre coverage up to find the
   genres the site systematically lacks.
7. **Survey-graded genres.** Check for prices/rates and visible dates — the
   extractable-fact genres arXiv:2607.14035 §7.2 names and §7.5 grades
   `Moderate`. Reported with the grade, never with an effect size.
8. **Marketing over evidence.** Compare promotional language against concrete
   substantiation, and attach the retrieval-backfire caution to the fix.
9. **Boilerplate.** Discount repeated chrome so it cannot inflate a page's
   apparent substance.
10. **Site-level rollup.** Emit the absorption distribution and the genre
    matrices the report renders.

## The one finding people get backwards

Adding an FAQ is the standard GEO recommendation. The paper measures Q&A
formatting as the **only negative** evidence genre:

| Genre | Influence with | Influence without | Difference |
|---|---|---|---|
| Code | 0.1747 | 0.0988 | **+76.9%** |
| Numbers / statistics | 0.1171 | 0.0725 | **+61.6%** |
| Definition markers | 0.1252 | 0.0795 | **+57.3%** |
| Comparison content | 0.1389 | 0.0894 | **+55.3%** |
| How-to content | 0.1296 | 0.0918 | **+41.2%** |
| **Q&A format** | **0.0947** | **0.1005** | **−5.7%** |

The mechanism the paper proposes: evidence genres create reusable support
units, while Q&A formatting is a surface wrapper. Rephrasing a thin page as a
question does not add anything to extract.

**This skill therefore never recommends adding an FAQ**, and flags Q&A-wrapped
pages that carry no evidence genre underneath.

## Checks and severities

Every check the procedure above can emit, with the claim level it is allowed to
assert.

| Check id | Detects | Severity | Claim level |
|---|---|---|---|
| `thin_content` | Pages below the site-calibrated word floor | high | 1 |
| `no_evidence_genre` | No definition, numeric, comparison, how-to or code content | high | 2 |
| `qa_wrapper_without_evidence` | Q&A packaging with no underlying evidence | medium | 2 |
| `unstructured_page` | Too few headings or paragraphs to segment | medium | 1 |
| `no_numeric_evidence` | Claims made with no figures anywhere on the site | medium | 2 |
| `no_comparison_content` | Nothing positioning the brand against alternatives | medium | 3 |
| `no_definition_content` | Nothing defining what the brand or product *is* | medium | 3 |
| `no_price_evidence` | No price, rate or cost anywhere on the site | medium | 2 |
| `no_date_evidence` | No published or updated date on any sampled page | low | 2 |
| `marketing_over_evidence` | Promotional hedges far exceeding extractable facts | medium | 3 |
| `low_absorption_site` | Site-wide readiness in the weak band | medium | 3 |
| `boilerplate_dominant` | Chrome outweighing substance | medium | 2 |

Severity is capped by claim level automatically. The three mechanism-level
checks (`no_comparison_content`, `no_definition_content`,
`marketing_over_evidence`) cannot exceed `medium` no matter how stark the
observation, because the paper supports them as interpretation rather than as
measured cause.

The two genre checks from the survey (`no_price_evidence`,
`no_date_evidence`) are grounded differently from the rest: arXiv:2607.14035
grades prices and dates `Moderate` on its lever table (§7.5, Table 4) rather
than reporting an effect size, so these findings cite the grade and are
capped at claim level 2. Neither is a defect — a page with no price is harder
to quote, not broken. A price or date is only useful when it is specific,
current and attributed; the research is explicit that the goal is not to
"add numbers" (survey §7.2), and a fabricated figure is worse than none. Much
of this module's advice recommends editing page content, so every such
recommendation also carries the survey's backfire warning (§7.4): in a
controlled arena, body-only rewrites *reduced* top-20 presence by about 9%,
top-10 after reranking by about 16%, and final citation by about 6%. Add the
missing fact; do not rewrite the page around it.

## Page-type exemptions

Absorption is not a universal goal. The skill exempts:

- **Legal pages** (privacy, terms, cookies) — optimising these for citation is
  not desirable.
- **Hub and category pages** — their job is routing, not explaining. Judging a
  storefront category page on prose depth is a false positive.

Exemptions come from `AuditConfig.expectations_for(page_type)` and are recorded
in the output so a reviewer can see what was skipped and why.

## Thresholds are derived, not hardcoded

The word-count floor is `max(corpus bottom quartile of 170, half this site's
median)`, capped at 600. A site of 2,000-word guides gets a higher bar than a
site of 200-word product pages, so "unusually thin *for this site*" stays
detectable either way. Every threshold reports its provenance in the finding's
evidence string.

## Output

`04-evidence-density.json` with per-page scores, the site rollup, the genre
matrix and the findings.

## Guardrails

Read-only; consumes saved HTML only and issues no requests of its own.

## Grounding

§8.1 structure quartiles (words 11.44x, headings 12.46x, paragraphs 5.69x,
list density 8.92x between top and bottom influence quartiles); §8.2 evidence
genre uplift; §8.3 semantic role influence (definition 0.1531, comparison
0.1524, down to reference 0.0529); Fig. 6 word-count bins. The scoring model
and its deliberate divergence from the paper's Equation (2) are documented in
`references/absorption-model.md`.
