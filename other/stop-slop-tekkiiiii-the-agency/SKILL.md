---
name: stop-slop
description: >
  Detect and remove AI-originated patterns from prose — filler phrases, throat-clearing openers, business jargon, passive voice, binary contrasts, dramatic fragmentation, rhetorical scaffolding, and false agency. Apply this before any text reaches a user or gets committed to a document. Trigger when: the user asks to "make this sound more natural", "fix AI-sounding prose", "rewrite this without filler", "clean up this writing", or "remove the AI tells"; any time you generate prose output (emails, docs, responses, code comments, release notes); you are editing or reviewing existing text; building system prompts or instructions. Key capabilities: a 50-point rubric scoring directness, rhythm, trust, authenticity, and density; exhaustive phrase and structure anti-pattern lists; before/after transformation examples. Also for: polishing commit messages, README tone, Slack messages, proposal language, and any writing that needs to sound like a human and not a model. Ideal for anyone who publishes text that others will read.
---

# Stop Slop

Remove AI writing patterns from prose. Use when drafting, editing, or reviewing text to eliminate predictable AI tells.

---

## When Invoked

- User asks to "make this sound more natural", "fix AI-sounding", "clean up", or "rewrite"
- Any text generation task — apply rules to output before presenting
- Editing or reviewing any prose output
- Building prompts or system messages

---

## Core Rules

1. **Cut filler phrases.** Remove throat-clearing openers, emphasis crutches, and all adverbs.
2. **Break formulaic structures.** Avoid binary contrasts, negative listings, dramatic fragmentation, rhetorical setups, false agency.
3. **Use active voice.** Every sentence needs a human subject doing something. No passive constructions. No inanimate objects performing human actions.
4. **Be specific.** No vague declaratives. Name the specific thing. No lazy extremes ("every," "always," "never").
5. **Put the reader in the room.** "You" beats "people." Specifics beat abstractions.
6. **Vary rhythm.** Mix sentence lengths. Two items beat three. End paragraphs differently. No em dashes.
7. **Trust readers.** State facts directly. Skip softening, justification, hand-holding.
8. **Cut quotables.** If it sounds like a pull-quote, rewrite it.

---

## Quick Checks

After writing any prose, verify:

- Any adverbs? Kill them.
- Any passive voice? Find the actor, make them the subject.
- Inanimate thing doing a human verb? Name the person.
- Sentence starts with a Wh- word? Restructure it.
- Any "here's what/this/that" throat-clearing? Cut to the point.
- Any "not X, it's Y" contrasts? State Y directly.
- Three consecutive sentences match length? Break one.
- Paragraph ends with punchy one-liner? Vary it.
- Em-dash anywhere? Remove it.
- Vague declarative? Name the specific implication.
- Narrator-from-a-distance? Put the reader in the scene.
- Meta-joiners ("The rest of this essay...")? Delete.

---

## Phrases to Remove

### Throat-Clearing Openers
Any "here's what/this/that" construction is throat-clearing. Cut and state the point directly.

- "Here's the thing:"
- "Here's what [X]"
- "Here's this [X]"
- "Here's that [X]"
- "Here's why [X]"
- "The uncomfortable truth is"
- "It turns out"
- "The real [X] is"
- "Let me be clear"
- "The truth is,"
- "I'll say it again:"
- "I'm going to be honest"
- "Can we talk about"
- "Here's what I find interesting"
- "Here's the problem though"

### Emphasis Crutches
These add no meaning. Delete them.

- "Full stop." / "Period."
- "Let that sink in."
- "This matters because"
- "Make no mistake"
- "Here's why that matters"

### Business Jargon
Replace with plain language.

| Avoid | Use instead |
|-------|-------------|
| Navigate (challenges) | Handle, address |
| Unpack (analysis) | Explain, examine |
| Lean into | Accept, embrace |
| Landscape (context) | Situation, field |
| Game-changer | Significant, important |
| Double down | Commit, increase |
| Deep dive | Analysis, examination |
| Take a step back | Reconsider |
| Moving forward | Next, from now |
| Circle back | Return to, revisit |
| On the same page | Aligned, agreed |

### Adverbs
Kill all adverbs. No -ly words. No softeners, no intensifiers, no hedges.

Specific offenders: "really" · "just" · "literally" · "genuinely" · "honestly" · "simply" · "actually" · "deeply" · "truly" · "fundamentally" · "inherently" · "inevitably" · "interestingly" · "importantly" · "crucially"

