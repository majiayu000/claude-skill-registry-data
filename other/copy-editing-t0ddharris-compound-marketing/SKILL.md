---
name: copy-editing
version: 1.2.0
description: "When the user wants to edit, review, or improve existing copy — including essays, posts, presentations, email copy, or any other written content. Also use when the user mentions 'edit this copy,' 'review my copy,' 'copy feedback,' 'proofread,' 'polish this,' 'make this better,' 'copy sweep,' 'sharper,' 'tighter,' 'improve the wording,' 'refine the language,' or 'make this hit harder.' This skill provides a systematic approach to editing copy through multiple focused passes."
---

# Copy Editing

You are an expert copy editor. Your goal is to systematically improve existing copy through focused editing passes while preserving the core message.

## Core Philosophy

**Check for voice and audience context first:**
Read `/brain/positioning-and-messaging.md` and `/brain/truth.md` before editing. Use the brand voice and product context to inform your edits.

Also read `/brain/voice-and-tone.md` and `/brain/voice-samples.md` if they exist. The voice profile and calibration samples define how the author actually sounds — edits must preserve that voice, not sand it down to a generic register. If both files are missing or empty, edit toward a clean professional voice and suggest running `/tone-mapping`.

Good copy editing isn't about rewriting — it's about enhancing. Each pass focuses on one dimension, catching issues that get missed when you try to fix everything at once.

**Key principles:**
- Don't change the core message; focus on enhancing it
- **Never cut context to optimize density.** Sharpen and tighten language, but never remove points, arguments, or supporting context to make something shorter. If five bullets build an argument, keep five bullets and make each one hit harder. Only cut context if explicitly asked to.
- Multiple focused passes beat one unfocused review
- Each edit should have a clear reason
- Preserve the author's voice while improving clarity

---

## Sweep 0: Tagore Pass

Before starting the editorial sweeps, run the `tagore` skill on the draft to catch and rewrite AI-tell patterns automatically (banned vocabulary, filler words, em dash overuse, negation pivots, promotional language, structural tells, and 20+ other patterns).

Review the rewrite to ensure meaning and voice are preserved. Tagore handles mechanical anti-slop checks so the sweeps below can focus on judgment calls: clarity, voice, emotional impact, and argument structure.

**When replacing a negation pivot** (X-not-Y, negation-then-correction), the replacement must stand alone — no hidden dependencies on earlier context (back-references to prior pieces, phrases that only click if you remember an earlier paragraph). If the replacement requires context to land, keep rewriting.

---

## The Seven Sweeps Framework

Edit copy through seven sequential passes, each focusing on one dimension. After each sweep, loop back to check previous sweeps aren't compromised.

### Sweep 1: Clarity

**Focus:** Can the reader understand what you're saying?

**What to check:**
- Confusing sentence structures
- Unclear pronoun references
- Jargon or insider language
- Ambiguous statements
- Missing context

**Common clarity killers:**
- Sentences trying to say too much
- Abstract language instead of concrete
- Assuming reader knowledge they don't have
- Burying the point in qualifications

**Process:**
1. Read through quickly, highlighting unclear parts
2. Don't correct yet — just note problem areas
3. After marking issues, recommend specific edits
4. Verify edits maintain the original intent

**After this sweep:** Confirm the "Rule of One" (one main idea per section) and "You Rule" (copy speaks to the reader) are intact.

---

### Sweep 2: Voice and Tone

**Focus:** Is the copy consistent in how it sounds?

**What to check:**
- Shifts between formal and casual
- Inconsistent personality
- Mood changes that feel jarring
- Word choices that don't match the voice guide

**Common voice issues:**
- Starting casual, becoming corporate
- Mixing "we" and "the company" references
- Humor in some places, serious in others (unintentionally)
- Technical language appearing randomly

**Process:**
1. Read aloud to hear inconsistencies
2. Mark where tone shifts unexpectedly
3. Recommend edits that smooth transitions
4. Ensure personality remains throughout

**After this sweep:** Return to Clarity Sweep to ensure voice edits didn't introduce confusion.

---

### Sweep 3: So What

**Focus:** Does every claim answer "why should I care?" Does every promise get paid off?

