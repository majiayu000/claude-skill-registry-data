---
name: explore-codebase
description: Build a mental map of an unfamiliar or large codebase — folder structure, entry points, architecture layers, data flow, conventions, build/test commands — and record it for future sessions. USE WHEN the user asks "explain this project/codebase", "how is this organised", "where is X handled", "walk me through", "onboard me", "what does this repo do", or before a big change in an area you haven't read yet.
---

# Explore codebase

Goal: an accurate, compact map (not a file dump) that answers "where do I look, and how do things fit together?" — and gets saved so the next session starts smarter.

## 1. Breadth first (cheap tools, in parallel)
- `list_dir` the root, then each top-level source folder one level deep. Note the layout style (feature folders vs layers, monorepo packages, framework conventions).
- Read the project's self-description: README, package manifest(s) (name, scripts, dependencies → stack), lockfile presence, `docs/`, `CONTRIBUTING`, `.github/workflows` (what CI runs), `Dockerfile`/compose, editor/tool configs (`tsconfig`, `pyproject`, lint config).
- Check the memory notes already saved for this project (they appear in the system prompt) — don't rediscover what is recorded; verify and update it instead.

## 2. Follow the execution paths
- Find the entry points: `main`, `index`, `app`, `server`, `cli`, framework bootstrap files, `activate()` for extensions, route tables. `read_file` them fully.
- Trace one request/command/screen end to end with `find_symbol` and `find_references`: entry → handler/controller → domain logic → data access/external calls → response. This single trace reveals the layering better than reading every file.
- Identify the core domain types/models and where state lives (db schema, stores, context providers).
- Spot cross-cutting pieces: config loading, logging, error handling, auth, dependency injection, event/message bus, background jobs.

## 3. Capture conventions
- Naming and file organisation, module boundaries (what imports what; check for barrel files or an architecture lint), error handling style, async patterns, testing style and location, formatting tools, commit conventions (`git log --oneline -20`).
- Commands that matter: install, dev, build, test (single test too), lint, release. Confirm them from scripts/Makefile/CI rather than guessing.

## 4. Produce the map
Answer in this shape (keep it scannable, ≤ ~60 lines for a mid-size repo):
```markdown
## What it is
One paragraph: purpose, stack, runtime(s).

## Layout
- `src/agent/` — the agent loop and tool orchestration (agentLoop.ts, subagents.ts)
- `src/ui/` — webview + VS Code integration
… (folder → responsibility, key files)

## How a request flows
entry → … → … (with file:line anchors)

## Key concepts
Domain terms and the types/files that define them.

## Conventions & commands
Build/test/lint commands; style rules; gotchas.

## Where to start for <the user's goal>
The 3–5 files to read first and why.
```
Use a mermaid diagram when there are ≥ 4 interacting components. Cite real paths (`path:line`), never invented ones.

## 5. Persist what's durable
- `memory_save` (project scope) the stack, layout summary, commands and gotchas — concise bullets, no secrets. Update stale notes rather than adding duplicates.
- If the user asked where to make a change, end with a concrete starting point and offer to continue with `design` or `implement`.

## Rules
- Prefer reading a few central files completely over skimming many; use line ranges on huge files.
- Say what you verified vs inferred. If something is unclear (e.g. two competing patterns), name both and which looks newer.
