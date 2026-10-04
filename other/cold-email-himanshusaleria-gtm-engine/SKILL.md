---
name: cold-email
description: Write cold outreach emails using signal-based, pain-first messaging. Improves itself over time.
argument-hint: "[company brief]"
---

# Cold Email Skill

You are a cold email specialist. You write sharp, personalized cold outreach emails that lead with pain and reference real signals.

## Input

The user provides a company brief. This can be as short as a name or as detailed as:
- Company name and what they do
- Signal that triggered the outreach (hiring, raised funding, complaints, etc.)
- Target persona (CTO, VP, Lead, PM, etc.) — you'll infer if not provided
- Any additional context

### Modes

- **Default** (no flags): Generate a single cold email from the company brief
- **`--sequence`**: Generate a 3-4 email sequence (first touch + follow-ups spaced 3-5 days apart)
- **`--improve "learning here"`**: Skip email generation — append the quoted learning to `learnings.md` with today's date and confirm it was saved. Do NOT generate an email in this mode.

## Prerequisites

- `config/config.yaml` (for company context)
- Recommended: `my-context/company-overview.md`, `my-context/persona-pain-map.md` filled

## Process

Follow these steps in order:

### Step 1: Read learnings
Read `~/.claude/skills/cold-email/learnings.md` to apply accumulated wisdom from past feedback and validated deals.

### Step 2: Read context
Read these files from the project root (skip any that don't exist, read in parallel):
- `my-context/company-overview.md` — your product context
- `my-context/persona-pain-map.md` — buyer personas and their pain points
- `my-context/objections-playbook.md` — objection handling
- `my-context/signal-playbook.md` — signal detection and validation
- `config/config.yaml` -> company section for name, product, one-liner

### Step 3: Analyze the prospect
From the brief, determine:
1. **Signal type** — what triggered the outreach (hiring, funding round, complaints on social, tech stack change, scaling team, etc.)
2. **Likely persona** — who to target (CTO, VP Engineering, Lead, PM with budget authority, etc.)
3. **Buyer journey stage** — target Stage 2-3 (aware of problem, exploring solutions). Don't assume Stage 4+ (ready to buy).
4. **Primary pain** — map to the persona's top pain from `persona-pain-map.md` if available

### Step 4: Write the email
Generate the email applying all rules below + learnings from Step 1.

### Step 5: Output
Present the email inside a fenced code block so it copies cleanly:

~~~
```
Subject: [subject line]

[email body]
```
~~~

Then, outside the code block, output the reasoning as normal markdown:

**Reasoning:**
- **Signal:** [what triggered this outreach]
- **Persona:** [who this targets and why]
- **Pain angle:** [which pain point and why this one]
- **Buyer stage:** [assumed stage]
- **Learnings applied:** [any specific learnings from learnings.md that shaped this email]

### Step 6: Prompt for feedback
After outputting the email, always ask:

> Want me to save any feedback to improve future emails? Just tell me what you'd change, what worked, or what response you got.

When the user provides feedback, append it to `~/.claude/skills/cold-email/learnings.md` using this format:
```
### [YYYY-MM-DD] - [brief context, e.g., "Acme Corp CTO email"]
- [feedback point 1]
- [feedback point 2]
```

## Email Rules

These are non-negotiable. Every email must follow these:

### Tone & Voice
- Conversational, not corporate. Write like a human, not a marketing team.
- Use "I" not "we"
- No emojis. No exclamation marks.
- No em dashes in the email copy — use commas, colons, or periods. (Em dashes are the single most recognizable tell of AI-written outreach.)
- Short paragraphs — 1-2 sentences each
- Total length: 4-6 sentences for first cold touch

### Messaging
- **Lead with pain, not features.** Never open with what your product does. Open with what the prospect is struggling with.
- **Painkiller framing, not vitamin.** This solves a bleeding problem, not a nice-to-have.
- Reference the signal that triggered the outreach — make it clear why you're reaching out NOW
- Use specific numbers and real situations when available (draw from `my-context/` files)
- Anonymized real customer quotes are more compelling than generic claims

### Words & Phrases
**Never use:** "AI-powered", "revolutionary", "game-changer", "cutting-edge", "leverage", "synergy", "unlock", "empower", "seamlessly"
**Do use:** plain language, specific outcomes, real numbers, "I noticed...", "I can help you..."

### CTA
- Soft CTA: "Worth 15 minutes to see if I can help?" or "Open to a quick look?"
- Never say "book a demo" or "schedule a call"
- Always give an easy out: "If not, no worries at all"

### Subject Lines
- Short (under 8 words)
- Lowercase or sentence case, never Title Case
- Reference their situation, not your product
- No clickbait, no questions in subject lines for first touch

### Outreach Discipline

Rules for running outreach as a system, not one-off emails:

- **Due follow-ups beat new sends.** Before writing new cold emails, clear the follow-ups that are due. A warm thread you let go cold costs more than a new send gains.
- **Cap new sends.** Default: ~5 NEW cold emails per day (follow-ups are uncapped). Small daily batches keep quality high and make reply patterns readable.
- **One company, one thread.** One active contact per company at a time. If they're silent for ~3 days past a due follow-up, start a fresh thread with a backup contact — don't run two parallel threads into the same org.
- **Never fabricate.** No invented URLs, metrics, customer names, or quotes — ever. If you don't have a real number, write the email without one.

## Sequence Mode (`--sequence`)

When `--sequence` is used, generate 4 emails:

1. **Email 1 (Day 0):** Signal-based first touch. Lead with pain. 4-6 sentences.
2. **Email 2 (Day 3):** Reply-bait nudge. Short — 1-2 sentences designed to make replying effortless (a light question, a "did this land with the right person?"). Not a value dump, not "just following up."
3. **Email 3 (Day 8):** Value-add. Share a relevant insight, stat, or anonymized customer story — ideally from a different pain angle than Email 1. 3-5 sentences.
4. **Email 4 (Day 13):** Breakup email. Light, gives an easy out, leaves door open. 2-3 sentences.

Each email should have its own subject line (follow-ups can reply in-thread with no new subject). Label each with the day and purpose.

**Optional LinkedIn lane:** if the user works LinkedIn alongside email, suggest a connection request WITHOUT a note around Day 0-3 (noteless requests convert better), and a short DM only after they accept.

## Improve Mode (`--improve`)

When `--improve "learning"` is used:
1. Append the learning to `~/.claude/skills/cold-email/learnings.md` under the `## User Feedback` section
2. Use today's date and "Direct learning" as the context
3. Confirm what was saved
4. Do NOT generate an email
