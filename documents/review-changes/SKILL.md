---
name: review-changes
description: Reviews the tip commit of a given branch against Context7 documentation and best practices for the language(s) touched. Use when the user says "review the last commit on <branch>", "review changes", or asks for a docs-grounded review of a specific commit/branch.
---

# Review Changes

Reviews a branch's tip commit using live library/language docs from Context7
(via HTTP API) instead of training-data assumptions.

## Requirements

- `CONTEXT7_API_KEY` env var must be set. Find it in the root .env.local file. If missing, tell the user and stop.
- Target must be a git repo with the branch present locally (fetch if needed).

## Quick start

```
/review-changes <branch>
```

If no branch is given, ask which branch to review — never guess.

## Workflow

1. **Resolve the commit**
   - `git fetch origin <branch>` (best effort, ignore failure if no remote)
   - `git log -1 --format='%H %s' <branch>` — the tip commit to review
   - `git show --stat <branch>` and `git diff <branch>~1 <branch>` for the full diff

2. **Identify languages/libraries touched**
   - From changed file extensions (`.ts`/`.tsx` → TypeScript, `.py` → Python, etc.)
   - From import/require statements added in the diff, to spot specific libraries
     (e.g. `react-hook-form`, `sqlalchemy`, `strawberry-graphql`)

3. **Pull Context7 docs for each language/library identified**
   - Search: `GET https://context7.com/api/v2/libs/search?libraryName=<name>`
     header `Authorization: Bearer $CONTEXT7_API_KEY` → returns candidate `id`s
   - Fetch context: `GET https://context7.com/api/v2/context?libraryId=<id>&query=<natural-language-question-about-the-diff>&type=json`
   - Ask a targeted question per library, e.g. "recommended pattern for async
     SQLAlchemy session handling" rather than a generic one — better results.
   - Use `WebFetch` for both calls since no Context7 MCP tool is registered in
     this environment; if an MCP tool named `mcp__context7__*` ever appears via
     ToolSearch, prefer it over raw HTTP.

4. **Review the diff against fetched docs and this repo's CLAUDE.md rules**
   - Flag deviations from official library/language best practices, citing the
     specific Context7 snippet that contradicts the code.
   - Flag deviations from this repo's CLAUDE.md conventions (strict TS, no
     `any`, layer separation in the FastAPI backend, etc.) — these take
     priority over generic best practice when they conflict.
   - Skip nitpicks Prettier/Ruff/ESLint already enforce.

5. **Report inline in chat** (see Output format) — do not write a report file.

## Output format

```
## Review: <branch> @ <short-sha> — "<commit subject>"

### Findings
- [file:line] <issue> — <Context7-sourced recommendation, with library name>
- ...

### Clean
<one line confirming what's fine, or omit section if everything has findings>
```

If no issues found, say so plainly — don't invent filler findings.

## Notes

- This skill reviews **one commit** (the branch tip), not the whole branch
  history. If the user wants a full PR review across multiple commits,
  point them to the existing `code-review` or `review` skill instead.
- If Context7 returns no useful match for a library, fall back to the
  language-level docs (e.g. plain "typescript" or "python") rather than
  skipping the review entirely.
