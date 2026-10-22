---
name: check-loop
description: Refines implementation plans when they need adversarial architecture review, assumption checking, simplification, or evidence-backed consensus before implementation.
argument-hint: "[--quick] [plan-path]"
---

# Codex-reviewed plan refinement

## Overview

The orchestrator owns the plan. The configured Codex reviewer critiques it in one persistent read-only thread. `codex-invoke.mjs round` runs the loop mechanics: it builds every reviewer prompt, redacts secrets, sends the whole plan only once and a diff afterwards, numbers findings, keeps the decision ledger, suppresses repeats, detects stalls, enforces the round limit, and saves resumable state. The orchestrator checks evidence, decides, and edits the plan.

**Core principle:** No evidence, no blocking finding. A confident reviewer statement is still only a claim until the orchestrator checks its source.

**Shape of a run:** round 1 is the one broad review. Every later round only confirms the orchestrator's fixes and checks the changed text for regressions. A later round can raise a new blocker only for a regression in the diff or a VERIFIED critical defect round 1 missed; the runner records anything else as a nonblocking note.

## Input

`$ARGUMENTS` holds the plan path and an optional `--quick` flag. If the path is empty, use the plan active in the conversation or locate one in the working directory. Ask for the path only when no single plan can be identified.

`--quick` means one review pass: add `--max-rounds 1` to the first `round` call. Use it for small or low-risk plans.

Read the complete plan, the original user request, and the repository files needed to verify claims.

## Preflight

This skill runs on the session's current model and effort; it does not switch models.

**In pi:** pi does not substitute `${CLAUDE_PLUGIN_ROOT}`; replace it with the absolute path two directories above this SKILL.md. `$ARGUMENTS` is the text appended after `/skill:NAME`.

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" setup --cwd "$(pwd)"
```

Proceed only when setup reports `Status: ready`. The first round freezes the reviewer model, effort, and round limit for the whole run; an explicit model or effort that is unavailable or substituted fails the round rather than switching reviewers.

## Start or resume

Check for an existing review of this plan:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" report --cwd "$(pwd)" --artifact PLAN_PATH
```

- No review found, or the report shows a finished outcome: start a new run.
- `AWAITING ADJUDICATION (...)`: resume it. Adjudicate the listed findings from the run file, then continue with the next `round` call. Do not start over unless the user asks.

Start a new run by writing the original user request to a temporary file and calling:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" round \
  --cwd "$(pwd)" --kind plan --artifact PLAN_PATH \
  --request-file REQUEST_FILE [--new] [--max-rounds 1]
