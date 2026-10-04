---
name: emperor-verify
description: >-
  Emperor Time — VERIFY / review / critique. Claim audit, eight-count
  self-critique, isolated hetero-critique, request-review HARD-GATE, receive-review HARD-GATE,
  verification-before-completion / evidence HARD-GATE, claim-audit HARD-GATE, critique eight-count HARD-GATE, verdict/breach HARD-GATE (G5), mechanical G4/G5. Use when
  reviewing a diff, requesting code review, claiming tests pass, saying done /
  fixed / green, or before commit/PR/deliver/merge.
license: MIT
metadata:
  version: 0.4.27
  part-of: emperor-time
  chain: judgment-chain
---

# Emperor Verify (Judgment wrapper)

## MUST — critique eight-count HARD-GATE before G4

Before opening G4, run `scripts/emperor critique <task-dir>` (or
`self-critique`). Doctrine: `chains/judgment-chain/self-critique.md`.
Missing axes / empty Checked cells / critique-file-present theater → exit 1.
G4 calls `scripts/lib/critique.py`; a critique file alone is theater.

## MUST — claim-audit HARD-GATE before G4

Before opening G4, run `scripts/emperor claim-audit <task-dir>` (or
`judgment-audit`). Doctrine: `chains/judgment-chain/claim-audit.md`.
Missing CLAIM AUDIT line / unfinished HYPOTHESIS|TESTED → exit 1.
G4 calls `scripts/lib/claim_audit.py`; a critique file alone is theater.

## MUST — request-review checklist first

Before merge to main, after a major feature, and after each subagent-driven
task, open `skills/emperor-verify/request-review-checklist.md`
(Chain Jail leaf from Superpowers `requesting-code-review` → When / How /
Act-on-feedback only)
and/or run `scripts/emperor review` (prints the mechanical REVIEW / STEP / MUST
card).

No author self-review in place of dispatch. Do not load whole
`requesting-code-review`; ET + emperor-verify orchestrate.


## MUST — receive-review checklist when acting on feedback

When receiving code-review feedback (human partner, external reviewer, or
hetero-critique) — before implementing suggestions — open
`skills/emperor-verify/receive-review-checklist.md`
(Chain Jail leaf from Superpowers `receiving-code-review` → The Response
Pattern / Forbidden Responses / When To Push Back only)
and/or run `scripts/emperor receive` (prints the mechanical RECEIVE / STEP /
MUST card).

No blind implement. No performative agreement. Do not load whole
`receiving-code-review`; ET + emperor-verify orchestrate.

## MUST — evidence checklist before completion claims

Before claiming tests pass, bug fixed, build green, requirements met, agent
done, or any satisfaction/completion phrasing — and before commit/PR/deliver —
open `skills/emperor-verify/verification-checklist.md`
(Chain Jail leaf from Superpowers `verification-before-completion` → The Iron
Law / The Gate Function only)
and/or run `scripts/emperor evidence` (prints the mechanical EVIDENCE / STEP /
MUST card).

No completion claim without a fresh proving command in this turn. Do not load
whole `verification-before-completion`; ET + emperor-verify orchestrate.

## Hard rules

1. Run `scripts/emperor evidence` → quote `EVIDENCE checklist=yes` before any
   completion / pass / fixed / done claim. Advance with
   `scripts/emperor evidence --advance N N+1` (skips fail). Unverified claim →
   `scripts/emperor evidence --reject-unverified` (HARD-GATE exit 1).
2. Run `scripts/emperor review` → quote `REVIEW checklist=yes`. Advance with
   `scripts/emperor review --advance N N+1` (skips fail). Self-review skip →
   `scripts/emperor review --reject-self-review` (HARD-GATE exit 1).
3. When acting on review feedback, run `scripts/emperor receive` → quote
   `RECEIVE checklist=yes`. Advance with `scripts/emperor receive --advance N N+1`
   (skips fail). Blind implement → `scripts/emperor receive --reject-blind-implement`
   (HARD-GATE exit 1).
4. Read `chains/judgment-chain/SKILL.md` and select **one** aspect:
   `claim-audit.md` | `self-critique.md` | `hetero-critique.md` |
   `gatekeeping.md` | `verdicts-and-breaches.md`.
5. Claim ledger: every VERIFIED row needs quoted evidence. Cross-agent rows
   start CONJECTURE.
6. Self-critique uses `templates/critique.md`. "No findings" without named
   commands/paths is a fail.
7. Hetero-critique: run `scripts/emperor review-pack <task-dir> <base> <head>` (Python core `scripts/lib/review_pack.py`; thin `review-pack.sh` / `review-pack.ps1`; isolation HARD-GATE `--reject-unisolated` / `--reject-author-diary` / `--check-isolation`) and
   dispatch the pack to a **different** context (Steal Chain worker or a fresh
   subagent). The builder does not write the hetero verdict.
8. Act on Critical immediately; Important before proceed; Minor noted; pushback
   only with quoted evidence (run `emperor receive` when implementing feedback).
9. Run `scripts/gate.sh g4 <task-dir>` and quote the tail.
10. Deliver only after `scripts/emperor verdict <task-dir>` and `scripts/gate.sh g5 <task-dir>` (verdict.py: no empty/theater Breach Register; Verdict cites claim audit / critique / hetero).

Proportionality / anti-loop: honor `effort_class` caps via `scripts/emperor proportionality --check-proportionality <task-dir>` (HARD-GATE `--reject-over-verify`; G4 records+checks). Missing class on critique/finish/grill → tiny hard cap (`bump_and_check`). Tiny asks do not re-run the museum of gates. Idle Steal/Jail/Holy SKIP (vacuous — no activity) is separate.
