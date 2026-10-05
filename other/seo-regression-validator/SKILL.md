---
name: seo-regression-validator
description: Validate SEO and LLM-readability claims against live HTML, local fixtures, and generated artifacts. Use this skill when the user asks to prove whether title, meta description, canonical, hreflang, JSON-LD, NewsArticle.image, OpenGraph, Twitter cards, RSS autodiscovery, robots.txt, llms.txt, sitemap, news-sitemap, crawler access, or performance evidence is actually present, and when subjective audits must become timestamped pass/fail reports.
---

# SEO Regression Validator

Use this skill after technical SEO/schema guidance exists, before claiming a site or skill output is done.

Read [references/regression-checklist.md](references/regression-checklist.md) before running a broad audit.

## Owns

- live HTML and local fixture checks;
- pass/fail severity model;
- timestamped evidence reports;
- schema/head metadata checks;
- public artifact reachability checks;
- regression report templates;
- negative tests for missing JSON-LD, duplicate canonical, missing image, and fake reports.

## Does Not Own

- implementing SEO fixes;
- Search Console credentialed data;
- analytics exports;
- external authority placement;
- mutating target websites.

## Workflow

1. Define target URLs or fixture files.
2. Record timestamp, target, method, and user agent.
3. Fetch or read the target without mutation.
4. Run deterministic checks using [scripts/audit_static_seo.py](scripts/audit_static_seo.py) when HTML is available.
5. Separate critical failures, warnings, and skipped checks.
6. Record skipped checks instead of treating them as passes.
7. Produce or update `seo-regression-report.json` and a human-readable validation summary.
8. Route implementation fixes to the appropriate specialist.

## Critical By Default

- missing `<title>`;
- missing meta description;
- missing or duplicate canonical;
- no JSON-LD on pages expected to have schema;
- invalid JSON-LD;
- NewsArticle without usable image;
- public page blocked or unreachable during live check;
- report claims success without fetching or reading target.

## Warning By Default

- missing hreflang when a multilingual equivalent is expected;
- missing OG/Twitter social tags;
- missing RSS autodiscovery;
- missing viewport;
- article meta tags missing when an article schema exists;
- no visible breadcrumb when BreadcrumbList is expected;
- performance metrics not measured.

## Safety And Privacy Boundaries

- Do not mutate target sites.
- Do not use credentials unless the user explicitly provides them for this task.
- Do not store cookies, tokens, raw private analytics, raw IP logs, or private Search Console rows in reports.
- Do not claim ranking, indexing, citation, or crawler behavior from one HTML check.

## Validation

Validate skill edits with:

```bash
python3 <codex-skills-dir>/senior-skill-architect/scripts/lint_production_skill.py ./skills/seo-regression-validator
python3 ./skills/seo-regression-validator/scripts/audit_static_seo.py ./skills/seo-regression-validator/fixtures/good-news.html
python3 ./plans/seo-llm-skill-cluster/scripts/lint_skill_cluster.py .
```

Forward tests live in [evals.json](evals.json).

## Output Shape

Return:

1. Targets checked.
2. Critical findings.
3. Warnings.
4. Skipped checks.
5. Evidence paths or URLs.
6. Implementation owner for each fix.

