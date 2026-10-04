---
name: cyber-security-essentials
description: >
  UK NCSC Cyber Essentials compliance assessor for code, config, and CI.
  Maps five technical controls to application checks; complements security-audit,
  bug-hunter, and engineering skills. Use on /cyber-security-essentials, UK CE
  readiness, supplier assurance, or chains cyber-essentials-*.
argument-hint: "Scope + mode: e.g. 'auth module CE check', 'pre-deploy', 'whole codebase'"
user-invocable: true
disable-model-invocation: false
---

# Cyber Security Essentials (UK)

**Purpose:** Assess **code, configuration-as-code, and CI** against **UK NCSC Cyber Essentials** five controls so the project can comply where engineering can act. Report organisational/infra gaps separately.

**Cache is king:** load manifest + CONCERNS + CONVENTIONS before deep source reads.

**Complements (do not duplicate):**

| Skill | Role |
|-------|------|
| security-audit-agent | Deep auth, permissions, consent, OWASP on findings |
| bug-hunter-agent | Logic defects, races, validation gaps surfaced by CE checks |
| schema-audit-agent | DB exposure, migration safety |
| project-drift-guardian | CI/deploy/config drift vs policy |
| ai-engineering-maturity | Organisational guardrails and SDLC maturity |
| git-workflow-guardrails | Pre-commit security checklist, dependency gates |

**Reference:** [uk-cyber-essentials.md](references/uk-cyber-essentials.md) · [report-template.md](references/report-template.md)

## Phase 0 — Load context (required)

1. `.github/project-manifest.yaml` or `.claude/project-manifest.yaml` — stack, paths, test command
2. `docs/codebase/CONCERNS.md` — known security risks
3. `docs/codebase/CONVENTIONS.md` + `docs/codebase/TESTING.md`
4. Latest `TODO/*.md` — in-scope work
5. User scope from `$ARGUMENTS` (module, path, `pre-deploy`, or `whole codebase`)

## Phase 1 — Mode

| Mode | Keywords | Behaviour |
|------|----------|-----------|
| **assess** (default) | assess, review, CE, cyber essentials | Report per five controls |
| **pre-deploy** | pre-deploy, release, ship | Assess + blockers for release |
| **gap-only** | gaps, delta, quick | Only CE-critical/high + out-of-code list |

Emit: `Cyber Essentials: mode=<mode> scope=<scope>`

## Phase 2 — Static scan (when scripts exist)

```bash
bash .github/skills/cyber-security-essentials/scripts/cyber-essentials-scan.sh
```

Review output; deepen with targeted grep/read on flagged paths. For Laravel apps use DDEV per `ddev-local-runtime` when running project tooling (`composer audit`, etc.).

## Phase 3 — Five-control pass

For each NCSC control, work through [uk-cyber-essentials.md](references/uk-cyber-essentials.md) checklist:

1. **Firewalls** — CORS, ingress/IaC, rate limits, public admin exposure
2. **Secure configuration** — debug off, headers, secrets in repo, error leakage
3. **User access control** — auth middleware/policies, MFA, sessions, least privilege
4. **Malware protection** — lockfiles, CI secret/dep scan, upload handling
5. **Security update management** — Dependabot, audit in CI, EOL runtimes

Flag **out-of-code** items (endpoint AV, perimeter firewall, board sign-off) under organisational gaps — do not mark as code PASS without noting them.

## Phase 4 — UK GDPR code slice (brief)

Where personal data is processed: minimisation in forms/APIs, retention hints, TLS, logging without unnecessary PII. Cross-reference security-audit for consent/CDD if applicable.

## Phase 5 — Report

Write to `reports/security/cyber-essentials/YYYY-MM-DD-<scope-slug>.md` using [report-template.md](references/report-template.md).

Include:

- Control summary table (pass/partial/fail per control)
- Findings `CE-001…` with severity, evidence, remediation
- Handoff bullets for security-audit / bug-hunter / drift-guardian
- Certification readiness: **ready / partial / not ready** (code slice only)

## Phase 6 — Fix policy

- **Read-only by default** — no code changes unless user passes `fix` in args or chain has fix_policy
- **CE-critical** in auth/secrets: suggest only; hand off to security-audit-agent
- **CE-medium/low** isolated config fixes: may suggest patch; never commit without approval

## Chains

| Chain | Composition |
|-------|-------------|
| `cyber-essentials-review` | this → security-audit-agent |
| `cyber-essentials-hunt` | this → bug-hunter-agent → security-audit-agent |
| `cyber-essentials-pre-deploy` | drift-guardian → this → bug-hunt-pre-deploy |
| `cyber-essentials-maturity` | this → ai-engineering-maturity → security-audit-agent |

Invoke: `.github/skills/chain/SKILL.md cyber-essentials-review` or `/cyber-security-essentials auth module`

## Anti-patterns

- Claiming full Cyber Essentials certification from code review alone
- Skipping out-of-code organisational requirements in the report
- Duplicating full OWASP pass (delegate to security-audit-agent)
- Running destructive scans or live-db tests