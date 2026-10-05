---
name: safari-fix
description: Use when scanning code for Safari/WebKit pitfall patterns and auto-fixing them — code that works in Chrome but breaks in Safari (100vh, svg width, date parsing, lookbehind regex, etc.). Static analysis only; no browser. Triggers - "/safari-fix", "check Safari compatibility", "find code that might break in Safari", "WebKit compat scan".
---

# safari-fix — Static scan + fix for Safari/WebKit pitfalls

Find **pitfalls** — code patterns that render or run fine in Chrome but break in Safari (WebKit) — by static analysis. No browser is launched; the code is the only input. Each pitfall carries a confidence tier that decides the action:

- **[auto-fix]** — the fix is safe with no side effects. Apply it directly.
- **[report-only]** — false-positive risk, or the fix requires a design / browser-support decision. Do not touch; report it.

Grep patterns, verdict criteria, fixes, and confidence tiers for every pitfall live in [PITFALLS.md](PITFALLS.md).

## 1. Scope

If a file/directory path is given as an argument, scan only that. Otherwise use the files being worked on in the conversation; failing that, all frontend files in the repository (css/js/html). List the target files at the top of the report.

## 2. Scan

Grep the target files for **every item** in PITFALLS.md.

**Completion criterion: every item is recorded as either "hit (file:line)" or "not present".** Do not move on with items skipped.

## 3. Verdict — filter false positives

A grep hit is a candidate, not a pitfall. For each hit, **read the actual code at that location** and check the verdict criteria (surrounding conditions) in PITFALLS.md. Example: `100vh` is a pitfall only on fixed full-screen elements; in a desktop-only section it is harmless.

**Completion criterion: every hit is recorded as confirmed / false positive / undecidable (with reason).**

## 4. Fix

- Fix **[auto-fix]** items only. Follow the surrounding code's style and comment conventions (e.g. this repo's CSS block-comment rule). Where a comment is warranted, state the WebKit issue in one line.
- Do not touch **[report-only]** items — put the decision they need (browser-support range, design impact) as a question in the report.
- Do not touch code unrelated to a pitfall. Every changed line must trace back to a specific pitfall.

## 5. Report

```markdown
## safari-fix results — <scope>

| Pitfall | Location | Verdict | Action |
|---|---|---|---|
| svg width missing from shrink-to-fit | product-detail.css:3042 | confirmed | ✅ added min-width |
| input font-size <16px (iOS zoom) | product-detail.css:812 | confirmed | ⚠️ report-only — design decision needed |

- Hits dismissed as false positives: (location + reason)
- Decisions needed from the user: (questions from report-only items)
```

Static analysis is inference without reproduction — end the report by recommending verification in real Safari (live verification is out of scope for this skill).
