---
name: finding-reconciliation
description: "Merge the independent A/B/C findings tables into one adjudicated ledger in `07-verification/documentation-verification-report.md` — normalizing to the finding schema, deduplicating by location and claim, recording per-finding corroboration without downgrading single-pass findings, promoting cross-pass disagreement to its own Critical finding, and splitting repairs into agent-repairable and owner-decision. Use when all three verification passes have returned their findings at Phase 9, or when ingesting an externally-produced audit. This skill MUST be consulted because publishing the findings table before repair is what makes the audit trail real, and because treating a lone dissenting pass as noise is exactly the correlated-error failure the three-pass design exists to prevent."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
agent: general-purpose
---

# Finding Reconciliation

Phase 9. Turns three independent findings tables into one adjudicated ledger, then drives repair and re-audit.

## Iron Law

**PUBLISH THE FINDINGS TABLE BEFORE ANY REPAIR, AND RE-AUDIT IN FRESH CONTEXTS AFTER. A finding seen by one pass is still a finding.**

A package that quietly fixes what it found and reports only the clean end state has destroyed its own audit trail. The pre-repair table is the evidence that verification happened.

## Never loaded by a verifier

This skill must not appear in any pass agent's `skills:` list. If a verifier could load the merge logic, it would reason about corroboration and drift toward the consensus it expects the other passes to reach — which is the correlated-error failure the whole three-pass architecture exists to prevent.

`tests/agent-independence.test.sh` enforces this mechanically. It is a structural guarantee, not a convention.

## Order of operations

1. **Collect raw.** Read each pass's table from `.dossier/runs/<id>/pass-{A,B,C}.md` verbatim. Do not edit, do not summarize, do not reorder.
2. **Normalize** to the canonical field set.
3. **Deduplicate** by `(location_normalized, claim_hash)`. Keep the highest severity. Merge the problem descriptions when they add different context — do not discard the second one's reasoning.
4. **Stamp corroboration** as `N/3`.
5. **Detect disagreement** and promote it.
6. **Publish the pre-repair table.** This is a commit point, not a draft.
7. **Split** into agent-repairable and `needs-owner`.
8. **Apply** the repairable ones, Critical and High first.
9. **Re-run** every check a correction touched.
10. **Re-audit** in fresh contexts when a correction materially changed architecture, product behaviour, data handling, security, reliability, or a public claim.

## Corroboration does not rank

`3/3` means three lenses independently saw it. `1/3` means one lens looked in the right place. Neither is a confidence score.

**A 1/3 finding is never downgraded for being lonely.** The passes have different lenses by design — pass C is the only one simulating a new engineer's first contribution, so a broken onboarding command *should* be 1/3, and it is no less real for that. Downgrading by vote count converts three specialized reviewers into a majority-vote committee and throws away the specialization.

Corroboration is recorded because it is useful when *ordering* repair work, and for no other purpose.

## Disagreement is its own finding

When two passes reach incompatible conclusions about the same claim — A says the evidence entails it, B says it does not — that is not a tie to break. It is a **Critical finding in its own right**, because the package contains a claim whose truth two independent reviewers could not agree on, and a reader will not do better.

Promote it, route it into the `CT-####` contradiction register, and resolve it with **evidence, not majority vote**. Two passes agreeing against one is not evidence; it is two passes.

## Resolve by evidence

When findings conflict, go back to the source. The adjudication records which evidence settled it and why. "Pass B was more thorough" is not an adjudication; it is a preference.

A finding you cannot adjudicate from available evidence becomes an `AQ-####` row with `needs-owner`, not a silent drop.

## Splitting repairs

| Class | Definition | Handling |
|---|---|---|
| **Agent-repairable** | The correction is a documentation change the evidence already supports | Apply it. Record the finding as `Corrected` |
| **Needs-owner** | Requires a business decision, legal interpretation, disclosure approval, risk acceptance, or evidence nobody has | Route to `AQ-`/`CT-`. **Blocks the gate** |
| **Blocked** | Correction is clear but the action ceiling forbids it | Record with the specific ceiling that blocks it |

`needs-owner` blocking the gate is deliberate. An unmade decision is a real reason a package is not release-ready, and hiding it behind a passing gate is the failure this package format exists to prevent.

## Repair without laundering

Applying a correction does not erase the finding. The row stays, its status becomes `Corrected`, and the correction is described. A reader must be able to see what was wrong, not only that it is now right — the trajectory is the diligence signal.

Never mark a finding `Corrected` because the affected sentence was deleted, unless deletion was the required correction. Removing the claim to clear the finding is laundering.

## When to re-audit

Re-run all three passes in fresh contexts when a correction materially changed architecture, product behaviour, data handling, security, reliability, or a public claim. Minor and clarity corrections do not require a full round.

Bounded by `verification.maxRounds`. On exhaustion, stop and report `conditionally ready` or `not ready` with the exact blockers — never `release-ready` with rounds remaining unrun, and never an unbounded loop.

## Output Format

Append a per-round section to `07-verification/documentation-verification-report.md`. **The pre-repair table is published before any edit and is never rewritten** — later rounds append, they do not revise history.

```markdown
## Round {n} — Pre-Repair Findings

Passes run: A, B, C · Independence tier: {in-plugin subagents | external model} · Models: {per pass}

| Finding | Required correction |
|---|---|
| **{id}** · {severity} · {N}/3 · dim {n} · `{location}`<br>{problem}<br>_Verifier evidence:_ {locator} | {exact change}<br>_Class:_ agent-repairable / needs-owner / blocked |

### Cross-pass disagreements
| ID | Claim | Pass positions | Adjudicating evidence | Outcome | CT row |
|---|---|---|---|---|---|

## Round {n} — Post-Repair

| Finding | Outcome |
|---|---|
| **{id}** · `{location}` | Corrected / Accepted risk / Blocked / Open<br>{what changed, or why it remains} |

### Round result
FINDINGS_TOTAL={n} CRITICAL={n} HIGH={n} CORRECTED={n} NEEDS_OWNER={n} BLOCKED={n}
RECHECKS_RUN={n} REAUDIT_REQUIRED={yes|no} SCORE_BEFORE={n} SCORE_AFTER={n}
```

## Rationalization Prevention

| Excuse | Response |
|--------|----------|
| "Only one pass flagged it, so it is probably noise" | The passes have different lenses. 1/3 is the expected count for a lens-specific defect. |
| "Two passes disagree, I will go with the majority" | Two is not evidence. Promote the disagreement to Critical and settle it from the source. |
| "I will fix these first, then write the report" | Then there is no evidence verification happened. The pre-repair table is the deliverable. |
| "The finding is gone because I deleted the sentence" | Deletion clears findings without fixing anything. Only correct if deletion was the required correction. |
| "This needs a legal decision, so it is out of scope" | It is `needs-owner`, it is in the report, and it blocks the gate. Not out of scope — unresolved. |
| "Round 3 hit the limit but it is basically fine" | Then it is `conditionally ready` with named blockers. `release-ready` requires the gate, not a feeling. |
| "The corrections were small, no re-audit needed" | Did any touch architecture, data, security, reliability, or a public claim? Then re-audit. |
| "Pass B was clearly more careful" | Which evidence settled it? If you cannot name it, you have not adjudicated. |

## Integration

Invoked by `/dossier:reconcile` after `/dossier:audit` returns, and when ingesting an external audit via `--findings <path>`. Routes unresolvable items to `gap-and-contradiction-register`. Hands the adjudicated ledger to `scoring-and-release-gate`, which alone issues the verdict.

References: `references/finding-schema.md`, `references/independent-audit-protocol.md`, `references/register-schemas.md`.
