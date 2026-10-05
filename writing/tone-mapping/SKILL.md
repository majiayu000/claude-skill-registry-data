---
name: tone-mapping
version: 1.1.0
description: "Build a voice and tone profile from real writing samples. Trigger with /tone-mapping or when the user mentions 'tone mapping,' 'voice profile,' 'how do I sound,' 'brand voice,' 'writing style,' 'tone of voice,' 'voice extraction,' or 'make it sound like me.' Extracts patterns across eight dimensions and writes brain/voice-and-tone.md, then optionally brain/voice-samples.md with quoted calibration examples."
---

# Tone Mapping

Build a voice and tone profile by analyzing real writing samples. The output is `brain/voice-and-tone.md`, which content-producing skills read to match the user's natural voice.

---

## Why This Matters

Without a tone map, every skill produces generic-sounding output. With one, blog posts, social content, emails, and landing pages start sounding like the person who runs the company wrote them.

---

## Workflow

### Step 1: Collect Writing Samples

Ask the user:

> I need 3-5 real writing samples to map your voice. These should be things you wrote yourself (not edited by someone else) that sound most like you.
>
> Options:
> 1. **Paste directly** — copy text from LinkedIn posts, blog posts, emails, newsletters
> 2. **Link to a URL** — I'll fetch the content (LinkedIn articles, blog posts, personal site)
> 3. **Point to a file** — if you've dropped samples in `/incoming/`
>
> Which works best?

**Minimum:** 3 samples, ideally 500+ words total. More samples produce a better map.

**If they have fewer than 3 samples:** Accept what they have but flag that the profile will be approximate. Suggest they update it later as they produce more content.

**What makes a good sample:**
- Written by them, not ghostwritten or heavily edited
- Represents how they want to sound going forward (not how they used to write)
- Variety helps: a casual post, a technical explanation, an opinionated take

### Step 2: Extract Patterns

Analyze the samples across eight dimensions. For each dimension, identify the specific pattern with evidence (quote a short phrase from the sample).

#### The Eight Dimensions

1. **Sentence rhythm**
   - Average sentence length (short/medium/long)
   - Variation pattern (do they mix short punchy sentences with longer ones, or stay consistent?)
   - How they open paragraphs (statement, question, anecdote, data?)

2. **Vocabulary register**
   - Formal to casual spectrum (1-5 scale)
   - Technical density (do they use jargon freely, explain it inline, or avoid it?)
   - Industry-specific terms they default to

3. **Structural patterns**
   - How they organize arguments (top-down conclusion first? build-up? problem-solution?)
   - Use of lists vs. prose paragraphs
   - Paragraph length tendencies

4. **Pronouns and perspective**
   - First person ("I") vs. collective ("we") vs. second person ("you")
   - How they address the reader (directly? as a peer? as a student?)
   - Do they use "one" or passive voice to generalize?

5. **Hedging vs. conviction**
   - Do they qualify claims ("might," "could," "tends to") or state directly?
   - How they handle uncertainty (acknowledge it, skip past it, frame it as a question?)
   - Strength of opinionated statements

6. **Humor and personality markers**
   - Dry wit, self-deprecation, sarcasm, none?
   - Use of analogies and metaphors (frequent, rare, specific domain?)
   - Personality that comes through (irreverent? earnest? measured?)

7. **Punctuation and formatting habits**
   - Em dash usage (heavy user? never?)
   - Parenthetical asides (frequent, rare?)
   - Bold/italic patterns
   - How they use colons, semicolons, ellipses

8. **Opening and closing patterns**
   - How they start pieces (hook, question, bold claim, anecdote?)
   - How they end (CTA, summary, open question, provocative statement?)
   - Transition style between sections

### Step 3: Confirm with Sample Sentences

Before writing the profile, test it. Generate 3 sentences that apply the extracted patterns to a topic the user hasn't written about. Present them:

> Here's how your voice profile would sound on a new topic. Do these sound like you?
>
> 1. [sentence applying their rhythm + vocabulary + conviction level]
> 2. [sentence applying their humor/personality + structural pattern]
> 3. [sentence applying their opening style + pronoun usage]
>
> What's off? Too formal? Too casual? Missing something?

Iterate until the user confirms the voice feels right. This is the most important gate in the process.

### Step 4: Write voice-and-tone.md

Write the profile to `brain/voice-and-tone.md` using the template structure. Include:

- The eight dimension scores with evidence
- A "Voice DNA" summary (3-4 sentences capturing the overall feel)
- A "Do / Don't" quick-reference table
- 3 sample sentences as calibration anchors

### Step 5: Update references

If `brain/INDEX.md` exists, check whether it already lists `voice-and-tone.md`. If not, add it under the Brand section.

Tell the user:

> Voice profile saved to `brain/voice-and-tone.md`. Content skills (blog, social-content, copywriting, copy-editing, email-sequence, case-studies) read it when drafting and editing.
>
> To update your voice profile later, run `/tone-mapping` again with new samples.

### Step 6: Offer Calibration Samples (voice-samples.md)

The profile captures the measurable dimensions of the voice. Calibration samples capture what dimensions can't: signature moves, argument structures, and real quoted examples. Offer this step:

> Want me to also build `brain/voice-samples.md`? It's the positive companion to the profile — your signature moves with real quotes from your writing, so drafts don't just match your metrics but reuse your actual patterns. Works best with 5+ samples.

If yes, extract from the same samples (plus any new ones):

1. **The voice in one paragraph** — describe the voice the way you'd brief an editor
2. **Signature moves (3-7)** — recurring patterns that make the voice recognizable (e.g., analogy-first framing, parenthetical asides, self-deprecation, direct address). For each: what it is, 2-3 quoted examples **taken verbatim from the samples**, and how often to use it
3. **Structural patterns** — how pieces open and close, paragraph and subhead habits, with quoted examples
4. **Argument structures** — how they build a case (e.g., consensus-then-pivot, experience escalation), with the beats spelled out
5. **What this writer rejects** — patterns that never appear in their writing, stated concretely
6. **Specificity calibration** — how concrete the voice gets (names, numbers, tools vs. pattern-level)

Write to `brain/voice-samples.md` following the template structure. Confirm the signature moves with the user — show each move with its quotes and ask "is this actually you, or an artifact of one post?" Drop anything that appears in only one sample.

**Hard rule:** every example in voice-samples.md must be quoted verbatim from the user's real writing. If you can't quote it, don't include the move.

If `brain/INDEX.md` exists, list `voice-samples.md` there too.

---

## Rules

- Never fabricate sample quotes. Only quote from the user's actual writing samples.
- The voice profile is descriptive, not prescriptive. Capture how they actually write, not how a style guide says they should write.
- If samples conflict (one is casual, another formal), ask which register they want as their default and note the range.
- Don't over-index on a single sample. Patterns should appear across multiple samples to be included.
- If the user already has a `voice-and-tone.md`, show what would change and confirm before overwriting.
- The profile should be concise enough that skills can read it quickly. Target 150-200 lines max. No padding.
