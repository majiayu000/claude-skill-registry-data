---
name: astra-efficient-orchestration
description: Choose a cost-aware Codex agent route for Plus or Pro when the user explicitly asks to optimize multi-agent model usage without sacrificing quality.
---

# Astra Efficient Orchestration

Optimize the cost of a *completed, acceptable result*, not the price of an isolated call. Delegation requires user authorization and an environment that supports it; this skill never overrides higher-priority instructions. Model availability, effort labels, and plan allowances vary.

## Choose the route

- **Direct Astra:** Prefer for small tasks, tightly coupled work, hard-to-test changes, or when correctness and quality outweigh usage. Do not create an agent tree by default.
- **Small coordinator → Astra worker:** For a bounded but implementation-heavy product task with observable acceptance, a Luna `xhigh` coordinator (or Terra/Sol when QA is difficult) can hand the original brief to one Astra `low`/light worker. Keep that worker's implementation thread continuous for focused follow-ups. The coordinator runs browser/behavior checks, returns screenshots and concrete defects, and owns the final handoff. Do not make the coordinator dictate technical solutions or have a weak worker author the entire quality-critical experience.
- **Astra-led plan:** For an ambitious multi-step task, complex architecture, consequential integration, or unreliable QA, use Astra `xhigh` to plan and resolve high-judgment decisions. Then delegate only bounded execution when useful; the coordinator/worker roles may differ by phase. The user's observed success with an `xhigh` Astra root is a valid profile to preserve and compare, not a universal guarantee.

See [model-routing.md](references/model-routing.md) for tradeoffs and [usage-profiles.md](references/usage-profiles.md) for Plus/Pro boundaries.

## Run a delegated implementation

1. Give the capable worker the user's goal, product constraints, relevant paths/assets, and observable finish line. Preserve the user's wording and reference screenshots when possible; avoid speculative architecture or aesthetic micromanagement.
2. Keep one worker thread for related implementation and repairs while its context is useful. Split or reset only when context becomes a liability. Do not spawn roles merely to fill a diagram.
3. Let the worker implement and fix issues it encounters. Have the coordinator exercise the real result, capture relevant screenshots, and send only new defects/evidence for a focused follow-up. Assign essential verification explicitly; never skip required tests, safety review, or approvals to save usage.
4. Stop when acceptance passes or a material blocker requires a user decision. Finish the requested deliverable and report what was verified. Limit speculative polishing and repeated full-context reviews.

Use [task-packets.md](references/task-packets.md) for concise handoffs and [prompt-recipes.md](references/prompt-recipes.md) for copyable prompts.

## Calibrate claims

The attached article reports two visual builds where a small coordinator plus Astra implementer saved API-equivalent cost and time versus its tested alternatives. That is not a measurement of ChatGPT Plus/Pro quota, nor proof of general parity. Compare routes on your own tasks using [evaluation.md](references/evaluation.md) and [evals.json](assets/evals.json); record quality, completion, retries, latency, and visible usage. Source and caveats: [research-basis.md](references/research-basis.md).
