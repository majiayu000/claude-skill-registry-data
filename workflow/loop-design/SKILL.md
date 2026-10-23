---
name: loop-design
description: "Use when an agent loop is about to be built or reviewed (fix until green, process a queue, keep a state healthy): is the goal decidable, who judges, what stops it. Not how to wire the loop; the native /loop and /goal own that."
---

# loop-design

Cross-cutting (`WORKFLOW.md` §2). A loop wraps feedback around a model that otherwise answers once. The
machine is good at closing the distance to a literal goal and has no way to doubt the goal. This block asks
two questions only: is the goal right, and will the loop run away. The mechanics of looping are the
platform's (`/loop`, `/goal`, `/schedule`, `references/claude-code-platform.md`) and are not restated.

## When
Before building a loop, and when an existing one spins, passes too easily or finished something wrong.

## Steps

### 1. Gate: four conditions, one miss is a veto
1. The task repeats, often enough to repay the build.
2. Verification can be automated.
3. The budget (tokens, time, CI minutes) can carry it.
4. The agent has tools that actually run the work and show the result.

Any miss: do the task by hand or another way. A repo with no tests and no lint guard does not deserve a
loop; the loop only amplifies its errors.

### 2. A decidable goal, with bounds
1. The exit condition is a yes or no that a command settles. "Make it good" is not one.
2. Pair it with what must not happen, or the loop satisfies the letter by breaking the spirit. Example:
   tests green AND no test deleted or weakened AND coverage not reduced.
3. Prefer an external reference over the agent's own assertion (a golden file, an upstream total).
   "All tests pass" can be gamed; a diff against a fixed reference is harder to.
4. Self-check: read the goal to someone outside the domain. Can they run one command and tell if it is
   met? If not, it is not decidable.

### 3. Plan, build, judge
- **Plan** writes the spec and the acceptance conditions as commands.
- **Build** implements and may not edit the acceptance conditions.
- **Judge** runs them independently and deterministically: CI, the test runner, a diff. Never the agent
  that did the fixing, and never "looks right".
- A cap on attempts, then a human. Three failed rounds usually mean the goal or the model of the problem is
  wrong, and more rounds will not fix that.

### 4. Review a loop: where it breaks
| Failure | Question |
|---|---|
| Spins | Can a machine judge the exit condition? |
| Self-grading | Is the judge the defendant? |
| Goodhart | Is there a boundary, or only a target? Could it delete the tests? |
| Wrong answer run to the end | Does anything depend on the agent asking mid-run? Settle every question before launch |
| Stale inputs | Are the notes and instructions it relies on current, and who maintains them? |

### 5. When one loop spans many sessions
A loop too long for one context window (an application built or migrated feature by feature) needs a session
protocol on top of the goal and the judge: an initializer and worker sessions, a task list that only a pass flag may
change, one feature per session, a re-check of an earlier pass before new work, a progress file and a clean tree at
exit: [`references/01-multi-session-harness.md`](./references/01-multi-session-harness.md).

### 6. Land it in stages
Run it once by hand, to find out how the judge decides; then as a skill or subagents; schedule it last.

## Output / checkpoint
No pipeline checkpoint. What it owes: a written decidable goal with its bounds, the named external judge,
the attempt cap, and the human who flips the last switch.

## Guardrails
- **The human flips the last switch**: merge, publication, anything whose failure cannot be afforded. A
  loop is the worker, never the acceptance officer.
- **The more a loop rewrites its own rules, the stricter the human review must be**, and it belongs before
  the action, not as a patch after. The target moves under a self-improving loop (Goodhart).
- Never let the loop edit its own acceptance conditions or the judge.
- Never use it for a one-off task or a plain timer.

## Origin
Mechanisms rewritten from the `loop-design-check` skill of the `ECC` collection (MIT), read 2026-10-02:
the four-condition gate, decidable goal with bounds, plan/build/judge with an independent judge, the
attempt cap and the human-keeps-the-last-switch line. Wording is ours. Left out: the cybernetic loop-type
taxonomy and the staging by cron, which the platform docs already cover. Not run on real work.

The multi-session protocol (`references/01-multi-session-harness.md`) was added 2026-10-20 from public descriptions of long-running coding harnesses and our own craft; no source text is taken. Provenance: [`references/origin.md`](./references/origin.md).
