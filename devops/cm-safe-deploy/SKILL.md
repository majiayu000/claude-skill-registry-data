---
name: cm-safe-deploy
description: Use when setting up deployment infrastructure or enforcing a gated release path. Routes to deploy gates, setup, or rollback based on the current deployment stage.
token_budget: 1500
token_core: 500
token_refs:
  gate-0-secret-hygiene: 620
  gate-0-5-security-scan: 300
  gate-1-syntax: 280
  gate-2-test-suite: 380
  gate-3-i18n: 260
  gate-4-5-build-dist: 340
  gate-6-deploy-smoke: 320
  setup-new-project: 360
  rollback: 220
compressed: true
deprecated: false
---

# Safe Deploy Pipeline v2

## TL;DR
- **Use before/during** staging or production deployment
- **Model**: gated deploy pipeline with hard stops
- **Decision**: choose setup, active gate execution, or rollback
- **Next**: `cm-quality-gate` for verification evidence

## The Iron Law
```text
NO DEPLOY WITHOUT PASSING ALL GATES.
GATES ARE SEQUENTIAL.
IF A GATE FAILS, FIX FIRST.
```

## When to Use
- Establishing deploy infrastructure for a new project
- Hardening an existing project that deploys without gates
- Recovering after incidents caused by weak release validation
- Running or reviewing a release pipeline before production changes

## Choose Your Path

```
Need to create deploy infrastructure for a project?
└─ YES → Setup path

Already have infrastructure and need to run or review gates?
└─ YES → Gate path

Did a deploy fail or need reversal?
└─ YES → Rollback path
```

| Path | Summary | Load |
|---|---|---|
| Setup | Establish scripts, tests, and deploy workflow | `references/setup-new-project.md` |
| Gate 0 | Secret hygiene | `references/gate-0-secret-hygiene.md` |
| Gate 0.5 | Security scanning | `references/gate-0-5-security-scan.md` |
| Gate 1 | Syntax validation | `references/gate-1-syntax.md` |
| Gate 2 | Test suite | `references/gate-2-test-suite.md` |
| Gate 3 | i18n parity | `references/gate-3-i18n.md` |
| Gates 4-5 | Build + dist verification | `references/gate-4-5-build-dist.md` |
| Gate 6 | Deploy + smoke verification | `references/gate-6-deploy-smoke.md` |
| Rollback | Recovery and reversal | `references/rollback.md` |

## Gate Map
```text
0   Secret hygiene
0.5 Security scan
1   Syntax
2   Test suite
3   i18n parity
4   Build verification
5   Dist verification
6   Deploy + smoke test
```

## Load Rules
- Load only the gate reference for the current stage.
- Load `setup-new-project.md` only when establishing infrastructure.
- Load `rollback.md` only when deployment fails or rollback planning is required.

## Integration
| Skill | Why |
|---|---|
| `cm-quality-gate` | verification and evidence checks |
| `cm-identity-guard` | deploy identity verification |
| `cm-safe-i18n` | i18n-specific gate setup |
| `cm-terminal` | monitored execution of gate commands |

## Rules
- Gates are sequential and blocking.
- Do not skip to later gates when an earlier gate fails.
- Keep deploy setup and active deploy execution separate in your head and in your prompts.
- Security and secret hygiene remain part of this skill; do not rely on deprecated skills.

## The Bottom Line
**Choose setup, the current gate, or rollback. Load only that path, and stop on failure.**
