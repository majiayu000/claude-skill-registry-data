---
name: visual-qa
description: "Capture reproducible browser evidence after UI changes. Use for desktop/mobile screenshots, overflow, console, failed requests, and keyboard focus; use design-reviewer for critique."
---
# Visual QA

Prove rendered behavior with small, reviewable evidence. Do not turn screenshots into a substitute for design judgment or functional tests.

## Core Rules
1. Start with the changed route, intended state, a running local or preview URL, and the browser tooling already present in the target repository.
2. Capture the default desktop and narrow-mobile viewports unless the product has a documented viewport matrix.
3. Check overflow, console errors, failed requests, and keyboard focus alongside screenshots. Treat these as evidence, not automatic design verdicts.
4. Use stable, seeded, or mocked data for visual comparisons. Do not claim a pixel comparison is meaningful when time, random data, ads, animations, or remote dependencies vary.
5. Do not install packages, send credentials, or browse authenticated production data merely to obtain evidence. Name the missing evidence instead.

## Workflow
1. Inspect existing browser tools, test runners, routes, auth setup, fixtures, and app start commands.
2. Read [references/browser-evidence.md](references/browser-evidence.md) before choosing a runner or interpreting results.
3. When the target repository already has Playwright, run `scripts/visual-qa.mjs` from the target repository root against an explicit URL. It writes base and keyboard-focus screenshots plus `report.json` to the requested output directory.
4. Use `agent-browser`, an existing Playwright suite, or the repository's browser tooling when the bundled helper cannot run. Preserve the same evidence matrix.
5. Send artifacts to `design-reviewer` for a visual verdict. Send functional gaps to `testing-engineer`.

## Verification Loop

1. Reproduce every reported overflow, console, network, or focus failure with the same route, viewport, state, and data assumptions.
2. After a fix, recapture the affected evidence matrix and send it back to the reviewer or tester; do not rely on the original screenshot.
3. Report unavailable states, authentication, or browser evidence as a blocker rather than filling gaps with assumptions.

## Bundled Helper
`scripts/visual-qa.mjs` is an optional Playwright adapter. It never installs dependencies and only visits caller-supplied same-origin HTTP(S) URLs without embedded credentials. It redacts URL query values and common credential patterns before writing evidence, but do not load pages that intentionally print secrets or sensitive personal data to the console or page.

Use `--dry-run` first when checking command shape. Use `--fail-on` only for checks the team agrees should block the task; screenshots still need review.

## Tool Output
Use RTK when available for noisy, non-destructive browser, Playwright, build, lint, or test output. Treat filtered output as triage and inspect raw output before reporting an exact runtime or release-gate finding.

## Evidence To Report
- URL, routes, viewports, browser tool, and data/auth assumptions
- base and `*-focus.png` screenshot paths plus `report.json`
- overflow, console, network, and focus findings
- states inspected and states that could not be produced
- the reviewer verdict or the reason review could not run

## Honest Opinion
Use `honest opinion:` when it adds decision value: reviews, audits, recommendations, plans, tradeoffs, or implementation close-outs with a material risk or gap. Be brutally honest and evidence-based. Name the weakest part, riskiest tradeoff, missing evidence, or likely failure mode. Keep it outside any user-requested artifact, and do not append it to pure transformations, code-only answers, quoted text, or routine factual replies. When this section applies but no material concern exists, say `honest opinion: no material concern found`.

## Output Shape
For visual evidence:

1. route and state covered
2. artifacts and tool used
3. runtime findings
4. evidence missing
5. reviewer or test follow-up
