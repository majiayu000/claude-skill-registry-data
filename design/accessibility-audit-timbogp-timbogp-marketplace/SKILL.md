---
name: accessibility-audit
description: This skill should be used when evaluating a design, page, or component against accessibility standards and producing a severity-scored report. Trigger phrases include "audit accessibility", "check a11y", "is this accessible", "WCAG audit", "check color contrast", and "accessibility review before handoff". Use it to assess WCAG 2.2 Level AA conformance from code, a screenshot, a description, or a live URL, and to grade findings by severity with concrete remediations.
version: 0.1.0
---

# Accessibility audit

Evaluate a design, page, or component against **WCAG 2.2 Level AA** and produce a **severity-scored report** with a remediation for every finding. This skill diagnoses and grades; when a fix means writing code, hand off to the `accessible-components` skill.

## When to use

Use when the user asks to "audit accessibility", "check a11y", run a "WCAG audit", "check color contrast", confirm "is this accessible", or do an "accessibility review before handoff". Also use proactively before a design ships to engineering.

## Inputs

Work from whatever is available, and say which mode you used:

- **Source code** (HTML/JSX/Vue/etc.) — inspect markup, roles, attributes, and styles directly. Most thorough.
- **A screenshot** — assess visual checks (contrast, target size, focus indication if captured, text legibility); flag what cannot be verified visually (keyboard, names, sequence) as "needs manual test".
- **A description** — reason about likely issues and list the manual checks the user must run.
- **A live URL or local HTML file** — run automated checks (see below) AND the manual walkthrough.

## Method: POUR

Walk the four WCAG principles in order. The full per-criterion checklist with criterion numbers and test steps is in `references/wcag-2.2-aa-checklist.md` — load it and work through it.

- **Perceivable** — text alternatives (1.1.1), captions/audio (1.2.x), info-and-relationships and meaningful sequence (1.3.1, 1.3.2), use of color not alone (1.4.1), contrast (1.4.3 text, 1.4.11 non-text), resize/reflow/text-spacing (1.4.4, 1.4.10, 1.4.12), content on hover/focus (1.4.13).
- **Operable** — keyboard (2.1.1) and no trap (2.1.2), enough time (2.2.x), no flashing (2.3.1), bypass blocks / headings / focus order / link purpose / multiple ways (2.4.x), **focus not obscured (2.4.11)**, focus appearance, pointer gestures and **dragging movements (2.5.7)**, **target size 24px minimum (2.5.8)**.
- **Understandable** — language (3.1.x), on-focus/on-input no surprise (3.2.x), **consistent help (3.2.6)**, error identification/labels/suggestions (3.3.1–3.3.4), **redundant entry (3.3.7)**, **accessible authentication (3.3.8)**.
- **Robust** — valid parsing, name/role/value (4.1.2), status messages (4.1.3).

### Manual checks the tools cannot catch

Always do these by hand (or instruct the user to):

1. **Keyboard-only walkthrough** — unplug the mouse. Reach and operate every control with Tab/Shift+Tab/Enter/Space/arrows. Nothing should be unreachable or trapped.
2. **Focus order** — Tab order must follow a logical, meaningful reading sequence; no jumps that lose the user.
3. **Visible focus** — every focusable element shows a clear focus indicator that is not clipped or hidden behind sticky headers (2.4.11).
4. **Screen-reader names** — with VoiceOver/NVDA, confirm each control announces a sensible name, role, and state. Icon-only buttons are the usual failure.
5. **Meaningful sequence** — DOM order matches the intended reading order independent of CSS positioning.
6. **Error identification** — trigger validation; confirm errors are announced, described in text (not color alone), and tied to their field.

## Automated assist

Use the bundled scripts to verify what is mechanical. Treat automation as a floor, not a verdict — it catches roughly a third of issues.

- **Color contrast** — `node scripts/contrast.mjs <foreground> <background>` for any color pair. Reports the ratio and pass/fail for AA/AAA normal, AA/AAA large, and UI/non-text. Example: `node scripts/contrast.mjs "#777" "#ffffff"` → ~4.48 (FAIL AA normal, PASS AA large).
- **Live page scan** — `node scripts/axe-scan.mjs <url-or-file>` runs axe-core via puppeteer when `puppeteer` and `@axe-core/puppeteer` are installed; it groups violations by impact. If those deps are absent it prints install instructions and exits cleanly, so it never breaks an audit.

## Scoring

For each finding, assign:

- **Severity** — one of:
  - **Critical** — blocks a task entirely for some users (e.g. unlabeled submit button, keyboard trap, content unreachable).
  - **Serious** — major barrier with a hard workaround (e.g. body text below 4.5:1, missing form labels, no visible focus).
  - **Moderate** — degrades the experience but task is completable (e.g. vague link text, minor heading-order gaps).
  - **Minor** — polish or edge case (e.g. redundant alt text, slightly-small decorative target).
- **Criterion** — the mapped WCAG success criterion number and name (e.g. `1.4.3 Contrast (Minimum)`).
- **Remediation** — a concrete fix. If the fix is code, name it and hand off to `accessible-components`.

Then compute a **summary score**: a count by severity and an **overall verdict for AA**:

- **Fail** — any Critical or Serious finding open.
- **Conditional** — only Moderate/Minor findings, or items that need manual confirmation.
- **Pass** — no findings at or above Minor that affect conformance and all manual checks passed.

## Output format

Produce a structured report:

```
# Accessibility audit — <target>
Mode: <code | screenshot | description | live>   Standard: WCAG 2.2 AA

## Summary
| Severity | Count |
|----------|-------|
| Critical | n |
| Serious  | n |
| Moderate | n |
| Minor    | n |
Verdict: Fail | Conditional | Pass

## Findings
### Critical
1. <title>
   - Criterion: 1.4.3 Contrast (Minimum)
   - Location: <selector / region / screenshot area>
   - Impact: <who is blocked and how>
   - Fix: <remediation; hand off to accessible-components if code>
### Serious
...
```

Group findings by severity (Critical first). End with the manual checks still outstanding, if any.

## References

- `references/wcag-2.2-aa-checklist.md` — full POUR checklist with criterion numbers and test methods.
- `scripts/contrast.mjs` — contrast ratio calculator.
- `scripts/axe-scan.mjs` — axe-core live scan (graceful if deps absent).
- For stack-aware code fixes, follow `../ux-foundations/references/stack-detection.md` and the `accessible-components` skill.
