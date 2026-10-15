---
name: copy-quality
description: Audit and rewrite website copy that reads as generic, inflated, repetitive, vague or machine-written - buzzwords, empty claims, symmetrical sentences, filler, generic CTAs - while keeping the personality that belongs to the product. Context-aware, evidence-only, no over-correction. Use when reviewing a landing page, product page, portfolio or any interface text before it ships.
---

# /copy-quality

The goal is not to make every site read like documentation. The goal is copy that is **clear, specific and natural**, and that sounds like the product it describes. Change a line only when the new version is clearer, more specific, more truthful or better suited to its context. If the original passes, leave it alone.

Related skills:
- `/interface-copy` writes microcopy from scratch: buttons, errors, empty states.
- `/template-tells` finds a generated look across visuals and code.

This skill audits and rewrites the words that are already on the page.

## 0. Collect the copy and the facts

- Extract every visible string per page in reading order: headings, body, buttons, links, labels, alt text, meta title and description.
- Gather the **facts you are allowed to use**: what the product actually does, real numbers, real customers, real constraints. Ask for missing facts. **Never invent features, numbers or customers.**

## 1. Identify the context before judging

Each context sets how much personality and how much technical detail is right.

| Context | Personality | Detail | Notes |
|---|---|---|---|
| Hero | high | low | One idea. What it is and who it's for, in under ~12 words. |
| Landing / company page | medium–high | medium | Argument in order: promise → proof → ask. |
| Product description | medium | high | Concrete nouns and verbs; what it does, not what it "is designed to" do. |
| Feature section | medium | high | Lead each feature with the outcome, then the mechanism. |
| Pricing | low | high | Exact prices, periods, limits, what happens at the end of a trial. |
| CTA | medium | — | The verb names the result: "Start a trial", "Book a call". |
| Navigation | none | — | Plain nouns users already know. |
| Button | low | — | 1–3 words, verb first, specific. |
| Onboarding | warm | medium | One step at a time; say why each step matters. |
| Documentation | low | very high | Direct, imperative, consistent terms. |
| Error message | calm | high | What happened, why, what to do next. No blame. |
| Empty state | warm | medium | What will appear here, plus the action that fills it. |
| Dashboard | none | high | Labels and units, not sentences. |
| Portfolio | high | medium | First person, real projects, real outcomes. |
| AI product | medium | high | Show the task being done; say what it can't do. |
| Developer tool | low–medium | very high | Real API names, code, limits, numbers. |
| Creative studio | high | low–medium | Voice matters. Cut only what's vague or untrue. |
| SaaS | medium | high | Specific jobs, honest pricing, proof with numbers. |

## 2. What to detect

Run the scan, then read every flagged line in context. A flag is a question, not a verdict.

```bash
# Buzzwords and inflation (case-insensitive, whole words)
rg -n -i -w "seamless(ly)?|powerful|effortless(ly)?|beautiful(ly)?|innovative|revolutionary|revolutioni[sz]e|next-generation|next-gen|cutting-edge|unlock|elevate|supercharge|transform(ative)?|unleash|game-chang(er|ing)|world-class|best-in-class|robust|leverage|empower|synergy|reimagine|state-of-the-art|holistic|delightful" src content
# Template phrasing
rg -n -i "designed to|built to help|whether you're|in today's|take .* to the next level|look no further|we believe|at the intersection of|more than just" src content
# Unsupported claims
rg -n -i -w "fastest|best|leading|#1|most powerful|industry-leading|trusted by|enterprise-grade|production-ready|guaranteed" src content
# Em-dash density: lines with two or more dashes
rg -n "—.*—" src content
```

Then read for what grep can't find.

- **Empty marketing:** a sentence that could describe any product ("A platform for modern teams").
- **Vague descriptions:** no noun you could point at, no verb you could watch happen.
- **Adjectives doing the work:** remove the adjective. If the sentence says nothing, the sentence was the problem.
- **Repetitive structure:** three paragraphs that start the same way, every heading shaped "Verb your noun", identical sentence lengths.
- **Symmetric tells:**
  - "Not X, but Y" used more than once on a page;
  - "Fast. Simple. Secure." triplets;
  - lists of three where the third item is filler;
  - mirrored clauses ("Less A, more B").
- **Filler openings:** "Welcome to…", "In a world where…", "We're excited to…". Start with the point.
- **Redundancy:** the body restating the heading; two sentences that say the same thing.
- **Excess em dashes:** more than one per paragraph usually means two sentences glued together.
- **"Designed to / built to / helps you":** say what it does ("Syncs your calendar", not "Designed to help you sync your calendar").
- **Generic CTAs:** "Learn more", "Get started", "Click here", "Submit" where a specific action exists.
- **Name repetition:** the product name in every sentence. Use "it" once the subject is clear.
- **Inconsistency:** one thing with two names ("workspace" and "team"), Title Case mixed with Sentence case, "sign in" and "log in" both.
- **Unclear references:** "this", "it" or "that" with no clear antecedent.
- **Overcomplicated sentences:** more than ~25 words, nested clauses, three ideas joined with "and".
- **Passive voice** where the actor matters ("Your data is encrypted" → "We encrypt your data at rest").
- **Template feel:** if you can swap the product name for a competitor's and nothing breaks, it isn't specific yet.

