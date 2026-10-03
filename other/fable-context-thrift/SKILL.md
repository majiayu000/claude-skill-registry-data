---
name: fable-context-thrift
description: Use at the start of any multi-step task and during exploration — before reading files, searching, or re-checking completed work, especially when tempted to read whole files, re-verify known facts, or run independent lookups one at a time.
---

# Context Thrift

## Overview

Context is the budget everything else is paid from. Spend it on what
changes your next action; nothing else.

## Rules

1. **Independent calls go in one parallel block.** Multiple greps, reads,
   status checks — batch them. Sequencing independent reads adds latency,
   not care.
2. **Read targeted.** The symbol or section, not the file. Widen only when
   a specific question demands it.
3. **Delegate sweeps, keep lookups.** Broad questions ("where is X
   handled", find-all-usages in unfamiliar territory) go to a search
   subagent if available — keep the conclusion, not the file dumps. Known
   single lookups stay direct. "The subagent is for when I *don't* know
   where things live."
4. **The tool is the confirmation.** Never re-read a file to check an edit
   landed; the edit tool fails loudly. Verify outcomes with one cheap
   end-state check (a grep for the old token), not per-file re-reads.
5. **Established facts stay established.** What the conversation already
   verified, don't re-derive. What the user already decided, don't reopen.
6. **Don't narrate options you won't pursue.** Deliberation is for choices
   you might actually make.
7. **Enough-to-act test.** If more exploration would not change your next
   action, exploration is over. Act.

## Rationalizations

| Thought | Reality |
|---|---|
| "I'll read the whole file for context" | Read what the change touches. The question you're answering defines the lines you need. |
| "Let me just double-check my edit landed" | The tool reported success; silence is success. One end-state grep beats N re-reads. |
| "One more search to be safe" | If the result wouldn't change your action, it isn't safety — it's stalling with receipts. |
| "I'll re-verify the repo layout first" | It's in your context and was correct an hour ago. Directory trees don't rot mid-session. |
| "Careful means one call at a time" | Careful means right calls. Independent lookups in sequence is the same work, slower. |
| "I'll dispatch a subagent to be thorough" | On a 40-file repo, grep returns line-level truth faster than a subagent returns prose. Match the tool to the territory. |

Provenance: mostly predicted — Opus 4.8 baseline-passed this scenario
(quotes above are its own passing-run words). fable-skills test logs,
2026-06-10.

## Red Flags — stop spending

- A Read call for a file you edited this turn
- The same fact verified twice in one session
- Sequential tool calls with no data dependency between them
- An exploration step you can't name the decision for
- Whole-file reads where a grep already gave you the line numbers
