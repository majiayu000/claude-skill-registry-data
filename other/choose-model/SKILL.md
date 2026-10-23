---
name: choose-model
description: "Use when writing a new agent or launching a one-off task and the model and reasoning budget have to be decided: Haiku for mechanical work, Sonnet by default, Opus for a gate or a judge, and the effort level for how hard it thinks."
---

# choose-model

Cross-cutting block (not a numbered pipeline step): applies every time an agent is created or a
one-off task is launched without a model already imposed.

**Two axes, not one.** The model decides what class of reasoning is available; the **effort level**
decides how much of it gets spent on this task. They are independent frontmatter fields and the
second one is the cheaper lever: raising a reader from Sonnet to Opus multiplies its cost on every
diff it will ever read, where `effort: xhigh` on the four agents whose verdict blocks a merge buys
depth exactly where being wrong is expensive. The available levels, the aliases and what each one
resolves to are in `references/claude-code-platform.md` §1 — read it there rather than trusting the
grid below to be current on model names. A cost figure shown by a dashboard or a tracker is an estimate
(usage times a price table), not a bill: a subscription or free tier has no per-request price, so read
spend limits as in `skills/spend-guard-fail-closed`.

## When
- While writing a new agent (`model:` and, where the verdict is hard to walk back, `effort:`).
- While launching a one-off task where the model isn't already set by an existing agent.
- When in doubt whether an existing agent is on the right model (over- or under-sized).
- When an agent is on the right model and still shallow: that is an effort decision, not a model
  one, and it is the case most often misdiagnosed as "we need Opus here".

## Steps

1. **Characterise the task**, not the agent's role:
   - Is it mechanical/repetitive (extraction, formatting, short summary, simple
     classification)? → **Haiku**.
   - Is it building work or normal reading (writing code, reviewing a diff, applying documented
     conventions)? → **Sonnet**, the default.
   - Is the verdict hard to walk back once taken (blocks a merge, decides between two
     architectures, judges with a fresh context and no immediate second chance)? → **Opus**.
2. **Check the cost of being wrong**, not just the apparent complexity: a task that looks simple
   but where an error is expensive to recover from (e.g. a gate that lets a bug through to
   production) moves up a tier rather than staying at the "perceived complexity" level.
3. **Never over-size out of reflex.** Opus everywhere is expensive and improves nothing on a
   mechanical task: over-sizing is a choice error too, not just under-sizing.
4. **Then set the effort level, separately — and leave it out by default.** An agent with no
   `effort:` **inherits the session's level**, which is the behaviour you want almost everywhere:
   the operator who ran the session at `xhigh` gets deeper readers for free, and the one who ran it
   cheap gets cheap readers. Declare a level only where the agent must **not** follow the session,
   and there are exactly two such cases. `effort: xhigh` where step 2 said the cost of being wrong
   is high — a gate, a security audit, an architecture verdict — so it stays deep even in a session
   someone ran cheap. And `effort: low` for a genuinely mechanical agent — a classifier, a router —
   which has no use for a deep session's budget and would otherwise burn it on a decision with one
   right answer. `max` is documented as prone to overthinking: test it on one case, keep it only if
   it demonstrably found what `xhigh` missed, never a default. **`effort: high` is almost always
   the wrong line to write.** It reads like a small improvement over omitting the field and is a
   different rule: a declared level overrides the session **in both directions**, so it caps a
   session the operator deliberately ran deeper. Write it only when capping is the actual intent,
   and say so in the same sentence.
5. **Write the reasoning down where the field cannot carry it.** `model:` is always declared, so a
   one-sentence note next to it is enough. `effort:` is usually absent, and an absent field cannot
   say whether it was decided or forgotten — an agent that needed a level and never got one reads
   identically to one where inheriting was the right answer. So the note says which: either
   "follows the session deliberately", or the reason for the level that overrides it.
6. **Know what actually wins at runtime.** For a subagent the model order is: the per-invocation
   `model` parameter, the agent file's `model:`, `CLAUDE_CODE_SUBAGENT_MODEL`, then the session's
   model — and `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` overrides all of it. An agent pinned to `opus`
   that came back reasoning like Sonnet is usually that variable, not a bad `model:` line. **Effort
   resolves on its own axis**: the frontmatter beats the session, and the environment variable
   beats the frontmatter — so an agent that ignores its own `effort: xhigh` is an environment
   question, not a file question (`references/claude-code-platform.md` §1).

## Output / checkpoint
The agent frontmatter's `model:` field is filled in, with a choice justifiable in one sentence
against the grid above, and `effort:` either declared with the same one-sentence justification or
deliberately omitted. For a one-off task with no dedicated agent, the model is chosen before
launching, not changed halfway through unless there's a strong signal (timeout, repeated
failure).

## Guardrails
- No rigid rule by agent name: an already "known" agent can change tier if the real nature of its
  work has changed.
- When in doubt between two tiers, take the lower one and move up only if a concrete failure
  justifies it: not the other way round. **The lower tier plus a higher effort level is the first
  move up**, not the next model.
- **Never pin a full model ID in a block.** Pin the alias. A hardcoded ID fails outright on a
  provider that doesn't carry it, where an alias degrades to the newest version that provider has
  — and this repo is meant to run on someone else's setup, which is exactly rule C applied to the
  frontmatter.

## Origin
Internal decision grid: characterisation by the nature of the task
(mechanical/building/hard-to-undo verdict) and by the cost of being wrong, not by perceived
complexity. No specific external source retained: several market model-routing frameworks exist,
but none was judged close enough to our stack/agent reality to be rewritten as-is; the grid above
is a synthesis of our own.

The **effort axis** (steps 4 and 6, and the "lower tier plus higher effort" guardrail) was added
2026-09-07: effort levels are a platform feature this block predated, and its absence had turned
the grid into a single-axis one, which is how "this reader is shallow" kept resolving to "put it on
Opus". Facts read the same day from `code.claude.com/docs/en/model-config` and stamped in
`references/claude-code-platform.md` §1 — the aliases and the per-model level lists live there, not
here, so this block doesn't have to be re-verified every time a model ships.

**Steps 4, 5 and 6 corrected 2026-09-07, same day.** The rewrite earlier that day said an omitted
`effort:` was "inherited (`high`, the default)", conflating two different facts: `high` is the
**session** default, while a subagent with no `effort:` inherits whatever the session is at.
Re-verified against code.claude.com/docs/en/sub-agents, and the correction matters because it
inverts a recommendation — the obvious-looking move of declaring `effort: high` on the eight
readers is not a small improvement on omitting it, it is a cap on any session the operator ran
deeper. What the corrected step asks for instead is the two narrow cases: `xhigh` where a verdict
must stay deep in a cheap session, and `low` where the agent is mechanical enough that a deep
session's budget is waste (`elrond`, the only one that qualifies today).
