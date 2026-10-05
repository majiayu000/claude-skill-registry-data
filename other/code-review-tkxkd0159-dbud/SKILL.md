---
name: code-review
description: Use when reviewing branch or PR changes against a base branch for correctness, security, concurrency, architecture, maintainability, testing, and performance risks.
argument-hint: "[--base BRANCH] [--comment [LANGUAGE]]"
disable-model-invocation: true
---

# Code Review

Review the current branch or PR against a base branch with adversarial, evidence-based scrutiny. Prefer concrete regressions over style feedback.

**Default to a single pass.** One reviewer reads the whole diff against the checklist in step 3; a single context keeps cross-cutting bugs (e.g. a change that is both a concurrency and a security issue) visible and findings high-signal. Reserve isolated subagents for one case: a diff too large to review in one focused pass. Partition the substantive files into a *few* cohesive groups (by module/directory), review each group against the full checklist — sequentially, or as a handful of parallel subagents — then merge and dedup. Never fan out by lens, and never one subagent per file — both fragment cross-cutting bugs and inflate false positives.

## Inputs

- Default base: `origin/main`. `--base BRANCH` compares against `BRANCH`.
- `--comment [LANGUAGE]`: after the report, gate posting through **Posting** (below) — the user approves a subset in chat and only that subset is posted via `add-pr-comments`. `LANGUAGE` sets comment language (default English). Without `--comment`, the report (step 6) is the final artifact and nothing is posted.

## Workflow

1. Pin the comparison. Set `BASE_BRANCH` from `--base` or `origin/main`, then:

   ```bash
   HEAD_SHA=$(git rev-parse HEAD)
   MERGE_BASE=$(git merge-base "$BASE_BRANCH" "$HEAD_SHA")
   ```

   Review `"$MERGE_BASE".."$HEAD_SHA"` for the entire pass.

2. Inventory the diff: changed files, shortstat, added/deleted files, diff body. Ignore generated files, vendored code, lockfiles, snapshots, and docs-only changes unless they affect runtime, build, or security.

3. Read the whole diff against this checklist — or, if it is too large for one focused pass, partition it as described in the intro. `correctness` always applies; the rest are cues — weight attention to what the diff actually touches. Gather evidence first (cited ranges, prior vs current behavior, touched callers, reachable inputs), then draft a finding only from evidence: title, severity, confidence, `file:line`, failure mode, fix.

   | Lens              | Look for                                                                                                       |
   | ----------------- | -------------------------------------------------------------------------------------------------------------- |
   | `correctness`     | logic, null handling, contracts, stale callers, data corruption, migrations, cache staleness, unreachable code |
   | `security`        | auth/authz, injection, unsafe deserialization, SSRF, path traversal, tenant or PII leaks                       |
   | `concurrency`     | non-atomic updates, lock ordering, cancellation hazards, retry interactions, double-submit/double-process      |
   | `architecture`    | boundary breaks, dependency direction, wrong-layer abstractions, cross-module coupling                         |
   | `maintainability` | brittle abstractions, unclear invariants, accidental complexity, obvious simplification not taken              |
   | `testing`         | coverage gaps for changed behavior, weak assertions, flakiness, fixture pollution                              |
   | `performance`     | query shape, N+1s, hot-path allocations, nested loops over user data, missing or wrong caching                 |

4. Apply the bar. Self-critique each candidate from the PR author's perspective and keep only what the author would clearly fix. **Returning zero findings is correct** — if nothing clears the bar, say so; never pad the report. Move plausible-but-unverified concerns to residual risks.

5. Validate every surviving finding against the current code and diff; drop anything the cited range does not support. Dedup overlapping findings, keeping the strongest severity/confidence.

6. Report in this order:
   - Review range: `<merge-base>..<HEAD>` resolved to short SHAs
   - Verdict: exactly one of `ready to approve`, `ready after fixes`, or `not ready` — one line, naming the blockers if any
   - Findings: title, `SEV/CONF`, `file:line`, failure mode, fix
   - Cross-cutting risks, if any
   - Residual risks: plausible-but-unverified concerns, if any

7. If `--comment` is set, gate posting through **Posting** below — the only path that writes to GitHub, and only after explicit user approval.

## Posting (`--comment`)

Posting is the only irreversible step — never invoke `add-pr-comments` or any `gh` write until the user approves the final set.

1. List the surviving findings with stable IDs (`F1`, `F2`, …). Ask the user to reply keep / drop / dive per finding — e.g. "drop F2, dive F4: check the lock at L138, keep the rest."
2. For each **dive**, re-investigate the finding inline against the cited code (with surrounding context), its lens, and the user's hint. Report the refined finding — or that it cannot be substantiated — then re-confirm keep/drop on it.
3. Show the final to-be-posted set and wait for an explicit go-ahead.
4. Re-check `git rev-parse HEAD`; if it moved since the review, warn that line anchors may have shifted and confirm before continuing. Hand the kept set + `LANGUAGE` (default English) to `add-pr-comments`.
5. If nothing is kept, post nothing and say so.

## Follow-ups

After the report, answer user follow-ups conversationally:

- **Clarification** ("why is F2 high severity?"): answer from the cited evidence; if the question is outside the diff, say so.
- **Deep dive** ("F4 looks shallow — did you check the lock at line 138?"): re-investigate the finding inline against the cited code (with surrounding context), its lens, and the user's hint; report the refined finding.
- **More lenses** ("focus on security too"): re-read the same merge-base/HEAD diff with that lens weighted and report.

## Severity

- `critical`: exploitable security issue, auth bypass, data loss, corruption, severe outage
- `high`: likely production failure or serious regression
- `medium`: real bug under a plausible edge case
- `low`: non-trivial issue worth fixing, not a blocker

A **blocker** is a finding that makes the change unsafe to merge as-is — `critical` or `high` by default, a `medium` only when its edge case is plausible in practice; `low` is never a blocker.

## Confidence

- `high`: directly supported by cited code
- `medium`: strong evidence with one assumption
- `low`: plausible but speculative — prefer residual risk over a low-confidence finding

## Avoid

- Pre-existing issues this change neither introduces nor worsens
- Style nits, formatting, subjective preferences, or linter-level issues
- "Check / verify / ensure / confirm X" hedges, or any comment that does not name a concrete failure mode
- Missing tests without a concrete regression risk
- Claims that cannot be verified from the diff and current code
