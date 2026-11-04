---
name: ideate
description: When Karan brings a new idea or feature, run frontier-level ideation - grill him one question at a time, spawn top-tier agent panels to stress the idea, then execute through a gated pipeline. Applies across ALL projects and repos.
---

# Ideate

Trigger: Karan proposes any new idea, feature, product direction, or "what if we..." in ANY repo. Do not just execute the idea. Do not answer ad hoc. Enter this flow.

## 1. Grill first (never skip)

Interview Karan about the idea one question at a time, /grilling style:
- One decision per message, your recommended answer stated first, then wait.
- Walk the decision tree: who is it for, what breaks without it, success metric, smallest honest version, what it displaces or conflicts with, why now.
- Look up facts yourself (repo, data, web); only decisions go to Karan.
- Stop when a shared understanding exists that you could hand to an implementer.

## 2. Panel of highest-tier agents (Fable-level)

Spawn 2-3 agents on the MOST capable model available in the session (forks of the top-tier model when possible so they inherit context), each with a distinct adversarial lens:
- The skeptic: why this fails, who will not use it, what is AI-slop about it.
- The builder: smallest excellent version, real effort estimate, seams in the existing code.
- The differentiator: what makes it a moat vs a feature any competitor copies in a week.
Synthesize the panel into a verdict: build now / build differently / park (with the reason). Present the verdict and the strongest dissent to Karan before any code.

## 3. Gated execution pipeline (the Case harness shape)

Once Karan approves, run: Implement -> gate -> Verify -> gate -> Review -> gate -> Close -> Retro.
- Implement: delegated agent in an isolated worktree, separate branch, writes code and tests.
- Verify: fresh-eyes agent (not the implementer) runs scenario tests against the spec.
- Review: principles + code-quality review by the top-tier reviewer (Fable role).
- Close: evidence check (CI green, claims verified), open PR; merge only per repo rules.
- Revision loop on failure: structured feedback to the SAME agent, max 2 cycles, then escalate to Karan instead of blind retry.
- Retro: one short paragraph on what the run teaches, recorded in the project log doc.

## Standing rules

- Announce model tier, exact version, and effort for every delegation.
- Fable-level (top-tier) agents for ideation and review; implementation tier matched to difficulty.
- Record everything in the project's running log doc for other collaborating models.
- This flow applies in every repo; adapt file names to the project, never the shape.
