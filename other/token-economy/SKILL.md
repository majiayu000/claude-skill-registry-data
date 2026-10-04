---
name: token-economy
description: Rubric for keeping Claude Code sessions cheap without losing quality — model tiering, cache hygiene, Read discipline, MCP pruning, subagent isolation. Use when cost feels wrong, before setting a budget, or when onboarding a teammate.
---

# Token economy

Three things drive cost in Claude Code: **context size**, **cache hit rate**, and **model choice**. Most waste comes from one of these being misconfigured and left alone.

## Model tiering — match the model to the task

| Task shape | Right model |
|---|---|
| Format fix, rename, small refactor, comment tweak | **Haiku** — ~15× cheaper than Opus, fast enough to feel instant |
| Routine feature work, bug fix, test writing, reviewing a small diff | **Sonnet** — the default; 5× cheaper than Opus |
| Architectural decision, cross-file refactor, debugging a subtle bug, reviewing a large diff | **Opus** — use when you need the reasoning, not by default |

Claude Code's `/fast` or model selection lets you pick. Don't use Opus by reflex for a typo fix.

## Cache hygiene — the 80% lever nobody talks about

Anthropic caches your prompt prefix for 5 minutes. A stable prefix = the next turn reads from cache at ~10% of input cost. A prefix that changes each turn = full price every time.

**What busts cache:**
- Timestamps in CLAUDE.md, in skill content, or in hook output
- Session IDs / UUIDs interpolated into system prompt
- Rotating "quotes of the day", random greetings
- MCP servers that return time-varying schema metadata

**What preserves cache:**
- CLAUDE.md that doesn't change day-to-day
- Skill/rule content that's additive, not mutating
- Hook `additionalContext` that's deterministic for a given input
- Turning off MCP servers you don't need (every schema change invalidates cache)

**How to check:** `/holocron:cost` — the cache hit rate line. Below 50% is a signal; above 70% is healthy.

## Read discipline — the most common leak

Claude's `Read` tool pulls whole files by default. A 2000-line file is ~8k tokens. Do that 5 times in a session and you've spent ~40k tokens reading the same file repeatedly.

**Pattern:**
1. `Grep` to find the relevant range (cheap — returns only matching lines)
2. `Read` with `offset` + `limit` for the range you identified

Holocron's `read-budget.js` hook nudges this on files > 500 lines, but the discipline has to be yours.

## MCP pruning — one-time setup, ongoing savings

Every MCP server's tool schemas ship to the model on every turn. An unused MCP server costs you tokens forever.

Audit with `/holocron:mcp-audit`. Disable servers you don't actively use. Two or three MCP servers is usually plenty; ten is a tax.

## Subagent isolation — don't pollute the main context

Research / exploration / "find me all the callers" work bloats the main transcript with files and noise you won't need after. Run it in a subagent:

```
Use the Explore agent to find how `authenticateUser` is called across the repo.
```

The subagent's findings come back as a summary; its exploration stays in its own context. Main session stays lean.

## Transcript discipline

Claude Code auto-compacts near the context limit, but compaction is lossy — it summarizes, and summaries forget things. Better:

- `/holocron:handoff` at logical boundaries — write state to a file, start fresh on the next task
- For long-lived work: `/holocron:plan` → plan file → execute → handoff. The plan file acts as durable memory.

## Subtle things

- **Large tool outputs stay in the transcript.** A single 20k-token tool result inflates every subsequent turn's input cost until compaction.
- **`Write` of a large file re-reads context.** Edit prefers over Write for big files.
- **Don't paste log output.** Summarize, grep, or point to a file.
- **Emojis are multi-token.** Harmless unless you're generating content heavy in them.

## Anti-patterns

- Running Opus on every turn "to be safe"
- Full-file Reads on generated/vendored files (`dist/`, `node_modules/`, generated protobufs)
- Keeping MCP servers installed that you tested once and never used again
- Timestamp-injecting SessionStart hooks (looking at you, naive `console.log(new Date())` in a hook that emits `additionalContext`)

## How to know it's working

Run `/holocron:cost` weekly. Healthy numbers:

- Cache hit rate > 60% (70%+ if you're disciplined)
- Median session cost under your per-session budget
- Per-model split skews Sonnet-heavy, with Haiku for small things, Opus for reasoning

If those aren't true, `@cost-analyst` can tell you why.
