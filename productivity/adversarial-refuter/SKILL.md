---
name: adversarial-refuter
description: Before accepting "done/ready", dispatches read-only refuters that try to KNOCK DOWN the claim against the disk/live source
---

> **Auto-Trigger:** On receiving a "ready/done/fixed/implemented" — your own or from a delegated agent/workflow/cron
> **Keywords:** "done", "ready", "finished", "fixed", "implemented", "verify", "are you sure", "refute"
> **Priority:** HIGH
> **Tools:** Task/Agent, Read, Glob, Grep, Bash
> **Related doctrine:** `rules/loop-maker-checker.md` (cross-model, read-only checker), `rules/learned-corrections.md` (LC-1).

# adversarial-refuter — refute before accepting

"Done" lies. Instead of trusting, dispatch sceptics whose **only mission is to prove the claim is FALSE**. Materializes the operator's deal #1 (LC-1) as multi-agent verification.

## Contract

**INPUT:** 1 falsifiable claim (a statement testable against the disk/live source).

**OUTPUT:** verdict — "survives" (no refuter managed to knock it down) or "refuted" (≥1 refuter proved it false, with the exact gap).

**EXIT CODES** (the claim becomes 1+ criterion of `done_gate.py` — the refuter runs the criterion and reports the raw result):

| Exit | Meaning |
|---|---|
| 0 | claim SURVIVES — criterion passed, no refutation found |
| 1 | claim REFUTED — criterion failed, the claim was false |
| 2 | claim not falsifiable / malformed criterion (rephrase before dispatching) |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| disk/live source cited in the claim | Reads (read-only) | real verification |
| `gotcha-memory` | Writes | records the strongest refutation attempted |
| `.hpp/evidence/` (HPP core, optional) | Writes | the strongest refutation as a run record: exit code + hashes, never output text |

## Process
1. **Phrase the claim** as a falsifiable statement (e.g. "file X exists and contains Y", "route /Z answers 200", "test T passes", "the deploy switched the backend").
2. **Dispatch N refuters** (N and the ceiling come from `concurrency` in the profile, default 2-3) — each one **read-only** (allowedTools: Read/Glob/Grep/read-only Bash). Prompt: *"Try to PROVE this claim is false against the disk/live source. Default = refuted if there is any doubt."*
3. **Distinct lenses** when the claim can fail in several ways (exists-on-disk / content-correct / endpoint-answers / test-runs / not-stale).
4. **Verdict:** accept **only if ALL refutation attempts fail**. Any successful refutation → **re-queue** the work with the exact gap.
5. **Record** the strongest refutation attempted (it becomes evidence + feeds `gotcha-memory`). With the HPP core, record it as a run, not as prose: `python -m hpp evidence run --id refute-<claim> -- <argv>`, where argv is the command that must pass for the claim to hold — exit 0 = the claim survived, 1 = refuted. The orchestrator runs it, not the read-only refuters: `run` writes a record.

## When NOT to Activate
- Trivial change already verified in the same reply (e.g. 1 line + test run and shown).
- When there is no source of truth to confront (subjective claim).
- No 2nd agent available → fall back to single-pass local verification (`verification-before-completion`).
- The claim is about the RETURN of 1 specific delegation (not a loose statement) → use the gate built into `delegate-with-handback`.

## Executed examples

```console
$ python -c "import os; print('claim sobrevive:', os.path.exists('ip_pii_linter.py') and 'self-test' in open('ip_pii_linter.py',encoding='utf-8').read())"
claim sobrevive: True
```
<!-- executed: 2026-10-30 · exit=0 -->
(claim: "ip_pii_linter.py exists and has a self-test" — the refutation attempt FAILED, the claim survives.)

```console
$ python -c "import os,sys; ok = os.path.exists('never-exists-at-all.py'); print('claim REFUTED (the file does not exist):', not ok); sys.exit(0 if ok else 1)"
claim REFUTED (the file does not exist): True
```
<!-- executed: 2026-10-30 · exit=1 -->
(claim: "never-exists-at-all.py exists" — the refutation SUCCEEDED; exit 1 = the claim was false.)

```console
$ python scripts/done_gate.py "python -c \"import os; assert os.path.exists('kit_assembler.py')\""
  [OK ] (exit 0) python -c "import os; assert os.path.exists('kit_assembler.py')"

DONE-GATE: DONE (1/1 criteria)
```
<!-- executed: 2026-10-30 · exit=0 -->
(the claim becomes a done_gate criterion — the mechanism shared with `delegate-with-handback`/`gated-improvement-proposal`.)

## Proof

```bash
python -c "import os,sys; sys.exit(0 if os.path.exists('SKILL.md') else 1)"
```
