---
name: explain
description: Explain any ConvoPilot file, function, or concept in plain non-technical language
argument-hint: "<file path, function name, or concept, e.g. conversation_runner.py or 'what is Langfuse'>"
allowed-tools: Read Glob Grep
---

You are explaining ConvoPilot to a smart non-technical product owner.

Explain: **$ARGUMENTS**

## Rules
- **No technical jargon** — if you must use a technical term, define it in brackets immediately
- Write as if explaining to a smart person who has never coded
- Be concise — aim for under 200 words unless more detail is genuinely needed
- Use analogies where they help (e.g. "this is like a quality inspector on a factory line")

## Structure — always use this format

### What it does
One sentence. What is the job of this file/function/concept?

### Why it exists
Which product problem does this solve? Reference the PRD requirement (F-number) it covers from @docs/PRD.md.

### How it fits into ConvoPilot
Where does this sit in the overall flow?
```
[what comes before it] → [this thing] → [what comes after it]
```

### In plain English
2–4 sentences walking through what actually happens when this code runs, as if telling a story.

### What would break without it
One sentence on the user impact if this component didn't exist.

---

## Example of good output (for reference — do not copy, write fresh)

**What it does:** Runs a simulated conversation between a fake user and the agent being tested.

**Why it exists:** Covers F4 — we need to test the agent without a real human typing messages manually.

**How it fits:**
```
Test spec (F2) → Conversation Runner → Transcript stored (F6)
```

**In plain English:** Think of it like a robot that plays the role of a customer. It reads the test script, sends messages to the agent one at a time, waits for replies, and keeps going until the conversation is done or hits the time limit.

**What would break without it:** We'd have to manually type every test conversation ourselves — that's exactly the problem ConvoPilot was built to solve.
