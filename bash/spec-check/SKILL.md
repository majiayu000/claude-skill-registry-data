---
name: spec-check
description: Check a task against the project's specs before implementing it, and again before declaring it done. Produces the requirement table that the code-kit path guard requires before a lane writes code on a branch. Use at the start of any non-trivial task, or when checking code against the spec.
---

# Spec check

The project's specs are in the folder named by `docs.specs` in `.claude/code-kit.json`. The engineering principles are in `docs.principles`, and the plan in `docs.plan`. Open the config with the Read tool. A shell script that reads it works too, but one that could write to it waits for a person's approval.

## Steps

1. **Find the section.** The task should name its requirement IDs (`BOOK-4`, headings in the specs) or a spec section. If it doesn't, search the specs folder for the domain nouns. Read the whole section, not just the matching lines, plus every section it references.
2. **Read the principles.** Re-read the parts of `docs.principles` that apply: layers, ports and providers, events, testing and the rules for agents. Note this lane's layer rules from `layers` in the config.
3. **Make a checklist.** One line per requirement: behaviour, fields, error cases, permissions, states, tests.
4. **Compare with the code.** For each line, search for where it's implemented, then read what implements it: the functions and types the requirement touches, not every file around them.
5. **Report** as a table:

| Requirement | Status (done / partial / missing / conflicts) | Where | Note |
| ----------- | --------------------------------------------- | ----- | ---- |

6. **List questions** for the lead wherever the spec is missing, ambiguous, or contradicts the code or another spec. Don't resolve them by guessing.

## Output

The table, the questions, and a one-line recommendation: ready to implement, or blocked on questions.

**Save it** to `.claude/state/spec-check/<branch>.md`, with `/` in the branch name replaced by `_` (for example `lane_data-e2-s1.md`). The table must keep its `| Requirement |` header. A lane can't write code on a branch until this report exists, and the lead reads it when reviewing the pull request. If the recommendation is "blocked on questions", stop and ask the lead instead of writing code.
