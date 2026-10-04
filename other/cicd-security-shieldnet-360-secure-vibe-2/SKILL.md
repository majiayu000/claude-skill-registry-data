---
id: cicd-security
version: "1.2.0"
title: "CI/CD Pipeline Security"
description: "Harden GitHub Actions, GitLab CI, and similar pipelines against supply-chain attacks, secret exfiltration, and pwn-request abuse. Use when authoring or reviewing workflow files, adding a third-party action, image, or script, wiring cloud or registry credentials into CI, or triaging a suspected pipeline compromise."
category: prevention
severity: critical
applies_to:
  - "when authoring or reviewing CI/CD workflow files"
  - "when adding a third-party action / image / script to a pipeline"
  - "when wiring cloud or registry credentials into CI"
  - "when triaging a suspected pipeline compromise"
languages: ["yaml", "shell", "*"]
token_budget:
  minimal: 1350
  compact: 1750
  full: 2200
rules_path: "checklists/"
related_skills: ["supply-chain-security", "secret-detection", "container-security"]
last_updated: "2026-06-21"
sources:
  - "OpenSSF Scorecard — Pinned-Dependencies / Token-Permissions"
  - "SLSA v1.0 Build Track"
  - "GitHub Security Lab — Preventing pwn requests"
  - "StepSecurity — tj-actions/changed-files attack analysis"
  - "CWE-1395: Dependency on Vulnerable Third-Party Component"
external_tools:
  - name: actionlint
    purpose: "GitHub Actions workflow lint (syntax, expressions, shellcheck on run: steps)"
    command: "actionlint"
---

# CI/CD Pipeline Security

## Rules (for AI agents)

### ALWAYS
- Pin every third-party GitHub Action by **commit SHA** (full 40-char), never by
  a floating tag (`@v1`, `@main`, `@latest`) — tags can be re-pushed. The
  tj-actions/changed-files March 2025 incident exfiltrated secrets from 23,000+
  repositories specifically because consumers used floating tags. Same applies to
  GitLab CI `include:` references and reusable workflows. Renovate / Dependabot
  can keep the SHA pins fresh.
  <!-- pattern: { id: gha-pin-actions-by-sha, severity: high, check: deterministic } -->
- Declare `permissions:` at the workflow or job level and default to
  `contents: read` only. Grant additional scopes (`id-token: write`,
  `packages: write`, etc.) job-by-job, never workflow-wide.
  <!-- pattern: { id: gha-default-permissions-read, severity: high, check: deterministic } -->
- Use **OIDC** (`id-token: write` + cloud provider trust policy) for
  short-lived cloud credentials. Never store long-lived AWS / GCP / Azure
  keys as GitHub Secrets.
  <!-- pattern: { id: gha-oidc-cloud-credentials, severity: high, check: deterministic } -->
- Treat `pull_request_target`, `workflow_run`, and any `pull_request` job
  that uses `actions/checkout` with `ref: ${{ github.event.pull_request.head.ref }}`
  as **trusted-context-on-untrusted-code** — the "pwn request" pattern documented
  by GitHub Security Lab. Either don't run them, or run with no secrets and no
  write tokens. A fork's GitLab merge-request pipeline is the same shape — it runs
  the fork's own `.gitlab-ci.yml` on your runners: isolate them, expose no
  protected variables.
  <!-- pattern: { id: gha-pr-target-no-untrusted-checkout, severity: critical, check: deterministic } -->
- Echo every untrusted expression (`${{ github.event.* }}`) through an
  environment variable first; never interpolate it directly into `run:`
  body — that's the canonical GitHub Actions script-injection sink. The GitLab
  sink has the same shape: `$CI_*` / `$TRIGGER_*` interpolated into `bash -c` or
  `eval`, where merge-request metadata carries the shell metacharacters.
  <!-- pattern: { id: gha-no-untrusted-script-injection, severity: critical, check: deterministic } -->
- Sign release artifacts (Sigstore / cosign) and publish SLSA provenance
  attestations. Verify provenance in any consumer pipeline that pulls the
  artifact.
- Pin `runs-on` to a dated runner image (`ubuntu-24.04`), not a floating label
  (`ubuntu-latest`) — the label moves underneath you. On GitLab, use ephemeral
  Docker-executor runners with `privileged: false`; a shared shell runner with
  `privileged: true` gives a compromised job root on the host. An egress firewall
  on runners handling secrets (StepSecurity Harden-Runner or equivalent) is
  defense-in-depth on top of that, not a substitute.
  <!-- pattern: { id: gha-harden-runner, severity: medium, check: llm } -->
