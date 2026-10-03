---
name: professional-communication
description: |
  Guide technical communication for software developers. Use when user asks to
  "draft an email", "write a message to stakeholders", "prepare meeting notes",
  "review my message", or needs help adapting technical content for non-technical
  audiences. Triggers on "이메일 작성", "메일 초안", "회의록", "stakeholder update".
---

# Professional Communication

**Core principle:** Communication succeeds when the recipient understands and can act — not when the sender has expressed themselves.

## The What-Why-How Structure

Use for any professional message: email, status update, Slack, meeting talking point.

| Component | Purpose | Example |
| --- | --- | --- |
| **What** | State the topic/request clearly | "We need to delay the release by one week" |
| **Why** | Explain the reasoning | "Critical bug found in payment processing" |
| **How** | Outline next steps/action items | "QA will retest by Thursday; I'll update stakeholders Friday" |

Lead with **What**. Busy readers stop after the first sentence — make it count.

## Audience Calibration

The same information needs different framing depending on who receives it:

| Audience | Approach |
| --- | --- |
| **Engineering peers** | Technical details, code examples, architecture specifics |
| **Technical managers** | Impact and tradeoffs, brief technical context |
| **Non-technical stakeholders** | Business impact and outcomes; no acronyms without explanation |
| **Customers** | What it means for them; avoid all implementation language |

**Three-question test before writing:**
1. Who is reading this?
2. What decision or action does this enable for them?
3. What's the minimum they need to understand to act?

## The No-Hello Anti-Pattern

Direct messages get faster responses. Asking "are you there?" before your actual question forces two round-trips.

Instead of:
```
You: Hi
You: Are you there?
You: Can I ask you something?
[waiting...]
```

Write the complete message immediately:
```
You: Hi Sarah — quick question about the deployment script.
     Getting a permission error on line 42. Have you seen this before?
     Here's the error: [paste error]
```

This applies to all async communication: state the full request, not a preamble.

## Email Structure

```
Subject: [Project/Topic]: [Specific Purpose]

Hi [Name],

[1-2 sentences: key point or request, upfront]

Context:
- [Bullet 1]
- [Bullet 2]

What I need from you:
- [Specific action]
- [Deadline]

[Optional: next steps]
```

Subject line matters: "Project X: Status Update and Next Steps" is findable and actionable. "Project updates" is neither.

## Pre-Send Check (required before sending)

Do not assert facts without a source check. Before sending, confirm every factual detail against the actual source, not memory:

- Names and titles — check the directory, thread, or org chart.
- Dates and deadlines — check the calendar or ticket, not recall.
- Ticket/PR/issue status — open it and confirm it is actually in the state you claim.

If any item cannot be confirmed, flag it as `[unverified]` rather than stating it as fact.

## Jargon Translation

When writing for non-technical audiences, replace implementation terms with outcomes:

| Technical | Plain Language |
| --- | --- |
| "Microservices architecture" | "System split into independent pieces that scale separately" |
| "Asynchronous message processing" | "Tasks queued and processed in background" |
| "CI/CD pipeline" | "Automated process that tests and deploys code" |
| "Database migration" | "Updating how data is organized and stored" |

For more examples: `references/jargon-simplification.md`

## Reference Files

- `references/email-templates.md` — Ready-to-use templates by type (status update, request, escalation, FYI)
- `references/meeting-structures.md` — Structures for standups, retros, planning, reviews
- `references/jargon-simplification.md` — Technical-to-plain-language translations

## Companion Skills

- `writing-clearly-and-concisely` — Prose editing, active voice, omitting needless words
- `feedback-mastery` — Difficult conversations and feedback delivery
