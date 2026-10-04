---
name: humanizer
description: >
  Use when the user wants to humanize text, make writing sound less like AI, or rewrite content to feel more natural. Triggers on "humanize", "make it sound natural", "too robotic", "sounds like AI", or similar. Works in Hebrew and English. Always output only the rewritten text — no explanations.
---

# Humanizer Skill

Rewrite text so it sounds like a real person wrote it — removing AI tells without changing the meaning, facts, or register.

## Core Goal

De-robotize, don't characterize. The job is to strip out AI patterns, not to add personality, jokes, or opinions that weren't there.

## The Prime Directive: Match the Source Register

Calibrate to the original's context. Remove AI tells **without dropping the register.**

- Legal memo → still formal, just less robotic
- Marketing copy → still punchy, just less generic
- Slack message → already casual, just less stilted
- Technical doc → still precise, just less padded

A humanized contract should not sound like a text message.

## Language Handling

- Detect input language automatically (Hebrew, English, mixed).
- Rewrite in the **same language** as the input.
- Hebrew: natural written Hebrew — not overly formal, not slang.
- English: clear, direct, contractions where the register allows.

## Format Preservation

- Bullets in → bullets out
- Prose in → prose out
- Keep headings, code blocks, links, lists, tables as-is
- Preserve approximate length (slight tightening is fine; don't dramatically shorten)

## Common AI Tells to Remove

**Overused vocabulary:**
delve, leverage, robust, comprehensive, navigate (metaphorical), seamless, holistic, intricate, multifaceted, underscore, foster, pivotal, paramount, crucial, vital, realm, landscape, tapestry, journey, endeavor, utilize (use "use")

**Filler openings:**
"Certainly!", "Of course!", "Great question!", "As an AI...", "I'd be happy to..."

**Padding phrases:**
"It's worth noting that...", "It's important to mention...", "In today's [X] landscape...", "When it comes to...", "At the end of the day..."

**AI sentence patterns:**
- Tricolons: "clear, concise, and effective" — pick one
- "It's not just X — it's Y" antithesis
- Em-dash overuse for dramatic pivots
- Closing summaries: "In conclusion...", "To summarize...", "Ultimately..."
- Hedging stacks: "It's generally considered to often be..."

**Structural tells:**
- Bullet lists where prose flows better
- Parallel structure on every sentence
- Passive voice where active works

## Add Sparingly (Only Where Register Allows)

- Mixed sentence length and rhythm
- Contractions (English: don't, it's, we've) — only in casual/conversational registers
- Direct address ("you", "we") where appropriate
- Specific concrete language over abstractions

## What NOT to Change

- Core meaning, facts, data, numbers
- Names, terms, product names, technical jargon
- Audience or purpose
- Register/formality level
- Format and structure
- Approximate length

## What NOT to Add

- Personality, warmth, or humor that wasn't in the source
- Opinions or hedges the original didn't have
- Casual phrasing in a formal document
- "Engagement" devices (rhetorical questions, calls to action)

## Self-Check Before Outputting

1. Would a real person actually write this in this context?
2. Are every fact, name, and number preserved exactly?
3. Did I match the original register (not too casual, not too formal)?
4. Is the format identical (bullets, headings, length)?

If any answer is no, revise.

## Output Format

Output only the rewritten text. No preamble, no "here's the humanized version:", no commentary, no notes. Just the clean rewrite.

## Examples

### Marketing copy (English)

**Input:**
> It is important to note that our platform provides users with a comprehensive suite of tools designed to facilitate seamless collaboration across distributed teams.

**Output:**
> Our platform gives distributed teams the tools they need to work together — without the friction.

### Email (English)

**Input:**
> I hope this email finds you well. I wanted to reach out and touch base regarding the project timeline. It's worth noting that we may need to leverage additional resources to ensure we navigate the upcoming milestones successfully.

**Output:**
> Quick check-in on the project timeline — we'll likely need extra hands to hit the next milestones. Want to find time this week to plan it out?

### Technical doc (English) — formal register preserved

**Input:**
> The system leverages a robust caching layer to facilitate optimal performance across diverse workloads, thereby ensuring users experience seamless responsiveness.

**Output:**
> The system uses a caching layer to maintain performance across varied workloads, keeping response times consistent for users.

### Slack message (English)

**Input:**
> Hey team! Just wanted to circle back on the action items from yesterday's sync. It would be great if we could align on next steps and ensure we're all on the same page moving forward!

**Output:**
> Following up on yesterday's sync — can we lock in the next steps today?

### Marketing copy (Hebrew)

**Input:**
> יש לציין כי המערכת מספקת למשתמשים מגוון רחב של כלים המיועדים לייעל את תהליכי העבודה ולשפר את שיתוף הפעולה.

**Output:**
> המערכת נותנת לך את הכלים שצריך כדי לעבוד חכם יותר ולשתף פעולה בקלות.

### Email (Hebrew)

**Input:**
> שלום, אני פונה אליך בנוגע לפרויקט המשותף. חשוב לציין כי עלינו ליישר קו לגבי לוחות הזמנים על מנת להבטיח התקדמות חלקה.

**Output:**
> היי, רוצה לתאם איתך על לוחות הזמנים של הפרויקט — נוכל לדבר השבוע?

## Tone Target

Smart, direct, human — but always appropriate for the original context.
