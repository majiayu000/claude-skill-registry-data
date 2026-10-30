---
name: claude-code-token-cost
description: Cut Claude Code token cost and prompt-cache waste. Use when the user asks why Claude Code (or Codex CLI, Gemini CLI, OpenCode) burns so many tokens, how much their sessions cost, whether the prompt cache is working, whether to /compact, or how to reduce the bill. Runs the local kvleak audit (no API key, no network) and turns its numbers into the one or two settings that actually move the bill.
---

# Claude Code token cost (kvleak)

kvleak reads the session files Claude Code, Codex CLI, Gemini CLI and OpenCode already keep
on disk and prices every model call at list price: uncached input, cache writes, cache reads,
output. It then shows how much of the input spend went to cache rebuilds that could have been
avoided, and which setting fixes most of it. Zero dependencies, MIT, no network calls.

## Run the audit first, never guess

```bash
uvx kvleak                 # or: pipx run kvleak · pip install kvleak && kvleak
kvleak --since 7d          # recent window
kvleak --json              # machine-readable, for your own summary
```

Read these lines of the report and quote them back to the user with their own numbers:

- `Cache hit rate`: usually 90%+ and **not** the problem. Say so explicitly; users expect it to be.
- `Leaked to misses`: the dollars (or rate-limit headroom on a subscription) that went to cache
  rebuilds and cold starts. This is the figure to lead with.
- `Where the leak comes from`: the top cause. Three usual answers:
  - *Idle gap outlived the cache TTL*: pauses longer than the 5-minute (or 1-hour) cache.
  - *New session cold start*: many short sessions each rebuilding the same prefix.
  - *Subagent cold start* / *Prefix changed*: multi-agent fan-out or settings edits mid-session.

## Then recommend by evidence, in this order

1. `kvleak tune` replays the last 30 days under each candidate value of the settings Claude Code
   already exposes (compaction window, cache TTL for `claude -p`, idle compaction, Bash output
   cap) and prints the saving per setting. `kvleak tune --apply` writes the winners to
   `~/.claude/settings.json` with a backup; `--reset` undoes it. This is normally the largest
   lever (a quarter of the bill on the maintainer's history) because compaction changes how much
   context is carried at all.
2. `kvleak whatif` puts every popular token-saver's advertised number (rtk, caveman,
   claude-token-optimizer, AgentDiet-style tool-result trimming, lower thinking effort) on the
   user's own bill as an upper bound. Use it to answer "should I install X?" with a dollar figure
   instead of an opinion. Tool-output compressors shrink what the context carries, which is paid
   at the cache-read price, the cheapest line of the bill; that is why their numbers come out small.
3. `kvleak skills` prices the skill listing that rides in every call's cached prefix and names the
   skills never invoked, with the command to turn each off.
4. `kvleak advise` answers "should I `/compact` now or hand off to a fresh session" from the
   current context size and cache state.
5. `kvleak hooks --install` keeps long shell output out of the context (head + tail + error lines
   + a path to the full output); `kvleak refine --apply` writes evidence-gated context-hygiene
   rules into `CLAUDE.md`; `kvleak statusline --install` puts a cache TTL countdown in the status
   bar. Each has an uninstall flag.
6. A week after applying anything, `kvleak probe` contrasts input spend per call, leak share and
   context size before vs after on real billed sessions.

## Rules for the answer you give

- Quote the user's own numbers from the report; do not quote the maintainer's.
- Lead with "leaked to misses" and its top cause, not with the hit rate.
- Recommend `tune --apply` only after showing the `kvleak tune` table so the user sees what
  changes and the undo flag.
- Subscription users: dollars are list-price equivalents; the percentages are their rate-limit
  headroom. Say this once.
- If `kvleak` finds no sessions, the user's transcripts live somewhere unusual; `kvleak --path
  <dir>` reads any JSONL with usage counters.

Repository and full guide: https://github.com/shangliy/kvleak
