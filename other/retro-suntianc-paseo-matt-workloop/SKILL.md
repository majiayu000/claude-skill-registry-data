---
name: retro
description: Review a session or a whole workloop run for recurring pitfalls and wasted effort. Output evidence-backed findings and suggested improvements for the user to decide; use when asked for retro or when assessing a completed run before archival.
---

# Retro

Find experience worth carrying into the next run. Output findings and suggestions; implementing them is a separate user decision. Save the retrospective when working on a run, but leave project files, rules, hooks and backlogs unchanged.

Read [writing-for-agents](../writing-for-agents/SKILL.md) when phrasing guidance for future agents. The [upstream retro](reference/upstream.md) is optional background for investigating a finding. Its advice to build checks is a possible recommendation here, not authorization to implement one.

## What to look for

Use these lenses rather than a mandatory checklist or score:

- **Recurring third-party failures:** dependencies, external APIs, tools or environments that keep failing. Look for confirmed limits and useful recovery methods.
- **Business pitfalls:** domain meanings, state transitions or edge cases repeatedly misunderstood.
- **Repeated wrong behavior:** losing context, recreating worktrees unnecessarily, duplicate dispatch or claiming completion before verification.
- **Repeated exploration:** rediscovering the same entry point, retrying ineffective approaches or repeating work whose answer was already available.

At run close, perform retro when evidence shows one of these patterns. A serious one-off event such as lost work or unauthorized action is also worth examining. A single ordinary review correction or successfully recovered transient error need not trigger it. Explicit user requests always get an assessment; no useful findings is a valid result.

## Read the evidence

Use the requested session or run; default to the current one. For a workloop run, cover the orchestrator's decisions and the executor/reviewer attempts, including replacements. Read the relevant conversation, reports, reviews, messages and events. Do not infer the process from the final summary alone.

When the [workloop-audit](../workloop-audit/SKILL.md) skill is installed, start a run's retro with `node <workloop-audit skill>/scripts/audit.mjs run <project>/<feature>`. It counts what the run's records show and flags what its rules expect but the records contradict. Answer every `check` flag in the retro, with its cause or why it was expected, and pass its reminder line, if it prints one, to the user. Without the skill, retro works as below.

`node <workloop skill>/scripts/workloop.mjs --run <run> evidence` saves child activity transcripts and their IDs under `evidence/`. Archived runs keep those files. CLI activity may curate tool output; return to original sessions when the precise output matters. State missing evidence or uncertainty rather than filling gaps with a guessed cause.

## Output

Keep each useful finding short: **what happened and its evidence → what would help → where that change belongs and why**. No fixed finding count or long template is needed.

Possible destinations:

- The project's agent instruction file (`Agent.md`, `AGENTS.md` or its actual convention) for a short, stable rule.
- A skill for a reusable workflow with several steps or decisions.
- A hook or script check for a reliably detectable mistake that can be blocked mechanically.
- A test for reproducible business behavior.
- Reference documentation for third-party limits and troubleshooting knowledge.

Choose the smallest useful improvement. Check whether it already exists or merely needs wiring up. Avoid turning a one-off workaround into a universal rule. Present the suggestions to the user without creating tickets, editing guidance or installing checks.

For a run, save the output with `WL retro --file <report>`. At normal close, if nothing warrants retro, use `WL retro --skip --reason "<brief reason>"`. `WL` is the workloop script with `--run <run>`; it records the result without applying suggestions. A mid-run assessment does not replace the assessment after `finish`.

After a completed run's assessment, `WL archive` can proceed without waiting for the user to choose improvements. Retro can be invoked again later using the retained evidence.
