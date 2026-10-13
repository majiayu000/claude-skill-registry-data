---
name: code-review-cicd
description: >
  Review CI/CD pipelines for security flaws — poisoned workflows, secret leakage, and injection.
  Load on GitHub Actions / GitLab CI / Jenkins config, ".github/workflows", pull_request_target,
  self-hosted runners, or "pipeline security". Signals: workflow YAML, secrets in CI, third-party actions.
domain: code-review
type: technique
stability: learning
modes: [bugbounty, defense, pentest]
severity: high
owasp: [A08:2021-Software-and-Data-Integrity-Failures]
cwe: [CWE-94, CWE-829, CWE-522]
mitre: [T1195]
tools: [semgrep, gitleaks]
schema_version: 1
---

# CI/CD pipeline security review

## When it applies
You can read a repo's CI config (GitHub Actions, GitLab CI, Jenkinsfile, CircleCI). Pipelines run
with secrets and often on attacker-influenced input (PRs), making them a high-value, under-reviewed target.

## Why it works
CI runs code with privileged tokens/secrets. Misconfigurations let a fork PR run in a trusted
context, inject commands via untrusted inputs, or exfiltrate secrets — a supply-chain foothold. On
public repos this can be exploitable by anyone who opens a PR.

## Method
1. **Dangerous triggers**: `pull_request_target` / `workflow_run` that check out and run **PR code**
   with secrets in scope → fork PRs can steal secrets or run arbitrary code (the classic GitHub Actions bug).
2. **Script injection**: untrusted data (`github.event.issue.title`, PR body, branch name) used
   directly in `run:` shells → command injection. Look for `${{ github.event.* }}` in `run` blocks.
3. **Secret handling**: secrets echoed/logged, passed to third-party actions, or available to fork PRs;
   overly broad `permissions:` (default `write`), long-lived `GITHUB_TOKEN`.
4. **Untrusted dependencies**: third-party actions pinned to a mutable tag/branch (not a SHA),
   curl-pipe-to-shell steps, unpinned package installs → supply-chain.
5. **Self-hosted runners** on public repos: fork PRs executing on your infra → RCE on the runner.

## Gotchas
- `pull_request` (safe-ish) vs `pull_request_target` (dangerous) — the trigger name is the crux.
- An action pinned to `@v3` (tag) can be moved; require a full commit SHA for third-party actions.
- Secret leakage often happens via a step passing `${{ secrets.X }}` to an untrusted action.

## Verify success
A concrete path where an outsider (fork PR / issue) can execute code with pipeline privileges or
exfiltrate a secret, or a clear secret-leak/injection in the workflow.

## References
GitHub Actions security hardening docs; "GitHub Actions pwn requests" (Nathan Davison); semgrep CI rules.
