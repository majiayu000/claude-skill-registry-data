---
name: prototype
description: Build a small throwaway script to answer one concrete design or logic question before committing to an implementation. Trigger on:- prototype, spike this, will this approach work, try it before building, compare two approaches.
allowed-tools: Write, Bash
model: claude-sonnet-5
---

# Prototype

Reach for it mid-build, independent of the pipeline chain
(`.specify/memory/constitution.md`). A prototype answers one question, then gets deleted. It is not a draft of the real implementation.

## When to use this

Before writing production code, if you're not confident the approach works — or you're choosing between two approaches — spend a few minutes proving it with throwaway code instead of guessing or debugging it live in the real codebase.

Skip this for anything you're already confident about. Not every feature needs a prototype first.

## Steps

1. **State the question in one sentence.** e.g. "Does this refresh-token rotation logic handle concurrent requests correctly?" or "Can SQLite handle write concurrency at this scale?" If you can't state it in one sentence, narrow it further before writing code.

2. **Write the smallest script that answers it.** A standalone file, a REPL session, a script run with test data — whatever is fastest. Don't wire it into the real app, don't add error handling or config, don't make it reusable. It only has to run once and produce an answer.

3. **Run it, get the answer.** Yes/no, which option wins, or what the actual behaviour is.

4. **Write the answer down where the real work is happening** — a comment, a commit message, or directly in the task/brief tracking the work. One or two lines: the question and the answer. If the prototype produced a snippet worth keeping (a schema, a tricky bit of logic), copy just that into the real code.

5. **Delete the prototype.** It's done its job.

## What not to do

- Don't polish it — no tests, no cleanup, no making it production-ready
- Don't leave it in the repo "just in case"
- Don't skip step 4 — an unrecorded answer means re-deriving it next time the question comes up