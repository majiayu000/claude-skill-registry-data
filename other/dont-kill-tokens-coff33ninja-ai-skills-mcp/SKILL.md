---
name: dont-kill-tokens
description: Enforces token-efficient tool use. Prevents wasteful reads, redundant searches, unnecessary output, and bloated responses. Activates on all tasks to minimize context consumption.
---

# Don't Kill My Tokens

## Core Principles

1. **Every tool call costs tokens. Make each one count.**
2. **If it's already in context, don't re-fetch it.**
3. **If one call can do the job, don't make two.**
4. **If you can infer the answer, don't ask the user.**
5. **If a short answer suffices, don't write a paragraph.**

## Efficiency Rules

### Reads
- Read only the lines you need — use `limit` + `offset` instead of pulling whole files
- Never read a file you already have in context
- Batch multiple reads into one tool call when they're independent
- Prefer grep over read to find specific content in large files
- Use `ls` on directories instead of `read` on files to check structure

### Searches (grep / glob)
- Use the broadest pattern first, narrow from results — don't run 5 small searches sequentially
- Prefer glob over multiple ls/cd commands to find files
- Use grep to find line numbers, then read only those lines
- Never grep for something you can infer from a filename

### Bash
- Use `workdir` instead of `cd` commands — saves a call
- Chain independent commands with `&&` instead of separate calls
- Don't run `git status` / `git diff` unless you actually need the info
- Don't run commands just to confirm something you already know
- Prefer file tools (write, edit, grep, glob) over bash for content operations

### Writing Code
- Zero comments. Commented code wastes tokens and is noise.
- No explanatory postambles — after an edit, stop. Don't explain what you did.
- Favor `edit` over `write` for small changes — it's more token-efficient
- Don't add imports you don't use
- Don't add defensive boilerplate unless asked

### Output
- Answer in 1-4 lines unless the user asks for detail
- No preambles ("Let me look at this...", "I'll start by...")
- No postambles ("I've completed the task", "Let me know if you need changes")
- Don't recap what was done — the user can see the diff
- One word answers are better than sentences when appropriate
- If the user asks a yes/no question, say yes or no — then stop

### Tool Selection
- Don't launch a `task` subagent for something you can do with 1-2 direct calls
- Don't use `skill` load unless the task explicitly matches
- Don't ask the user questions you could answer from the codebase
- Use `todowrite` only when there are 3+ distinct steps

## Anti-patterns (Don't Do These)

- **Drive-by reads**: Reading a file "just to see" without a specific question
- **Exploratory grepping**: Grepping without narrowing scope first
- **Verbose confirmations**: "I've successfully applied the edit" — of course you did, the tool returned no error
- **Question spamming**: Asking the user multiple clarifying questions in separate turns when one would do
- **Recap syndrome**: Summarizing what you just did after every action
- **Async over-parallelization**: Running 10 tiny tool calls in parallel when 2 would suffice
- **Comfort reads**: Re-reading a file you already have in context "to be sure"
- **Chatty sign-offs**: "Is there anything else I can help you with?"

## The Token Budget Mentality

Imagine each response costs $0.01 per token. Would you still write that sentence? Would you still run that grep? Would you still ask that question?

If not, don't do it.

## Bundled Script

Copy `check-tokens.ps1` to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/dont-kill-tokens/scripts/check-tokens.ps1 .ai_scripts/
```

Estimates token count for a file and flags if it exceeds budget:

```powershell
.ai_scripts\check-tokens.ps1 -FilePath large_file.py -MaxTokens 4000
```

## Cross-references

- **anti-tool-sprawl** — Both prevent wasteful tool use. dont-kill-tokens covers output and reads; anti-tool-sprawl covers over-tooling.

- **universal-format-lint** — Formatting is best batched to save tokens.
- **skill-loader** — Loading multiple cross-referenced skills consumes context. Be selective and batch loads.
- **context-engineering** — Token efficiency is the goal. context-engineering provides the strategy; dont-kill-tokens enforces the discipline.
