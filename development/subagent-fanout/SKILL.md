---
name: subagent-fanout
description: Delegate breadth — multi-file searches, independent investigations, noisy command output — to subagents with precise briefs, then verify their claims before acting on them. Use when locating an answer means reading more than ~4 files, when several unrelated investigations could run in parallel, or when raw output would flood the context needed for synthesis and edits. Not for a single known file or symbol lookup.
---

# subagent-fanout

Weak delegation looks like: reading twelve files inline to answer one "where is X handled" question, or sending an agent "look into auth" and getting back an essay you can't act on. Strong delegation spends subagent context on search and keeps main context for synthesis and edits.

## When to fan out

1. **Breadth, not depth:** "where is auth handled", "find every caller of X", "which configs mention Y". If locating the answer would mean reading more than ~4 files, delegate.
2. **Independent investigations in parallel:** three unrelated questions = three agents launched in one message, not a sequence.
3. **Noisy output:** a test run, log grep, or build whose 2,000 lines you'd skim for three — have the agent run it and return the three.

## When not to

4. **The single lookup.** If you know the file or symbol, one Grep/Read beats an agent round-trip.
5. **Work that needs your context:** judgment calls that depend on what the user said, or edits to code you've already reasoned about. Delegate finding; keep deciding.
6. **Already delegated.** Once an agent is searching, don't run the same search inline while waiting.

## The brief

A subagent has none of your context. Every brief states:

- **Goal** — the one question, phrased so it has a definite answer.
- **Scope** — directories or globs to search, and what to skip (generated code, vendored deps, tests unless asked).
- **Constraints** — read-only unless told otherwise: no edits, commits, or installs.
- **Return format** — e.g. "list of `file:line` + one-line role each, then a two-sentence conclusion; say 'not found' rather than guessing". Cap the length.
- **What you already know**, so it doesn't rediscover it.

If you can't write the return format, you don't yet know what you're asking.

## After it returns

7. **Verify at the point of use.** Before editing based on an agent's claim about a signature, call site, or behavior, Read the cited lines yourself (see workmanship). Agents can invent paths and line numbers; a cited `file:line` that doesn't exist invalidates that finding, not the whole report.
8. **Keep the conclusion, drop the transcript.** Record what you carry forward in one or two lines; don't paste the agent's full output into your reasoning.
9. **Attribute in the report.** A finding that came from a subagent and wasn't independently confirmed is labelled as such.
