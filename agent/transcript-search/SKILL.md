---
name: transcript-search
description: "Use when you need to search past sessions, find what we decided about a topic, recall an earlier conversation, find where an agent discussed something, search agent history or transcripts, or work out which session mentioned a word, error or command. Covers thrum transcript search, show and reindex - count first, narrow, search with a small limit, read one window, delegate broad questions to a cheap sub-agent."
---

# Searching Past Sessions and Agent Transcripts

`thrum transcript` searches and reads the agent session transcripts on THIS box only. It talks to the local daemon;
there is no cross-peer search. It is a Pro feature.

## Workflow

1. Count first: `thrum transcript search --count <query>`. It prints a total and, while the count is exact, matches per
   agent, with no snippets.
2. Narrow with `--agent`, `--worktree`, `--since`, `--until`, `--runtime` or `--in`.
3. Search with a small limit: `thrum transcript search --limit 5 <query>`.
4. Read one or two windows only: `thrum transcript show <runtime>:<session>:<seq>`.
5. For a broad question, use the `history-search` skill: a cheap sub-agent runs steps 1-4 and returns a short cited
   answer. Never paste raw transcript text back into your own context.

Each hit prints as `agent · YYYY-MM-DD · runtime:session:seq · snippet`. Pass the `runtime:session:seq` to `show`.

## Scope

- With no scope flag the search covers your own agent.
- `--agent a,b` searches those agents. `--worktree w1,w2` searches sessions in those worktrees. `--all` searches every
  agent on this box. The three are mutually exclusive.
- When several agents share one worktree, each session is attributed to only one of them. `--worktree` finds all of
  those sessions; `--agent` may miss some. Use `--worktree` when an expected session does not appear.
- `--since` and `--until` take `7d`, `24h`, an RFC3339 time or `YYYY-MM-DD` (UTC; `--until` covers the whole day).
- `--runtime claude` (or `codex`, and so on) keeps one runtime. `--in prose` or `--in code` keeps only prose or only
  fenced code.
- `--by session` groups results by session. `--limit` defaults to 5; the maximum is 50.
- `--json` prints the full response and lifts the 8 KiB output cap.

## Query syntax

| You type | It means |
| --- | --- |
| `deploy rollback` | both words must appear (AND) |
| `"exact phrase"` | the exact words, no stemming |
| `-word` or `-"a phrase"` | exclude matches containing it |
| `a OR b` | either word; `a OR b c` means (a or b) and c |
| `migrat*` | any word starting with `migrat`; needs at least 2 characters before the `*` |

- Unquoted prose words are stemmed: `deploying` also finds `deployed`. Quote a word to match it exactly.
- Text from `--in code` is matched exactly, without stemming.
- A query is limited to 50 terms.
- A query starting with `-` needs `--` first: `thrum transcript search -- -flaky timeout`.
- A query needs at least one positive term; a query of only exclusions is refused.

## Show

`thrum transcript show <runtime>:<session>:<seq>` prints the entries around one hit; the hit itself is marked with
`>`. Defaults are 3 entries before, 3 after and 4000 bytes of text. `--before` and `--after` go up to 10 and
`--max-bytes` up to 16000. Larger values are clamped.

## Reading the output

- `N of TOTAL` is the number of hits shown out of all matches. A broad search (`--all`) counts exactly up to 1000
  matches and then reads `1000+`, meaning at least that many; no per-agent counts are printed then. `(output capped at
  8 KiB)` means some hits were dropped from the end; lower `--limit` or narrow the query.
- `(partial: index catching up...)` means the index is still catching up with new transcripts, so results may be
  incomplete. Retry later for a complete answer.
- `(many matches: newest first; add words to rank by relevance)` means the query is too broad to rank, so hits are
  listed newest first. Add words, quotes or filters.
- `session was pruned by retention` means that session's transcript is gone.

## Unavailable and refused

- `Transcript search requires a license: not entitled for this machine. Run 'thrum license activate' to enable it.`
  Tell the user. Do not retry.
- `transcript search: transcript search index not available` (reindex says `transcript reindex: ...`) or
  `transcript store unavailable` means the daemon is still starting, transcripts are disabled
  (`transcripts.enabled` is false), or the search index could not be opened. There is no fallback search. Tell the
  user; do not retry in a loop.

## Reindex

`thrum transcript reindex` rebuilds the search index in the background. It is rarely needed; searches report
`partial` until it finishes.
