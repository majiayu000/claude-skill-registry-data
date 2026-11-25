---
name: agent-receipt
description: Create a compact, evidence-backed proof-of-work receipt for a completed AI agent run. Use when the user wants to summarize what an agent actually built, how long it took, what changed, tests run, interventions, deployment status, or skills used.
---

# Agent Receipt

1. Gather only evidence available in the current run/repo.
2. Never infer a passed test, deployment, duration, or intervention count. Use `unknown` instead.
3. Write a local JSON manifest with: project, agent, duration_minutes, interventions, files_changed, tests_passed, tests_total, verification, deployed, skills_used, and evidence.
4. Run `scripts/receipt.py <manifest> --out <public-result.json>`. The public result contains evidence hashes and counts, never raw evidence values.
5. Run `scripts/render.py <public-result.json> --svg <card.svg> [--png <card.png>]`.
6. Keep the source manifest and raw evidence local unless the user explicitly approves publishing selected evidence.
7. Publishing is a separate external action. Confirm destination and visibility immediately before uploading unless the current request already authorizes it.
