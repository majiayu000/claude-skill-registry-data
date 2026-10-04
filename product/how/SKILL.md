---
name: how
description: "Use for \"how does X work\", a walkthrough before changing something, and placement questions like \"where should this live\" or \"which package owns this\". Explains a subsystem, a feature flow, or a runtime path at the depth a senior engineer needs to start working in it. For why it's built that way, use why."
---

# How

Answer "how does X work?" by reading the code and explaining it at the level of a senior engineer onboarding onto that area. Enough to build a working mental model. Not annotated source.

## Step 1. Pin the question and size it

Work out what's being asked: a subsystem ("how does the rate limiter work"), a feature flow ("how do we bill on-demand usage"), an overview ("how is the auth service structured"), or a runtime trace ("what happens when a user submits the form").

If the scope is unclear, state your best reading and go. Don't ask. The human can redirect.

Then size it.

- **Simple.** One module, a small utility, a narrow question about one function. Explore and explain yourself in one pass. Go to step 2b.
- **Complex.** Several files or services, a cross-cutting feature, a full overview. Fan out explorers first. Go to step 2a.

When in doubt, call it simple. You can fan out later if you hit a wall.

## Step 2a. Explore (complex only)

Split the question into two to four angles, each a distinct slice so explorers don't repeat each other. For "how does the rate limiter work":

- Data model and state.
- Request path and enforcement.
- Config and metrics.

Narrow question, two explorers. Broad subsystem, up to four.

Spawn them all at once as read-only subagents, each with the base prompt from `references/explorer-prompt.md` plus its angle. Each one:

- Starts broad. Lists the relevant directories, searches for the key types and names.
- Follows the thread from an entry point through callers, callees, and data.
- Reads the code. No guessing from file names.
- Stops when it can describe the full path from input to output without hand-waving a step.
- Notes anything surprising or that a newcomer would get wrong.

They return structured findings: components, flow, files read, boundaries, the non-obvious, open questions. Overlap is fine. The explainer reconciles.

The main thread gets their summaries, not their raw reads. That's the point of sending them out.

## Step 2b. Explain directly (simple only)

Search and read the code yourself, then write the explanation in the format below. Skip to step 4.

## Step 3. Synthesize (complex only)

Spawn one read-only subagent with the prompt from `references/explainer-prompt.md`, all the explorer findings, and read-only access to check anything. It merges overlapping findings, settles contradictions by reading the code, and writes one explanation.

## Step 4. Present

Show the explanation. Light edits for clarity or context from the conversation are fine. Don't rewrite it. The explanation is the product.

Every sentence follows the writing rules. Short, one idea each, plain words, no em dashes, file paths where the reader needs to go look.

## Output format

Adapt to the question. Not every section every time.

**Overview.** One or two paragraphs. What it is, what it does, why it exists. Enough to decide whether to keep reading.

**Key concepts.** The types, services, or abstractions you need to follow the rest. Brief definitions, not a catalog.

**How it works.** The longest section. What triggers it, what happens step by step, where data goes, where decisions get made. Prose, not pseudocode. Name files and functions so the reader can go look. No code dumps unless a snippet is the point. A mermaid diagram when several components talk to each other or data changes shape through stages. Skip it when prose covers it.

**Where things live.** The files and directories someone needs to start working here. Not all of them.

**Gotchas.** Surprising behavior, historical leftovers, sharp edges. Skip the section if there aren't any.

## Placement questions

"Where should this live" and "which package owns this" are how questions with an opinion at the end. Run the same flow on the area, then answer with one recommendation and the reason. Name the obvious location, the one another agent would assume, unless there's a reason it's wrong that you can say out loud.
