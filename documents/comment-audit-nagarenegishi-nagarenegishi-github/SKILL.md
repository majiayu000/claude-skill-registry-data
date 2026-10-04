---
name: comment-audit
description: >
  Audit the repository for comment coverage and bring under-commented source up
  to standard. Walks one file at a time, proposes comments per file for approval,
  and tracks progress to resume across sessions. Invoke with /comment-audit.
disable-model-invocation: true
---

# Comment Audit

Audit the repository for comment coverage and bring under-commented source up to standard. Resumable across sessions via a tracker.

## Comment standard

Documentation format: use the language's native doc-comment convention (C# `///`, Java `/** */`, Python docstrings, JavaScript/TypeScript JSDoc/TSDoc, Go `// Name ...`, Rust `///`; otherwise that language's accepted standard).

File header: a concise one or two line header stating what the file is in general, by role or category. Do not enumerate the specific types or functions it contains; generalize instead. No implementation detail.

Function comments: document every function with what it does, not how. Skip trivial, self-evident, or conventionally undocumented functions (getters, setters, obvious one-liners).

Inline comments: only where logic is complex or a decision is non-obvious. Explain the reason or key point, not the mechanics.

Style: concise but meaningful, written for a human in natural language. No filler, narration, or AI-tell phrasing. Never add a comment that only states the obvious.

Existing comments: do not modify or delete them. Adding is free. Changing an existing comment needs permission.

Consistency: if processed.json lists previously processed files, read 1–2 of them as style references and match their phrasing, voice, and level of detail. If none exist yet, follow the comment standard as written and let your choices set the precedent.

## Scope

Audit only human-written source code. Skip:
- dependencies and vendored code
- build and output artifacts
- generated code and migrations
- minified and lock files
- non-code files (data, docs, images, config)
- the `.claude/` directory

Prefer the version-control tracked file list, then apply these skips.

## Tracker

`.comment-audit/processed.json`. Create if missing: `{ "files": {} }`.

Each entry maps a repo-relative path to the ISO-8601 timestamp it was last resolved:
`{ "files": { "src/app/main.py": "2026-06-25T10:00:00Z" } }`

- No entry: process the file.
- Within 30 days: skip.
- Older than 30 days: re-check.

## Flow

1. Ensure the tracker exists.
2. List in-scope source files. Sort by path ascending for stable, resumable order.
3. Process one file at a time:
   a. If resolved within 30 days, skip.
   b. Read only this file. Check it against the comment standard.
   c. If it already meets the standard, change nothing and stamp it.
   d. If comments are missing, propose additions for this file and wait for approval.
   e. On approval, apply to this file only, then stamp it.
   f. If deferred, leave it unstamped so it recurs.
4. Continue until the list is exhausted or the user stops.

## Constraints

- Never load the whole codebase into context. One file at a time.
- Do not force comments onto files that already meet the standard.
