---
name: workflow
description: Use to run a dynamic, goal-driven workflow — orchestrate a multi-step goal by composing skills, tools, and MCPs, with a quality gate and verification at each step. Trigger on "/workflow", "run the <name> workflow", "orchestrate X", or a multi-step recurring goal ("draft the investor update", "give me my morning brief"). Follows references/sops/dynamic-workflows.md and the wf-*.md cards. Respects the autonomy/cadence gate (auto on reversible/internal, draft-then-approve on external/regulated).
---

# Workflow — run a dynamic workflow

Orchestrate a goal end-to-end: **plan → route → compose skills/tools/MCPs → gate each step → verify → fail safe.** The engine for speed + quality. Pattern: `references/sops/dynamic-workflows.md`. Named workflows: `references/sops/wf-*.md`.

## How to run
1. **Resolve the goal.** Named workflow (`/workflow investor-update`) → load its `wf-*.md` card. Free-form goal → first run `/structure` to get Context · Outcome · Goal · Success criteria, then plan the steps.
2. **Check the autonomy gate per step.** Internal/reversible/no-PHI → may run unattended. External/irreversible/regulated → **stop and have the user approve** (draft-never-send; never to a sensitive recipient without approval).
3. **Execute step by step.** For each: run the action (a `/skill`, a `tools/*.py`, or an MCP call) → **run its gate/verify check** → **branch** on the result (e.g. missing data → flag + ask, don't guess). Reuse existing capabilities; don't rebuild.
4. **Fail safe.** On error: read it, retry/repair if trivial, else escalate to the user with what's blocked. Never silently drop a step.
5. **Verify done.** Confirm the success criteria are met (evidence, not assertion) before reporting complete.
6. **Deliver.** Internal → your sanctioned cloud / chat. External → draft to the user. Log meaningful decisions to `decisions/log.md`.

## Build / refine a workflow
New recurring multi-step goal that composes ≥2 capabilities and has a definable "done"? Author a `references/sops/wf-<name>.md` card (format in `dynamic-workflows.md`) and add it to the inventory. Don't workflow-ify one-offs (Simplicity). Don't overwrite a workflow card without asking.

## Guardrails
All of `CLAUDE.md`. Especially: the autonomy gate per step, quality gate before "done", cite-don't-invent, no confidential data persisted, draft-never-send external.
