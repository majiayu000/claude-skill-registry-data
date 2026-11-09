---
name: playwright-reporting
description: Generate non-interactive Playwright evidence reports that replace Playwright UI mode and HTML report browsing in Hephaera sessions.
engines: [AGNOSTIC]
---

## When to use

Use when the user asks to inspect Playwright results, summarize browser test evidence, review screenshots/traces/videos, or produce a report in an environment where interactive Playwright UI tools are unavailable.

Typical triggers:
- "show the Playwright report"
- "summarize test results"
- "index screenshots and traces"
- "create a report from Playwright artifacts"
- "UI mode will not work"

## Output

Produce one or more host-owned Markdown reports:
- test run summary from `test-results/results.json`
- artifact index for screenshots, traces, videos, logs, HTML reports, JSON/XML reports, and snapshots
- browser discovery report from `.playwright-cli/`
- bundled evidence report linking the generated reports

## Notes

- Prefer `commands/playwright-evidence-report.sh` for a one-command report bundle.
- Use `commands/playwright-report-summary.sh` when JSON reporter output exists.
- Use `commands/playwright-artifact-index.sh` to replace browsing report/artifact folders manually.
- Use `commands/playwright-discovery-report.sh` to summarize browser discovery sessions.
- Reports should be written to the host `.hephaera/.cache/reports/` directory by default.
- Do not open Playwright UI mode or start the HTML report server unless the user explicitly asks for an interactive local view.
