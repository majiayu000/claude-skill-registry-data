---
name: year-in-ai
tier: D
category: knowledge
description: "A Spotify-Wrapped-style retrospective of your year with AI agents, computed from local history across harnesses (Claude Code, Codex, T3, Conductor, Gemini CLI, bridged transcripts, exports). Two layers. (1) A year-round HARVEST folds every turn into a text-free ledger (counts, hashes, who wrote it) and optionally ARCHIVES the transcripts that their own tools prune (Claude Code deletes sessions after ~30 days), because a December extract alone cannot cover a year. (2) The recap: ATTENTION folds the ledger into words you wrote vs words you read (final reply per human turn × a stated read share, 60-70% by default), separating human prompts from agent-dispatched ones per each store's own author flags; EXTRACT/RENDER build the story deck. (3) REFLECT reasons about how the year went, not just how much: it rebuilds each session the person drove as an episode (their prompts verbatim, trimmed final replies, invoked skills, corrections), fans out digest subagents per batch, joins episodes to merged PRs, tickets and KG entities, and has the invoking agent write a cited reflection.md (monthly arcs plus four chapters) that a lint holds to the data. USE WHEN year in ai, your year in ai, ai wrapped, wrapped for my agents, year in review of my ai usage, how much have I written to agents, how much have I read, words written and read, harvest agent history, archive agent transcripts, set up the year-in-ai harvest, reflect on my year with agents, what patterns did I have with agents, themes of my year in ai, how did I work with agents this year. NOT FOR billing or token cost (use the provider's usage tools), single-session search (use session-search), or health/sleep recaps."
argument-hint: "[harvest|attention|run|reflect] [--year YYYY]"
effort: medium
---

# year-in-ai

A Wrapped-style recap of a year spent working with agents, built from the
history already on this machine. Nothing leaves the machine.

## Why there are two layers

Local transcript stores decay. Claude Code prunes sessions after about 30
days, and a harness migration can lose a whole window, so the recap cannot be
computed in December from the stores alone. The skill therefore has:

1. **Harvest (all year).** `harvest` reads every store it can find and folds
   each turn into a ledger row: timestamps, word and character counts, content
   hashes and author flags. **Rows never hold message text.** `--archive-to`
   also copies the stores that prune themselves to a larger disk. Nothing
   archived is ever lost: a file is replaced only by one that extends it byte
   for byte; a rewritten or truncated source opens a numbered revision,
   `<name>.rev-<n>.jsonl`, which later growth extends in place. A file its
   tool rewrites wholesale every week would add one revision per rewrite;
   none of the archived stores does that, and `harvest` prints the revision
   count so growth is visible. Revisions are kept for quoting and are **never
   ledger input**: the harvest skips every `*.rev-<n>.jsonl` file. Turns that
   exist only in a revision (a transcript rewritten and then pruned at its
   source) are preserved on disk but not counted. A transcript whose own name
   ends in `.rev-<n>.jsonl` would be skipped too; Claude Code and Codex name
   sessions by UUID.
2. **Recap (once a year).** `attention` folds the ledger into what you wrote
   and read. `extract` and `render` build the story deck from transcripts.
3. **Reflect (once a year).** Reads what was actually said and writes a
   cited `reflection.md`: themes and ideas, how you worked with agents,
   challenges and outcomes, insights for next year. See "Reflect" below.

## Commands

Run from `scripts/` with Python 3.9 or later. No third-party packages.

```bash
# First run: read everything still on disk.
python3 year_in_ai.py harvest --backfill --archive-to /Volumes/Archive/agent-traces

# Scheduled run (weekly is safe: the shortest store retention is ~30 days).
python3 year_in_ai.py harvest --days 45 --archive-to /Volumes/Archive/agent-traces

# Words written and read for a year, from the ledger.
python3 year_in_ai.py attention --year 2026 --out attention.json

# The story deck.
python3 year_in_ai.py run --year 2026 --outdir ./year-in-ai-out
```

## Stores and how each says who wrote a turn

| Store | Default location | Author signal |
|---|---|---|
| T3 | `~/.t3/userdata/statev2.sqlite` | `createdBy` user/agent per message; subagent threads skipped |
| Claude Code | `~/.claude/projects` | `entrypoint`: `cli` is a person, `sdk-cli` is `claude -p`, `sdk-ts` is an app (not counted) |
| Claude prompt history | `~/.claude/history.jsonl` | typed in the CLI; usage probes dropped |
| Codex | `~/.codex/sessions` (`.jsonl`, `.jsonl.zst`) | `originator`/`source`: `codex_exec` is a script |
| Codex prompt history | `~/.codex/history.jsonl` | typed in the TUI |
| Conductor | `~/Library/Application Support/com.conductor.app/conductor.db` | user role |
| Gemini CLI | `~/.gemini/tmp/*/chats` | user role |
| Paseo | `~/.paseo/agents` | its Claude sessions count as orchestrator traffic |
| Bridged markdown | config `bridged` | none: filtered, then used only before exact coverage |
| Exports | config `exports` | none: filtered |

