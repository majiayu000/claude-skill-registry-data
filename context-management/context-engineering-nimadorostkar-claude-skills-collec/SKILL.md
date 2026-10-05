---
name: context-engineering
description: Use when managing what an LLM sees. Covers context-window budgeting, retrieval and compaction, memory across turns, tool-result pruning, and the failure modes that come from too much context rather than too little.
metadata:
  category: ai
  version: 1.0.0
  tags: [context, llm, memory, compaction, retrieval]
---

# Context Engineering

## Purpose

Decide what an LLM sees, and what it does not. Context is a finite budget with a nonlinear cost curve: more context is not more capability, and past a point it is actively less.

## When to Use

- Building an agent or assistant that runs over many turns.
- A model that performs worse as the conversation gets longer.
- Managing tool results, retrieved documents, or long files.
- Reducing token cost in a long-running system.

## Capabilities

- Context budgeting and allocation.
- Retrieval: putting the right thing in, not everything.
- Compaction and summarization of history.
- Memory: what persists across sessions, and in what form.
- Tool-result pruning and progressive disclosure.

## Inputs

- The task, and what information it genuinely requires.
- The context window and its cost.
- The failure symptom, if the system is degrading over long runs.

## Outputs

- A context budget with an allocation per component.
- A compaction strategy that preserves what matters.
- Measurably better performance on long tasks.

## Workflow

1. **Budget the window explicitly** — System prompt, tools, retrieved context, history, and the response all compete for the same space. Decide the allocation rather than letting history consume everything.
2. **Retrieve narrowly** — Ten highly relevant chunks outperform a hundred marginally relevant ones. Irrelevant context does not sit inertly; it distracts.
3. **Compact, do not truncate** — Dropping the oldest turns loses the decisions that explain the current state. Summarize the history into the facts and decisions that are still live.
4. **Prune tool results** — A tool returning 50 KB of JSON when the agent needs three fields is spending the budget on noise. Filter at the tool boundary.
5. **Disclose progressively** — Provide a file listing, not the files. Let the model request what it actually needs. This is how a large codebase fits in a small window.
6. **Externalize memory** — Long-lived state belongs in a file or a store the model can read and write, not in a conversation history that grows without bound.

## Best Practices

- Long context degrades attention. A model given 200,000 tokens of context often performs worse than the same model given the 5,000 tokens that mattered. Adding context is not free.
- Information in the middle of a long context is attended to least. Put the critical instruction at the start or the end, not buried in the middle.
- Compaction is lossy by design. Preserve the decisions, the constraints, and the unresolved questions; discard the exploration that led to them.
- A tool that returns raw API output is a context leak. Wrap it, select the fields, and return a summary with a way to fetch the detail.
- Cache the stable prefix. A system prompt and tool definitions that do not change should be cached rather than re-sent and re-processed each turn.
- Write important state to a file. A note the model writes and re-reads survives compaction; a fact buried in turn 12 does not.

## Examples

**Explicit context budget:**

```text
Window: 200,000 tokens. Allocation:

  System prompt + skill      4,000    stable, cached
  Tool definitions           3,000    stable, cached
  Working memory file        2,000    the agent's own notes, re-read each turn
  Retrieved context         20,000    top-k, re-retrieved per turn, not accumulated
  Conversation history      40,000    compacted when it exceeds this
  Tool results              30,000    pruned; only the most recent kept in full
  Reserve for response      16,000
                          --------
                           115,000    leaving deliberate headroom

Rules:
  - History exceeding 40k triggers compaction, not truncation.
  - Retrieved context is replaced each turn, never appended — otherwise it
    grows monotonically and crowds out everything else.
  - Tool results older than 3 turns are replaced by a one-line summary.
```

**Compaction that preserves what matters:**

```python
COMPACTION_PROMPT = """\
Summarize the conversation so far into a working state document. This summary
replaces the full history, so anything you omit is lost permanently.

Preserve:
- The user's goal and any constraints they stated.
- Decisions made, and the reason for each.
- Facts discovered (file paths, API shapes, error messages, values).
- What has been tried and failed, so it is not retried.
- Open questions and the current next step.

Discard:
- Exploration that led nowhere.
- Full file contents (keep the path and what was learned from it).
- Tool call mechanics and intermediate output.

Write it as a factual state document, not a narrative."""
```

**Progressive disclosure instead of loading everything:**

```python
# Wrong: 400 files, 2M tokens, does not fit and would not help if it did.
context = "\n".join(read(f) for f in repo.all_files())

# Right: give the model a map, and a tool to fetch what it decides it needs.
context = repo.tree(max_depth=3)          # ~2,000 tokens
tools = [read_file, grep, list_directory] # the model pulls what it needs
```

## Notes

- The "lost in the middle" effect is well-documented: retrieval accuracy for a fact placed in the middle of a long context is substantially lower than for the same fact at either end. Placement is not neutral.
- Prompt caching makes a large stable prefix cheap after the first call. It changes the economics of a long system prompt entirely — but only if the prefix is genuinely stable, byte for byte.
- The instinct to give the model more context is usually wrong. The instinct to give it *better* context is usually right.
