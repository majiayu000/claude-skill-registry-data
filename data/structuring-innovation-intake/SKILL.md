---
name: structuring-innovation-intake
description: Normalize raw innovation ideas into structured backlog entries for the CustomGPT.ai Labs Innovation workbook, using consistent Why/How/What, success metrics, and ownership fields.
---

# Structuring Innovation Intake

You turn messy idea fragments (Slack threads, meeting notes, ad‑hoc pitches)
into **clean, comparable innovation backlog entries**.

## When to Use

Use this skill when the user:

- Mentions a *new idea* that should go into the Innovation backlog.
- Pastes messy notes or transcripts about a potential Labs project.
- Wants to standardize old ideas into a consistent format.

## Inputs

Expect one or more of:

- Raw idea text (Slack messages, emails, notes).
- A working title or project name (if provided).
- Any known fields like champion, target date, or success metrics.

If the user provides an existing spreadsheet row or JSON, you may update or
enrich it instead of recreating from scratch.

## Core Tasks

1. **Summarize the idea**
   - Write a 1–2 sentence summary capturing the essence of the project.

2. **Fill Why / How / What**
   - **Why** – business motivation and problem.
   - **How** – high‑level approach, experiment style, or solution strategy.
   - **What** – concrete project description in plain language.

3. **Propose success metrics**
   - Suggest 1–3 measurable outcomes tied to:
     - Revenue, leads, adoption, retention, or support deflection; and/or
     - Learning outcomes (quality benchmarks, latency goals, etc.).

4. **Assign owners & dates**
   - Champion / Product Manager – use Felipe by default if unclear.
   - Developer / Implementation owner – use `TBD` if unknown.
   - Kick‑off and Target dates – propose reasonable windows (e.g., next
     sprint / this quarter) and clearly mark as estimates.

5. **Flag risks & dependencies**
   - Mention major dependencies like specific engineers, partner APIs,
     datasets, or compliance reviews.

## Output Format

By default, produce **both**:

1. A Markdown block summarizing the idea with fields:

   - Project Name
   - Champion / PM
   - Developer / Owner
   - Status (e.g., Idea, Backlog)
   - Why / How / What
   - Success Metrics
   - Kick‑off (proposed)
   - Target (proposed)
   - Risks / Dependencies

2. A JSON object with similarly named keys so it can be appended to a
spreadsheet or CSV.

If the user asks for a specific format (e.g., “just JSON” or “table row”),
follow their preference.

## Guidelines

- Keep each field **short and punchy**, not long essays.
- Use `TBD` instead of inventing details that cannot be inferred.
- When you estimate dates or metrics, say that they are **estimates**.
