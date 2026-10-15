---
name: lean-context
description: Use to keep context lean. Read only what you need. Compress aggressively.
---

# Keeping the context window lean

Claude Code has a large context window, but every token you spend on noise is a token you cannot spend on reasoning. The cost of a sloppy investigation is silent: latency, money, and worse answers later in the same session.

## When to trigger
- The task involves exploring an unfamiliar codebase or a large file tree.
- You are about to `Read` a file over ~500 lines.
- You are running `WebFetch`, `WebSearch`, or an MCP tool whose output you cannot predict.
- The user asks "look across the repo" or "find every place that ...".
- You catch yourself about to dump a long file or command output into a response.

## Core strategy

Always narrow before you read.

1. **Use `Glob` first** to find the candidate files by name pattern.
2. **Use `Grep` next** with `output_mode: "files_with_matches"` or `"count"` to rank files by relevance.
3. **Then `Read` precisely**, with `offset` and `limit`, only the regions you need.

Reading the whole file is occasionally the right call - small configs, the entry point you are about to edit - but it should be a deliberate decision, not the default.

## Reading large files

- `Read` defaults to 2000 lines. For anything bigger, decide what you actually need.
- If the file is a log, `Grep` it with `-n` and `-C 5` to get matching lines plus context.
- If the file is source code, `Grep` for the symbol, then `Read` with `offset` set ~20 lines above the match and `limit` 80-150.
- Never `Read` a generated file (lock files, minified JS, vendored bundles) in full. Either skip it or grep for one specific thing.

## Subagents for noisy exploration

When you need to crawl a lot of files to answer one question, spawn a subagent and tell it to return a one-paragraph answer. The subagent burns its own context, not yours.

Good subagent prompts are narrow:

- "Find every place in `src/` that calls `legacyLogin` and report the file paths and a one-line description of each call site."
- "Read the three docx files in `./inputs/` and return a single bullet list of all section headings."

Bad: "Explore the repo and tell me about it." - the subagent has to make the same judgment calls you do.

## Web and MCP output

`WebFetch` already runs the page through a small model with your prompt, so phrase the prompt as a question, not "give me the page". Same for MCP tools that return large blobs - prefer tools that take a filter argument over tools that return everything.

If a tool returns a giant JSON dump, do not paste it back in chat. Save it to a file (or let the tool do that), then `Grep` or `Read` slices on demand.

## Not repeating content

- Do not quote large file regions back to the user. They have the file.
- Do not narrate "I'm now going to read X, then Y, then Z" before doing the reads - just do them in parallel and report the conclusion.
- Final summaries should reference file paths, not paste code, unless the exact text is load-bearing for the answer.

## Plan before bulk reads

If a task will require more than ~5 file reads, stop and write a short plan first:

1. What am I trying to learn?
2. Which files are most likely to answer it?
3. What is my stopping condition?

This prevents the "read 30 files, then realize I should have grep'd for one string" failure mode.

## When to read whole files

It is fine - sometimes correct - to read a whole file. Cases where it is the right move:

- The file is under ~300 lines and you are about to edit it.
- The file is the entry point and you need to understand its shape.
- The user explicitly pointed at it and asked "what does this do?".

Use judgment. The rule is "narrow by default", not "never read full files".

## Red flags

- You have read 10+ files and still do not know what you are looking for. Stop, write a plan.
- You are about to paste a 500-line file into the response. Don't.
- The same `Grep` query keeps coming back empty - you are searching the wrong tree. Step out a level and `Glob` to confirm the files exist.
- A subagent's response is itself thousands of lines. Re-prompt with a stricter output format.
- You are reading lock files, `node_modules/`, build output, or vendored dependencies. Filter them out with `Glob` exclusion patterns.
- Your last 10 tool calls were all `Read`. You are probably overshooting - switch to `Grep`.

## References

- `Glob`, `Grep`, `Read` tool docs in the system prompt.
- `document-handling` skill - the same "do not dump it into chat" rule applies after extraction.
- `using-memory` skill - persistent notes live in memory, not in scrollback.
