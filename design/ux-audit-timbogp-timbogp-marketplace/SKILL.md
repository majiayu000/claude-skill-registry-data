---
name: ux-audit
description: This skill should be used when the user wants a structured usability review of an interface and asks to "audit this UX", "run a usability review", "do a heuristic evaluation", "review this flow/screen", "what's wrong with this UI", or "is this usable". It produces a scored, severity-ranked usability report from screenshots, a live URL, a description, or source code.
version: 0.1.0
---

# UX Audit

Run a structured usability audit and produce a scored, severity-ranked report. This skill is the qualitative-heuristics counterpart to two siblings: `ux-metrics` (quantitative behavioral data — task success, time-on-task, conversion, drop-off) and `accessibility-audit` (WCAG conformance — contrast, keyboard, screen readers, semantics). Keep the division of labor clear: this skill judges whether the design is *usable and well-structured for a sighted user completing tasks*; it does not measure traffic and it does not certify accessibility. A full `/ux-audit` engagement combines usability findings (this skill) with an accessibility pass (`accessibility-audit`) so nothing falls between the cracks.

## When to use

Trigger on requests like: "audit this UX", "usability review", "heuristic evaluation", "review this flow", "review this screen", "what's wrong with this UI", "is this usable", "evaluate this onboarding". Use it whether the goal is a quick critique or a formal scored report — always produce the scored output, scaled to the input.

## Inputs

Work from whatever is available, in rough order of richness:
- **Screenshots / mockups** — evaluate visible structure, hierarchy, copy, affordances. Note that hidden states (loading, error, hover) cannot be judged and must be flagged as assumptions.
- **A live page or URL** — the strongest input; walk real tasks, trigger real states, count real steps.
- **A description** — evaluate the described flow and intent; ask for screenshots or a link if findings would be speculative.
- **Source code** — read component markup, routing, and state to infer the rendered experience and locate issues precisely (file and component names sharpen recommendations).

When the input is thin, state what could and could not be evaluated rather than inventing findings.

## Method

Evaluate across these dimensions. Read `references/nielsen-heuristics.md` before scoring — it defines each heuristic, what to look for, and the severity scale.

1. **Nielsen's 10 usability heuristics.** The backbone of the audit. Inspect each heuristic in turn against the interface; do not stop at the first problem found per heuristic.
2. **Information architecture & navigation.** Is grouping logical? Are labels predictable? Can the user tell where they are, where they can go, and how to get back? Look for orphaned pages, ambiguous menus, and hidden but important destinations.
3. **Task / flow analysis.** Pick the primary task(s) and walk them end to end. Count the steps, clicks, and fields required. Flag friction (redundant input, unexpected detours), dead-ends (states with no forward path), and points where the user must guess.
4. **Error prevention & recovery.** Can mistakes be avoided (constraints, good defaults, confirmation on destructive actions)? When an error occurs, is it caught early, explained plainly, and recoverable without losing work?
5. **Content hierarchy & scannability.** Does the visual hierarchy match importance? Is text scannable (headings, chunking, short lines) or a wall? Is the primary action obvious?
6. **Consistency.** Internal (same concept, same name/component/placement throughout) and external (matches platform and common conventions).

For each problem found, record it as a **finding** with: a tag for the heuristic violated, the location (screen/component/step), a clear observation, the user impact, and a concrete recommendation.

## Scoring

Assign every finding a **severity on Nielsen's 0–4 scale**:

- **0** — Not a usability problem (note only; often a passing observation).
- **1** — Cosmetic; fix if time permits.
- **2** — Minor; low priority.
- **3** — Major; important to fix, high priority.
- **4** — Catastrophe; must fix before release.

Severity is a judgment over three factors (defined in the reference): **frequency** (how often it's hit), **impact** (how hard it is to overcome when hit), and **persistence** (whether users adapt or keep tripping). A market-wide problem affecting every user repeatedly trends toward 4.

Then summarize:
- A **heuristic scorecard** — for each of the 10 heuristics, the number of issues found and the worst severity.
- An **overall usability verdict** — a short plain-language judgment (e.g., "usable but high-friction checkout") backed by the scores.
- **Top issues ranked** by roughly *severity × frequency × impact* — the handful that, if fixed, move the needle most.

## Output

Fill in the template at `assets/audit-report-template.md`. Keep observations specific (point at the exact element/step), keep recommendations actionable (say what to change, not just that it's wrong), and keep the scorecard honest — passing heuristics with no issues are a result worth reporting.

## Hand-offs

Route findings outside this skill's scope to the right place rather than half-solving them:
- **Accessibility issues** (contrast, focus order, alt text, keyboard traps, ARIA) → `accessibility-audit`.
- **Copy and microcopy issues** (unclear labels, blaming errors, weak CTAs, empty states) → `ux-copy`.
- **Missing or unhandled states** (no loading, empty, error, or success feedback) → `interaction-feedback`.
- **Quantitative validation** (does the data confirm the suspected friction? where do users actually drop off?) → `ux-metrics`.

Name the hand-off in the finding so the reader knows where to take it next.
