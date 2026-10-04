---
name: index-memory
description: Save conversation Q&A pairs to persistent memory for later retrieval
allowed-tools: mcp__cc-forever-mcp__store_memory
user-invocable: false
---

# Index Conversation to Memory

Save recent Q&A pairs to the index.

## Arguments

- If `$ARGUMENTS` is a number: save that many Q&A pairs
- If `$ARGUMENTS` is empty: save the most recent 1 Q&A pair

**Count:** $ARGUMENTS (default: 1)

## Steps

1. Identify the recent Q&A pairs (specified count)
2. Call store_memory with the formatted content

## Format

Content must be in this format:

    Human: User's question
    Assistant: Claude's response

For multiple pairs, concatenate them.

## Example Call

Call store_memory with:

- content: "Human: How do I use CC-Forever?\nAssistant: CC-Forever is a plugin for persistent conversation memory..."
- project: current directory name
- tags: ["manual-index"]

## Completion

Report the number of Q&A pairs saved.
