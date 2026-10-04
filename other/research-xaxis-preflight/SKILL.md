---
name: research
description: Map an unfamiliar area of the codebase before changing it. Returns a distilled map — key files, real call flow, conventions, landmines — instead of raw file dumps. Use when starting work in code you don't already know, or when a question spans many files.
argument-hint: [area, file, or question]
context: fork
agent: "preflight:explorer"
---

Map this area and return a distilled map: $ARGUMENTS

Runs in a forked explorer context, so the reading happens here and only the map returns to the main conversation. Follow the explorer's method and return format.

## Scope

If the request names a specific area, map that. If it names a question ("how does auth work?"), answer the question and map only what supports the answer.

Anchor to what's actually there. If the request assumes something the code contradicts — a file that doesn't exist, a pattern that was replaced — lead with that contradiction. It is the most valuable thing you can return, and the caller is about to plan against a false premise.

## Before returning, cut

- Anything the caller can infer from a filename.
- Files you opened that turned out not to matter.
- Whole-file quotes. Cite `file:line` instead.
- Generated, vendored, and lockfile content.

The map should let someone plan a change without reopening the files you read. If it doesn't, it's too thin. If it reads like a transcript of your search, it's too thick.
