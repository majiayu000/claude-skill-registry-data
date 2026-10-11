---
name: shallow-codebase-audit
description: "Run a fast, low-token UX/feature and easy-bug audit of a large unfamiliar codebase by fanning out scoped read-only workers under a strict finding-line contract, then verifying every claim against the cited lines before reporting."
---

# Shallow codebase audit

Goal: a high-yield "easy bugs + UX papercuts" pass over a repo too large to read
(hundreds of KB of source), in one session, without burning the context window.

Not for: deep security review, architecture critique, performance work.

## 1. Recon (cheap, ~2 calls)

- List the repo root and the main package directory. Note file sizes — they set
  the budget rule below.
- Read only the CLI/entrypoint surface: the argparse/commander/clap block, and
  any project `CLAUDE.md` / `AGENTS.md`. The context file is the highest-value
  read in the whole audit: it states what was *deliberately removed* and what
  the invariants are, which turns "is this stale?" into a checkable question.

Do not read a 60-170KB module. Ever. Grep, then read ±30 lines.

## 2. Fan out scoped workers

Split by surface, not by file count. A workable 5-way split for a Python
service with a web UI and a sidecar package:

1. CLI + launchers + destructive commands (reset/wipe) + lockfiles
2. Web UI: server, API, actions, frontend
3. Core loop: supervisor / orchestrator / agent / LLM client
4. State + config + persistence (sqlite, YAML, ticket/record parsing)
5. Any second-language sidecar and its cross-language protocol contract

Each brief MUST carry:

- **READ-ONLY**: no edits, no test runs, no formatters, no state-changing git.
- **Budget rule**: "these files are 40-170KB; NEVER read a whole file; grep
  first, read ±30 lines around each hit."
- **The greps to run** — give them explicitly, do not make the worker invent
  them. See §3.
- **Confirm before reporting**: every finding must be read at the cited line.
- **Output contract**, verbatim:

  ```
  Your final reply is ONLY a list of at most N findings, one per line,
  most severe first, in exactly this format:
  SEV | path:line | what is wrong (one sentence) | the fix (one short sentence)
  where SEV is high/med/low. Prefix the problem text with `UX:` when it is a
  usability issue rather than a defect.
  No preamble, no summary, no "consider adding tests".
  ```

- **Exclusions**: style nits, type hints, missing tests, speculation.
- For an auth/security sub-question, add: "If a check passes, do NOT report it —
  only report defects." Otherwise half the output is a list of things that
  are fine.

## 3. The high-yield grep set

Language-agnostic, in rough order of hit rate:

- `except Exception:\s*(pass|continue)` / bare `except:` / `catch {}` —
  swallowed failure. Rank by *what* is swallowed: a swallowed operator-input
  read or an index write is a real bug; a swallowed cosmetic call is not.
- Text-mode file I/O paired with manual byte-offset arithmetic — CRLF drift on
  Windows. Check writer newline mode against reader newline mode.
- `while True` — check the exit condition against empty/failed responses.
- HTTP/subprocess/socket calls without `timeout=` — and **asymmetry** between
  two sides of a protocol (one side has a timeout, the other doesn't).
- `.json()[`, `["choices"]`, `[0]` on external/model output — KeyError/IndexError.
- `sqlite3.connect`, per-statement commit inside a loop, multi-write ops with no
  enclosing transaction.
- `startswith(dir)` path containment without a trailing separator — sibling escape.
- `listen(`/`bind(` with no `'error'` handler.
- Token/secret interpolated into a URL or message that is then logged.
- Same value validated in one branch and not in the parallel branch
  (e.g. `int` path bounds-checked, `str.isdigit()` path not).

## 4. Stale-doc sweep — the cheapest findings in the repo

Cross-check documentation against the parser and the loader. These are almost
always present and almost always real:

- Every flag/subcommand named in help text, epilog examples, README, or launcher
  scripts → does it exist in the parser?
- Every example config → does it load? Grep for a "removed/rejected sections"
  list in the config loader and diff it against the example file's top-level keys.
- Destructive-command help text → does it match what the function actually
  deletes? (Compare the `--help` string, the docstring, and the delete list;
  they drift apart in that order.)
- Anything the project's `CLAUDE.md` says was removed → grep for it still being
  referenced.

## 5. Verify before you report

Non-negotiable. Workers hallucinate line numbers and mis-rank severity.

- Open the cited lines for every finding you intend to publish.
- For a two-sided bug (writer vs reader, frontend vs backend), read **both**
  sides — a claim about one half is not the bug.
- Correct workers' mechanism claims: e.g. "argparse falls through to
  `unhandled command`" is usually wrong, argparse rejects an unknown subcommand
  with `invalid choice` first. Report the real failure mode.
- Anything you could not open, publish tagged `[worker-reported]` or
  `[INFERENCE]`, or drop it.

## 6. Report shape

Two sections — **Real bugs**, **UX papercuts** — each line severity-ranked with
`path:line`, one-sentence mechanism, one-sentence fix. Then:

- A short "not worth acting on" section covering the deliberate fail-open sites
  you looked at and rejected. This proves coverage and stops the same finding
  coming back next audit.
- One ranked closing line: which two to fix first and why.

Do not open a PR or edit anything. Offer the fix; wait for the ask.
