---
name: Trust Decay
description: Capture a confident agent claim (Phase 1) or resolve one as right/wrong (Phase 2) in vault/memory/TRUST_DECAY.md. Builds the longitudinal record of agent calibration over time. Pairs with /honesty-check (which should reduce Phase 1 frequency) and /diagnose (which surfaces causes that often reveal Phase 2 events).
---

# Trust Decay

The two-phase ledger that tracks confident agent claims and their eventual outcomes. See [[Cost of Confidence]] for the doctrine.

## When to use

### Phase 1 — Capture a confident claim

- An agent declared something "fixed", "tested", "verified", "complete", "deployed"
- The claim is unhedged or treated as ground truth
- The claim is consequential enough that being wrong about it would matter
- Triggered by Caddy on prompts like: "/trust-decay capture", "log this claim", "capture confidence", "agent claimed", "I claimed", "the agent said it was fixed", "another agent verified"

### Phase 2 — Resolve a claim

- A previously-captured claim has been confirmed (right) or revealed wrong
- The principal noticed a discrepancy between an earlier claim and reality
- Triggered by Caddy on prompts like: "/trust-decay resolve", "the bug came back", "that wasn't actually fixed", "trust event", "wrong claim", "confidence was wrong"

## How to execute

### Phase 1 — Capture

```markdown
## YYYY-MM-DD — {short claim summary}
**Claim:** "{the actual confident statement, verbatim}"
**Source:** {agent name or self}
**Context:** {what task, what session, what was being worked on}
**Verification stated:** {what the claimant said they verified, if anything}
**Status:** OPEN — awaiting outcome
```

Append to `vault/memory/TRUST_DECAY.md` under the "Open" section.

The principal can capture manually, OR `/honesty-check` (when wired) can auto-capture any unhedged confident claim it produces.

### Phase 2 — Resolve

When a previously-captured claim is proved or disproved:

1. Find the open entry in `vault/memory/TRUST_DECAY.md` matching the claim
2. Append resolution data:

```markdown
**Resolution (YYYY-MM-DD):** WRONG | PARTIALLY WRONG | CONFIRMED CORRECT
**Evidence:** {what surfaced the discrepancy — file/line/log/observation}
**Time-to-discovery:** {duration from claim to discovery}
**Trust-decay event:** YES | NO
**Pattern:** {one line — what category of mistake/correctness was this?}
```

3. Move the entry from the "Open" section to the "Resolved" section.

### Step 3 — Optional aggregate

If the principal asks for the trust trajectory, walk the ledger and compute:

```
Trust trajectory ({start date} → {end date}):
- Total claims captured: N
- Confirmed correct: M (X%)
- Wrong: P (Y%)
- Partially wrong: Q (Z%)

By category:
- Doc work: X/Y correct
- Infrastructure: ...
- Production fixes: ...

Recurring patterns:
- {pattern name}: occurred N times — promote to /diagnose checks?
```

This output becomes the basis for `/retro` analysis and feeds into the [[Common Failure Modes]] corpus.

## Why two phases

The pairing is the whole point. A confident claim with no resolution is just rhetoric. A wrong outcome with no original claim is just a bug. The pair — *confident claim, then disconfirmation* — is what measures calibration.

## Anti-patterns this prevents

- Forgetting that the agent claimed something was fixed three weeks ago when the same bug recurs (no audit trail)
- Treating every fresh occurrence of an old bug as new (no pattern detection)
- Letting agent confidence levels drift without a corrective signal (no calibration data)
- Blaming the agent in the moment without realizing it's the Nth time the same pattern has played out (no longitudinal context)

## What this skill is NOT

- **Not a punishment system.** The ledger calibrates the agent's claims against outcomes. It's measurement, not judgment.
- **Not adversarial.** Capturing a confident claim isn't accusing the agent of being wrong; it's noting what the agent said so the eventual outcome can pair with it.
- **Not the only place to track confidence.** [[Honesty Check]] is the agent-side discipline; [[Reading Agent Output Defensively]] is the principal-side discipline; this skill is the longitudinal data layer that makes both useful over time.

## Connects to

- [[Cost of Confidence]] — the doctrine note this skill instantiates
- [[Honesty Check]] — should reduce Phase 1 capture frequency over time (fewer unhedged claims = fewer entries to resolve later)
- [[Reading Agent Output Defensively]] — the principal-side pattern that often triggers a Phase 1 capture
- [[Common Failure Modes]] — sister corpus tracking layer-level failures rather than confidence-level failures
- `vault/memory/TRUST_DECAY.md` — the ledger file
- [Closing the Measurement Loop](../../docs/closing-the-measurement-loop.md) — the `Stop` hook that prompts a Phase 1 capture when a turn's confident claims went unrecorded
- `/retro` (forthcoming v0.3) — quarterly analysis that consumes this ledger
