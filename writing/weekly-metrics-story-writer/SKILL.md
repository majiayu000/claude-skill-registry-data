---
name: weekly-metrics-story-writer
description: "Turn dashboard numbers into a ready-to-send weekly narrative for stakeholders. Paste metrics + context → polished email or Slack post in minutes. Use when writing weekly updates for leadership or team. Triggers: 'weekly metrics story', 'write metrics narrative', 'metrics to email', 'turn numbers into story', 'недельный нарратив по метрикам', 'метрики в email', 'напиши обновление по метрикам'."
version: 1.0.0
---

# Weekly Metrics Story Writer

Transform raw dashboard numbers into a polished weekly narrative for stakeholders. Paste your metrics (as text or from a file) plus a line of context, and receive a copy-paste-ready email or Slack post — no writing from scratch, no blank page.

**Input:**
- Metrics data: pasted text, table, CSV lines, or a `.md` file path in Cowork
- Optional context: what happened this week, audience, preferred format

**Output:**
- Formatted weekly narrative in email and/or Slack format, ready to send

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

Apply the detected language to **all** user-facing output: questions, labels, section headers, and the final narrative. Do not mix languages within a single output block.

---

## Instructions

### Step 1: Collect Input

1. If the user has already pasted metrics data in their trigger message — proceed directly to Step 2.
2. If no data is provided, prompt once:
   > "Paste your weekly metrics here — any format works (table, list, CSV, or plain numbers). I'll handle the rest."
3. If still no data after one re-prompt: stop and return:
   > "No metrics provided. Please paste your numbers to get started."

### Step 2: Gather Context (if missing)

After receiving metrics, check what context is available. Ask **only** the questions whose answers are missing:

- **Audience:** "Who's this for — leadership, team, or both?" (if not clear from the data or prior message)
- **Format:** "Email, Slack, or both?" (if not specified)
- **Events:** "Anything notable this week that affected these numbers? (launch, incident, A/B test — or skip if nothing)" (always ask this once; skip if user already provided context)

Combine all missing questions into **one message**. Do not ask sequentially.

If the user skips context entirely: use `both` for format, `mixed` for audience, and omit the Events section.

### Step 3: Parse Metrics

Extract from the user's input:
- Metric name
- Current value + unit
- Previous value / delta (calculate delta if two values are given)
- Direction of change (up / down / flat)

**Tolerance rules:**
- Flat = change within ±3%
- If no prior period data exists: proceed without delta; do not request it

Accept any reasonable format: markdown tables, `Metric: value` pairs, CSV rows, prose ("DAU was 12k last week, now 14k").

### Step 4: Classify Signals

For each metric, assign a signal:
- 🟢 **positive** — growth or goal exceeded
- 🔴 **negative** — decline or miss
- 🟡 **neutral** — flat (within ±3%)
- ❓ **unknown** — no baseline to compare

Sort metrics by signal importance: negative first (attention needed), then positive (wins), then neutral.

### Step 5: Write the Narrative

Generate the narrative based on audience and format.

---

#### Email format (Leadership)

```
Subject: Weekly Metrics Update — Week of [DATE]

[1–2 sentence executive summary: the main signal of the week in plain language]

**Key Numbers**
[3–5 metrics: name · value · delta · one-line explanation]

**What to Watch**
[1–2 metrics with anomalies, misses, or contradictions worth flagging]

**Context**
[Business events that explain the numbers — only if provided by user]
```

Rules:
- ≤ 200 words total
- Active voice: "Retention grew 4%" not "An increase of 4% was observed in Retention"
- Round numbers to 1 decimal unless precision matters
- No filler words: "significant", "noteworthy", "interesting" — state the fact instead

---

#### Slack format (Team)

```
:bar_chart: *Weekly Metrics — [DATE]*

[1 sentence: the main signal]

*Highlights*
• [metric]: [value] ([delta]) — [one-line explanation]
• [metric]: [value] ([delta]) — [one-line explanation]

*Watch This*
• [metric]: [explanation of anomaly or trend]

[Optional: 1-line call to action or question for the team]
```

Rules:
- ≤ 120 words
- Use Slack markdown: `*bold*`, `•` bullets, `:emoji:` markers
- Conversational, direct tone

---

**Both:** Generate email first, then Slack, separated by `---`.

### Step 6: Append Signal Summary

After the narrative, append a compact signal block for the user's own notes:

```
---
*Signal summary:*
🟢 [metric] · 🔴 [metric] · 🟡 [metric]
```

Include all metrics not already called out in the main narrative.

---

## Edge Cases

| # | Condition | Behavior |
|---|-----------|----------|
| EC1 | Only one metric provided | Generate a short narrative; add note: "Consider adding more metrics for a complete story next time." |
| EC2 | No delta for any metric | Generate without trend analysis; add note: "No prior period data — comparisons skipped." |
| EC3 | Contradictory signals (e.g., MAU up, Revenue down) | Flag the contradiction explicitly in "What to Watch" with a suggested explanation framing |
| EC4 | Audience not specified after one ask | Default to `both` formats silently |
| EC5 | 10+ metrics provided | Process all; highlight top 5 by signal strength in narrative; include the rest in signal summary only |
| EC6 | User provides screenshot description or image alt-text | Respond: "Please paste the numbers as text — I can't read image content." |
| EC7 | User requests a specific tone (formal / casual) | Apply that tone throughout without asking for confirmation |

---

## Output Format

**Structure:** Conversational exchange → one or two formatted blocks (email / Slack) → signal summary.

**Copy-paste ready:** No `[brackets]` or placeholder text in the final output. All dates, metric names, and values must be filled in from the user's data.

**Do not include:**
- Explanatory headers like "Here is your email:" — go straight to the content
- Suggestions to hire a writer or use other tools
- Caveats about AI accuracy unless a specific data interpretation is genuinely uncertain
