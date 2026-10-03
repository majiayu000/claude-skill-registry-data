---
name: swarm
description: Patterns for fanning out work across multiple parallel agents instead of doing everything serially in the main thread. Use when a task is genuinely parallelizable — broad research, multi-angle review, independent implementations, or a hard problem worth solving more than one way — not as a default for everything.
---

# Swarming agents

Parallel agents win when the sub-tasks are **independent** (don't need each other's
output to start) and each is **substantial enough** that coordination overhead is
worth paying. For a single-file fix or a linear task, don't swarm — one agent doing it
directly is faster and simpler.

Four patterns cover almost everything this template needs. All of them rely on the
standard rule: batch independent `Agent` calls into one message so they actually run
in parallel, let background agents report back rather than guessing their results,
and only run in the foreground when you need the output before you can proceed.

## 1. Research swarm

**When:** a question spans multiple subsystems and no single grep/read pass will
answer it — e.g. "how does auth flow through this whole app," "what would break if we
removed X."

**How:** spawn one `Explore` (or `general-purpose` for judgment-heavy sub-questions)
agent per subsystem/angle, each with a narrow, self-contained question. Run them in
the background, in one batched message. Synthesize their reports yourself once they
land — don't just concatenate them.

```
Agent(subagent_type: "Explore", description: "Map auth middleware",
      prompt: "Where is auth enforced across HTTP routes in this repo? ...")
Agent(subagent_type: "Explore", description: "Map auth in the job queue",
      prompt: "Does the background job runner check auth/permissions anywhere? ...")
```

## 2. Review swarm

**When:** a diff is worth more than one lens before it ships — non-trivial features,
anything touching auth/data/money, or whenever you'd otherwise eyeball a diff and call
it done.

**How:** spawn `reviewer-correctness`, `reviewer-security`, and `reviewer-simplicity`
(`.claude/agents/`) in parallel over the *same* diff. Each stays in its lane by
design — don't ask one agent to cover all three lenses, that's what serial review
already does. Merge their findings yourself, dedupe overlaps, rank by severity. For a
maximal, cloud-billed version of this same idea across a whole PR, `/code-review
ultra` exists — this in-repo swarm is the free, always-available version for everyday
diffs.

## 3. Worktree implementation swarm

**When:** two or more features/fixes are truly independent (different files, no
shared state) and you want them done in parallel instead of one after another.

**How:** spawn one `implementer` agent per unit of work with `isolation: "worktree"`
so each gets its own git worktree and can't collide with the others mid-edit. Give
each a tight, self-contained scope. After they report back, review and merge each
worktree branch deliberately — don't auto-merge multiple worktrees without looking,
since independent-looking changes can still conflict semantically even when they
don't conflict textually.

## 4. Ensemble / competitive swarm

**When:** there's a genuinely hard problem with more than one plausible approach and
picking wrong is expensive — a tricky algorithm, a perf-sensitive path, an ambiguous
bug with multiple candidate root causes.

**How:** spawn 2–3 `implementer` (or `general-purpose`) agents with the *same*
problem statement but different constraints/strategies named explicitly in each
prompt (e.g. "optimize for readability," "optimize for allocation count," "assume the
input is adversarial"). Compare their results yourself — correctness first, then the
actual tradeoff you care about — and either pick the best one or merge ideas. Don't
present an ensemble as more "objective" than it is; you're still the one judging.

## What not to swarm

- A task with a genuinely linear dependency chain (step 2 needs step 1's output).
- Anything where the coordination/synthesis cost exceeds just doing it directly.
- Never swarm to avoid disagreeing with yourself — if you want a second opinion on a
  judgment call, ask the user, don't spin up an agent to rubber-stamp your first
  answer.
