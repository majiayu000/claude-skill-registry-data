---
name: experiment-advisor
description: >
  Given a research goal, use existing skills, training reports, and references
  to propose a small, concrete experiment plan.
metadata:
  short-description: "Plan next experiments using past knowledge"
---

# Skill: experiment-advisor

## When to use

Use this skill when:
- The user message starts with `<advise>`, or
- The user clearly asks "What should we try next?" in an experiment context.

## Inputs

- User goal (including constraints like run budget, hardware).
- Optional references to files (configs, reports, logs) mentioned in the goal.

## Behavior

1. **Understand the goal**
   - Parse which models, datasets, tasks, and constraints are involved.
   - If unclear, ask a concise clarifying question.

2. **Gather context**
   - Scan `.codex/skills/` for **relevant result skills**:
     - Matching models, datasets, or task types.
   - Read relevant `training_reports/*.md`:
     - Start with the most recent ones that mention these models/datasets.
   - Skim the last few days of `references/experiment-log.md`.
   - If the goal mentions an error, look up matching patterns in
     `references/troubleshooting.md`.

3. **Propose a plan**
   - Design **2–5 experiments**, each with:
     - Input data selection (possibly mixtures).
     - Model / architecture details (at a high level).
     - Key hyperparameters (LR, batch size, epochs, etc.).
     - Any relevant variation (e.g. different mixture ratios).
   - Respect run/hardware constraints.
   - When applicable, **reuse defaults** from existing skills instead of inventing new ones.

4. **Output format**
   - Start with a short natural-language summary.
   - Then provide a markdown table with the experiments:

     | id | description | key_differences | notes |
     |----|-------------|-----------------|-------|

   - Optionally propose file paths for configs or reports to create.
   - If errors were mentioned, explicitly call out how this plan avoids
     known failure patterns from `troubleshooting.md`.

5. **Logging**
   - When useful, append a short entry to `references/experiment-log.md`
     summarizing the newly proposed plan (only if the user agrees).
   - Include a short "General description" line in the entry for non-technical
     context.