Add archive copies and extra stores in `~/.config/year-in-ai/config.json`. If
that file is absent the config is empty; a `--config` that does not exist, or
any config that cannot be read or is not a JSON object, stops the run with
status 2 instead of silently dropping its stores:

```json
{
  "roots": {
    "claude_projects": ["/Volumes/Archive/agent-traces/claude-projects"],
    "codex_sessions": ["/Volumes/Archive/agent-traces/codex-sessions"],
    "bridged": ["~/workspace/docs/conversations"],
    "exports": ["~/exports/conversations.jsonl"]
  },
  "archive_to": "/Volumes/Archive/agent-traces",
  "text_only_until": "2026-10-18",
  "utc_offset_hours": -5
}
```

## Identity: occurrences first, turns second

Every row a reader emits has an **occurrence** identity: the store's own
message id where it has one (T3, Conductor, Claude Code, Gemini), otherwise
the session, timestamp, role, text hash and a count of earlier identical
occurrences. The occurrence id is stable across harvests and carries no text.
A **row** is one revision of an occurrence: its id is the occurrence plus the
hash of its text, so an unchanged message harvested twice is one row, an
edited one adds a row for the same occurrence, and two occurrences never share
a row. The ledger stamps each row with a harvest sequence; the fold keeps each
occurrence's latest revision by that sequence, and a message that returns to
earlier text gets a new row (`revision_identity`). Pruning or inserting
records moves no other occurrence id. `tests/test_reader_contract.py` runs these cases against every reader in
`sources.REGISTRY` and fails when a reader has no fixture. Whether two
occurrences are the same *turn* is a separate, evidence-based decision in the
fold.

## Requirements

Python 3.9 or later, nothing else, except **zstd** for compressed Codex
transcripts (`*.jsonl.zst`). It is looked for on `PATH`, then in
`/opt/homebrew/bin`, `/usr/local/bin` and `/usr/bin`, so a launchd job with a
minimal `PATH` still finds a Homebrew install.

**No file is ever skipped silently.** Readers find files only through
`list_files` and read them only through `read_lines` and `read_text` (a test
fails otherwise), and these report every failure: a directory that cannot be
listed, zstd missing, a corrupt or truncated archive, a file that cannot be
opened or read, a malformed Gemini chat, an unreadable T3 or Conductor
database, and a store that exists but cannot be reached (permission denied on
it or on a directory above it). Only a store that does not exist is absent.
Symlinked directories inside a store are followed. A failure counts as
`skipped` on its source, never as an empty store; `harvest` prints a warning naming the cause and exits with status 4.
Exit 4 always means the totals are incomplete, never a quiet week. Read the
warning's reason: a stall or "not accessible" points to missing disk access
(grant Full Disk Access); zstd not found, a corrupt archive or an unreadable
file each need their own fix.

## Live stores and their archives

A store and its archive copy hold the same files under the same names, and
`harvest` reads one copy of each: the newest write, with ties going to the
live store. For transcripts that only grow (Claude Code, Codex), an older
copy wins instead when its content, decompressed, extends the newest one byte
for byte, because the newest was truncated. Size alone is never taken as
freshness, since an edit can shorten a file.

## How "written" and "read" are counted

- **Written:** prompts a person wrote, counted as turns. Each store's author
  signal (table above) decides who wrote a prompt, and a prompt marked as an
  agent's never counts. Only T3's per-message `createdBy` is exact enough to
  stand alone. Every other store's human prompts also pass three filters,
  because a script can drive those harnesses the way a person does (see the
  known limit below): no automation opening, no exact text repeated across
  three sessions, no opening repeated across four. Prompts from stores with no
  author at all (bridged markdown, exports) must also be 1,500 characters or
  shorter: longer unflagged prompts were dispatched briefs far more often than
  writing. A turn recorded by two stores counts once (the closest
  same-text turn within 36 hours, 20 minutes under 80 characters). A resumed
  or forked session's copy counts once, but only on evidence: the store's own
  message id, a T3 fork's creation time, or, for markdown and exports, a run
  of matching neighbouring turns. Anything else typed twice counts twice.
- A ledger written by an older schema version is never mixed in: `harvest`
  refuses to append to it and `attention` ignores its rows. Rebuild with
  `harvest --backfill` into a fresh ledger directory.
- **Read:** the final reply to each counted prompt, times the read share
  (`--read-low`/`--read-high`, default 0.60–0.70). Prompts from stores that never kept
  replies get an estimated reply from measured replies of the same harness
  family (a CLI prompt from CLI replies), reported separately. A family with
  no measured replies is never estimated from another family; its prompts are
  reported as `unestimated_prompts`.
