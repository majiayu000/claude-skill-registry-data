---
name: defuddle
description: Use when extracting readable main content from HTML or URLs with Defuddle, or when debugging Defuddle parser behavior, selector removals, standardization, markdown conversion, and fixture-based regressions in browser, Node.js, CLI, or worker environments.
---

# Defuddle

Use this skill to choose the right Defuddle interface, extract clean article content, and debug parsing mistakes without introducing unsafe HTML handling or weak regression coverage.

## Choose The Interface First

- Browser: use `defuddle` on the current `document` for extensions and web apps.
- Node.js: use `defuddle/node` with a DOM `Document` from `linkedom`, `jsdom`, `happy-dom`, or a similar implementation.
- CLI: use `npx defuddle parse <url-or-file>` for quick experiments, one-off conversions, and regression checks.
- Worker or hosted API: validate with `curl`, not a browser, so the response body is inspected directly.

## Happy-Path Extraction

1. Start with the narrowest output that answers the task.
   - HTML output: default parse result
   - Markdown: `markdown: true` or `--markdown`
   - Metadata bundle: `--json`
   - Single property: `--property <name>`
2. When parsing detached HTML, provide the page URL so relative links can be resolved correctly.
3. Use the smallest bundle that fits the job. Prefer the core bundle unless markdown or math fallbacks require the fuller variants.

## Debug Wrong Extraction Systematically

1. Turn on debug mode first.
   - Code path: `debug: true`
   - CLI path: `--debug`
2. Inspect:
   - `result.debug.contentSelector`
   - `result.debug.removals`
3. Disable one transformation at a time to find the stage that drops useful content.
   - `removeSmallImages`
   - `removeHiddenElements`
   - `removeLowScoring`
   - `removeExactSelectors`
   - `removePartialSelectors`
   - `removeContentPatterns`
   - `standardize`
4. If auto-detection chooses the wrong node, set `contentSelector` explicitly and re-run.
5. If selectors are the issue, review the exact and partial selector lists before adding new heuristics.
6. After a fix, add a minimal anonymized fixture and expected output, and prove the fixture fails before the fix.

## Security And Correctness Rules

- Never parse with raw `innerHTML`; route parsing through the DOM utility layer so scripts and external resources do not execute.
- Strip unsafe scriptable URLs, `data:text/html`, iframe `srcdoc`, and inline `on*` handlers.
- Convert live HTML collections to static arrays before mutating the DOM.
- Treat code and preformatted blocks as protected when adjusting removal heuristics.

## Verification Strategy

- Worker or local API: `curl http://localhost:8787/...`
- Hosted service: `curl https://defuddle.md/...`
- CLI regression check: `npx defuddle parse ... --markdown`
- Codebase regression check: add fixtures under `tests/fixtures/` and expected output under `tests/expected/`

## Reference Material

- Read `references/defuddle-notes.md` for environment selection, useful options, and source provenance.
