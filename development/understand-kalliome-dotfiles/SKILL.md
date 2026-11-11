---
name: understand
description: Research a topic in the codebase thoroughly with subagents, split it into understandable chunks saved under .work/understand/<title>/, then teach it chunk by chunk with discussion. Default topic is the current PR (diff against main/master). Resumable across sessions. Use when the user says "understand", "explain this PR", "walk me through how X works", "how do we use <library>", "teach me <feature>", or wants to resume an understanding session.
argument-hint: "[topic | resume <title>]  (default: current PR)"
---

# Understand

Build a durable, chunked explanation of a topic and teach it interactively.
State lives in files so any agent can pick up the session later.

## Arguments

`$ARGUMENTS` is one of:

- **empty** → topic is the current change set (Step 1). If a session for the
  same branch already exists in `.work/understand/`, resume it instead.
- **`resume`** / **`continue`** (optionally with a title) → go to **Resume**.
- **anything else** → the topic: a feature ("how invoicing works"), a library
  ("how we use Prisma transactions"), a subsystem, a directory, a ticket ID.

## Step 1: Resolve the topic

**Default (current PR):**

```bash
git branch --show-current
git rev-parse --verify main 2>/dev/null || git rev-parse --verify master 2>/dev/null
```

- Feature branch with `main`/`master` → range `main...HEAD` (or `master`).
- On `main`/`master` → uncommitted changes, `git diff HEAD`.
- Gather `git log --oneline <range>`, `git diff --name-status <range>`, and
  the full diff. Also read the PR description if `gh pr view` works.

**Explicit topic:** locate the entry points yourself (grep/glob for the
feature name, library import sites, routes, components) so the research
briefs below are concrete.

Pick a `<title>`: kebab-case, short, stable. For the PR default use the
branch name. Session dir: `.work/understand/<title>/`.

## Step 2: Research with subagents

Do not read file after file yourself. Decompose the topic into 3–8
independent research slices and dispatch them **in one batch** of read-only
`scout` agents. Typical slices:

- Entry points and triggers (UI, routes, jobs, CLI) and how control reaches
  the code.
- Data model and persistence (schema, migrations, queries, invariants).
- Core logic / algorithms and the decisions encoded in them.
- Integration points (external libraries, services, other modules) and the
  contracts between them.
- Tests: what they pin down and what they reveal about intent.
- History: commit messages, ADRs, docs, related tickets — the *why*.
- For a PR: what changed vs. what already existed; risks and review focus.

Each brief must state: the topic, exact starting files/symbols, what
questions to answer, and that the output must cite `file:line` for every
claim and include short code excerpts for the load-bearing parts. Scouts skip
formatters, linters, and test suites.

Fill gaps yourself after the scouts return. If a scout's result is thin or
contradictory, re-dispatch that slice with a narrower brief.

## Step 3: Chunk it

Turn the research into **3–8 chunks** a reader can hold in their head, in the
order they should be learned:

1. Start from the outside in: what it is for and how you encounter it.
2. Then the main flow end to end.
3. Then the details, one concern per chunk (data model, edge cases,
   integrations, tests, history/decisions).
4. Last: open questions, risks, gotchas, and where to look next.

Chunk rules:

- One idea per chunk; if the summary needs "and also", split it.
- Every chunk names real code (`path:line`, function, route) so the reader
  can jump from prose to source.
- Include a mermaid diagram (sequence or flowchart) where a flow spans
  several files; skip for trivial chunks.
- Prefer short code excerpts over paraphrase for the load-bearing lines.
- Do not repeat: later chunks link back to earlier ones.

## Step 4: Write the session files

```
.work/understand/<title>/
  README.md          # overview, chunk index, current position, log
  01-<slug>.md       # chunk 1
  02-<slug>.md       # chunk 2
  ...
  research/          # raw scout outputs, one file per slice
```

**README.md** template:

```markdown
# Understand: <human title>

Topic: <what was asked, or "PR <branch> vs <base>">
Created: <date>   Repo: <path>   Branch: <branch>   Range: <range or n/a>

## Chunks
1. [<chunk title>](01-<slug>.md) — one-line summary
2. ...

## Position
Current chunk: 1
Status: not-started | explaining | discussing | done
Last updated: <ISO timestamp>

## Log
- <ISO timestamp> chunk 1 explained
- <ISO timestamp> chunk 1 discussed: <one-line what was asked / clarified>
```

**Chunk file** template:

```markdown
# <N>. <Chunk title>

**In one sentence:** ...

## Explanation
Prose + code excerpts + optional mermaid diagram.

## Key files
- `path:line` — role

## Discussion
(Q&A recorded during the session; empty until discussed)
```

Write all chunks **before** explaining anything. Commit nothing — `.work` is
never committed.

## Step 5: Explain and discuss, one chunk at a time

Loop from the chunk in `README.md → Position`:

1. Update `README.md` first: `Current chunk: N`, `Status: discussing`,
   timestamp, log line. Do all file and tool work for this chunk **before**
   presenting it.
2. Present the chunk as the visible text of your final reply: the
   one-sentence summary, the explanation, and the key files. The chunk text
   must be in the reply itself — not only in your thinking, not only in the
   chunk file, and never followed by more tool calls (the user only reliably
   sees the final reply). Never write "part N is above"; if you did not put
   the chunk in this reply, the user has not seen it. A chunk reply may
   exceed general brevity limits (use a TL;DR if the reply style asks for
   one). Do not dump every chunk at once.
3. End with: *"Questions on this, or move on to chunk N+1: <title>?"*
4. While the user asks questions:
   - Answer from the research; read more code if needed rather than guess.
   - Append each Q&A as a short entry under `## Discussion` in the chunk
     file. If the answer corrects the chunk, fix the explanation too.
   - Add a one-line entry to the README log.
5. When the user says next/continue/ok, advance `Current chunk` and repeat.
6. After the last chunk set `Status: done` and give a five-line recap of
   the whole topic.

The user may skip around ("jump to the tests chunk") — update the position
accordingly. A detour into other work is fine; the files hold the place.

## Resume

When resuming (explicit `resume`, or a matching session exists):

1. If no title given, list `.work/understand/*/README.md` with their
   position lines and ask which one (or pick the only one).
2. Read `README.md` and the current chunk file, including its Discussion.
3. Say in two lines where the session stands, then continue the loop at the
   current chunk. If status was `explaining`, re-present that chunk; if
   `discussing`, ask whether there are more questions or to move on.
4. If the code moved since `Last updated` (`git log --since`), say so and
   refresh affected chunks before continuing.

## Style

- Teach, don't summarise: explain the why behind each decision the code
  encodes, not just the what.
- Concrete over abstract: real names, real lines, real values.
- Keep each chunk explanation under ~60 lines of terminal output; the file
  can hold more detail than the spoken version.
- Never invent behaviour — every claim traces to a file the scouts or you
  read.