```

Add `--new` when a finished run exists. Do not paste protected content (`*.env*`, `*.secret*`, `*credentials*`, `**/secrets/**`) into the request or plan; the runner also redacts credential-shaped values from every payload and from its state file.

## The round result

Each `round` call prints one JSON object:

```json
{"status":0,"error":null,"round":1,"maxRounds":6,"next":"adjudicate","summary":"Round 1/6: 2 new blocker(s) (F1, F2), 3 note(s).","blockers":[...],"notes":[...],"unconfirmed":[],"questions":[],"reviewer":{"model":"...","effort":"..."},"runFile":"..."}
```

Show the user only the `summary` line per round. Do not narrate bookkeeping.

Act on `next`:

| `next` | Action |
|---|---|
| `adjudicate` | Adjudicate every blocker, edit the plan, call `round` with the adjudication. |
| `adjudicate-final` | Same, knowing this was the last round: fixes you apply now will be unreviewed unless the user approves a closeout round. |
| `stalled` | The same blockers survived two closure rounds, or a confirmed fix came back. Ask the user before adjudicating (see below). |
| `cap` | The round limit is reached with fixes applied but unreviewed. Ask the user (see below). |
| `done` | Finish with the report. |
| `retry` | The reviewer turn failed or timed out; nothing was recorded. Rerun the identical command once. If it fails again, stop and show the error. |

A nonzero exit or `status: 1` is never a review result and never approval. Malformed reviewer output also fails without recording anything.

## Adjudication

For every blocker in `blockers`:

1. Open the cited plan section or repository location. Re-run a cited command when safe and necessary.
2. Check that the evidence exists, is current, and supports the exact claim and failure condition.
3. Decide:
   - `ACCEPT`: verified, and the correction improves the plan.
   - `REJECT`: contradicted, unsupported, irrelevant, or preference-only.
   - `COUNTER`: verified concern, but a different correction is safer or simpler. Apply the orchestrator's alternative.
   - `WAIVE`: only when the user explicitly accepts the risk. Name the user's decision in the reason.

Blockers with a `priorDecision` are either fixes the reviewer says did not land (`reviewerNote` explains) or a one-time dispute of a rejection. Decide them again on the evidence.

Edit the plan once per round for all accepted and countered findings. Change only what each finding requires: no new defensive plumbing, no extra tests or sections the finding did not ask for. Prefer the smallest correct edit, and prefer removing complexity to adding it. Plans that grow every round give the reviewer more to find.

Write the decisions to a temporary JSON file and continue:

```json
{"decisions":[
  {"id":"F1","decision":"ACCEPT","reason":"plan.md:42 retries after capture; added an idempotency key to step 3."},
  {"id":"F2","decision":"REJECT","reason":"src/billing/charge.ts does not exist; the payment path is src/pay/capture.ts, which already dedupes."}
]}
```

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" round \
  --cwd "$(pwd)" --artifact PLAN_PATH --adjudication-file DECISIONS_FILE
```

The runner rejects a decision set that misses a pending ID, names an unknown one, or lacks a reason. It refuses to continue if you accepted a finding but did not change the plan. If every blocker is rejected or waived, the run converges without another reviewer turn.

`notes` (minor, INFERENCE, UNVERIFIED, or out of scope for a closure round) and `questions` never block. Answer a question by improving the plan only when the answer is verified and material.

### Example

The reviewer reports F4 `[critical] [VERIFIED]`: "The plan can double-charge customers", citing `src/billing/charge.ts:88`. The repository has no such file. Decision: `REJECT` with the reason "src/billing/charge.ts does not exist; the cited evidence cannot support the claim." The `critical` label does not override missing evidence.

## Asking the user

Ask only in these cases, with named options:

- **Stalled, or a verified blocker you cannot fix:** list the blocker IDs and titles, then offer *Keep fixing* (adjudicate normally), *Waive these risks* (adjudicate them as `WAIVE`), or *Stop here* (finish with the report and the status `BLOCKED — NOT APPROVED`).
- **Cap:** list the unconfirmed fix IDs, then offer *Run one closeout round* (`round --closeout`, which only confirms fixes and checks for regressions), *Accept as is* (finish with the report; the outcome stays `FIXES APPLIED — UNCONFIRMED`), or *Stop here*.

Never describe an unconfirmed or blocked result as approved, and never start a fresh `--new` run to get around the round limit.

If the user cancels, stop. The plan and run state stay as they are, and the next `/check-loop` on the same plan resumes the run. Report `CANCELLED — NOT APPROVED`.

## Final report

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" report --cwd "$(pwd)" --artifact PLAN_PATH
```

Show its output. Add at most two sentences of your own if something in it needs explaining. The plan file is the source of truth; the run file holds the full ledger.

## Common mistakes

| Mistake | Correct action |
|---|---|
| Accepting a finding because it is critical | Verify its evidence first. |
| Treating two-model agreement as proof | Inspect the cited source. |
| Blocking on a plausible race or edge case | Mark it inference until reproduced or directly supported. |
| Trusting a file:line without opening it | Read the current file and confirm line drift. |
| Fixing a finding with a new subsystem | Make the smallest edit that resolves the verified failure. |
| Hand-building reviewer prompts with `turn` | Use `round`; it owns prompts, diffs, and the ledger. |
| Asking Codex to rewrite the plan | The orchestrator owns plan decisions and edits. |

## Red flags

Stop adjudication when reasoning includes:

- "Codex probably checked it."
- "Better safe than sorry."
- "Both models agree."
- "The deadline means we should accept it."
- "The citation looks plausible."

Each phrase substitutes confidence or pressure for evidence. Verify before proceeding.