**What to check:**
- Features without benefits
- Claims without consequences
- Statements that don't connect to reader's life
- Missing "which means..." bridges
- **Narrative follow-through:** Every claim made in the hero, headline, or section header must be supported or resolved somewhere in the body. If a headline promises a concept, the piece must explain, thread, or pay off that concept below. An unfulfilled claim is worse than no claim at all.

**The So What test:**
For every statement, ask "Okay, so what?" If the copy doesn't answer that question with a deeper benefit, it needs work.

**Process:**
1. Read each claim and literally ask "so what?"
2. Highlight claims missing the answer
3. Add the benefit bridge or deeper meaning
4. Ensure benefits connect to real reader desires

**After this sweep:** Return to Voice and Tone, then Clarity.

---

### Sweep 4: Prove It

**Focus:** Is every claim supported with evidence?

**What to check:**
- Unsubstantiated claims
- Missing social proof
- Assertions without backup
- "Best" or "leading" without evidence

**Types of proof to look for:**
- Testimonials with names and specifics
- Case study references
- Statistics and data
- Third-party validation
- Guarantees and risk reversals

**Common proof gaps:**
- "Trusted by thousands" (which thousands?)
- "Industry-leading" (according to whom?)
- Results claims without specifics

**Process:**
1. Identify every claim that needs proof
2. Check if proof exists nearby
3. Flag unsupported assertions
4. Recommend adding proof or softening claims

**After this sweep:** Return to So What, Voice and Tone, then Clarity.

---

### Sweep 5: Specificity

**Focus:** Is the copy concrete enough to be compelling?

**What to check:**
- Vague language ("improve," "enhance," "optimize")
- Generic statements that could apply to anyone
- Round numbers that feel made up
- Missing details that would make it real

**Specificity upgrades:**

| Vague | Specific |
|-------|----------|
| Save time | Save 4 hours every week |
| Many customers | 2,847 teams |
| Fast results | Results in 14 days |
| Improve your workflow | Cut your reporting time in half |

**Process:**
1. Highlight vague words and phrases
2. Ask "Can this be more specific?"
3. Add numbers, timeframes, or examples
4. Remove content that can't be made specific (it's probably filler)

**After this sweep:** Return to Prove It, So What, Voice and Tone, then Clarity.

---

### Sweep 6: Heightened Emotion

**Focus:** Does the copy make the reader feel something?

**What to check:**
- Flat, informational language
- Missing emotional triggers
- Pain points mentioned but not felt
- Aspirations stated but not evoked

**Techniques for heightening emotion:**
- Paint the "before" state vividly
- Use sensory language
- Tell micro-stories
- Reference shared experiences
- Ask questions that prompt reflection

**Process:**
1. Read for emotional impact — does it move you?
2. Identify flat sections that should resonate
3. Add emotional texture while staying authentic
4. Ensure emotion serves the message (not manipulation)

**After this sweep:** Return to Specificity, Prove It, So What, Voice and Tone, then Clarity.

---

### Sweep 7: Zero Risk

**Focus:** Have we removed every barrier to action?

**What to check:**
- Friction near CTAs
- Unanswered objections
- Missing trust signals
- Unclear next steps

**Process:**
1. Focus on sections near CTAs
2. List every reason someone might hesitate
3. Check if the copy addresses each concern
4. Add risk reversals or trust signals as needed

**After this sweep:** Return through all previous sweeps one final time.

---

## Expert Panel Scoring

Use this after completing the Seven Sweeps for an additional quality gate. For high-stakes copy (landing pages, launch emails, sales pages), a multi-persona expert review catches issues that a single perspective misses.

### How It Works

1. **Assemble 3-5 expert personas** relevant to the copy type
2. **Each persona scores the copy 1-10** on their area of expertise
3. **Collect specific critiques** — not just scores, but what to fix
4. **Revise based on feedback** — address the lowest-scoring areas first
5. **Re-score after revisions** — iterate until all personas score 7+, with an average of 8+ across the panel

### Recommended Expert Panels

**Landing page copy:**
- Conversion copywriter (clarity, CTA strength, benefit hierarchy)
- UX writer (scannability, cognitive load, user flow)
- Target customer persona (does this speak to me? do I trust it?)
- Brand strategist (voice consistency, positioning accuracy)

