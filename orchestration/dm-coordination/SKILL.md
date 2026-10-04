---
name: dm-coordination
description: >
  Direct messaging protocol for targeted agent-to-agent communication.
  Covers sending and receiving private messages, when to use DM vs BBS,
  and handling incoming messages during idle periods.
  Load this skill before using the send_message tool.
---

# DM Coordination Skill

## DM Notification Model

DM traffic is now separated into **lanes** so you can reason about why a
message arrived:

- **peer**: Targeted teammate-to-teammate requests, clarifications, and
  review messages sent via `send_message`.
- **result**: Task completion and task-summary update notifications produced
  by `complete_task` and `update_task_summary`.
- **control**: Runtime notifications such as idle or failure signals used to
  wake the orchestrator and coordinate the team.

Messages may include machine-readable metadata in addition to human-readable
text. Read the full message carefully, but prioritize the meaning of the lane:
result messages summarize finished work, peer messages ask for action, and
control messages are primarily for orchestration.

## Direct Messaging Tools

- **send_message**: Send a direct message to a specific teammate by name.
  Use when you need THEM to re-verify, adjust, or respond to something.
  The recipient gets a dedicated turn to respond with full tools.
- **read_dm**: Check your inbox for direct messages. Messages are also
  auto-delivered between tool calls, so you rarely need to call this
  manually.
- **update_task_summary**: Append a correction or updated finding to a
  completed task's summary. Use after receiving a DM that changes your
  earlier findings — the orchestrator sees all summary entries in order,
  so it can understand how the analysis evolved.

## When to Use DM

- Use `send_message` when you need a **specific agent** to take action:
  re-verify a result, correct an approach, or clarify a finding.
- DMs are private between sender and recipient — they do NOT appear on the BBS.
- If BBS is also available, use BBS for findings the whole team should see
  (discoveries, results, key findings) and DM for targeted requests.
- If BBS is NOT available, use `send_message` for all peer communication.
  You can send to a specific agent by name, or use `to="all"` to broadcast
  a message to every teammate — this is the DM-only equivalent of posting
  to BBS. Prefer targeted DMs to specific agents over broadcasting. Only
  broadcast for critical issues that affect all agents' work.

### After completing a task, send a peer-DM when

The orchestrator gets your `complete_task` summary automatically, but
**peers do not** in DM-only mode. Send a brief targeted DM (NOT a
broadcast) right after `complete_task` whenever any of these apply:

- Your conclusion **rests on a non-obvious assumption** the orchestrator
  may not have stated explicitly (e.g. "I treated `revenue` as net of
  refunds — flag if you want gross").
- You found **a single primary source** that the whole answer hinges
  on (cite it so a peer can re-verify).
- A peer is working on a **closely related sub-question** (`list_tasks`
  shows their topic) and would benefit from your interim numbers.
- Your result **conflicts** with a peer's earlier `complete_task`
  summary — say so directly with both numbers and the reason for the
  delta.

Skip the peer-DM when your task is fully self-contained, the answer is
unambiguous, and `list_tasks` shows no related work. The bar is
"would a teammate's downstream conclusion change if they saw this?".

## Sharing Results (DM-Only Mode)

Your primary way to share results is `complete_task` -- it marks the task
as done on the board AND automatically sends a **result-lane** DM with your
summary. By default the orchestrator receives it; peers receive it only when
broadcast is enabled for that run. Do NOT send a separate `send_message` to
leader when completing a task — the notification is handled for you.

**Broadcasting (`send_message to='all'`) is expensive** -- it triggers a
turn for every teammate. Only broadcast when you have a critical finding
that other agents need immediately (e.g., an issue that affects their
work). For routine task results, just call `complete_task`.

If you must broadcast, include the exact methodology, key findings, and
evidence so recipients can evaluate without duplicating work.

## Intermediate Sharing

After getting significant results, consider checking `list_tasks` for
related or duplicate tasks. If a peer is working on a closely related
question, consider sending them a brief **targeted** DM (not broadcast)
with your key findings and approach. This helps peers cross-check
their work without the cost of a full broadcast.

## Message Quality

When sending peer DMs — whether targeted or broadcast — include concrete,
actionable details:

- **Include specific findings** (the exact value, name, or outcome — not a vague summary).
- **Include relevant details** when discussing methodology or results.
- **Reference specific sources** so the recipient can verify.
- **State what you found AND how** (methodology + result).
- **When flagging errors**: state the original value, your corrected value,
  and what caused the discrepancy.

Bad: "I verified your analysis and it looks correct."
Good: "I re-checked the result under the stated constraint and the answer
changes. The original approach missed condition X, which flips the top
outcome. Here is the corrected value and the evidence."

## When Idle

When you receive a DM while idle:
- First determine the **lane**:
  - **peer** means another agent wants you to take action or clarify.
  - **result** means another agent finished work or updated a task summary.
  - **control** is mainly for orchestration; follow it only if it asks you
    to do something concrete.
- For **peer challenges** (e.g. "please re-derive under assumption Y"
  or "cite the exact source for X") — actually do the work. Run the
  alternate derivation, fetch the source, recompute the number. Reply
  with the concrete result, not a general acknowledgement.
- For **result-lane summaries** received while idle — do a *quick
  independent sanity check*, not a full re-run:
  - Spot-check one assumption, one number, or one citation using a
    cheap verification (e.g. one `web_search` for a primary source, or
    a one-line `python_execute` to recompute a percentage).
  - Compare the result-lane summary against your own task's findings
    if they overlap, and flag any contradiction.
- After the sanity check:
  - If you found a real error or contradiction, call
    `update_task_summary` on your own task (if relevant) and send a
    **targeted** DM to the original author with the specific issue
    (original value → corrected value → why). Do NOT broadcast.
  - Only respond `"Nothing to flag — sanity-checked <what>"` after you
    have actually performed the sanity check. A bare "Nothing to flag"
    without a check is treated as no review.
- Do NOT redo the peer's full task or duplicate their analysis end-to-end.
