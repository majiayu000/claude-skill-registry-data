---
name: verify-this
description: "Formal proof of one concrete claim. Use only for an explicit verify, prove, measure, or confirm request, or when a required high-risk acceptance gate needs a verdict."
source: https://github.com/shaneholloman/cursor-plugins/tree/main/cursor-team-kit/skills/verify-this
license: MIT
---

# Verify This

Use only for an explicit verification request or a required high-risk acceptance gate. Goal: prove or disprove one falsifiable statement. Not for routine completion checks, ordinary test/lint runs, general research, or vague quality claims ("the code is cleaner").

Use GO/NO-GO mode for acceptance gates: high-risk completion checks, migration readiness, PR cleanup readiness, or independent verifier decisions.

Invoke once per claim. Do not reread this skill or restart the workflow in the same task unless the claim, threshold, evidence, or environment changed.

## Workflow

1. Restate claim in falsifiable form: condition, metric, threshold, expected direction.
2. Capture baseline evidence when possible (merge base, parent commit, current broken repro), then treatment evidence with the same command, data, and environment. Compare raw artifacts, not summaries.
3. Return exactly one verdict.

Prefer inline evidence. Do not persist secrets, credentials, customer data, or private code extracts without explicit consent.

## Verdict Rules

- `VERIFIED`: baseline and treatment differ in predicted direction by claimed threshold with no obvious confound.
- `NOT VERIFIED`: behavior unchanged, moves wrong way, or misses threshold.
- `INCONCLUSIVE`: no valid baseline, noisy signal, failed measurement, or environment difference invalidates comparison.

```text
VERIFIED | NOT VERIFIED | INCONCLUSIVE
Claim: <falsifiable claim>

Evidence:
<metric/artifact>: baseline=<...>, treatment=<...>, delta=<...>, threshold=<...>

Reasoning:
<one tight paragraph naming evidence and confounds>
```

## GO/NO-GO Mode

For shipping decisions rather than a single claim verdict.

1. Restate acceptance criteria as falsifiable checks.
2. Verify against current local artifacts/code/live UI. Do not trust prior assistant reports.
3. Check every expected artifact exists, is non-empty, matches source of truth; check no secrets or sensitive data persisted when relevant.
4. `GO` only when every required check passes with current evidence. `NO-GO` when any check fails, is blocked, or cannot be verified.

```text
GO | NO-GO
Scope: <what was verified>

Evidence:
| Check | Evidence | Result |
| --- | --- | --- |
| <criterion> | <artifact/command/live check> | PASS/FAIL |

Repair actions:
- <only when NO-GO>

Residual risks:
- <only real remaining risks>
```

Do not soften negative results. Clear `NOT VERIFIED` is useful.
