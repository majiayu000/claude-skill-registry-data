---
name: coach
description: "Run the token-efficiency coach on a Claude Code session transcript: find wasted tokens (uncached context, bloat, oversized tool output, redundant reads, wrong-tier spend) and report the fixes with dollar estimates. Use when a session felt expensive/slow or the user wants to cut token spend."
disable-model-invocation: true
argument-hint: "[optional/path/to/session.jsonl]"
allowed-tools: "Bash(python3 *)"
---

# Token-Efficiency Coach

Reads a Claude Code session transcript and coaches the user on **token waste** — the
observable inefficiencies (uncached context, context bloat, oversized tool output,
failed tool calls, output-heavy turns, wrong-tier routing, redundant reads) — with a
per-finding fix and a dollar estimate. It flags *waste*; it never grades work *quality*
or scores a person. The analyzer runs locally and reads only your own session log, so
no prompt leaves your machine.

The report below is generated at command time by the shared engine (`scripts/analyze.py`),
which auto-finds the latest session for this project when no path is given, or analyzes
the path you pass as an argument.

## Coach report
!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/analyze.py" $ARGUMENTS`

## Your task
1. **Relay the ranked report above to the user** in your own words — lead with the
   headline (total cost, the single biggest recoverable amount) and then the findings
   in priority order. Keep dollar figures framed as upper-bound estimates, exactly as
   the engine does. Do not invent numbers the report did not produce.
2. **Offer to apply the top fix.** Pick the highest-severity finding and propose the
   concrete remedy it implies, for example:
   - *Low cache hit* → restructure the session so stable context (system prompt,
     instructions, pinned files) sits at the FRONT and stays byte-identical so it caches.
   - *Context bloat / very long thread* → compact the conversation or split the remaining
     work into a fresh session to shed dead context.
   - *Oversized tool output / redundant reads* → read targeted line ranges, grep for the
     lines needed, and pipe noisy commands through head/tail instead of dumping whole files.
   - *Everything on the priciest model* → route mechanical steps (renames, greps,
     boilerplate, file reads) to a cheaper tier and reserve the top model for real reasoning.
3. **Offer to wire up the live statusline** if the user does not already have one. The
   plugin ships `scripts/statusline.py` (live `$cost · ctx tokens · cache-hit% · ⚠`),
   but a plugin cannot register a `statusLine` itself — it must go in the user's
   `~/.claude/settings.json` pointing at a stable copy of the script. If they say yes,
   walk them through the README's "Wire up the statusline" steps (copy the script to a
   stable path, add the `statusLine` block, accept the trust dialog).

If the report says no waste patterns tripped, congratulate the user on a clean session
and skip the fix offer (the statusline offer may still apply).

## Notes for maintainers
- All detection logic lives in `scripts/analyze.py` (the single engine). This command
  adds **zero** analysis logic — it only injects the engine's output and relays it.
- Waste patterns + coaching copy live in `scripts/patterns.json`; prices in
  `scripts/prices.json`. Edit those, not this file, to tune behavior.
- `${CLAUDE_PLUGIN_ROOT}` is substituted in skill content for plugin skills, so the
  engine path above resolves to the installed plugin's `scripts/analyze.py`.
