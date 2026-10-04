---
name: proof-orchestrator
description: Route Codex proof work to the right verification path before making done, fixed, safe, current, or complete claims. Use when the user asks to verify, prove, validate, review proof, confirm a fix, check if something is really done, compare proof levels, choose between tests/runtime/end-to-end evidence, or when a task risks fake closure.
---

# Proof Orchestrator

Use this skill to choose the proof plan. Do not use it as proof by itself.

## Core Rule

Map the claim to the weakest proof level that would still be honest. If the user asks for a stronger proof level, use the stronger one.

- `implemented`: files/config/docs changed and inspected.
- `code_proven`: current source inspection supports the claim.
- `test_proven`: fresh automated tests support the claim.
- `runtime_proven`: fresh evidence on the supported runtime path supports the claim.
- `end_to_end_proven`: fresh evidence across the real user-visible path supports the claim.

Never upgrade one level into another. Say `not_proven_yet` when the available evidence is weaker than the claim.

## Routing

1. Restate the claim as a falsifiable sentence.
2. Identify the required proof level and why.
3. Route to the smallest existing skill or proof surface that can falsify it.
4. Run or request the proof. Do not summarize stale proof as current proof.
5. Report the strongest safe truth, proof gaps, and next proof step.

## Proof Paths

- Bug, regression, crash, slowness, flaky behavior: use `$diagnose` first to build the feedback loop, then prove the fix with fresh evidence.
- Specific claim with measurable baseline/treatment: use `$verify-this`.
- Code review or behavioral regression risk: use review mode first; findings outrank summary.
- GitHub PR/CI truth: use GitHub/CI proof surfaces, then report only what the current checks prove.
- UI or browser behavior: use a real preview/browser path when available; screenshots alone are not enough for interaction claims.
- CLI/TUI behavior: use a real terminal transcript or deterministic command output; avoid visual inference only.
- Docs/current-version truth: inspect source docs or official upstream before claiming current behavior.
- Security or supply-chain safety: prefer source inspection, version pinning, advisory checks, and minimal execution before trust.
- Human-in-the-loop, approvals, credentials, paid actions, private data, legal/business decisions: stop at the human gate. Do not treat repeat/continue/resume as approval.

## Claim Calibration

Use these words precisely:

- Say `implemented` only for changed files or configs.
- Say `test_proven` only when the relevant fresh test actually ran and passed.
- Say `runtime_proven` only when the supported runtime path was exercised.
- Say `end_to_end_proven` only when the real user-visible flow was exercised.
- Say `inconclusive` when the proof surface failed, was blocked, or measured the wrong thing.

## Output

Use this shape:

```text
Proof target: <falsifiable claim>
Required level: <implemented|code_proven|test_proven|runtime_proven|end_to_end_proven>
Route: <skill/tool/test/runtime path>
Evidence collected: <fresh evidence or none>
Verdict: <proven level or not_proven_yet/inconclusive>
Gap: <next proof needed, if any>
```

If the evidence is stale, indirect, or only from a tracker/doc, name it as weak evidence instead of proof.