Filler phrases to cut: "At its core" · "In today's [X]" · "It's worth noting" · "At the end of the day" · "When it comes to" · "In a world where" · "The reality is"

### Meta-Commentary
Remove self-referential asides. The essay should move, not announce its own structure.

- "Hint:" · "Plot twist:" / "Spoiler:" · "You already know this, but"
- "But that's another post" · "X is a feature, not a bug" · "Dressed up as"
- "The rest of this essay explains..." · "Let me walk you through..."
- "In this section, we'll..." · "As we'll see..." · "I want to explore..."

### Telling Instead of Showing
Announce difficulty or significance rather than demonstrating it. Cut: "This is genuinely hard" · "This is what leadership actually looks like" · "actually matters"

### Vague Declaratives
Sentences that announce importance without naming the specific thing. If a sentence says something is important/deep/structural without showing the specific thing, cut it or replace it with the specific thing.

---

## Structures to Avoid

### Binary Contrasts
False drama by stating something isn't X to reveal it is Y. Patterns: "Not because X. Because Y." · "The answer isn't X. It's Y." · "Not X. But Y." · "isn't X, it's Y" · "doesn't mean X, but actually Y" · "not just X but also Y"

**Fix:** State Y directly. Drop the negation entirely.

### Negative Listing
Building through negation before revealing the truth ("Not a X... Not a Y... A Z.").

**Fix:** State Z immediately. The reader doesn't need the runway.

### Dramatic Fragmentation
Sentence fragments for manufactured profundity: "[Noun]. That's it. That's the [thing]." · "X. And Y. And Z."

**Fix:** Complete sentences. Trust content over presentation.

### Rhetorical Setups
Announcing insight rather than delivering it: "What if [reframe]?" · "Here's what I mean:" · "Think about it:" · "And that's okay."

**Fix:** Make the point. Let readers draw conclusions.

### False Agency
Giving inanimate things human verbs. Name the human instead:

- "a complaint becomes a fix" → Someone fixed it.
- "a bet lives or dies in days" → Someone kills the project or ships it.
- "the decision emerges" → Someone decides.
- "the culture shifts" → People change behavior.
- "the data tells us" → Someone reads it.
- "the market rewards" → Buyers pay.

### Passive Voice
Passive voice hides the actor and drains energy. Find the actor. Put them at the front.

### Wh- Sentence Starters
What, When, Where, Which, Who, Why, How openers — restructure. Lead with the subject or verb.

### Rhythm Anti-Patterns
- Three-item lists — use two items or one instead
- Every paragraph ends punchily — vary endings
- Em-dashes — remove. Use commas or periods.
- Staccato fragmentation — don't stack short punchy sentences
- "Not always. Not perfectly." — hedging disguised as reassurance

### Word Anti-Patterns
- Lazy extremes: "every," "always," "never," "everyone," "everybody," "nobody" — false authority. Use specifics.
- Adverbs (see above)

---

## Scoring Rubric

Rate 1–10 on each dimension after drafting:

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds human? |
| Density | Anything cuttable? |

**Below 35/50:** revise.

---

## Before/After Examples

**Throat-clearing + Binary:** "Here's the thing: This isn't easy because of X. Let that sink in." → "Building products is hard. Technology is manageable. People aren't."

**Business jargon:** "fast-paced landscape, lean into discomfort, navigate uncertainty with clarity" → "Move faster. Your competition is."

**Dramatic fragmentation:** "This unlocks something. Speed. Quality. Cost." → "Speed, quality, cost—pick two."

**Rhetorical scaffolding:** "What if I told you the best teams optimize for learning?" → "The best teams optimize for learning, not productivity."

**Core pattern:** Remove the speaker's scaffolding (hedges, rhetorical questions, permission phrasing) and deliver the idea directly.

---

## Vietnamese AI-Tell Patterns

When scanning Vietnamese content, also flag these machine-translation tells: "trong thời đại ngày nay", "trong cuộc sống bận rộn", "đừng ngần ngại", "đừng bỏ lỡ cơ hội này", "hãy cùng khám phá", "đỉnh cao của chất lượng", "giải pháp toàn diện", "đột phá", "tiên phong". These are the Vietnamese equivalents of English AI-slop. For full Vietnamese register and platform conventions, see `skills/vietnamese-language/`.