- Require a human reviewer on a dependency-bump PR when `supply-chain-security` raises
  a **trust-boundary** change — a maintainer or ownership change, a new or changed
  install hook, a registry or source transition, a provenance regression. Gate on that
  signal, not on the version number: a patch release that changes maintainer warrants
  more review than a major bump that does not.
- Consult `supply-chain-security` before any dependency install step
  (`npm install`, `pip install`, `docker pull`) — in CI it is untrusted code
  execution on a runner holding your credentials. It owns install-script risk
  (`postinstall`, `setup.py`, `build.rs`) and registry pinning;
  `container-security` names the command that fixes the lockfile half (`npm ci`,
  `--frozen-lockfile`) rather than adding flags to `npm install`.

### NEVER
- `curl | bash` (or `wget -O- | sh`) any installer script in CI.
  The 2021 Codecov bash-uploader compromise exfiltrated env vars to an
  attacker for ~10 weeks because thousands of pipelines ran
  `bash <(curl https://codecov.io/bash)`. Always download, checksum,
  then execute.
  <!-- pattern: { id: gha-no-curl-pipe-bash, severity: critical, check: deterministic } -->
- Echo secrets to logs, even on failure. Use `::add-mask::` for any
  computed-at-runtime secret, and double-check with the GitHub
  workflow-log search.
- Cache mutable state (e.g. `~/.npm`, `~/.cargo`, `~/.gradle`) keyed only
  on `os`. A cache hit cross-job is a cross-tenant attack surface — key
  on a lockfile hash and scope to the workflow ref.
  <!-- pattern: { id: gha-cache-key-scope, severity: medium, check: deterministic } -->
- Trust artifact downloads from arbitrary workflow runs without verifying
  the source workflow + commit SHA. Build-cache poisoning works through
  unscoped artifact reuse.
  <!-- pattern: { id: gha-artifact-verify-source, severity: medium, check: deterministic } -->
- Store secrets in repository variables (`vars.*`) — they are plaintext
  to anyone with read access. Only `secrets.*` are gated by the secret
  scanning + scope rules. GitLab's equivalent: a CI/CD variable without
  `protected: true` + `masked: true` is exposed to every feature-branch pipeline.

### KNOWN FALSE POSITIVES
- First-party actions in the same organization that you mirror or fork
  in-house may legitimately be pinned by tag if the org enforces signed
  tags + branch-protection on the action repo.
- Public-data pipelines that handle no secrets and produce no signed
  artifact (e.g. nightly link-checkers) don't need OIDC or SLSA
  provenance, and may use floating tags without practical impact.
- `pull_request_target` is legitimate for label / triage bots that only
  call the GitHub API with the minimal scopes needed, do not check out
  PR code, and don't expose secrets in env.

## Context (for humans)

CI/CD is now the most lucrative single supply-chain target. A pipeline
runs trusted code against trusted credentials and trusted registries —
compromising it once gives access to every downstream consumer of every
artifact it produces. The 2021 Codecov compromise, 2021 SolarWinds
incident, 2024 Ultralytics PyPI release-pipeline poisoning, and the
2025 tj-actions/changed-files mass exfiltration all hinged on
unauthenticated changes to CI-consumed scripts or actions.

Most of the defenses are mechanical: pin by SHA, minimize permissions,
use OIDC, sign artifacts, verify provenance. The hard part is enforcing
them across an organization. OpenSSF Scorecard automates checks for the
mechanical defenses and integrates with branch protection.

This skill emphasizes the design-pattern weaknesses (pwn requests,
script injection, curl-pipe-bash, floating tags, untrusted artifact
download) because they are the patterns AI-generated workflow YAML
reinvents most often.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `checklists/gitlab_ci_hardening.yaml`
- [OpenSSF Scorecard](https://github.com/ossf/scorecard).
- [SLSA v1.0 Build Track](https://slsa.dev/spec/v1.0/levels).
- [GitHub Security Lab — Preventing pwn requests](https://securitylab.github.com/research/github-actions-preventing-pwn-requests/).
- [StepSecurity — tj-actions/changed-files attack analysis](https://www.stepsecurity.io/blog/tj-actions-changed-files-attack-analysis).
- [CWE-1395](https://cwe.mitre.org/data/definitions/1395.html).
