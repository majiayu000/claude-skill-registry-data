---
name: case-study-capture
description: Log a manual observation about the current session. Invoke when the user runs /case-study-capture to record something noteworthy that automatic hooks cannot detect -- a successful pattern, a human override, a context architecture insight, or friction the hooks missed.
disable-model-invocation: true
allowed-tools: Bash, Read
argument-hint: [ observation description ]
---

# Capture Manual Observation

Record a single observation to the case study harness log. Follow these steps in order.

## Step 1: Get the observation

The user's observation is: $ARGUMENTS

If the arguments are empty, ask the user to describe what they observed and wait for their response
before continuing.

## Step 2: Classify the category

Based on the user's description and the current conversation context, assign exactly one category from
the list below. Do NOT ask the user to choose -- determine the category yourself.

| Category               | Use when                                                                                                                 |
|------------------------|--------------------------------------------------------------------------------------------------------------------------|
| `successful_pattern`   | Something the agent did well that is directly attributable to a harness decision (rule, skill, CLAUDE.md section, hook)  |
| `human_override`       | The user stepped in to correct something the harness should have prevented or guided                                     |
| `context_architecture` | An observation about where context lives (rule vs. skill vs. CLAUDE.md vs. memory) and whether that placement worked     |
| `friction`             | The agent misunderstood, went off-track, or hit a wall -- use when the automatic friction hook did not capture the event |
| `other`                | The observation does not fit the above categories                                                                        |

## Step 3: Generate a context summary

Write a 1-3 sentence summary of what was happening in the session when this observation occurred.
Include: what task was in progress, what the agent just did, and why the observation matters. This
summary provides context that the user's description alone may not capture.

## Step 4: Run the logging script

Invoke the script with the three values you determined above:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/write_manual_entry.py" \
  "<category>" \
  "<user_description>" \
  "<context_summary>"
```

Replace placeholders with the actual values. Quote each argument to preserve spaces and special
characters.

The script validates the category, constructs the JSONL entry with a UTC timestamp, and appends it
to `case-study-harness/data/manual-observations.jsonl`. It prints a confirmation line on success.

## Step 5: Confirm

Report to the user:

- The category you assigned and why
- The context summary you generated
- That the observation was logged (relay the script's confirmation)
