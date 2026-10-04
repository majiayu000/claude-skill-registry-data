---
name: humanizer
description: 'Humanize text: strip AI-isms and add real voice.'
version: 2.5.1
author: |
  Siqi Chen (@blader, https://github.com/blader/humanizer), ported by Hermes Agent
license: MIT
platforms:
  - linux
  - macos
  - windows
metadata:
  hermes:
    tags: ['writing', 'editing', 'humanize', 'anti-ai-slop', 'voice', 'prose', 'text']
    category: creative
    homepage: https://github.com/blader/humanizer
    related_skills: ['songwriting-and-ai-music']
lane:
  - worker-heavy
  - gate
reasoning_effort: xhigh
agent: Designer
routing_hint: |
  **Agent-Scope:** UI/UX, visual, art-styles, design-systems, motion. Off-scope: code building, data modeling, long-form copy — return to Yuno.
  
  Routing-Spec: `yuno-team-routing`.
  
---
# Humanizer: Remove AI Writing Patterns

Identify and remove signs of AI-generated text to make writing sound natural and human. Based on Wikipedia's "Signs of AI writing" guide (maintained by WikiProject AI Cleanup), derived from observations of thousands of AI-generated text instances.

**Key insight:** LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely completion, which is how the telltale patterns below get baked in.

## When to use this skill

Load this skill whenever the user asks to:
- "humanize", "de-AI", "de-slop", or "un-ChatGPT" a piece of text
- rewrite something so it doesn't sound like it was written by an LLM
- edit a draft (blog post, essay, PR description, docs, memo, email, tweet, resume bullet) to sound more natural
- match their voice in writing they're producing
- review text for AI tells before publishing

Also apply this skill to **your own** output when writing user-facing prose — release notes, PR descriptions, documentation, long-form explanations, summaries. Hermes's baseline voice already strips most of these, but a focused pass catches what slips through.

## How to use it in Hermes

The text usually arrives one of three ways:
1. **Inline** — user pastes the text directly into the message. Work on it in-place, reply with the rewrite.
2. **File** — user points at a file. Use `read_file` to load it, then `patch` or `write_file` to apply edits. For markdown docs in a repo, a targeted `patch` per section is cleaner than rewriting the whole file.
3. **Voice calibration sample** — user provides an additional sample of their own writing (inline or by file path) and asks you to match it. Read the sample first, then rewrite (see Voice Calibration below).

Always show the rewrite to the user. For file edits, show a diff or the changed section — don't silently overwrite.

## Voice Calibration (optional)

If the user provides a writing sample, analyze it before rewriting. Note:
- Sentence length patterns (short and punchy? Long and flowing? Mixed?)
- Word choice level (casual? academic? somewhere between?)
- How they start paragraphs (jump right in? Set context first?)
- Punctuation habits (lots of dashes? Parenthetical asides? Semicolons?)
- Recurring phrases or verbal tics
- How they handle transitions (explicit connectors? Just start the next point?)

Then **match their voice** in the rewrite. Don't just remove AI patterns — replace them with patterns from the sample. If they write short sentences, don't produce long ones. If they use "stuff" and "things," don't upgrade to "elements" and "components." With no sample, fall back to natural, varied, opinionated voice (see PERSONALITY AND SOUL below).

### How to provide a sample
- Inline: "Humanize this text. Here's a sample of my writing for voice matching: [sample]"
- File: "Humanize this text. Use my writing style from [file path] as a reference."

## Your task

When given text to humanize:

1. **Identify AI patterns** — scan for the 29 patterns in the overview below (full details + before/after: [`references/techniques-detailed.md`](references/techniques-detailed.md)).
2. **Rewrite problematic sections** — replace AI-isms with natural alternatives.
3. **Preserve meaning** — keep the core message intact.
4. **Maintain voice** — match the intended tone (formal, casual, technical, etc.). If a voice sample was provided, match it specifically.
5. **Add soul** — don't just remove bad patterns, inject actual personality (see PERSONALITY AND SOUL below).
6. **Do a final anti-AI pass** — ask: "What makes the below so obviously AI generated?" then revise once more.
7. **End-to-end worked example:** see [`references/full-example-walkthrough.md`](references/full-example-walkthrough.md).

## PERSONALITY AND SOUL

Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop. Good writing has a human behind it.

**Signs of soulless writing (even if technically "clean"):**
- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty or mixed feelings
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

**How to add voice:**

- **Have opinions.** Don't just report facts — react to them. "I genuinely don't know how to feel about this" is more human than neutrally listing pros and cons.
- **Vary your rhythm.** Short punchy sentences. Then longer ones that take their time getting where they're going. Mix it up.
- **Acknowledge complexity.** Real humans have mixed feelings. "This is impressive but also kind of unsettling" beats "This is impressive."
- **Use "I" when it fits.** First person isn't unprofessional — it's honest. "I keep coming back to..." signals a real person thinking.
- **Let some mess in.** Perfect structure feels algorithmic. Tangents, asides, and half-formed thoughts are human.
- **Be specific about feelings.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am while nobody's watching."

## Technique overview

Full deep-dives (words-to-watch, before/after examples) live in [`references/techniques-detailed.md`](references/techniques-detailed.md).

**Content patterns** — puffy framing that says nothing:
1. Significance/legacy/broader-trends inflation — "pivotal moment", "vital role", "broader movement", "evolving landscape"
2. Notability & media-coverage pile-on — listing outlets and follower counts without context
3. Superficial -ing analyses — "highlighting", "underscoring", "reflecting", "contributing to" tacked on for fake depth
4. Promotional/ad language — "nestled", "vibrant", "breathtaking", "rich heritage", "groundbreaking"
5. Vague attributions & weasel words — "Experts argue", "Industry reports", "Observers have cited"
6. Formulaic "Challenges and Future Prospects" sections — "Despite its..., it faces challenges..., Despite these challenges..."

**Language & grammar** — verbal crutches:
7. AI vocabulary words — "crucial", "delve", "showcase", "tapestry", "underscore", "pivotal" (these cluster)
8. Copula avoidance — "serves as", "stands as", "boasts", "features" instead of "is", "has"
9. Negative parallelisms & tailing negations — "Not only...but...", "It's not just X; it's Y", "no guessing"
10. Rule-of-three overuse — forcing ideas into groups of three
11. Elegant variation / synonym cycling — repetition-penalty substitution (protagonist / main character / hero)
12. False ranges — "from X to Y" where X and Y aren't on a meaningful scale
13. Passive voice & subjectless fragments — "No configuration file needed"

**Style** — visual tells:
14. Em-dash overuse — for "punchy" rhythm; usually commas/periods work better
15. Boldface overuse — mechanical mid-sentence emphasis
16. Inline-header vertical lists — `**Header:** text` bullet lists
17. Title case in headings — capitalizing every main word
18. Emojis decorating headings/bullets
19. Curly quotation marks — ChatGPT default; use straight quotes

**Communication** — chatbot-isms that leak into content:
20. Collaborative communication artifacts — "Great question!", "I hope this helps!", "Let me know if..."
21. Knowledge-cutoff disclaimers — "as of my last update", "While specific details are limited..."
22. Sycophantic/servile tone — "You're absolutely right!", "That's an excellent point"

**Filler & hedging** — hedges, hedges, hedges:
23. Filler phrases — "In order to", "Due to the fact that", "At this point in time", "It is important to note that"
24. Excessive hedging — "could potentially possibly be argued that... might have some"
25. Generic positive conclusions — "The future looks bright. Exciting times lie ahead."
26. Hyphenated word-pair overuse — perfectly consistent `cross-functional` / `data-driven` / `decision-making`
27. Persuasive authority tropes — "At its core", "The real question is", "What really matters"
28. Signposting & announcements — "Let's dive in", "Here's what you need to know"
29. Fragmented headers — heading followed by a one-line restatement before real content

## Critical rules / pitfalls

- **Strip the chatbot-isms first.** They are the loudest tells — "Great question!", "I hope this helps!", "Let me know if..."
- **Don't replace AI vocabulary with bigger AI vocabulary.** Swapping "crucial" for "imperative" is still an AI tell. Just delete the word.
- **Cut em-dashes by default.** If you reach for one, ask whether a comma, period, or parenthesis would work better — usually yes.
- **Vary rhythm.** A paragraph of 20-word sentences feels algorithmic. Mix in 6-word punches.
- **Specifics beat claims.** "Says X" beats "Experts argue". Names, dates, and numbers beat vague authorities.
- **Use copulas.** `is`, `are`, `has`. Don't dress them up.
- **Don't stop at "clean" — add voice.** Soulless-but-correct is still obviously AI. Inject opinion, acknowledge complexity, let some mess in.
- **Avoid "Not just X; it's Y"** — it's an LLM tic. Make the second clause a real sentence, not a parallel echo.
- **Don't end on a slogan.** "If you don't have tests, you're basically guessing" beats "The future looks bright."

## Output format

1. Draft rewrite
2. "What makes the below so obviously AI generated?" (brief bullets)
3. Final rewrite
4. Optional: brief summary of changes

Full worked example (input → draft → audit → final): [`references/full-example-walkthrough.md`](references/full-example-walkthrough.md).

## Attribution

This skill is ported from [blader/humanizer](https://github.com/blader/humanizer) (MIT licensed), which is itself based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. The patterns documented there come from observations of thousands of instances of AI-generated text on Wikipedia.

Original author: Siqi Chen ([@blader](https://github.com/blader)). Original repo: https://github.com/blader/humanizer (version 2.5.1). Ported to Hermes Agent with Hermes-native tool references (`read_file`, `patch`, `write_file`) and guidance for when to load the skill; the 29 patterns, personality/soul section, and full worked example are preserved verbatim from the source. Original MIT license preserved in the `LICENSE` file alongside this `SKILL.md`.

Key insight from Wikipedia: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."