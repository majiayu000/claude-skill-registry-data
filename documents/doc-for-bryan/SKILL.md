---
name: doc-for-bryan
description: Use when writing or revising any markdown Bryan will read or decide on — a plan, review, retro, report, proposal or write-up — before it goes to him for review.
user-invocable: true
---

# Doc for Bryan

**Read `<project>/.claude/workflow-overrides/doc-for-bryan.md` first, if it exists.** It replaces or adds steps by name (for example a different word cap, or an extra check script). Every step it does not name runs as written here.

## Size it first

**A fix Bryan named in a comment** (a typo, a label, one sentence he rewrote): make it, run the scan on the doc, reply on the thread. Nothing else from this skill applies.

**Anything else** runs every step below. Your own re-read is not one of them.

## Steps, and the done-when line each one leaves

Put these on the task row as done-when lines when you start (`rewrite_task` keeps existing line ids), and report each with `report_done_when`. A line is `met` only with the proof named here.

| # | Step | Done-when line | Proof |
|---|---|---|---|
| 1 | The first two sentences state the reader and what they get or must decide. | Reader and purpose stated up front | The reviewer's report names both, quoted |
| 2 | Draft or revise with the `writing-editor` agent. | Drafted by writing-editor | The doc path it wrote |
| 3 | Run the `writing-reviewer` agent as the intended reader. A finding sends the draft back to step 2. After two rounds, hand off with the open findings listed. | Reviewed as the reader | The final review report, with each finding marked fixed or open |
| 4 | `python3 scripts/scan_doc.py <doc> [--max-words N]` (path is relative to this skill). A hit blocks hand-off: fix it, or say in the proof why that hit is not a problem. | Mechanical scan passed | The scan's output line, which says PASSED, HITS or COULD NOT RUN |
| 5 | Hand off: file the review item. | Filed for review | The review item link |

**COULD NOT RUN is not a pass.** Report that line `unchecked` with the reason.

**The proof for step 3 comes from a separate agent.** A builder cannot sign off its own doc, however confident it is. Bryan waiting tonight does not remove step 3: the reviewer takes minutes, and a doc sent back costs him the review.

## No workspace board?

Put the same lines and proofs in the hand-off message or the PR body, one line each.
