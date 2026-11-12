---
name: token-economy
version: 1.1.2
description: Token and cost control for coding agents — context and cache hygiene, batching, subagents for mechanical work, escalation, session measurement, guardrails, RTK/CodeGraph audit. Use when saving tokens, cost or context.
---

# Token Economy

Spend tokens where they buy accuracy and nowhere else. Most waste is not long replies: it is
bytes that enter the context once and are re-sent on every later turn, caches paid twice,
subagents that inherit a huge context, retries on a model out of its depth, and sessions that
carry three unrelated tasks. Two modes: **working rules** (sections 2-7, 10) and **measure and
audit** (section 9). Templates in [RECIPES.md](RECIPES.md); tool notes in
[TOOLS.md](TOOLS.md); Claude Code settings and hooks in [GUARDRAILS.md](GUARDRAILS.md).
Reply-style compression is [caveman](../caveman/SKILL.md); how skills get imported into a
project is [rsk-guide](../rsk-guide/SKILL.md).

## 1. When to invoke

- **Measure / audit / setup** — "where did my tokens go", a surprising bill, new machine or
  project, installing context-mode, RTK or CodeGraph, sessions hitting limits early.
- **Working** — before a broad exploration, before a refactor, audit or edit that repeats over
  many files, when choosing a model or subagent, before polling a job, when a session has
  grown long or drifted across tasks, when a cheap model starts looping.
- **Not this skill** — "just be terse" is [caveman](../caveman/SKILL.md).

## 2. Where tokens go

Ranked by what they usually cost over a session:

1. **Resent context.** Every request re-sends the whole conversation, so cost grows with
   turns x context: a 5k-token read on turn 3 of 40 is paid ~37 more times. Caching makes
   repeats cheaper, not free, and cached tokens still count toward rate limits.
2. **Cache rebuilds.** An expired or invalidated cache re-pays the whole prefix at the write
   price (section 7).
3. **Subagents that inherit context.** A fork starts with the parent's full context and pays
   for it on every one of its turns.
4. **Always-loaded instructions and injections.** `CLAUDE.md` / `AGENTS.md` and their
   `@imports`, OpenCode `instructions`, MCP tool schemas, every installed skill's description,
   and whatever hooks inject. Paid every turn.
5. **Retries.** A failed edit or wrong guess costs its input, its output and the cleanup.
6. **Thinking.** Billed as output, and kept in the history. High effort on mechanical work is
   pure waste.
7. **Reply text.** Priced several times input, but the smallest volume.

**Configuration beats instructions.** A setting is paid once and always applies; a sentence
asking for restraint is paid every turn and enforces nothing. Prefer settings, then hooks,
then instructions ([GUARDRAILS.md](GUARDRAILS.md)).

**Rule: cut what persists before cutting what is said.**

## 3. Always-on rules

