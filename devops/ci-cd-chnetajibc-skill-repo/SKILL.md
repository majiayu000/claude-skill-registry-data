---
name: ci-cd
description: "CI/CD: shift left, quality gates, flags, failure feedback loops. Reproduce CI failures locally first."
---

# ci-cd

CI is the gate, not the suggestion box: fast, hermetic, least-privileged.

## Activate when

- Designing pipelines, adding quality gates, or diagnosing red builds.

## Do NOT activate for

- GitHub Actions syntax specifics (see devops/github-actions); release mechanics (see git/git-release).

## Procedure

1. Gates in order: lint → typecheck → test → build; fail fast; cache deps with correct keys.
2. Shift left: every CI check runnable locally with one command; CI and local must agree.
3. Red builds: reproduce locally with the same command first, then fix; never "fix" by weakening the gate.
4. Secrets via encrypted secrets with minimal permissions; no secrets in logs; pin third-party actions.
5. Verify: green run on the change, no skipped required checks, failure drill (break it on purpose, watch it fail loud).

## References
- Related: `../../devops/github-actions/`.
