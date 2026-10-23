---
name: plain-copy
description: >-
  Write or edit marketing copy so a stranger understands it in one read and it doesn't sound machine-written — ads, banners, landing-page blocks, cold emails, support and retention messages, research reports. Removes AI patterns (rhetorical triples, punchy fragments, clever circumlocutions, invented authority), fixes numbers without context, keeps the author's voice. Use when writing or reviewing any customer-facing text, or when copy "sounds like AI", "is unclear", "too clever", "too long". Triggers: "make this plainer", "this sounds like AI", "edit this copy", "tighten this".
---

# Plain copy

One test decides everything: **would a person who has never heard of the product understand this line in one read, and know why it matters to them?**

The rules below are corrections collected from real review rounds on ads, landing pages, emails and support messages. Each one is a rejection that happened. Examples are in `references/patterns.md`.

## How to work

1. **Identify the job of the text** — ad or banner, landing-page block, email, support message, report. Rules differ slightly; the sections below say where.
2. **Read the product facts first** if a facts file exists (`product-marketing.md`, `brief.md`, `products.md`). Never add a fact, number, feature or claim that is not in the source.
3. **Write or edit line by line**, applying the rules.
4. **Self-check** with the list at the end before showing anything.
5. **When editing someone else's copy, show the rewrite, not advice about it.** One line of why per change.

When choosing between shortening and punching up — **shorten**.

## Rules for every text

### Clarity
- **One direct thought per line.** Not a comparison in two moves ("agencies charge $5k… / get it for 80% less"). State the benefit directly.
- **The subject is the product, the verb is what it does.** "One tool schedules every interview" reads instantly; "One setup for your whole hiring calendar" doesn't say what is offered.
- **Name the object.** "Save 6 hours a week" — whose hours? "Save 6 hours a week per recruiter."
- **A two-clause line shows its own join.** Don't leave the reader to connect two statements; spend the extra words on "because" or "so".
- **Check who "you" and "your" point at.** If the line is aimed at the support agent, "your customer" is right and "your team" is not.
- **Speak it aloud.** "ISO 27001:2022, GDPR, HIPAA" is a register; "Fully GDPR compliant, ISO and HIPAA certified" is a person talking.

### Numbers
- **Every number is instantly clear or removed.** If a reader asks "why that many?", the number fails.
- **One number per ad or banner.** Two competing numbers cancel each other.
- **No unexplained figures** anywhere — say what was measured, when and by whom.

### AI patterns to remove
- **Rhetorical triples** — "what works, what doesn't, and what's next". Pick the one that matters.
- **Punchy one-line fragments** — "Not a sales call." "No setup. No code. No stress."
- **Clever circumlocution** — "people doing my job in companies like ours" → "people responsible for growth".
- **Authority inserts nobody asked for** — WCAG, GDPR, SOC 2, ISO, HIPAA, "industry-leading", "enterprise-grade", "(per W3C…)". If the source doesn't mention it, don't add it. If removing a phrase doesn't weaken the selling point, it was padding.
- **Performative warmth** — "it just feels wrong to let you walk", "give it a proper shot".
- **Em dashes** — go easy; one per paragraph at most.

### Voice
- **Keep the author's generalisations.** "Most teams still hire an agency for this" is voice, not an error. Demand a source (or remove) only for specific, checkable claims: a number or percentage, a price, a date, a named company's feature or plan, a ranking, a legal or regulatory statement, a statistic presented as fact.
- **Long prose is not a defect.** Don't chop a clear paragraph into bullets to look scannable.
- **Proven copy stays word for word.** If a block already converts, change only what must change (the headline, the platform name, the screenshot) and leave the rest.
- **Don't describe the category negatively.** Show the product working well on hard cases instead of listing how everything else fails.
- **Never promise what can't be guaranteed** — "identical speed for everyone", "today", "within the hour".

## By text type

**Ads and banners.** The hook lands the essence immediately: either what the product is ("A live AI note-taker for {sales} calls") or a pain a stranger recognises, with who, what and the obstacle. A mechanism, a feature or a number is never the opening line — it belongs in line two. Headline ≈ 40 characters or less, as a real sentence. Copy doesn't repeat what the visual already shows. One script per idea with a swappable slot beats six different phrasings of the same idea.

**Landing pages.** The headline names the reader's problem or benefit; the mechanism goes in the subhead. Reuse sections that already work instead of reinventing them. Platform and product names in full ("Microsoft Teams", not "Teams").

**Cold email.** Short plain sentences, literal wording, no triples, no dramatic fragments. Readers in marketing recognise LLM-written email instantly, and that kills the reply rate.

**Support and retention.** Chat, not email — often one sentence is enough. No empathy openers. No timeframes you can't guarantee ("until your subscription ends", "3–5 business days, depending on your bank"). Retention offers help the person actually use the product ("let me help you set it up"), never "keep it, just in case". Ask, don't push: "Would that work for you?"

**Reports and docs.** Full sentences, every term explained at first use, a link for every fact, neutral tone, no personal address. Write for the least technical reader first.

**Facts files for bots and agents.** Write only what is true now. Change a fact in place when it changes; never keep the old value "as a warning" — agents read it anyway.

## Self-check before showing

- [ ] A stranger understands every line in one read.
- [ ] Every line resolves — into what the product does or what the reader gets. No "and so what?"
- [ ] Every number is clear, sourced and alone in its line.
- [ ] No triples, no fragments, no authority inserts, no performative warmth.
- [ ] Nothing added that isn't in the source facts.
- [ ] Shorter than the draft, unless clarity needed the words.

For a second opinion on ad copy, run the `copy-critic` subagent from this kit.

## Adapt it

Every time you correct a piece of copy, add the correction to `references/patterns.md` as a before / after with one line of why. After a month the file is your house style, and the skill writes like you.
