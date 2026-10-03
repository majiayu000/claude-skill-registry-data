---
name: continuous-review
description: Pattern for running an independent, sandboxed agent that keeps auditing the main agent's generated code over the course of a session — not a one-off review, a recurring one. Use when a session is producing a lot of code quickly (a long autonomous build, a big feature list) and you want a standing check separate from the agent doing the writing, not instead of the normal correctness gate or /code-review.
---

# Continuous review

The correctness gate (`scripts/run-checks.sh`) catches mechanical issues.
`/code-review` and the swarm review pattern (`.claude/skills/swarm/SKILL.md`)
catch a single diff's logic/security/simplicity issues on demand. Neither is
designed to keep watching *while* a long session keeps producing more code —
by the time you remember to ask for a review, ten more features have landed on
top of what you meant to check.

This pattern closes that gap with `sandbox-auditor`
(`.claude/agents/sandbox-auditor.md`): an agent that runs in its own isolated
git worktree, so it can freely inspect and test the repository without any
risk of colliding with work still in progress on the main branch, and that
tracks its own scope between runs via a local git tag rather than relying on
conversation memory.

## When to use it

- A session is autonomously implementing a long list of features or fixes and
  you want an independent check running alongside it, not just at the end.
- You're delegating a large chunk of work (via `/swarm` or a big task list) and
  want assurance that nothing slipped through while you weren't watching every
  diff yourself.
- You want drift detection — not just "is this one diff correct" but "has
  anything violated a documented decision or invariant since I last checked."

Don't use it as a substitute for the correctness gate (still required before
any turn is "done") or for `/code-review` on a specific PR-sized diff you
actually want a thorough one-time pass on — this is for the in-between,
ongoing case.

## How to run it

**One-off audit of everything since the last check:**

```
/audit
```

(or, without the slash command, ask directly: "spawn the sandbox-auditor
agent to review what's changed since the last audit")

**Recurring, during a long autonomous session:**

```
/loop 15m /audit
```

Fifteen minutes is a reasonable default for a session that's actively
generating code continuously; lengthen it for slower-paced work. The loop
skill handles the actual recurring invocation — this skill and the agent are
what it calls each time.

## What you get back

A findings report scoped explicitly to "everything since commit X" (or "since
the beginning," on a first run), covering: whether the gate is currently
clean, correctness/security/simplicity issues in the new code, and anything
that drifted from a decision recorded in `.claude/knowledge-graph/`. An empty
findings list is a normal, good outcome — it means the audit ran and found
nothing, not that it didn't run.

## Why a worktree, and why a tag instead of memory

Isolation via `isolation: "worktree"` on the Agent tool means the auditor can
run the full test suite, check out arbitrary commits, and poke around without
any chance of stepping on files the main agent is mid-edit on. The git tag
(`sandbox-audit/last`, local-only, never pushed) is what lets a *stateless*
agent — one with no memory of prior runs — pick up exactly where the last run
left off. Don't replace the tag with an in-conversation note or a memory
entry; the whole point is that this keeps working correctly even across
sessions that share no context.