- **The ratio** is words read over *authored* words written: pasted blocks,
  paste placeholders and fenced code blocks are removed, and what remains is
  capped at 4,000 characters per prompt (a longer one is a paste, whatever its
  markup).
- **Known limits.**
  - An agent that drives the interactive `claude` CLI through a terminal looks
    exactly like a person to every store. Only the scripted-prompt filters
    (repeated text, repeated openings, automation markers) catch it, and a
    person who types the same long prompt into three sessions is filtered too.
  - Stores without message ids (Codex rollouts, the Claude and Codex prompt
    histories, bridged markdown, exports) identify a turn by its text. A turn
    whose text changes there is a second turn. In practice these stores do
    not edit history: rollouts and histories only append, and bridged
    markdown is a generated rendering, used only before `text_only_until`.
  - Identical prompts in a store without message ids (same session, time and
    text) are told apart by order, so pruning one can relabel the others;
    their count in the ledger stays right.
- **The agents' own year:** replies to agent-written prompts are reported on
  their own, never added to what you read.
- Set `text_only_until` to the date a store with exact authors starts covering
  you. Measured on one machine, only ~18% of bridged "user" turns after that
  date matched a human-typed prompt.

## Reflect: how the year went, not just how much

Counts say how much; the reflection says what the work was, how it was
steered, what got hard and what shipped. It runs in stages. Code does
everything that can be checked; agents do the reading; a lint holds the
prose to the data. All output goes to `~/.local/share/year-in-ai/reflect/<year>/`
(mode 0700, files 0600). It holds the user's words, so it never goes in the
ledger, a repository, a ticket, a PR, or any third-party service.

```bash
cd scripts
python3 year_in_ai.py reflect status   --year 2026   # what exists, and the next step
python3 year_in_ai.py reflect episodes --year 2026   # 1. episodes + digest batches (code)
#                                                       2. digest subagents, one per batch
python3 year_in_ai.py reflect check    --year 2026 --complete   # 3. the digest gate
python3 year_in_ai.py reflect join     --year 2026 --kg ~/workspace/research/entities  # 4. outcomes (code)
python3 year_in_ai.py reflect reduce   --year 2026   # 5. data.json, months/, index.md (code)
#                                                       6. the invoking agent writes reflection.md
python3 year_in_ai.py reflect lint     --year 2026   # 7. the gate on the reflection
python3 year_in_ai.py reflect share    --year 2026 --redact-term acme   # redacted copy to share
```

**1. Episodes (code only).** Every session with a human-written turn in the
year becomes an episode `e-<8 hex>`: dates, harness, repository, directory and
branch, ticket ids and PR URLs mentioned, skills and slash commands invoked,
the user's prompts verbatim (their authored words: pastes and code fences
removed, as `attention` counts them), each turn's final reply trimmed to its
head and tail, correction markers (a later prompt that redirects the agent,
plus interrupts), and a size and correction score. Who wrote a prompt is
never re-derived: `episodes` reads the stores through the ledger's own
readers with a text tap and joins the text back to the rows
`attention.classify` decided were human. The 30 longest and 30 most-corrected
sessions also get a sampled tool trace (the opening, every error, the events
around each correction, the close). Batches of about 25 episodes go to
`batches/batch-NNN.json`, and `digest-instructions.md` holds the schema.
Exit 4 means a store was partly unreadable (the warning names it); the
episodes from what was read are still written.

**2. Digest (fan-out).** Launch one subagent per batch, in parallel waves
(about ten at a time). Give each the path of its batch file and of
`digest-instructions.md`, and nothing else: it writes one
`digests/<episode id>.json` per episode (goal, topics, kind of work, how the
user steered, main obstacle and resolution, outcome with evidence, ideas, one
quote candidate) and finishes by running `reflect check --batch NNN` until it
passes. Digests are cached against each episode's content hash: rerunning
`episodes` only batches sessions that are new, grew, or whose digest failed
the check. Tell subagents not to echo episode text in their replies and to
keep any helper script in the private `scratch/` directory, never `/tmp`
(a real run found workers leaving digest scripts there).

**3. Check (the digest gate).** Rejects a digest with a missing field, a value
outside the schema, a stale hash, or a quote that is not verbatim in that
episode's prompts (whitespace and quote style aside; never a reply).

