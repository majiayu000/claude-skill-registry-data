---
name: judgment-day
description: "Trigger: judgment day, judgment-day, adversarial review, dual review, doble review, juzgar. Blind review with synthesis, bounded fixes, and escalation."
license: Apache-2.0
metadata:
  author: gentleman-programming
  adapted_by: andresnator
  source: gentleman-programming/sdd-agent-team
  version: "2.0.0"
  status: in-progress
---

## Contract

The coordinator scopes and synthesizes; judges review blindly; the fixer edits only authorized findings. Missing target is `ASK`, never a partial review. Load at most 3-5 relevant project rules and inject the same distilled rules into every child brief.

## Full protocol

1. Launch `jd-judge-a` and `jd-judge-b` independently, preferably in parallel. A emphasizes correctness/edge cases; B emphasizes security/performance. Each gets one sweep, or two only for >400 changed lines or a hot path.
2. A valid result is clean or contains evidence-backed findings with stable ids and failure scenarios. Retry one malformed child once; a second malformed return is `JUDGMENT: INVALID ROUND`.
3. Synthesize: both judges = confirmed; one judge's CRITICAL/WARNING inside its emphasis = emphasis-confirmed; other single findings = suspect; disagreement = contradiction. Keep ids and lifecycle `open | fixed | verified | refuted | wont-fix`.
4. Without preset mode, ask whether to fix/re-judge, fix only, or stop. Never edit before authorization. `verdict-only` stops; `full` authorizes the first fix.
5. `jd-fix` touches confirmed and emphasis-confirmed rows only. Re-judge those ids with fresh A/B judges. Any open verdict stays open; both fixed = verified; both refuted = refuted. Defects introduced by the fix are new findings.
6. Maximum two fix rounds. Each later fix/re-judge needs a continue gate. Remaining confirmed issues escalate; never loop forever.

## Light protocol

Use one `jd-solo` sweep. Retry malformed output once. Auto-fix CRITICAL rows only when light mode was preset, once, with no re-judge. Report other findings and recommend full judgment if evidence is severe or contradictory.

## A2A

Judges return one line per finding:

`<path:line> <critical|warning|note> <problem>; fix=<intent>`

Then `TOTAL critical=<n> warning=<n> note=<n>` or `CLEAN evidence=<one-line check>`. Re-judge uses `VERDICT <id>=fixed|open|refuted evidence=<path:line>`. Fixer returns `OK fix files=<csv> check=<one-line>` plus one `OPEN <id> <reason>` per unresolved row. No logs, diffs, praise, or empty fields.

User questions, security warnings, irreversible actions, ambiguity, and the final human verdict use normal language. Persist an SDD ledger at the active change root when requested.

## Assets

- `assets/judge-prompt.md`
- `assets/fix-prompt.md`
- `assets/output-formats.md`
