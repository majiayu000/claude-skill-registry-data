---
name: session-postmortem
description: "Use when a past or running agent session went wrong and the operator wants to know why (repeated work, ignored plan, a skill that did not fire, slow or costly): pin the problem down, read the transcripts read-only, report with path:line evidence."
---

# session-postmortem

Cross-cutting (`WORKFLOW.md` §2), applied to a session rather than a product. It reports what happened,
with evidence; it does not fix, export or file anything.

**Core rule: every finding cites `path:line`. No citation, no finding.** Every number comes from the
transcript or from a command that was run, never from memory.

## When
After a session that repeated work, ignored its plan, stalled, skipped an expected skill, or cost more
than expected, and someone wants the cause.

## Steps

1. **Intake, one question at a time**, until there is a statement naming the session, the turn range if
   known, what was expected, what happened, and the observable that matters (wall-clock, tokens, a
   repeated action). "It took too long" is a complaint, not a statement. Nothing below starts before the
   operator has answered; if they are away, write the questions and stop.
2. **Locate the transcripts.** Resolve each session to absolute paths. Confirm a past session by quoting
   its first prompt and timestamp. List every candidate rejected, with the reason, or write "none".
   Enumerate subagent transcripts too; in those, the "user" is the parent agent.
3. **Context safety, every file, every time.** One record can be a megabyte.
   - Measure first (`wc -lc`, list lines over a size threshold).
   - Never print a transcript to read it. Get line numbers and counts first, then small fields from named
     lines, cut to a few hundred characters.
   - Anything longer than that for one record means the slice was too wide.
4. **Analyse in seven dimensions**, in parallel where the transcript is long, splitting by turn range:
   1. timeline of skills fired and not fired;
   2. adherence to the plan, compaction points first;
   3. repeated work;
   4. stumbles (errors, retries, dead ends);
   5. quality evidence (was success shown or asserted);
   6. conflicts between requests;
   7. cost and time.
   Discard any returned finding without `path:line`.
5. **Report**: the verdict first, then findings in the order of the operator's complaint, each with its
   citation, then what could not be determined.

## Output / checkpoint
No pipeline checkpoint. A report with cited findings and an explicit coverage note (what was and was not
read).

## Guardrails
- **Read-only.** Never modify, move or delete a session file.
- **Operator words only.** Hook output, system reminders and tool results are not the operator's prompts.
- **Report, do not diagnose the framework.** State what the transcript shows; whoever triages decides
  whether a block changes. No advice unless asked.
- No bundle export, no issue drafting, no scrubbing: out of scope here by choice.

## Origin
Mechanism rewritten from the `diagnosing-superpowers` skill of the `superpowers` collection (MIT), read
2026-10-02: the intake-before-analysis gate, rejected-candidate listing, the seven analysis dimensions, the
path:line rule and the transcript context-safety procedure. Left out: bundle export, scrubbing, issue
writing and similar-session search. Wording and structure are ours. Not run on real work.
