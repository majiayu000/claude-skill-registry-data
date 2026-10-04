---
description: "Loads documents fully into the main agent's context so the agent can answer questions, summarize, or work with that content in subsequent turns. Use whenever the user wants to ingest, read, study, review, absorb, or pull in documents — especially when they say things like \"load these docs\", \"read all of these\", \"ingest this folder\", \"pull in these PDFs\", \"load all docs in X\", or paste a list of file paths/URLs and ask you to read them. Handles local files (text, code, markdown, PDFs, notebooks, images), entire folders (recursively), and remote URLs. The skill is single-turn — once the agent reports \"DONE\", it deactivates until the user invokes it again."
---
# Load Documents

The user wants documents pulled into your context window so you can work with them in later turns. Your job is to read every document they specified, completely, and then say "DONE".

## When the user gives you nothing

If the user invokes this skill without naming any documents, folders, or URLs, ask them what to load. Don't guess. One short question, then wait.

## What counts as "a document"

Anything the user points at:
- Local file paths (any type the `Read` tool supports — text, code, markdown, PDFs, notebooks, images)
- Folders / directories — read everything inside, recursively, with sensible filtering (see below)
- URLs — use `WebFetch` to retrieve and read the content

## Core rule: read it yourself, completely

**Never delegate reading to a subagent.** The whole point is that the content lands in *your* context so you can answer questions about it in later turns. A subagent's context is thrown away when it returns.

**Read every document end-to-end.** If a file is longer than what `Read` returns in one call (the tool defaults to 2000 lines and may truncate long lines), keep calling `Read` with `offset` advanced by the chunk size until you've covered the whole file. Don't stop at the first chunk and assume you've got the gist — the user is trusting you to actually have the full content available.

For PDFs longer than 10 pages, use the `pages` parameter to walk through page ranges (max 20 pages per call), continuing until the whole PDF is covered.

For URLs, `WebFetch` returns the content in one shot — you don't need to chunk, but if the response is clearly truncated (e.g., the page is enormous), note this honestly rather than pretending you got it all.

## Build a checklist before you start

Before reading anything, list every document you're about to load and track them with `TodoWrite`. One todo per document. Mark each one completed only after you've finished reading the *entire* file (all chunks, all pages). This is the mechanism that prevents you from losing track and skipping documents — without the checklist, partial reads slip through.

For folders: first list the folder contents (use `Glob` or `Bash ls`), apply the filtering rules below, then create one todo per file that survives the filter. The user should see the full list before you start reading so they can correct you if you've picked up the wrong scope.

## Folder filtering (sensible defaults)

When the user points at a folder, recursively include all files **except**:
- Hidden files and directories (anything starting with `.` — `.git/`, `.env`, `.DS_Store`, etc.)
- Dependency directories: `node_modules/`, `vendor/`, `venv/`, `.venv/`, `__pycache__/`, `dist/`, `build/`, `target/`, `out/`
- Lockfiles: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `poetry.lock`, `Gemfile.lock`, `composer.lock`, `go.sum`
- Binaries and large media that aren't meaningful as documents: `.exe`, `.dll`, `.so`, `.dylib`, `.zip`, `.tar`, `.gz`, `.mp4`, `.mov`, `.mp3`, `.wav`, `.iso`
- Anything the user's `.gitignore` would exclude, when one is present and obvious

If you're unsure whether to include something, include it — better to read an extra config file than to silently skip something the user wanted.

If the filtered file count is very large (say, 50+), tell the user the count *before* starting and ask if they want to narrow the scope. Loading 200 files into context is rarely what someone actually wants.

## Reading order

Read in a sensible order — usually the order the user listed them, or alphabetically for folders. If there's an obvious entry point (`README.md`, `index.md`, `_index.md`), read that first so the rest has context.

## When you're done

Once every checklist item is complete, respond with exactly `DONE` and nothing else. No summary, no recap, no "I've loaded N documents" — just `DONE`. The user will follow up in the next turn with what they actually want to do with the content; your job here is just confirmation that the load finished.

The "single-turn" nature of this skill means: after you say DONE, don't keep applying these instructions. If the user's next message is "what was in the third doc?", just answer normally from the context you now have — you're not re-running the load workflow.

## What to do if something fails

- **File not found / permission denied**: Note the failure in your response (instead of just "DONE") and list which files succeeded vs. failed. Don't pretend you read something you didn't.
- **URL fetch fails**: Same — be honest about which URLs loaded and which didn't.
- **Binary or unreadable file you couldn't filter out**: Skip it and mention it in your final message.

In any of these partial-failure cases, your final message should be the failure summary followed by `DONE` on its own line, so the user knows the skill has finished even though some items didn't load.