**4. Join (code only).** Links episodes to merged PRs (by mention, the
harness's own PR record, the head branch, or a ticket in the PR title within
three weeks; `data.json` counts only the first three as the episode's own
outcome, and a shared ticket as related). A head-branch match counts only
when the episode directory's git remote is exactly the PR's `owner/name`;
otherwise, or when the directory is gone, it is a `branch-name` link and
counts as nothing, ticket ids, and knowledge-graph entities (by ticket, URL, or
created during the episode and named in it). Every source is optional and
reported: `harness` (PRs a store linked, e.g. T3's snapshots), `github`
(`gh` lists the owner's own merged PRs month by month; no session text is
sent), `git` (local first-parent history, used when `gh` is absent),
`linear` (an optional export, `--linear-json`), `kg` (`--kg` or config
`kg_entities`). An absent source is printed and recorded in `outcomes.json`;
the join continues without it.

**5. Reduce (code only, then the agent).** `reduce` writes `data.json` (every
number the reflection may use: totals, per-month figures, kinds, steering,
outcomes, topics, skills, repositories, shares as whole percents),
`months/<YYYY-MM>.md` (one compact block per episode: digest plus joined
outcomes) and `index.md` (recurring topics, obstacles by corrections, ideas
in time order, quote candidates). Then reduce in two levels: one subagent per
month reads its packet and writes a cited arc (what the month was about, what
moved, what stalled), and the invoking agent reads the arcs, `index.md` and
`data.json` and writes `reflection.md`:

1. `## Monthly arcs`: one short cited paragraph per month;
2. `## Themes and ideas`: what the year was about and how it changed,
   recurring ideas and principles;
3. `## How you worked with agents`: briefing and steering style, corrections,
   delegation and fan-out, which skills and harnesses carried the work, how
   that changed through the year;
4. `## Challenges and outcomes`: the hardest problems and what broke them,
   what shipped and what stalled;
5. `## Insights for next year`: blind spots and concrete changes, each tied
   to the episodes that show the pattern;
6. optionally `## Data notes`: coverage and absent sources (the only section
   exempt from citations; numbers are still checked).

**7. Lint (the gate).** A reflection holds only headings, paragraphs, list
items and blockquotes: a table (with or without outer pipes), a fenced block,
HTML, a footnote or a definition list fails, as does an unclosed HTML
comment. A closed comment hides only itself; text after it is linted.
`reflect lint` fails on: a claim (paragraph, list item, blockquote) with no
`[e-…]` citation; a citation that does
not resolve; a quote (a blockquote, or a quoted span of three or more words)
not verbatim in a prompt of an episode the same claim cites; a number not in
`data.json` (thousands separators, `%`, `K`/`M` are understood; ISO dates,
ids, `#123`, URLs, quotes and `inline code` are not numbers, so write version
numbers as code); a missing section. The reflection is done when the lint
passes. The lint proves each number appears in `data.json`, not that it is
the right figure for its sentence: after re-running `join` or `reduce`,
re-check every figure in the text against the new `data.json`, because a
stale value that matches another field passes
([BRO-3774](https://linear.app/broomva/issue/BRO-3774/year-in-ai-reflect-the-lint-checks-a-figure-exists-not-that-it-is-the)).

**Privacy.** Local only. Never paste episode text, digests or the reflection
into a ticket, PR, chat service or upload. `reflect share` writes
`reflection.share.md`, a **review draft, not a share-safe copy**. It replaces
blockquotes, quoted spans of every kind and inline code, and any run of five
or more words that appears in a prompt or reply (quoted or not, across line
breaks); it removes URLs and paths and masks `--redact-term` values, and
prints how many of each it removed. It needs `episodes.jsonl` and refuses to
run without it. It cannot recognise a short name, a credential or a
paraphrase of something private in model-written prose: a person reads every
line, adds `--redact-term` for anything private, and reruns before the draft
leaves the machine.

**From chapters to video.** The four chapters are the script for the recap
video: hand `reflection.share.md` and `data.json` to the `motion-lab` skill
(`skills/video/motion-lab`), as tracked in
[BRO-3752](https://linear.app/broomva/issue/BRO-3752/year-in-ai-recap-video-command-motion-lab-liquid-midnight-style).

## Privacy

- The ledger holds no message text. Session ids are stored as hashes, and
  attribution fields accept only known values (anything else becomes
  `other`). Tests fail the build if a fixture phrase reaches a ledger file or
  metadata carries free text.
- Text hashes of very short prompts ("yes", "go") can be guessed by
  dictionary. Keep the ledger as private as the transcripts.
- `extract --share` redacts client and CRM paths and verbatim prompts before
  anything is shared.

## Scheduling on macOS

A launchd job that reads an external or encrypted volume needs Full Disk
Access. Run the harvest through `/bin/bash` (grant it access) and the system
`/usr/bin/python3`. Homebrew's Python hangs on the privacy prompt instead of
failing.

Without that access, zstd blocks opening a compressed transcript on the
volume, waiting for a privacy prompt nobody sees. The harvest does not wait
forever: a zstd that produces no output for 120 seconds is killed, every
compressed file in the run is reported as skipped, and `harvest` exits 4
naming the stall.

## Tests

```bash
python3 -m pytest tests/ -q
```
