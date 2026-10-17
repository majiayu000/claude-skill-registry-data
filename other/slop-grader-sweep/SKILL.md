---
name: slop-grader-sweep
description: LLM-graded prose quality sweep (no-ai-slop + tech-docs rulesets) for docs/wiki/specs markdown
version: 1.0.0
---

# Slop grader sweep

Complements `skills/writing-heuristics/` (deterministic, regex-based) with
LLM-graded checks slop-grader's `no-ai-slop` and `tech-docs` rulesets catch
that regex cannot: rhetorical AI tells, document-level structural quality,
undefined jargon, stale placeholders.

## Trigger

- **`changed` mode**: pre-commit hook, staged `.md` files under
  `docs/`, `wiki/`, or `**/specs/`. Warn-only, always exits 0.
- **`sweep` mode**: scheduled GitHub Actions workflow
  (`.github/workflows/slop-sweep.yml`), weekly, full repo. Report-only,
  writes `drift/SLOP-REPORT.md`.

## Input/Output

**`changed` mode**
- Input: none (reads `git diff --cached` directly).
- Output: stdout summary of findings (file:line, rule, severity), exit
  code always 0.

**`sweep` mode**
- Input: none (globs the repo directly).
- Output: `drift/SLOP-REPORT.md` — `Status: DEGRADED` header on failure,
  otherwise a findings-by-file report.

## Setup

One-time, after `npm ci` inside this directory:

```bash
node scripts/install-hook.mjs
```

See `docs/USAGE.md` for the full workflow, troubleshooting, and the
manual smoke-test procedure.
