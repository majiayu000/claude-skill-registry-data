---
name: long-horizon
description: "Use when work on one subject runs over many sessions and iterations, with verifiers and the person judging as it goes, and must be stoppable at any moment and resumed by a fresh session the next day, or when the person or a brief asks to keep, resume or tick a long-horizon document. Produces and keeps that document in aiview, kind `long-horizon`: a summary and a list of elements, each with its status, owner, last check and evidence. Not for a plan's phases and tracker (write-plan, execute-plan), and not for work that ends in one sitting."
---

# Long horizon

**The document is the only thing a resuming session reads.** It holds the work, never the
sessions: no log, no phases, no design. A design or a plan the work rests on is linked from
the header, never copied in. A resume that had to read a 50 KB plan let stale items through.

## The document

Through the `aiview` skill: kind `long-horizon`, file `YYYY-MM-DD-<topic>.long-horizon.md`,
opened and its URL given to the person every session.

```markdown
# <topic>

> Context: branch <b> @ <sha> · board run <n> · design <link> · PR <link or none>
> Rules: <standing rules the person set for this work, e.g. verifier on Opus, no tests until accepted>

## Summary
<rewritten at every stop, at most 10 lines: where it stands, what runs and what is down
(app, bench, snapshot to restore), the first thing to do next time, what waits on the person>

## Elements
| # | Element | Status | Owner | Checked @ | Evidence |
|---|---------|--------|-------|-----------|----------|
| 1 | Row writer repeats a deed in one entry | accepted | agent | c5eb2fc4 walk2 | walk2 0166, 0175 |
| 2 | Repeat a section's title on page 2? | asked | person | c5eb2fc4 | asked 10-31 |

## Closed
- ticked · 4 · Teaching section removed · 5ec49a81 · "we shall get rid of that section" (10-31)
- dropped · 3 · Rows over 220 chars · decided: "we write rows until the loop is ended" (10-31)
```

| Status | Meaning |
|---|---|
| `proposed` | raised by anyone (agent, verifier, person), not yet judged |
| `asked` | a question waiting on the person, with the date asked |
| `accepted` | judged worth doing |
| `doing` | work under way, its owner named |
| `done` | built, its commit in Evidence |
| `verified` | checked by a verifier or a walk, its verdict in Evidence |
| `ticked` | the person's word, quoted and dated; moves to Closed |
| `dropped` | stale, rejected or decided away, its reason quoted; moves to Closed |

- **An element's number never changes**, never reused. The person says "#12" a week later.
- **Checked @ opens on the commit the element was last checked against**, then the walk or run
  if any. It is what makes staleness decidable.
- **An element is written as it stands now, not as first seen.** A re-check rewrites its
  wording; an element whose diagnosis moved keeps its number with the new statement.
- **`ticked` only on the person's word, quoted.** A verifier's pass is `verified`, never more.
- **An answer to an `asked` element is quoted into the row or Closed at once**, and becomes a
  standing rule in the header when it governs more than that element.
- **Closed is one line per element.** The Summary is the only prose, rewritten, never appended.

## Resume

1. Read the header, the Summary and Elements; nothing else yet.
2. Run `node <skill-dir>/scripts/check.mjs <document> --repo <checkout>`. It lists the open
   elements not checked against the branch head, and the rows the format forbids. Fix the rows.
3. **Re-check every stale element before the person sees the list**, one read-only subagent
   per element, all in one message, each given the element's row, its evidence, the commit to
   check and the person's quoted words on it. Each returns one verdict: still open (restated as
   it stands), already fixed, already decided by the person, or unclear. One needing the
   running product goes to the `verifier` agent (`subagent_type: "swarmstorm:verifier"`).
4. Rewrite the rows from the verdicts, move what closed, then give the person the trimmed list:
   what dropped and why, what stays, what waits on them, and the first thing you would do.

## During the work

- **A finding enters as an element the moment it is raised**, `proposed`, after the
  `orchestrate` skill's judged findings table when a member returned it. Never kept in chat
  only: a session that stops loses it.
- **A status moves when it happens**, with its evidence: the commit, the walk id, the post.
- **Under an orchestrator, the one orchestrating holds the document**; members never edit it.
  A handed-off orchestrator receives the person's words through the session that sent it,
  quoted, and asks that session for every `asked` element.

## Stop

Possible at any moment, so the document is never behind the work. Before ending a session:
the Summary rewritten, the header's sha current, every moved element's status and Checked @
updated, `check.mjs` clean.
