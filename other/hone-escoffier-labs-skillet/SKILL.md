---
name: hone
version: 0.1.0
license: MIT
description: Use when a prompt, worker brief, or task description is about to be sent to another agent or model and should be deeper first, or the user says "sharpen this prompt", "hone this brief", "make this deeper, not bigger", or "improve this before I dispatch it".
---

# hone

A knife gets sharper, not bigger. A first-draft prompt usually asks for the obvious version of the task. This skill makes the prompt ask for what an expert would actually do, without growing the scope or taking decisions that belong to its author.

**Core principle:** deeper, not bigger. Do not run the task. Return a better prompt and the choices still open.

## Procedure

Take the prompt as written. Before rewriting it, answer four questions in a few lines each:

1. **The professional's move.** What would a top practitioner in this field do here that the prompt does not ask for? (A security reviewer traces data flow from the entry point; the prompt only said "look for bugs".)
2. **The rawest material.** What would they start from instead of something already digested for you? (The raw logs, not the summary; the source file, not the README; the original dataset, not the chart.)
3. **Methods and tools.** Which specific techniques and tools would they use, named concretely enough that a worker could run them?
4. **Independent proof.** What, other than the agent or the author, would show the result is right? (A failing-then-passing test, a reproducible command, a second source, a measurement against a baseline.)

Then rewrite the prompt so it asks for exactly that.

## Rewrite rules

- **Same task, more depth.** Keep the goal and scope. If a change would widen scope, list it under open choices instead.
- **Leave the author's decisions open.** Where the prompt has a real fork (which approach, which tradeoff, which audience, how much to spend), do not choose. List it.
- **Make the asks checkable.** Each added requirement should name an observable result, not an adjective ("rigorous", "thorough").
- **Keep the voice and constraints.** Preserve stated limits, output format, and anything the author fixed on purpose. Do not add ceremony, role-play preambles, or filler.
- **Do not run it.** No research, no code, no answers to the underlying task. If you need a fact to sharpen the prompt, say what to look up and leave it to the author.

## Output

```text
Four answers: <1-4, short>
Rewrite:
<the sharpened prompt, ready to send>
Open choices: <decisions left to the author, each with the options>
```

If the prompt is already specific, grounded in raw material, and names its own proof, say so and change nothing.

## Common mistakes

- Answering the task instead of improving the prompt.
- Making the prompt longer without making it deeper.
- Resolving a fork the author left open, such as choosing the framework or deleting a constraint.
- Adding "be thorough and think step by step" in place of a named method.
- Requesting proof that only the same agent can produce.
