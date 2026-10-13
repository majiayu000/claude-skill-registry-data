---
name: pr-review
description: >
  Fast, one-line-per-finding PR review. Severity-tagged, no praise, no scope
  creep. Written in the Nimbus caveman format so the output stays scannable.

  Trigger this skill when:
  - User says "review this PR", "review the diff", "audit this file", or invokes
    `/pr-review`.
  - After a `gh pr diff` or a `git diff` the user pastes.
  - Before merging a PR the user wants a second opinion on.
---

## Output format

One line per finding. Nothing else.

```
<path>:<line>: <emoji> <severity>: <problem>. <fix>.
```

Severities + emojis:

| Emoji | Severity | Meaning |
|---|---|---|
| 🔴 | `critical` | Broken in prod / security / data loss risk. |
| 🟠 | `high` | Real bug, will bite once shipped. |
| 🟡 | `medium` | Design smell, works today, fragile. |
| 🔵 | `low` | Nit-pick worth mentioning. |

## Behavior

1. Get the diff. Sources:
   - `gh pr diff <N>` if user gave a PR number.
   - `git diff <base>..<head>` if user gave a branch.
   - Pasted diff in the message.
2. Walk hunks. For each concerning line, emit one finding.
3. Group findings **by severity, descending**. Within severity, by file.
4. End with a one-line summary: `Total: N critical / M high / K medium / L low`.
5. If the diff is clean, say: `No blocking issues.` — no praise, no fluff.

## Focus areas (in order)

1. **Security** — SQL injection, XSS, secrets, auth bypass, path traversal, SSRF.
2. **Correctness** — off-by-one, wrong error codes, missing await, race conditions.
3. **Data integrity** — migration safety, transaction boundaries, ORM misuse.
4. **API contract** — breaking changes, missing versioning, wrong HTTP codes.
5. **Performance** — N+1 queries, unbounded loops, sync in async, blocking calls.
6. **Testing** — untested critical paths, mock-heavy tests hiding real bugs.
7. **Reversibility** — hard-to-revert migrations, force pushes, deletes.
8. **Style** — SKIP unless a style choice changes semantics. Format failures
   are the `preflight` skill's problem, not yours.

## Do not

- Praise ("great job", "clean code"). Never. Just findings.
- Suggest additional features. Stay in-scope.
- Rewrite prose in comments unless the comment is wrong.
- Flag `TODO` without ownership as critical — it's a `low`.
- Mention "style" — CI + preflight catch style.

## Nimbus-specific gotchas to always check

- **cidca-platform ecg_auto**: any migration touching `api_ecg`, `api_center`,
  `api_organization`, `api_patient`, `api_discounttag` columns → 🟠 high.
  Invoke `db-migration-safety` skill for detailed check.
- **cidca-services lambdas**: `lambda_handler.py` methods > 50 lines → 🟡 medium.
- **cidca-platform ecg-ui**: hardcoded hex colors (`#fff` OK on overlays, else no) → 🔵 low.
- **horus web**: `bg-white` / `text-gray-900` hardcoded (bypasses light/dark mode) → 🟠 high.
- **zotea**: any `pnpm db:migrate` invocation outside `.github/workflows/db-migrate.yml` → 🔴 critical.
- **All Nimbus repos**: `--no-verify` in commit/push → 🔴 critical (skips hooks).
- **All Nimbus repos**: `git push --force` to `dev` / `main` / `master` → 🔴 critical.

## Length cap

Never exceed 50 findings. If the PR is larger, review only the highest-severity
20 + say `Truncated. Review the rest in follow-up.`