Habits only work if they are loaded every session, so they live in `AGENTS.md`, not here. Offer
to paste the block from [RECIPES §1](RECIPES.md#1-agentsmd-rules-block). Its substance:

- **Locate, then read.** Grep/glob (or CodeGraph) first; read line ranges; never re-read a file
  you just edited.
- **Ask tools for the smallest useful answer.** `git diff --stat` first, quiet flags, failing
  tests only, errors only from builds, `tail`/`grep` on logs; index web pages instead of
  reading them whole.
- **Batch independent calls** into one turn.
- **Edit, don't rewrite.** A targeted edit over a full-file write; never print a file back.
- **Ask before building on an ambiguous request.** One question or a short plan is cheaper than
  implementing the wrong thing.
- **No pastes of long output.** A pasted log or screenshot stays for the whole session; let the
  agent run the command, or write it to a file and read a range. Crop screenshots.
- **Replies lead with the result.** No recap, no narration. Code, commits and docs in full prose.
- **One task per session**, carried across in a handoff note, not the transcript.
- **Two-failure rule.** Second failed attempt at the same thing: stop, escalate (section 5).

## 4. Delegating to subagents

A subagent works in its own context and returns only a summary. It is not free: it starts
with its own system prompt and tool schemas, so a lookup of 1-3 tool calls is cheaper inline.
**Use fresh subagents with a brief, never forks of a deep context** (section 7).

### Reading

| Task | Model | Effort | Ask it to return |
|---|---|---|---|
| Locate (where is X, which files) | haiku | low | paths + one line each |
| Understand (how does X flow) | haiku or sonnet | medium | <=300 words with `file:line` |
| Sweep / review many files | sonnet | medium | findings list, ranked |
| Design call, hard bug | opus | high | a recommendation, not a survey |

- **Brief it like a peer:** goal, what is ruled out, where to look, output shape, word cap.
- **Reports come back in caveman style.** Only a model reads them; fragments with exact paths,
  symbols and `file:line` refs lose nothing. Never for commits, docs or code, and not for user replies unless the user asked for caveman mode.
- **Fan out only for independent questions**, in one turn; don't redo the agent's work.
- **Claude Code:** built-in Explore runs on the *main* model; a user agent named `Explore`
  with `model: haiku` overrides it ([RECIPES §2](RECIPES.md#2-claude-code-agents)).
- **OpenCode:** subagents are `agents` entries with `mode: subagent`; effort is a model variant
  (`provider/model#high`). Leave built-in `explore` alone: `system` replaces its prompt.

### Doing

Work that follows a decided pattern runs on a cheaper tier. Cheapest first: **a script** (sed,
a codemod, ast-grep, a shell loop) when no item needs judgment, at zero model tokens per item;
then a **worker subagent** (haiku or Flash, low effort) when each item needs a little reading.
The strong model writes the pattern and checks the result, never the repetitions.

| Work | Tier | What makes it safe |
|---|---|---|
| Mechanical refactor: rename, move, apply a decided pattern, lint fixes | script, else worker | pattern fixed upstream; tests and lint verify |
| Checklist audit: frontmatter, headers, missing tests, deprecated APIs, drift | script, else worker | yes/no per item against a written checklist |
| Repetitive loop: same edit over N files, call-site migration, fixtures, bumps | script, else worker per batch | one worked example plus an acceptance command |
| Waiting on a job | a script with bounded output | no judgment at all |

- **Do item one yourself** (or a spec with one worked example) plus the acceptance command.
- **Verification is a command**, never the worker's word; review `git diff --stat` and the
  check, and read only the diffs that failed or look odd.
- **Batch by files**, independent batches in parallel; an item that fails twice comes back up.
- **Not delegable:** design judgment, behaviour across modules, security-sensitive code, or a
  spec you could not write down.
- **When the main session is already the cheap model**, invert it: get the spec from a stronger
  subagent or session, execute on the main model. Worker in
  [RECIPES §2](RECIPES.md#2-claude-code-agents).

## 5. Choosing the model and moving up

- **Default tier:** Sonnet at medium effort in Claude Code; the cheap model (e.g. DeepSeek
  V4.1 Flash) in OpenCode.
- **Escalate when** the two-failure rule fires, a decision will outlive the session, or a bug
  is not localised after one focused pass. Cheapest first:
  - **Subagent at the higher tier** when the problem fits a brief
    ([RECIPES §5](RECIPES.md#5-subagent-brief)).
  - **Fresh session at the higher tier** when it needs many turns or the context is polluted;
    write a handoff note ([RECIPES §4](RECIPES.md#4-handoff-note)).
  - **Switch model in place** only while the context is small: it discards the cache.
- **Come back down** once the hard part is decided.
- **Effort:** low for mechanical, medium by default, high for real reasoning; `xhigh` / `max`
  only when the user asks.

## 6. Cheap models (DeepSeek V4.1 Flash and similar)

When tokens are already cheap, the waste is turns and retries, and quality falls off faster
with context length.

- **Don't compress instructions.** Small models need explicit steps and examples. Terse
  *replies* are fine.
- **Keep the prefix stable.** DeepSeek caches prefixes automatically and a hit costs about 2%
  of a miss; don't toggle MCP servers or instructions mid-session. Off-peak is half price.
- **Compact earlier** ([RECIPES §3](RECIPES.md#3-opencode-config)); **verify by running**, not
  rereading; **retry narrowly** (re-read only the target range, once).
- **Hand the model smaller tasks.** One file, one change, explicit acceptance check.

## 7. Cache and context hygiene

- **Know the cache TTL.** Claude's prompt cache defaults to 5 minutes; Claude Code can pin 1 hour
  (`promptCacheTtl`, `subagentPromptCacheTtl`). A 1h write costs more than a 5m one, and pays
  off from the first idle gap it survives.
- **Poll inside the TTL or far beyond it.** With a 5-minute TTL, a 5-60 minute cadence is the
  worst case: every poll rebuilds the whole prefix. Better still, let a script wait and report
  once, with bounded output.
- **After a long break, `/clear` rather than resume** a large context: the first turn back pays
  a full rebuild either way, and a fresh session pays it on far less.
- **No forks at depth.** A fork inherits the parent's context and re-sends it on every turn;
  turn automatic forking off and brief a fresh subagent instead.
- **Choose a ceiling.** A very large window with auto-compaction near its end lets context (and
  cost per turn) grow for hours. Either cap it, or confirm at thresholds; not both.
- **Compaction is not free**: it is a summarisation pass over the whole context. `/clear` at a
  task boundary is.
- **Trim the index budget per project.** Install only the skills and MCP servers a project uses;
  each description and tool schema is paid every turn. Claude Code defers MCP schemas behind
  tool search; OpenCode loads them all.
- **Watch injections.** Every hook's output enters the context. Measure them (section 9) and
  remove any that inject unasked-for content.

Settings, permission rules and hook patterns that enforce these: [GUARDRAILS.md](GUARDRAILS.md).

## 8. Tools

context-mode (tool outputs), RTK (shell output) and CodeGraph (structure queries) are
expected, and their absence is a gap; caveman covers reply prose. Each has side effects worth
checking: what it adds to the always-loaded instructions and what its hooks inject. Install,
overlap and pitfalls in [TOOLS.md](TOOLS.md); commands in [RECIPES §6](RECIPES.md#6-tool-setup).
Keep the setup in a config repo ([RECIPES §7](RECIPES.md#7-setup-repo)) so a machine is one
command and `check` doubles as the audit.

## 9. Measure and audit

- **Config:** `bash scripts/audit.sh [project-dir]` (read-only) reports `OK` / `GAP` / `WARN` for
  tools and their wiring, the `Explore` override, always-loaded instruction size (following
  `@imports`), whole `SKILL.md` files imported at start, injecting hooks, and MCP servers.
- **A session:** `python3 scripts/session-usage.py [session-id]` (Claude Code, read-only) sums
  the transcripts: requests, uncached input, cache reads and writes per TTL, output and
  thinking, the largest context sent, per subagent, plus the characters each hook injected.
  Live views: `/context` and `/cost`; tool views: `ctx stats`, `rtk gain`.
- **Before and after.** Measure a comparable session before a change and after; vendor savings
  figures are their own benchmarks.
- **Report** a short table: finding, cost, fix. **Ask before fixing**: installs and edits to
  `CLAUDE.md`, `AGENTS.md`, `settings.json`, `opencode.json(c)` or agents change shared config.
- Offer the rules block (section 3) if `AGENTS.md` lacks one.

## 10. Anti-patterns

Each habit above (sections 3-9) is also its own anti-pattern: long reads and pastes, subagents for one grep,
forks at depth, strong models on mechanical loops, idle polling in the cache TTL, mixed-task sessions,
unasked hook output (and `prompt`/`agent` hook handlers, which spend tokens on every fire), caveman style outside model-only text (unless the user asked for caveman mode). Also:

- Importing whole `SKILL.md` bodies at start; every skill installed in every project.
- Adding or removing MCP servers mid-session.
- Quoting a tool's savings percentage without measuring it here.
