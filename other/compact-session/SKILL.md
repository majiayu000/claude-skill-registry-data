---
name: compact-session
description: Summarize entire session and save to index as compact Q&A pairs
allowed-tools: mcp__cc-forever-mcp__store_memory
user-invocable: false
---

# Compact Session

## CRITICAL RULE

store_memory must be called EXACTLY ONCE. No retries. No corrections.

## Pre-call Checklist (ALL must be YES before calling store_memory)

- [ ] Identified ALL main topics (3-5)?
- [ ] Written summaries for EVERY topic?
- [ ] Combined ALL summaries into ONE content string?
- [ ] Displayed the complete content string?

## Process

1. List all main topics discussed in this session (3-5 topics)
2. For each topic, write: "Human: [question]\nAssistant: [answer]"
3. Concatenate all pairs with blank lines between them
4. Display the COMPLETE content string
5. Call store_memory ONCE with that complete string

## Format Example

Content string should look like:

    Human: How to setup CC-Forever?
    Assistant: Run /cc-forever:setup to configure.

    Human: What embedding models are available?
    Assistant: English (MiniLM), Multilingual (e5), Japanese (Ruri).

## store_memory Call

- content: The COMPLETE string containing ALL topic summaries
- project: current directory name
- tags: ["compact", "session-summary"]

## After Calling

Report: "Saved N topic summaries" and STOP. Do not call store_memory again.
