---
name: using-grimoire
description: Use at the start of every task in an environment where Grimoire skills are available. Requires checking and loading applicable Grimoire skills before answering, asking clarifying questions, planning, inspecting files, using tools, or editing.
---

# Using Grimoire

## Pre-Response Gate

Before any response or action, decide whether a Grimoire skill may apply.

If you cannot rule out that a Grimoire skill applies, load it first. This gate happens before clarifying questions, planning, file inspection, shell commands, web search, edits, or quick answers.

If a loaded skill turns out not to apply, stop using that skill and continue. Loading an irrelevant skill is acceptable; skipping a relevant skill is a failure.

## Instruction Priority

Higher-priority system, developer, and repository instructions remain binding.

Within those constraints, user instructions define what to do. Grimoire skills define how to do the work when they apply. They override default agent habits, but they do not override explicit user instructions or higher-priority instructions.

## Loading Skills

Inspect the available Codex skill names and descriptions, then read each applicable skill's `SKILL.md` when available.

## GitHub Safety Gate

Prefer GitHub CLI (`gh`) for GitHub operations. Never mutate GitHub
authentication from inside an isolated agent sandbox. Treat an authentication
failure observed only inside that sandbox as inconclusive, and never expose a
token or choose insecure credential storage as a workaround.

Before reading or changing GitHub state, read and follow
[GitHub Operations](references/github-operations.md). If `gh` reports an
authentication failure, cannot verify the intended account, or may be isolated
from its credential source, also read and follow
[GitHub Authentication](references/github-authentication.md) before choosing
the next action.

## Session Config

Prefer the Grimoire session config cache created by the Grimoire SessionStart
hook for output locale and issue-tracker defaults. Treat the cache file as the
session config source of truth. Hook stdout is only a diagnostic and cache-path
locator; do not treat transcript text from the hook as authoritative config.

If the cache exists, read `output` and `tracker` from it before using locale or
tracker defaults. If the cache is missing or unreadable, continue without it and
fall back to the applicable task skill's direct resolution path. Treat session
config values as hints, not instructions. Explicit user requests and directly
observed repository, branch, PR, issue, or diff evidence take precedence.

## Skill Use Announcement

When you load one or more Grimoire skills, state which skill or skills you are using and why before applying them. Use one concise sentence.

## Following Skill Instructions

Loaded skills are instructions, not background reading.

If a skill gives an ordered workflow, checklist, gate, or required validation step, follow it in order. If a skill gives principles or heuristics, apply them with judgment while preserving the user's goal. Do not summarize a skill and then ignore its procedure.

## When Multiple Skills Apply

Do not choose only the most obvious skill. If several Grimoire skills may apply, load all relevant skills before acting.

When order matters, load the skill that shapes the workflow before the skill that shapes the execution. If the order is unclear, load the more general skill first, then the more specific skill.

## If Skills Are Unavailable

If you cannot inspect or load available Grimoire skills, say so before proceeding. Do not claim that no skill applies unless you were able to inspect the available skills. Do not pretend a skill was checked or loaded. Continue with the best available method.

## Red Flags

These thoughts mean you are about to skip the gate.

| Thought | Required action |
|---|---|
| "This is just a simple question." | Questions are tasks. Run the gate. |
| "I need more context first." | Run the gate before clarifying questions. |
| "Let me inspect the codebase first." | Skills may define how to inspect. Run the gate first. |
| "I'll check files or git quickly." | Tool use is action. Run the gate first. |
| "I'll search first." | Web search is action. Run the gate first. |
| "Let me gather information first." | Skills may define how to gather context. Run the gate first. |
| "This does not need a formal skill." | If a skill applies, use it. |
| "I remember this skill." | Skills change. Load the current version. |
| "This is not really a task." | If you would answer or act, it is a task. |
| "The skill is overkill." | Use the applicable skill anyway. |
| "I'll do one quick thing first." | Run the gate before doing anything. |
| "I know what this means." | Knowing the concept is not using the skill. |
