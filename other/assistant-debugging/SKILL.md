---
name: assistant-debugging
description: "Diagnose an unknown failure by reproducing and isolating before fixing. Use for debugging, root causes, flaky tests, or unexplained breakage."
requires:
  - assistant-review
---

# Evidence-First Debugging

## Goal

Find and fix the real cause of a failure with the smallest durable change and
evidence that explains the symptom, cause, fix, and verification.

## Success Criteria

- The symptom and expected behavior are explicit.
- Reproduction evidence exists, or an exact blocker explains why it cannot.
- Competing hypotheses are tested and disconfirming evidence is retained.
- Root cause is supported by code, config, or runtime evidence.
- Verification covers the original failure path and a relevant regression check.
- When a repair can affect another consumer, record compact change-impact
  applicability evidence. Only shared, materially unresolved, or explicitly
  carried expanded repairs use the bounded artifact through verification;
  source fixes do not relabel a symptom-only assessment as completion evidence.

## Constraints

- Use local, company-safe diagnostics by default; redact secrets and private data.
- Ask before destructive, production-affecting, network, migration, or sensitive-data diagnostics.
- Do not patch from a guess or claim root cause when evidence supports only mitigation.
- Ask for missing context only when it materially blocks safe reproduction or isolation.

## Progressive Contract Loading

Canonical tier files are `contracts/input.yaml`, `contracts/output.yaml`,
`contracts/phase-gates.yaml`, and `contracts/handoffs.yaml`.

Read `contracts/index.yaml` first. Canonical contracts remain authoritative, but
load only the boundary currently being enforced:

- `entry` for symptom, scope, reproduction target, safety, and edit permission;
- `current_phase` for SCOPE, REPRODUCE, HYPOTHESIZE, ISOLATE, FIX, or VERIFY;
- `change_impact` when a diagnosis, repair, cosmetic, or locality claim affects consumer
  verification; and
- `selected_handoff` only when investigation or fix delegation is selected; and
- `completion` only for the artifact being returned.

If a selector is missing or invalid, load the full named canonical contract.
Do not load every contract at entry.

## Ownership

assistant-debugging owns diagnosis until the failure mechanism is reproducible
or bounded strongly enough for a fix. Generic workflow may coordinate planning,
delegation, and review, but specialist gates are authoritative.

## Method

1. **SCOPE** — capture symptom, expected behavior, affected path, recent changes,
   constraints, and severity.
2. **REPRODUCE** — run the smallest safe failing test/command or record the exact
   blocker with available log/code/config evidence.
3. **HYPOTHESIZE** — keep at least three plausible causes unless evidence
   justifies fewer. Rank by likelihood, diagnostic cost, and blast radius.
4. **ISOLATE** — run the cheapest high-signal check first. Track supporting and
   disconfirming evidence until one cause predicts the symptom and fix.
5. **FIX** — add a regression test when feasible, then make the smallest change
   that addresses the cause. Label uncertain emergency changes as mitigations.
6. **VERIFY** — rerun the reproduction, focused test, relevant regressions, and
   normal project checks. Skipped checks remain residual risk.

When change impact is triggered, load `references/change-impact.md`. The
common checker is resolved from the active installation, so standalone
debugging does not depend on assistant-workflow being installed.

Use `assistant-debugging` before `assistant-tdd` when a meaningful RED test
cannot yet be written. Once the mechanism is understood, hand the regression
test and evidence into the TDD cycle. Use `assistant-review` after non-trivial or
risky fixes.

## Output

Return status, symptom, reproduction or blocker, ranked hypotheses, root cause
and confidence, fix summary, verification results, and residual risks.

## Stop Rules

- Stop before speculative edits when the failure is neither reproduced nor bounded.
- Stop and ask before unsafe diagnostics.
- If every hypothesis is refuted, gather new evidence instead of cycling guesses.
- Use `mitigated` or `inconclusive` when proof is insufficient for root cause.
