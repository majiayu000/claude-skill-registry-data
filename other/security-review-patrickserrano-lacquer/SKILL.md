---
name: security-review
description: >
  Adversarial security review of a change (branch diff, PR, or working tree) before merge.
  Use when the user asks to "review this for security", "security review", "check for
  vulnerabilities", "is this safe to merge", or before merging anything that touches a
  trust boundary — auth/authz, input parsing, secrets/keychains, file writes, shelling out,
  untrusted-input-into-shell/YAML, CI workflows that run on privileged runners, or
  generated LLM instructions. Also the standing gate this repo runs on every lacquer PR.
---

Review the change adversarially — assume the diff is hostile until proven safe. Report
only findings you can tie to a concrete failure scenario; do not pad with generic advice.

## Scope the diff

1. Establish the base: `git diff <base>...HEAD` for a branch, `gh pr diff <n>` for a PR,
   or `git diff` for the working tree. Read enough surrounding context to judge each hunk —
   never review a hunk in isolation.
2. If the change is large, fan out: one reviewer per trust boundary (auth, input parsing,
   secrets, CI/exec, file I/O), then dedupe. A single pass misses cross-cutting issues.

## What to hunt for

- **Injection**: untrusted input (user data, `github.event.*`, PR titles/branch names,
  file contents, tool output, dependency changelogs) reaching a shell, `eval`, SQL, YAML,
  or an LLM instruction context. Trace the value from source to sink; quote both.
- **Path/traversal & symlink**: writes that can escape a root, TOCTOU between check and
  write, following a symlink, absolute paths sneaking in through a config field.
- **Secrets**: keys/tokens echoed, written to files that become artifacts, passed on a
  command line (visible in the process table), over-scoped, or leaking across CI jobs.
- **Privilege**: CI that runs untrusted fork code on a privileged/self-hosted runner;
  missing least-privilege `permissions:`; unpinned third-party actions or tool installs.
- **Fail-open**: a guard that silently passes on error, a `|| true` that swallows a real
  failure, a check that no-ops when its input is missing.

## Verify before reporting

For each candidate finding, state the exact inputs/state that trigger it and the resulting
wrong behavior. If a nearby check already prevents it, drop the finding and say so. Default
to "refuted" when uncertain — a plausible-but-wrong finding wastes more than a missed nit.

## Report

Ranked, most-severe first: `file:line`, severity (critical/high/medium/low), the concrete
exploit/failure scenario, and a suggested fix. Then a short "defenses confirmed" list so the
reader knows what is already solid. If nothing survives verification, say so plainly.

For a fresh-eyes pass on high-risk changes, run this as a separate agent given ONLY the diff
(no implementation context) — it catches bug classes the implementer's own tests miss.
