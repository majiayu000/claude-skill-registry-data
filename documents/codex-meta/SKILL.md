---
name: "codex-meta"
description: "Use when the user wants to understand, design, or improve Codex itself: hooks, subagents, skills, AGENTS.md or PLANS.md guidance, config-aware workflow design, Codex docs navigation, or deciding when to use codex exec, the SDK, App Server, GitHub Action, or automation. Inspect the current local Codex setup before recommending repo- or machine-scoped changes."
---

# Codex Meta

Use this skill for Codex-system questions and docs-grounded workflow design.

Use it when the hard part is not just wording, but how Codex surfaces such as hooks, skills, subagents, or automations should be shaped and related.

Before recommending or editing Codex surfaces, read and follow [TERMS.md](TERMS.md). Use its surface names and state terms instead of vague workflow language.

Keep this file lean. Load deeper references only when they are actually needed:

- [references/codex-system.md](references/codex-system.md) for surface choice, hooks, subagents, memories, config, and grouped doc scaffolding
- [references/codex-programmatic.md](references/codex-programmatic.md) for `codex exec`, the SDK, App Server, GitHub Action, and embedded or CI Codex workflows
- [references/codex-local-state.md](references/codex-local-state.md) for privacy-safe self-inspection of local Codex sessions, rollouts, memories, logs, automations, and SQLite state

## Use this skill for

- hooks, subagents, skills, `AGENTS.md`, `PLANS.md`, and Codex workflow design
- prompting or documenting Codex-specific surfaces such as hooks, skills, subagents, or automations when the surface itself is the design question
- deciding what belongs in prompts versus Codex surfaces
- docs-guided recommendations about current Codex capabilities, surfaces, and setup
- deciding when a workflow should move into `codex exec`, the SDK, App Server, GitHub Action, or automation
- privacy-safe introspection of local Codex history and state when the task is about improving Codex using prior sessions, rollout artifacts, logs, memories, or automation state

## Core rules

### 1. Inspect live local context when the scope is local

Before recommending repo- or machine-scoped changes, inspect the relevant live setup instead of guessing from older context.

Start with:

- `~/.codex/config.toml`
- `~/.codex/hooks.json`
- `~/.codex/agents/*.toml`
- directly relevant local skills under `~/.codex/skills/`
- repo-local `AGENTS.md`, `PLANS.md`, or repo skills when the task is repository-scoped

### 2. Prefer the smallest safe surface

- Start by asking what the smallest safe change surface is.
- Decide whether the fix belongs in a prompt, `AGENTS.md`, a skill, a hook, config, a subagent, automation, or a programmatic Codex surface.
- If repeated prompt tweaks are not fixing the goal, step back and diagnose whether the real issue is surface choice, missing context, invocation shape, tool design, or evaluation.
- Keep durable behavior in the right layer instead of re-explaining it in ad hoc prompts.

### 2.5 Treat local `~/.codex` findings as approval-gated

- Anything derived from inspecting local `~/.codex` state is private by default.
- You may use local `~/.codex` artifacts for diagnosis, private analysis, or identifying possible patterns.
- Do not document new concepts, features, product behavior, or reusable guidance into this skill from local `~/.codex` evidence unless the user explicitly approves that documentation step.
- If local evidence suggests an interesting new concept or behavior, stop before editing public-bound skill content and ask for permission to promote that lesson into the skill.
- Prefer official OpenAI docs and other public sources for durable skill guidance. Treat local `~/.codex` evidence as a private hint or validation layer, not an automatic source for public documentation.

### 3. Keep hooks thin and pick the right Codex surface

- Hooks are for concise lifecycle context injection, light plumbing, or crisp objective guardrails.
- Do not use hooks as semantic planners, prompt classifiers, or hidden workflow engines.
- If nuanced judgment is required, prefer better model-facing instructions, better surface choice, better agent design, or a better evaluation loop.
- Once a surface is chosen, keep its prompt or instructions specific to that surface: hook text should be terse and objective, skill guidance should define one reusable job, subagent briefs should set ownership and proof expectations, and automation prompts should describe the durable task rather than the schedule.
- Use `$prompt-writing` when the surface is already chosen and you need to write or refine the model-facing prompt or instructions so they fit the intended goal, runtime, and terminology.
- Load [references/codex-system.md](references/codex-system.md) when the hard part is surface choice across hooks, `AGENTS.md`, skills, subagents, config, MCP, worktrees, memories, or automations.
- Load [references/codex-programmatic.md](references/codex-programmatic.md) when the hard part is `codex exec`, the SDK, App Server, GitHub Action, or Codex as infrastructure inside a larger system.

### 4. Use live docs only when facts may have drifted

Use live docs only when the recommendation depends on drift-sensitive facts such as:

- current model names or preferred families
- current Codex feature behavior
- newly released guides or docs that may supersede older local guidance

Prefer official OpenAI sources. If `$openai-docs` is available, prefer it. Use the local references above to keep the main skill small and load live docs only when the details are likely to have changed.

## Workflow

Choose the primary docs-and-surface question first. Keep the work anchored on setup, architecture, local context, and current docs.

### 1. Clarify the hard part

- surface choice across prompts, skills, hooks, subagents, config, memories, or automation
- surface-specific prompt shaping for hooks, skills, subagents, or automations
- programmatic Codex usage such as `codex exec`, the SDK, App Server, or GitHub Action
- privacy-safe learning from local rollouts, memories, logs, or automation state
- docs navigation or drift-sensitive Codex recommendations

### 2. Inspect the relevant local setup

- inspect the current local setup before recommending repository-scoped or machine-scoped changes
- use only the surfaces that materially change the recommendation
- keep incidental local context out of any public-bound guidance

### 3. Load the right reference

- Load [references/codex-system.md](references/codex-system.md) when the hard part is surface choice, hooks, subagents, config, memories, or doc-map guidance.
- Load [references/codex-programmatic.md](references/codex-programmatic.md) when the hard part is CI, structured automation, embedded Codex, custom clients, or Codex as infrastructure.
- Load [references/codex-local-state.md](references/codex-local-state.md) when the hard part is learning from local rollout artifacts, session files, memories, logs, automations, or SQLite state without leaking sensitive content.

### 4. Keep the recommendation surface-shaped

- Recommend the smallest durable surface that solves the problem.
- Separate architecture guidance from any follow-on artifact writing.
- If the surface is already chosen and you need to refine the model-facing prompt or instructions for that surface, hand that work to `$prompt-writing`.
- Keep the final recommendation concise enough that a later implementation, config edit, or prompt draft can pick it up cleanly.
