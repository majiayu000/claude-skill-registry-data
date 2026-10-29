---
name: lore
description: Lore, history, and archaeology for code, config, or a system. Use for why something is this way, bug or deliberate, where a number or setting came from, how we did it before, who owns or changed it, what incident led to it, or how it is doing now. Returns cited, confidence-graded evidence from the repo, team, agent sessions, and runtime.
argument-hint: "[--depth quick|full] [--include <surfaces>] [--exclude <surfaces>] [--since <date>] [--until <date>] [--review <ref|PR>] [--constraints] [--live] [--] <target or question>"
---

# Lore

Recover a target's **lore**: its past (intent, origins, precedent, ownership,
incident lineage) and its present (usage, health, callers, activity), graded
by how strongly the record supports each claim. Explaining mechanics, such as
what a function returns or how a request flows, belongs to reading the code.

Work as a careful investigator. The record is fragmentary and biased; a
verbatim quote with a precise citation beats a plausible paragraph, and a
named gap beats a confident guess.

Every run is **read-only** on every surface: no posts, reactions, mark-read,
comments, ticket edits, branch switches, or checkouts. Read other refs with
`git show <ref>:<path>`. Paths in this file are relative to this skill.

## Arguments

| Argument | Default | Effect |
| --- | --- | --- |
| `--depth quick\|full` | `full` | `quick` runs inline, walks surfaces in order, and stops at the first Direct citation. |
| `--include <surfaces>` | every available | Comma-separated surfaces to search. |
| `--exclude <surfaces>` | none | Comma-separated surfaces to skip. |
| `--since`, `--until <date>` | unbounded | Bound every search to the window (YYYY-MM-DD, both days included). Translate to each tool's own bounds. |
| `--review <ref\|PR>` | off | Apply the history lens to a change: read [review lens](references/review-lens.md). |
| `--constraints` | when a change is implied | Always end with Preserve / Change / Avoid / Risk. |
| `--live` | off | After synthesis, check each rationale against present reality. |
| `--` | | Ends options; the rest is the question. |

Flags take `--flag value` or `--flag=value`. Prompt wording is a preference,
not a flag: "check Slack first" orders the search, `--include team` restricts it.
The repo anchor runs under every surface filter, `--exclude repo` included,
because the other searches key off it; the filters govern step 3.

## Surfaces

| Surface | Record kept by | Reference |
| --- | --- | --- |
| `repo` | the codebase and its forge: history, blame, comments, tests, ADRs, PRs, reviews, issues, ownership files | [repo](references/repo.md) |
| `agents` | coding agents: session logs, agent-written plans and handoffs | [agents](references/agents.md) |
| `team` | people: design docs, tickets, wikis, postmortems, chat, meeting notes, email | [team](references/team.md) |
| `runtime` | the running system: metrics, logs, traces, errors, alerts, deploys, CI, analytics | [runtime](references/runtime.md) |

The order is cost order, cheapest first. Quick mode walks it top to bottom.

## Guidance layers

Optional guidance tells you which tools an organization uses and how to query
them. Resolve it per choice with this precedence: explicit arguments, then the
conversation, then the repo's `.agents/lore.md`, then the user's
`~/.agents/docs/lore.md` and any `lore-*.md` beside it, then the built-in
surface references. A missing layer is normal. Without guidance, infer tools
from what this session can call.

## 1. Frame the question

Name the **target** (file and line range, symbol, config key, number, service,
or decision) and the **question shape**: why, bug or deliberate, provenance,
precedent, ownership, incident lineage, or present health. A vague target gets
your best reading from the conversation, stated in one line so the user can
redirect. Treat any hypothesis embedded in the question as a candidate to
test. This step is complete when target, shape, and arguments are written down.

## 2. Build the anchor

Run the anchor recipe in [repo](references/repo.md) inline: blame and history
through renames, the pickaxe for the exact text, each substantive commit's
full message and trailers, its pull request through the commits-to-pulls API,
and that PR's body, reviews, and linked issues and tickets. The **anchor** is
the seed every other search keys off: paths, symbols, SHAs, PR numbers and
URLs, authors, merge dates, ticket IDs, and distinctive strings. A shallow or
partial clone needs the handling in that reference before history is
trusted. The recipe runs cheapest first; in quick mode, stop at the first
Direct citation and mark the fields not reached. This step is complete when
the anchor lists those fields, each one found, absent, unreachable, or not
reached.

## 3. Search the surfaces

**Quick.** Continue down the surface table inline, one anchored search at a
time, and stop at the first Direct citation that answers the question. Then
synthesize inline against [epistemics](references/epistemics.md).

**Full.** Discover what is reachable: this session's tools and MCP servers,
CLIs on PATH (`gh`, `agent-slack`, `agentsview`, others named by guidance),
and the guidance layers. Map each reachable tool to its surface; several
servers or CLIs fronting the same system count as one tool. Spawn one
read-only investigator per tool in the included surfaces, all at once, each
with the [investigator brief](references/investigator.md), the anchor, the
question, and its surface reference. The repo investigator extends the
anchor (precedent, ownership, in-flight work, linked issues) rather than
repeating it. A surface with no reachable tool is a gap to report. Skip a
reachable tool only when it is provably irrelevant, with the reason written
down. Investigators return metered queries as leads; put each to the user
with its estimated cost before running it. This step is complete when every
investigator has reported or failed, and each failure is recorded as a gap.

## 4. Synthesize

**Full.** Spawn one synthesizer with the
[synthesizer brief](references/synthesizer.md), this skill's absolute
directory, the question, the anchor, every investigator report including
empty ones, and the gaps with reasons.
It re-opens each Direct citation before grading it. Subagents inherit the
current model and reasoning configuration.

The result follows [epistemics](references/epistemics.md): every claim sits in
one tier with phrasing to match, and every Direct or Supported claim carries
its citation. This step is complete when the synthesis passes the epistemics
final check.

## 5. Check it live (`--live`)

For each rationale claim, check present reality read-only on the `runtime`
surface: does the guard, retry, or flag still fire; does the condition it
defends against still occur; has the basis for the number moved; is the bug
or upstream limit it works around fixed. Mark each claim **Still holds**,
**No longer holds**, or **Unverifiable**, with the query or link. Before a
metered query, state its estimated cost and ask.

## 6. Report

Lead with the answer and its tier. Then:

- **Evidence**: each claim with its tier, a permalink, and the quoted sentence
  that carries the reason. Links rot and sit behind access controls; the quote
  survives.
- **Present** (when asked or `--live`): the live checks.
- **Unknown**: what was searched, with what terms, and what came back.
- **Sources checked**: one line per surface and tool, including empty results,
  skipped tools with reasons, unreachable surfaces, and retention cliffs.
- **Preserve / Change / Avoid / Risk** when the question leads into a change or
  `--constraints` is set.

When the reason lived only in chat, a meeting, or a session, name the durable
home it deserves (a code comment, ADR, or commit trailer) as a suggestion.

To add a tool, surface, or guidance, read [extending](references/extending.md).
