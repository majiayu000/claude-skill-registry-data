---
name: session-analyst
description: "Produce an end-of-session report: what happened, what worked, what friction recurred, and which candidate learnings emerged. Use when the user asks /evolution report or invokes this manually at session end. Writes to evolution/reports/, never to stable/."
---

# session-analyst

## When to use
- User runs `/evolution report` or asks "summarize this session."
- Manually before compacting context or ending a session, if the session produced load-bearing evidence.

## Protocol
1. Scan `~/.claude/evolution/records/*.jsonl` for events with `ts` within the current session (use `session` id if known, otherwise last hour).
2. Group by `type`:
   - corrections → list with summaries
   - wins → list with summaries
   - friction → group by similar summary token overlap
3. Identify candidate patterns: any friction or correction theme that already appears ≥ 2 times in prior session records.
4. Run `bash ~/.claude/evolution/bin/evolve-collect.sh` — this updates `candidates/` based on fresh records.
5. Write a report to `~/.claude/evolution/reports/YYYY-MM-DD-session-<short-sid>.md` with sections:
   - Session summary (1 paragraph)
   - Corrections observed
   - Wins observed
   - Candidate learnings updated / created
   - Suggested next actions

## Hard rules
- Never write to `~/.claude/evolution/stable/` directly.
- Never promote a candidate — that goes through the promotion gate.
- Do not invent evidence. Only summarize what is in `records/`.

## Output
A single markdown file in `evolution/reports/`. Show the user the path and a 3-line summary inline.
