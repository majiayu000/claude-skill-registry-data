---
name: power
description: Use when starting any conversation in a repository that uses PWDEV Power - establishes how to find and apply Power skills before any response, including clarifying questions
---

# Using PWDEV Power

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill and do the
task you were given.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If there is even a 1% chance a skill applies to what you are doing, invoke it.

If a skill applies to your task, you do not have a choice. This is not negotiable, and you
cannot reason your way out of it.
</EXTREMELY-IMPORTANT>

## The rule

Invoke the relevant skill **before any response or action** — including clarifying questions,
reading files, or looking around the repository. If it turns out to be the wrong skill for the
situation, you can stop using it. You cannot skip checking.

Then say "Using [skill] to [purpose]" and follow it exactly. If it has a checklist, make one
todo per item.

## Which skill

Process skills set the approach; implementation skills carry it out. Process comes first.

| Situation | Skill |
|---|---|
| "Let's build X", any new behavior | `power-brainstorm`, then `power-plan` |
| An approved design needs decomposing | `power-plan` |
| An approved plan needs executing | `power-execute` |
| Writing any implementation code | `power-tdd` |
| A bug, test failure, or surprise | `power-debug` |
| About to claim something works | `power-verify` |
| Reviewing, or receiving a review | `power-review` |
| A requirement or a roadmap | `power-product` |
| Roadmap status, health, coverage, or next action | `power-roadmap-status` |
| A change of at most three files | `power-quick` |
| Starting isolated feature work | `power-worktree` |
| Implementation complete and green | `power-finish` |
| Running approved phases in parallel | `power-fleet` |
| Refactoring an existing skill with metrics | `power-skill-refactor` |

## Red flags

Each of these thoughts means stop — you are rationalizing:

| Thought | Reality |
|---|---|
| "This is just a simple question" | Questions are tasks. Check for a skill. |
| "I need more context first" | The skill check comes before clarifying questions. |
| "Let me look at the code first" | Skills tell you how to look. Check first. |
| "Let me gather information first" | Skills tell you how to gather it. |
| "This doesn't need a formal process" | If a skill exists, use it. |
| "I remember this skill" | Skills change. Read the current one. |
| "The skill is overkill here" | Simple things become complex. Use it. |
| "I'll just do this one small thing first" | Check before doing anything. |
| "I know what that means" | Knowing the concept is not applying the skill. |
| "This feels productive" | Undisciplined motion is what skills prevent. |

## Non-negotiables

Three rules survive every rationalization, because each exists to stop a specific failure that
has already happened:

- **No production code without a failing test first** (`power-tdd`).
- **No fix without root cause investigation first** (`power-debug`).
- **No success claim without running the command and reading its output** (`power-verify`).

## Runtime

You are exactly one runtime. Read the mapping for yours before dispatching anything:
`../../references/claude-tools.md`, `../../references/codex-tools.md`, or
`../../references/hermes-tools.md`.

## Precedence

Direct user instructions and repository governance files outrank skills, which outrank your
defaults. Skip a skill's workflow only when the human explicitly tells you to.
