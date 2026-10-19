---
name: honest-status
description: "Writing a STATUS.md that stays true: separates done/verified/in-progress/blocked, detects false-done claims, records evidence pointers, and writes handoff notes so the next agent does not repeat work. Use when asked to report status, write a handoff, audit a STATUS.md, or decide whether a task is really finished."
license: MIT-compat
compatibility: "framework-agnostic; text; any host"
metadata: {}
allowed-tools: []
---

Standard: name/description/length rules — [agentskills.io standard](../references/agentskills-standard.md).
# Honest Status Skill — Quick Reference (body <500 lines; full procedure in references/honest-status-procedure.md)

## When to use this skill (trigger)
- You are asked to write STATUS.md, a handoff note, or a progress report *for work another agent will pick up* (a README checkbox is NOT a status ledger).
- You must decide whether a task is really DONE or merely "coded" — i.e. a check ran and passed, not just that the code is written.
- A previous agent claimed something is finished and you need to audit it for false-done claims.
- You need evidence pointers that a human or another agent can actually open in under 60 seconds.

## Disambiguation
- Fires: writing STATUS.md/handoff for work another agent picks up, auditing for false-done, deciding DONE vs coded.
- Does NOT fire for: a changelog/release notes, a chat update reviewed in the same session, or a single README checkbox (that is a doc, not a ledger).

## When NOT to use this skill
- Writing a changelog or release notes (use the project's release process; this skill governs the work ledger, not the product log).
- Informal chat updates reviewed in the same session — a status with no persistence need not be written down.
- A task that has no evidence at all — the skill does not invent a pointer, it records FALSE_DONE and names the blocker.
- A single checkbox in a README — that is a doc, not a status ledger; use the ledger only for work that another agent will pick up.

## Decision table — status bucket
| Bucket | Meaning | Required evidence |
|--------|---------|-------------------|
| DONE | Implemented AND verified by a runnable check | test/log/commit pointer |
| VERIFIED | A check ran and passed, but the change is not yet integrated | check output pointer |
| IN_PROGRESS | Work exists but the check has not passed yet | current diff pointer + blocker |
| BLOCKED | Cannot proceed without an external answer | open question + owner |
| FALSE_DONE | Claimed done but no evidence exists | flag, downgrade to IN_PROGRESS |

## Numbered procedure (summary; full recipe in references/honest-status-procedure.md)
1. **Enumerate claims** — list every claim in the current STATUS.md or handoff.
2. **Find evidence** — for each claim, locate a runnable artifact (test, log, command output).
3. **Classify** — DONE / VERIFIED / IN_PROGRESS / BLOCKED / FALSE_DONE using the decision table.
4. **Write the buckets** — one section per bucket; never merge DONE and IN_PROGRESS.
5. **Flag false-done** — any claim without evidence is downgraded and listed under FALSE_DONE.
6. **Add handoff notes** — what to retry first, what is missing, who owns the open question.
7. **Re-read aloud** — every line must be checkable in under 60 seconds.

## Worked examples
Good (every DONE has a pointer that opens in <60s):
```markdown
## DONE
- `scripts/check_outbox.py` shipped — `python3 scripts/check_outbox_test.py` (exit 0)
  evidence: skills/engineering/outbox-idempotency/scripts/check_outbox_test.py#L12
## VERIFIED
- Poller ordering rule verified against Docker Postgres 15 —
  evidence: tests/e2e/outbox-ordering.log (8 KB, 2026-10-13)
## BLOCKED
- axe-core upgrade blocked until the integrator records the bump in `docs/STATUS_ALL.md` —
  owner: integrator, question: "which axe-core minor is approved for the Freeze 4 bump?"
```
Bad (DONE with prose only — this is FALSE_DONE):
```markdown
## DONE
- Outbox checker is working and handles everything.
```
Bad (DONE and IN_PROGRESS merged — hides what is actually shippable):
```markdown
## DONE
- Outbox checker written, tests added, needs one more edge case.
```

## Pitfalls from research
- "Done" without a pointer is the most common lie; always require a runnable artifact.
- A green test for the wrong behaviour is not evidence of correctness.
- Copying a previous STATUS.md forward preserves its false-done claims.
- Vague blockers ("investigate later") are never resolved; name an owner and a date.
- Evidence that only exists in your head is not evidence; write it down.
- A BLOCKED entry that names a version that does not exist is worse than no blocker — it
  trains the next agent to ignore the line. Re-fetch the registry before writing a version
  gate (`registry.npmjs.org/axe-core` returned 4.14.0 on 2026-10-14, so "until it returns
  4.15" is not a live question); name the decision-maker and the artifact that would
  authorize the bump instead.

## Near-miss triggers (act before the incident)
- "It's basically done" — run `scripts/check_status_evidence.py STATUS.md --root .` before writing.
- "The test passed earlier" — re-run it now; a pass 3 hours ago is not a pass today.
- "Just copy last quarter's STATUS.md" — every claim must be re-verified this week.
- "The blocker will sort itself out" — name an owner and a date, or it is not BLOCKED, it is IN_PROGRESS.

## Verification checklist (all must pass before you finish)
- [ ] Every DONE entry has a runnable evidence pointer.
- [ ] No IN_PROGRESS entry is listed as DONE.
- [ ] FALSE_DONE claims are explicitly flagged and downgraded.
- [ ] BLOCKED entries name an owner and a concrete next question.
- [ ] Handoff notes tell the next agent what to retry first.
- [ ] `python3 scripts/check_status_evidence.py STATUS.md --root .` exits 0.

## Scripts
- `scripts/check_status_evidence.py` — offline, deterministic gate. A claim in DONE or
  VERIFIED without an evidence pointer that resolves to a non-empty file is downgraded to
  FALSE_DONE. Exit 0 = clean; 1 = findings; 2 = usage error.
- `scripts/check_status_evidence_test.py` — offline self-tests (good/bad STATUS fixtures).

## References
- Full procedure, decision table and worked examples: `references/honest-status-procedure.md`.
- Eval prompts with expected behaviour and failure signs: `references/EVALS.md`.
- Primary sources with URLs and retrieval dates: `references/SOURCES.md`.

## Related skills
- [shared-tree-git](../shared-tree-git/SKILL.md) — commit status with a task-id prefix.
