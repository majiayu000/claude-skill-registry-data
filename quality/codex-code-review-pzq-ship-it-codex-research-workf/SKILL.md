---
name: codex-code-review
description: Use when the user asks for code review, PR review, merge readiness, quality/security/maintainability assessment, review after implementation, or severity-rated findings; inspect code changes with independent reviewer posture, file/line evidence, deterministic verdicts, and no self-approved fixes unless separately requested.
---

# Codex Code Review

Review code for bugs, regressions, security, performance, maintainability, and architecture risk. This is the native Codex adaptation of OMX `$code-review`: keep severity gates, architect/watchlist perspective, independent review posture, and deterministic verdicts; omit OMX HUD/state.

## Review Stance

Lead with findings. Do not bury bugs under summary. If no issues are found, say so clearly and name residual risk or unrun checks.

Default to read-only review. Apply fixes only when the user explicitly asks for review-and-fix or the current surrounding workflow requires implementation.

## Workflow

1. Identify scope with `git diff`, requested files, PR branch, or changed artifacts.
2. Inspect relevant tests, contracts, configs, docs, and calling paths.
3. Review with two lenses: code correctness/security/quality and architecture boundaries/tradeoffs.
4. Rate severity: Critical, High, Medium, Low.
5. Produce deterministic verdict:
   - Request changes if Critical/High or architect BLOCK exists.
   - Comment if only Medium/Low or architect WATCH exists.
   - Approve only when evidence supports it and no blocking risks remain.

## Evidence Rules

- Every finding needs a concrete file/line reference or command/artifact evidence.
- Distinguish confirmed bug from risk.
- Do not invent line numbers.
- Do not self-approve your own recent implementation when independent review is required; use a fresh lane if available or report the limitation.

## Output Shape

- Findings by severity
- Open questions / assumptions
- Verdict
- Test gaps or residual risk
- Optional change summary, only after findings

## References

Read `references/review-checklist.html` for category and verdict details.
