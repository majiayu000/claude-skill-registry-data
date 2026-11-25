---
name: codegraph
description: Read and understand code in a repo through its pre-indexed CodeGraph knowledge graph instead of grepping and reading files — one call returns the relevant source, the call paths between symbols, and the blast radius of a change. Use for "explore this codebase", "how does X work", "how does X reach Y", "who calls X", "what breaks if I change X", "which tests cover these changes", and for reading any indexed file. Also use unprompted before any code search in a repo that has a .codegraph/ index.
---

# codegraph

Every repo under `~/git.work` is already indexed. **Do not run `init` or `index`** —
that is the user's call and costs minutes.

## The one rule

`codegraph_explore` is the tool. It answers "how does X work", a flow ("how does X
reach Y"), a survey of an area, *and* a plain file read. Reach for it first, and
reach for it again when the first answer is thin.

**Treat source it returns as already read.** Do not re-open those files with
`read`. Do not re-verify with `grep`. Explore *is* the pre-built index — a
grep/read loop only repeats work it already did.

**When an answer is incomplete, the fix is another `codegraph_explore` on the
uncovered area — not a fallback to grep or read.** Falling back early is the
single biggest waste: measured, a read loop after an explore costs more than the
explore saved.

## Respect the budget line

Every explore response ends with its own budget, e.g. *"Explore budget: 2 calls
for this project (975 files indexed). Each call covers ~6 files."* That number is
tuned to the repo. Obey it literally:

- Spend every remaining call on the **uncovered** area before considering `read`.
- When the budget is spent, **synthesize and answer.** Do not start a read sweep
  to reach completeness the budget did not buy.
- If the question genuinely spans more files than `calls × files-per-call`, it is
  too broad. Split it and answer the part that matters, or say which part is
  uncovered — do not silently fall back to reading 20 files.
- Explore also prints `... and N more files`. That is a scope signal, not an
  invitation to read them.

## Writing a good query

Explore ranks on the names you give it. Vague questions get vague answers, and a
vague answer is what tempts you back to grep.

- Name concrete symbols and files: `"SessionStore.refresh src/auth/session.ts token rotation"`
- Use qualified `Class.method` names when you know them.
- For a flow, name both ends: `"how does handleRequest reach executeQuery"`.
- To read a file, just name its path — you get line-numbered source back.

## What arrives without asking

One default explore already includes:

- **verbatim source** for the relevant symbols, grouped by file
- **call paths** between them, including callback / interface→impl hops grep cannot follow
- **blast radius** — what depends on each symbol
- **covering tests** — `tested via callers: ...` per symbol

So there is no separate callers, callees, impact, or symbol-search step. Asking
for those separately buys nothing and costs a round trip.

## The other two tools

- `codegraph_affected_tests(files)` — which tests cover a list of changed files.
  The one question explore cannot answer, because it takes a file list rather
  than a query. Use when reviewing a diff.
- `codegraph_status(action)` — `status` before the first query in an unfamiliar
  repo; `sync` when results look stale after a rebase or a batch of edits made
  outside this session. Pi does not run codegraph's file watcher, so the index
  does not auto-update here.

If `status` reports `reindexRecommended: true`, the index was built by an older
extraction engine and explore's coverage is below what the current build gives.
Tell the user and let them decide — never re-index on your own.

`structure_only: true` on explore gives a ~1 KB map with no source bodies. Use it
only to orient on a large unfamiliar area — the full mode is what answers
questions.

## Do not

- Do not grep or glob a repo before trying `codegraph_explore`.
- Do not `read` a file that explore already returned.
- Do not cap explore's output. It scales its own budget to the repo's file
  count; capping starves the answer without saving tokens.
- Do not delegate exploration to a sub-agent — the sub-agent reads files and
  codegraph becomes pure overhead. Answer directly.
- Do not run `init`, `index`, `uninit`, `install`, or `daemon`.
- Do not query from `~/git.work` itself unless you mean to search all repos at
  once; the root carries its own 20k-file graph. Pass `path` or `cd` into the repo.

## Tuning a noisy repo

If explore keeps surfacing scripts, fixtures, or vendored code over real source,
add a `codegraph.json` at the repo root — `deprioritize` drops paths in ranking
while keeping them findable, `exclude` removes them from the index:

```json
{ "deprioritize": ["scripts/", "optional-skills/"], "exclude": ["static/vendor/"] }
```

## Known trade-off

Explore cuts tokens *processed*, but its dense payloads stay resident in the
context window longer than many small grep results would. In a long session on a
small window, that footprint is real. It is still the cheaper path per answer.

## In Claude Code

Claude Code runs codegraph's own MCP server (`claude mcp add -s user codegraph -- codegraph serve --mcp`). It exposes only `mcp__codegraph__codegraph_explore`; every rule above applies to it unchanged. The other two tools become CLI calls through Bash:

| pi tool                    | Claude Code (Bash)                                                        |
| -------------------------- | ------------------------------------------------------------------------- |
| `codegraph_affected_tests` | `codegraph affected <files...> [-p <repo>]`                               |
| `codegraph_status`         | `codegraph status [<repo>]`, `codegraph sync [<repo>]`, `codegraph files` |

`serve --mcp` runs codegraph's file watcher, so the index stays current here and `sync` is rarely needed.
