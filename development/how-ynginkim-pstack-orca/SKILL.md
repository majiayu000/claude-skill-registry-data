---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
disable-model-invocation: true
---

# How

> Names in backticks, such as `spawn-worker` and `find-sessions`, are capabilities, not commands. Read `../resolve-capability/SKILL.md` before the first step. It says how each one is done here and whether a worker on another agent can be started.

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

Every seat is read-only, and its brief says not to edit files. Read `~/.agents/skills/select-model/SKILL.md` and choose each seat's model and how to start it from it. Start every seat as the Subagents section of `../poteto-mode/SKILL.md` says, which also covers a missing `select-model`. The table says what each seat needs, not which model fills it. Pick each subagent's reasoning level and speed for the job, per that section.

| Seat | Kind | Needs | Count and diversity |
|---|---|---|---|
| Explorer | read | read-only | two to four, one per angle, all together. None in the simple case. |
| Explainer | prose and judgment | read-only | one. In the simple case it explores and explains alone. |

## 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. Spawn one explainer that explores and explains in one pass, built from `references/explainer-prompt.md` without the explorer-findings section. Go to step 4.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): go to step 2.

When in doubt, take the simple path.

## 2. Explore (complex only)

Decompose the question into 2 to 4 angles, each a distinct slice of the subsystem. Start all explorers at once, each with `references/explorer-prompt.md` and its angle filled in. A report a worker writes to a file goes under a scratch path, not `durable-store`.

## 3. Synthesize (complex only)

Once all explorers have returned, spawn one explainer with `references/explainer-prompt.md` and every explorer's findings filled in.

## 4. Present

Present the explainer's output. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Output format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
