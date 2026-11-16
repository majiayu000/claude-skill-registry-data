---
description: Compatibility redirect — the work `/issue` names is spread across four skills, so this one forwards. Invoke as `/issue <what to do> #<N>` and it runs `/plan`; with no number it names `/propose-issue` and stops. Kept because handoff blocks and muscle memory still say `/issue`.
---

`/issue` is the name four skills stand behind. Reading an issue is
`@.claude/skills/take-issue/SKILL.md`, which nothing but a skill calls; deciding
what happens to one is spread across `/task`, `/plan`, `/go` and
`/propose-issue`. So this name forwards on the one thing that distinguishes the
cases rather than unconditionally: whether the argument carries an issue number.

**With a `#<N>` in the argument:** load and follow
`@.claude/skills/plan/SKILL.md`, passing the argument through unchanged — prose,
number and all. Then say in one line that `/task` and `/go` take that same
argument: `/task` hands the plan-or-not call back to the agent, and `/go` skips
it.

`/plan` is the default of the three because it is what `/issue … #<N>` invoked
before the split, so it is what an operator typing the old name is expecting to
happen.

**With no number:** there is no issue to take, and the prose is an unfiled unit
of work. Name `@.claude/skills/propose-issue/SKILL.md` and stop rather than
running it — filing is the one of the four that writes to the tracker, so it is
the operator's call to make explicitly.

Do not act on the summary above — this file carries no procedure of its own
beyond the fork, and `/handle`'s Do-NOT names acting on a one-line summary of a
skill as the failure mode.

Adopting repos: the source's `.claude/skills/update-muthur/catalog.md` states
when this entry is worth taking.