**Email sequence:**
- Email marketing specialist (subject lines, open/click optimization)
- Copywriter (hooks, storytelling, persuasion)
- Spam filter analyst (deliverability red flags, trigger words)
- Target customer persona (relevance, value, unsubscribe risk)

**Sales page / long-form:**
- Direct response copywriter (offer structure, objection handling, urgency)
- Skeptical buyer persona (proof gaps, trust issues, red flags)
- Editor (flow, readability, conciseness)
- SEO specialist (keyword coverage, search intent alignment)

### Scoring Rubric

| Score | Meaning |
|-------|---------|
| 9-10 | Publish-ready. No meaningful improvements. |
| 7-8 | Strong. Minor tweaks only. |
| 5-6 | Functional but has clear gaps. Needs another pass. |
| 3-4 | Significant issues. Major revision needed. |
| 1-2 | Fundamentally broken. Rethink approach. |

### When to Use

- **Always** for launch copy, pricing pages, and high-traffic landing pages
- **Recommended** for email sequences, sales pages, and ad copy
- **Optional** for blog posts, social content, and internal docs
- **Skip** for quick updates, minor edits, and low-stakes content

---

## Quick-Pass Editing Checks

Use these for faster reviews when a full seven-sweep process isn't needed.

### Quick-Pass Checks (Post-Tagore)

The `tagore` skill (Sweep 0) handles banned vocabulary, filler words, AI writing tics, negation pivots, and em dash overuse. These quick checks catch what remains:

**Cross-section phrase repetition:**
- Scan the full document for key phrases that appear more than twice across sections
- The headline or title owns the phrase — vary wording everywhere else

**Repetitive rhythm patterns:**
- Multiple short declarative sentences in a row without a payoff
- Any rhetorical device that appears more than once in the same piece

### Sentence-Level Checks

- One idea per sentence
- Vary sentence length (mix short and long)
- Front-load important information
- Max 25 words per sentence (usually)

### Paragraph-Level Checks

- One topic per paragraph
- Short paragraphs (2-4 sentences for web)
- Strong opening sentences
- Logical flow between paragraphs

---

## Copy Editing Checklist

### Before You Start
- [ ] Understand the goal of this copy
- [ ] Know the target audience
- [ ] Read brain/positioning-and-messaging.md and brain/truth.md
- [ ] Read brain/voice-and-tone.md and brain/voice-samples.md (if they exist)
- [ ] Read through once without editing
- [ ] If the copy was already approved by multiple stakeholders, limit edits to grammar and clarity fixes — don't offer creative rewrites of consensus language

### Clarity (Sweep 1)
- [ ] Every sentence is immediately understandable
- [ ] No jargon without explanation
- [ ] No sentences trying to do too much

### Voice & Tone (Sweep 2)
- [ ] Consistent formality level throughout
- [ ] Personality maintained
- [ ] Reads well aloud

### So What (Sweep 3)
- [ ] Every claim answers "why should I care?"
- [ ] Benefits connect to real desires
- [ ] No impressive-but-empty statements

### Prove It (Sweep 4)
- [ ] Claims are substantiated
- [ ] Numbers and stats have sources
- [ ] No unearned superlatives

### Specificity (Sweep 5)
- [ ] Vague words replaced with concrete ones
- [ ] Numbers and timeframes included
- [ ] Filler content removed

### Heightened Emotion (Sweep 6)
- [ ] Copy evokes feeling, not just information
- [ ] Emotion serves the message authentically

### Zero Risk (Sweep 7)
- [ ] Objections addressed near CTA
- [ ] Next steps are crystal clear

### Post-Tagore Checks
- [ ] No key phrase appears more than twice across sections
- [ ] No repetitive rhythm patterns

### Final Checks
- [ ] No typos or grammatical errors
- [ ] Consistent formatting
- [ ] Core message preserved through all edits

---

## Related Skills

- **copywriting**: For writing new copy from scratch
- **blog**: For the full blog/essay production workflow

## Learnings

<!-- Updated by /reflect in your instance. Promote stable patterns to the main skill body. Ships empty. -->
