---
name: openopc-request-analysis
description: >-
  Light OpenOPC-inspired analysis of user requests before acting: clarify goal,
  decompose work, verify against real artifacts, avoid claiming results that
  were not checked. Use with low priority as a thin overlay on any non-trivial
  request (bugs, payroll, deploy, audits, multi-step features). Do not override
  project-specific skills (FST payroll, architecture, TDD, etc.).
---

# OpenOPC Request Analysis (low priority)

Distilled from [OpenOPC](https://github.com/HKUDS/OpenOPC) for Cursor agents.
**Priority: low.** Apply as a short pre-flight check. Project skills and user
rules always win when they conflict.

## When to use

- Multi-step or ambiguous requests
- Bug reports / “shows X but you said Y”
- Audits, payroll, deploy, “check everything”
- Any claim about app state that must match the UI or data

Skip for trivial one-file edits the user already specified precisely.

## Pre-flight (keep short)

Before coding or asserting numbers, run this mentally (or in 3–5 bullets if
the task is large):

1. **Goal** — What outcome does the user want in the product, not in chat?
2. **Evidence** — Which month, employee, screen, or file proves success?
3. **Work items** — Split into 1–5 concrete slices (investigate → fix → verify).
   Do not widen scope past the ask.
4. **Done bar** — What would a reviewer check in under a minute?

## Self-Built / Self-Run / Self-Grown (adapted)

| OpenOPC idea | In Cursor |
|--------------|-----------|
| Self-Built | Identify which modules/roles own the change (calc vs UI vs deploy). |
| Self-Run | Execute one slice; leave a verifiable handoff (file + expected number/UI). |
| Self-Grown | If the same mistake repeats (e.g. chat ≠ app), tighten verification next time. |

## Hard rules (from OpenOPC collaboration discipline)

- **Do not invent status.** Never say “deployed / fixed / equals 2037” unless
  you verified against production, build output, or a reproducible calc on
  the same month/employee the user sees.
- **Chat ≠ product.** If you describe expected math, label it as expected
  and separately report what the code/UI currently produces.
- **Same context.** Month, employee, plan/fact hours must match the user’s
  screen before comparing totals.
- **Handoff over vibes.** Prefer: symptom → root cause → fix location →
  how to re-check. No long theory without a check.
- **Stay in the work item.** Do not silently expand into unrelated refactors.

## Verification checklist (use when numbers or deploy are involved)

- [ ] Same month as the user’s screenshot / message
- [ ] Same employee (tab / name)
- [ ] Plan/fact hours from the same source as the timesheet totals
- [ ] Gross = base + OT + bonuses + brigadier − penalties (as applicable)
- [ ] After deploy: hard refresh note (Ctrl+F5) only if deploy actually succeeded

## Output style when analyzing a request

Keep analysis brief. Prefer:

```text
Goal: …
Slices: 1) … 2) …
Verify: …
Risk: …
```

Then act. Do not turn every message into a long OpenOPC org chart.

## What this skill is NOT

- Not a full OpenOPC company runtime (no MCP company_mode, no talent pool).
- Not a replacement for `fst-payroll-georgia`, `debugging-and-error-recovery`,
  or other project skills — those take precedence.
- Not a reason to over-plan simple tasks.

## Source

Installed from local archive `OpenOPC-main.zip` (HKUDS/OpenOPC). Core ideas
kept: work-item discipline, verify before claim, durable preferences only.

See also: [reference.md](reference.md)
