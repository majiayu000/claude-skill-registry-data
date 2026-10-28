---
name: docs
description: Write or update project documentation that matches the code — README, getting started, architecture overview, API/CLI reference, inline doc comments for public APIs, changelog entries. USE WHEN the user asks to "document", "write a README", "explain how this works" for others, "API docs", "update the docs", "changelog", or after a feature that changes how the project is used.
---

# Docs

Goal: documentation a new contributor or user can follow without asking anyone — and that is true, because it was checked against the code.

## 1. Find what exists and who reads it
- `file_search` for `README*`, `docs/**`, `CHANGELOG*`, `CONTRIBUTING*`, `*.mdx`, docs site config (Docusaurus/MkDocs/Jekyll/VitePress). Follow the existing structure, tone and formatting; don't create a parallel docs tree.
- Identify the audience for this piece: end user (how to use), developer (how it works / how to contribute), operator (how to run). Write for one at a time.

## 2. Get the facts from the code, not memory
- Commands and flags: read the package manifest scripts, CLI argument parser, Makefile, CI workflow. Run `--help` with `run_command` where possible and paste real output.
- Config: read where env vars/settings are parsed and list every one with type, default and purpose.
- API: read the route/handler/type definitions; document the actual request/response shapes and error codes.
- Architecture: `list_dir` the source tree; read entry points; describe the real modules and data flow (a small mermaid diagram helps).

## 3. Write
Structure for a README (adapt to what exists):
1. One-line description + badges (only ones that work)
2. Why / what it does (3–5 bullets, user benefits)
3. Quick start — the shortest path to a working result, copy-pasteable, tested
4. Usage — the common tasks with examples and expected output
5. Configuration — table of options
6. Project layout — folders with one-phrase purpose
7. Development — install, run, test, build, release
8. Troubleshooting / FAQ — real issues with fixes
9. License

Style: short sentences, second person ("run", "you"), one idea per paragraph, code blocks with language tags, relative links to files, headings in sentence case, no marketing fluff, no screenshots you can't produce (ask or skip).

Doc comments (public API only): what it does, parameters that aren't obvious, return/throws, one example if the usage isn't self-evident. Don't annotate private helpers or restate the code.

Changelog: Keep-a-Changelog format under `Unreleased` → Added / Changed / Fixed / Removed; one line per user-visible change, written for users.

## 4. Verify
- Run every command you wrote down (`run_command`) in a clean-ish state; fix the docs or the code when they disagree.
- Click/check every relative link exists (`file_search`). Render-check Markdown mentally for broken tables/fences.
- `get_diagnostics` if you edited code comments in typed languages.

## 5. Report
- Open the main page you wrote with `show_markdown` so the user can read it rendered, then list what was written/updated (files + sections), what you verified by running, and gaps you couldn't fill (e.g. needs a screenshot or a decision).
