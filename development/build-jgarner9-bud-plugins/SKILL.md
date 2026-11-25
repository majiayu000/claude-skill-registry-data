---
name: build
description: Building mode. How a coding task is worked so it costs few tokens and stays correct; one task per context, a spec before code, the code written by the cheapest coder that can follow the spec, and checks instead of reading. Use when starting to write, fix or change code, working an issue, or picking the next task. Not for explaining code or planning what to build.
---

# Building

Every tool call resends the whole conversation, so the cost of a task is the size of this context times the number of calls. Keep both small.

## One task per context

One issue, one context. When a task is committed, stop and tell Jason to `/clear` (or `/compact` when the next task needs what was learned) before the next one. A hook enforces it: after a commit, a prompt naming a different issue is refused until the context is cleared or compacted.

## The loop

1. **Read only what the task names.** The issue, then the files and lines it points at. A search across many files goes to the `Explore` agent, which returns conclusions, not file contents. Send independent tool calls in one turn.
2. **Decide, then write the spec.** Every decision and edge case is yours. The spec is what a coder needs and nothing else: the files to touch with line anchors, signatures, the behaviour as numbered rules, the exact error text, the tests, and the commands that must pass. Put it where the repo keeps such things, or in the brief when it is short.
3. **Rate what is left and hand it over.** Use the table. The brief is the spec's path, the files the coder may touch, and the checks. No history, no background.
4. **Check, don't read.** Run the repo's check yourself. Read the diff stat and the test names; read code only where no test can speak for it. Send corrections back to the same coder.
5. **Commit and move the issue**, then stop (see above).

| Rating | The coding that is left | Coder |
| --- | --- | --- |
| 0 | Under about 60 changed lines | Write it yourself: a coder costs more than it saves |
| 1–2 | One file, nothing existing to understand | `bud:coder`, model `haiku`, effort `low` |
| 3 | A few files, mechanical | `bud:coder`, `haiku`, `medium` |
| 4–5 | Several files, has to fit existing code | `bud:coder`, `sonnet`, `medium` |
| 6–7 | State, error paths, many callers | `bud:coder`, `sonnet`, `high` |
| 8+ | Concurrency, security, or the design is the work | Write it yourself |

Say the rating and the coder in one line before dispatching. A coder that fails the checks twice moves up one row.

## Load when the task needs it

- `bud:code-style`: before writing or reviewing code yourself.
- `bud:debugging`: a bug, a failing test or behaviour nobody expected.
- `bud:verify`: before saying anything is done or passing.
- `bud:tools`: finding code or looking up a library.
- `bud:release`: cutting a release.