## 3. Rules for rewriting

**Specificity.** Replace praise with information: a task, an object, a number, a constraint.

| Instead of | Prefer (only if it's true) |
|---|---|
| An innovative platform designed to revolutionise how modern teams collaborate. | Plan projects, assign work and track progress in one workspace. |
| Lightning-fast performance. | Pages load in under a second on a phone on 4G. |
| Seamless integrations. | Connects to Slack, GitHub and Google Calendar. |

**Claims.** Never add "fastest", "best", "leading", "#1", "most powerful", "revolutionary", "industry-leading", "trusted by thousands", "enterprise-grade" or "production-ready" without evidence the user supplied. If a claim is already there and unsupported, flag it, and either ask for the evidence or rewrite it into a checkable statement.

**SEO.** Write for the person first. Use the words searchers actually use where they fit naturally, in the title, the `h1` and the first paragraph. Never repeat a keyword unnaturally, never write headings only for keywords, never insert unrelated terms. If it reads awkwardly aloud, it's wrong. For page-level search work, see `/seo-auditor`.

**Accessibility.**
- Buttons and links say where they go or what they do: "View pricing", "Read the documentation", "Browse components".
- Headings are meaningful on their own.
- Link text makes sense out of context.
- Instructions are short and ordered.
- Error messages name the field and the fix.

**Global audience.** Prefer common words, one idea per sentence and standard terms. Keep idioms, slang and culture-specific references rare and intentional. Define abbreviations once. Global doesn't mean bland: keep the voice and lose the obscurity.

**Don't over-correct.** Don't turn:
- creative copy into a manual;
- marketing into documentation;
- a brand voice into corporate neutral;
- a portfolio into a spec sheet.

A vivid image, a dry joke or a confident short line is personality, not slop, as long as it is specific and true.

## 4. Principles drawn from strong product sites

These come from studying product sites known for clear copy: Linear, Stripe, Vercel, Raycast and Things by Cultured Code. Borrow the principles, never their wording, slogans or voice.

1. **Concrete verbs and nouns carry the feature.** The task being done is named, not praised.
2. **Evidence sits next to the claim.** A number with its unit and timeframe, a named customer outcome, a real interface state.
3. **Structure repeats so content can vary.** Every feature gets the same short shape (outcome, mechanism, proof), so readers can scan and pick their depth.
4. **Rhythm follows urgency.** Short lines where a decision is made; longer, plain sentences where something complex is explained.
5. **CTAs match the reader's stage.** Exploring ("See how it works"), deciding ("Compare plans"), committing ("Start a trial"), each worded as its result.
6. **Restraint is the personality.** Warmth and wit come from precise word choice and understatement, not from exclamation or superlatives.
7. **Depth is progressive.** Plain value first, then specifics, then technical detail for those who want it.

From the style references (ASD-STE100, Google's developer documentation style guide, Apple's Human Interface Guidelines on writing), in summary:

- one meaning per word, used consistently;
- short sentences and active voice;
- address the reader directly where it helps;
- no ambiguous words;
- respectful and direct, never cute at the user's expense;
- technical precision when the reader is technical.

## 5. Output format

For each change:

> **Original** — the existing copy.
> **Problems** — exactly what's weak (vague, unsupported claim, generic CTA, repetitive structure…).
> **Rewrite** — the new copy.
> **Why** — one line on what improved.

Group the changes by page and section. List lines you kept on purpose under **Kept**, with a word on why, so the review shows judgement and not just deletion. List missing facts under **Needs evidence**.

## 6. Vitrine voice

When auditing Vitrine itself (tryvitrine.dev), keep its personality: **premium, creative, precise, calm, confident, slightly unconventional**. Short declarative lines, concrete craft detail (timings, materials, behaviours) and quiet wit are on-voice. Enterprise filler and hype are not. The test: does it read as *designed, not generated*?

## 7. Final test, for every rewritten line

1. Is it clearer?
2. Is it more specific?
3. Is every claim true?
4. Does it sound natural read aloud?
5. Does it fit the product?
6. Does it fit the audience?
7. Is the filler gone?
8. Is the useful personality still there?
9. Is it free of generic AI phrasing?
10. Would a thoughtful product team publish it?

Any "no" means revise again. If the original already passed, restore it.
