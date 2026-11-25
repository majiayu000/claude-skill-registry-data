---
name: skill-battle
description: Run a credible with-skill versus without-skill evaluation for an Agent Skill, preserve evidence, and prepare a public-safe result. Use when the user asks whether a skill actually works, wants to benchmark a skill, compare a baseline with a skill, or generate proof for a skill claim.
---

# Skill Battle

## Default behavior

1. State one narrow claim the target skill should improve.
2. Choose representative tasks that measure that claim, not generic model quality.
3. Run identical tasks with and without the skill. Use multiple trials for stochastic tasks.
4. Prefer deterministic graders; use blind LLM judging only where necessary.
5. Track regressions, cost/time, token usage, and user burden alongside quality.
6. Keep full prompts, outputs, traces, and local artifacts **local by default**.
7. Use a train/held-out split if the skill or rubric is tuned during the experiment.
8. Never publish demo/synthetic numbers as benchmark results.
9. For multi-turn skills, simulate the same hidden user state in both conditions rather than flattening the workflow into one prompt.
10. Use the repository's sibling `skill-eval-loop` when available. It already enforces blind paired runs, skill-load checks, deterministic verification, and strict-majority adoption.

## Publication

Run locally first. Do not imply a cloud submission happened unless the configured Edge endpoint returned a canonical result identifier.

The default public record is **Results Only**: scores, deltas, exact model, skill and method hashes, counts, cost, latency and token aggregates, plus technical provenance. It excludes prompts, outputs, transcripts, private files, secrets, and proprietary instructions.

Before the first upload, disclose the destination and fields. Then offer optional sharing:

- `insights`: derived failure, improvement, and regression tags plus redacted findings
- `evidence`: selected raw or redacted benchmark inputs, outputs, grader traces, or transcripts

Never silently escalate disclosure.

## Trust

Treat trust and disclosure separately:

- Community → Reproduced → Attested → Edge Verified
- Results Only → Insights → Evidence

A Reproduced Results Only result is valid social evidence even when private prompts never leave the runner's machine.

Never invent a Battle URL. If no Edge publishing endpoint is configured, return the local evidence path and state that hosting remains pending.
