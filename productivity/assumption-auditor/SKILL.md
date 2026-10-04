---
name: assumption-auditor
description: Use when Codex needs to identify hidden assumptions, stale or unverified facts, fragile premises, overclaims, inferred user preferences, or risky defaults before trusting a plan, answer, artifact, research claim, workflow, prompt, code change, or decision. Use for assumption audits, premise checks, "what are we assuming?", "could this be wrong?", "where might this be stale?", and pre-implementation or pre-decision reviews.
---

# Assumption Auditor

Expose the premises that could silently break the work. This skill is for auditing assumptions, not for doing the full plan, research, implementation, or adversarial QA pass.

## Workflow

1. State the claim or action being audited.
   - Name the answer, plan, artifact, decision, code change, or workflow that depends on assumptions.
   - If the target is unclear, audit the user's latest request and the intended next action.

2. Separate assumptions by type.
   - Facts: external, local, temporal, technical, legal, financial, medical, or source-derived.
   - Interpretations: what the user probably meant, which audience matters, which quality bar applies.
   - Environment: tools, paths, permissions, dependencies, credentials, services, model behavior, runtime state.
   - Design choices: defaults, priorities, tradeoffs, non-goals, compatibility expectations.
   - Success criteria: what counts as done, good, current, safe, or acceptable.

3. Rate each assumption.
   - Confidence: high / medium / low.
   - Blast radius: high / medium / low if the assumption is false.
   - Drift risk: stable / version-sensitive / time-sensitive.
   - Verification cost: cheap / moderate / expensive / impossible in this turn.

4. Decide the next treatment.
   - Verify now when confidence is low, blast radius is high, and verification is cheap.
   - Ask the user when the missing premise is a preference or decision boundary that cannot be inferred safely.
   - Proceed with a recorded assumption when the default is low-risk and reversible.
   - Route to `$uncertainty-router` when the main problem is choosing the cheapest verification path.
   - Route to `$codex-adversarial-qa` when the artifact needs hostile scenario testing, not just premise inspection.

5. Keep the audit compact.
   - Lead with the assumptions that could change the answer or work.
   - Do not list obvious background truths unless they affect risk.
   - Do not block execution on low-risk assumptions; record them and continue when the broader task calls for action.

## Output Shape

Use this structure unless the user requested another format:

- Audited target
- Critical assumptions
- Moderate assumptions
- Safe defaults / recorded assumptions
- Verification plan
- User question, only if needed

For tabular work, use columns:

`Assumption | Type | Confidence | Blast radius | Drift risk | Verification | Treatment`

## Stop Conditions

- Stop when the remaining uncertainty no longer changes the next action.
- Do not turn an assumption audit into a full implementation plan.
- Do not present unverified assumptions as confirmed facts.
- When using memory-derived facts without current verification, mark them as memory-derived and note stale risk when relevant.
