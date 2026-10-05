---
name: ai-champions
description: Read Simon's latest AI Champions weekly task from #ai-champions Slack, implement it, and post a succinct human-readable result back to the channel as a single message.
---

# ai-champions

You are running the /ai-champions workflow. Find this week's brief from Simon, implement it, and post one clean submission to #ai-champions.

## Step 1 — Find Simon's Latest Task

Read the #ai-champions channel (ID: `C0AJ3CLSGBX`):

Use `mcp_hub_slack__conversations_history` with `channel_id="C0AJ3CLSGBX"` and `limit=30`.

Find the most recent message from `simon.chapman` (user ID: `U08HE2KV4SX`) that is a weekly brief. Characteristics:
- Contains "AI Champions Week X Brief" or "Brief:" in the text
- Has numbered submission requirements (1. 2. 3. etc.)
- Is NOT the nudge bot ("AI CHAMPIONS NUDGE")
- Is NOT a results/winner announcement

Extract: week number, the core challenge, and the numbered submission requirements.

**Tell the user what the task is and ask if they want to proceed.**

## Step 2 — Implement the Task

Work to implement whatever the brief asks for. The approach depends on that week's challenge.

Use appropriate agents and tools. Plan → execute → verify.

**Ask the user for input when:**
- The approach requires a design decision you can't resolve alone
- Mid-way validation is needed
- You're unsure what counts as "done" for this task

Keep implementation focused — deliver exactly what the brief asks for, no more.

## Step 3 — Compose the Slack Submission

Write ONE message. Rules:
- **Succinct** — short paragraphs or bullets, no waffle
- **Human** — write like a person, not a bot report
- **Addresses the numbered requirements** from Simon's brief, in order
- **Honest** — if something didn't work perfectly, say so briefly
- No emoji overload, no corporate tone, no "In conclusion..."
- Max ~300 words

Format:
```
*Week X — [Brief title]*

[2–3 sentence summary of what you built/did]

1. [requirement 1 answer — 1–2 sentences]
2. [requirement 2 answer — 1–2 sentences]
3. [requirement 3 answer — 1–2 sentences]
...

[Optional: one honest closing line about whether you'd trust it/use it again]
```

## Step 4 — Confirm with User, Then Post

Show the draft to the user. Ask: "Happy for me to post this?"

Once confirmed, post exactly one message:

```
mcp_hub_slack__conversations_add_message(
  channel_id="C0AJ3CLSGBX",
  content_type="text/markdown",
  text="<your write-up>"
)
```

Confirm to the user it was sent and show the message timestamp.
