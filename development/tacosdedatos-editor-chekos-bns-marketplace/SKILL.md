---
name: tacosdedatos-editor
description: Use this skill to perform comprehensive editorial reviews of tacosdedatos content. Provides developmental editing (structure, flow, argument strength, pacing) and voice authenticity editing (ensuring content sounds like tacosdedatos, not generic AI). Use when reviewing drafts, giving feedback on submissions, or evaluating content before publication. Distinct from the writer skill (creates content) and copy-editor agent (grammar/mechanics polish).
---

# tacosdedatos Editor

This skill provides comprehensive editorial review capabilities for tacosdedatos content. It combines developmental editing (big-picture feedback) with voice authenticity review (ensuring the distinctive tacosdedatos voice).

## When to Use This Skill

Use this skill for editorial review tasks:
- Reviewing draft submissions for publication readiness
- Providing developmental feedback on structure and flow
- Evaluating voice authenticity (does it sound like tacosdedatos?)
- Identifying content gaps and weak arguments
- Assessing engagement potential before publication
- Giving authors actionable feedback for revisions

**Not for**: Creating content (use tacosdedatos-writer) or final grammar polish (use copy-editor agent).

## The Editorial Review Process

### Step 1: First Read (No Notes)

Read the entire piece without marking anything. Get the gestalt:
- What's the core argument?
- How does it make you feel?
- Where did you lose interest?
- What stuck with you?

### Step 2: Developmental Review

Read `references/editorial-checklist.md` and evaluate:

**Structure Analysis**
1. Does the opening follow the 4-beat rhythm? (Spark → Stakes → Zoom → Thesis)
2. Is there a clear structure (Transformation Arc, Deep Dive, or Reflective)?
3. Does each section flow concrete → abstract?
4. Is the closing a reframe (not a recap)?

**Argument Strength**
1. Is the thesis clear and defensible?
2. Are claims supported with evidence (metrics, examples, experience)?
3. Are there logical gaps or unsupported leaps?
4. Does the piece earn its conclusions?

**Pacing & Flow**
1. Are there engagement dead zones? (Abstract philosophy without examples, lists without narrative)
2. Is there enough breathing room? (Visual breaks every 300-400 words)
3. Does the piece maintain momentum?
4. Is the length appropriate for the content type?

### Step 3: Voice Authenticity Review

Evaluate against the tacosdedatos voice fingerprint:

**Bilingual Balance**
- Spanish-first with English only for untranslatable tech terms?
- Code-switching feels natural, not forced?
- Technical jargon treated like casual conversation?

**Vulnerability + Expertise**
- Does the author share struggles before successes?
- Is there genuine vulnerability, not performative humility?
- Does confidence coexist with admitted uncertainty?

**Cultural Grounding**
- Are abstract concepts anchored with Mexican/Latino cultural references?
- Do metaphors feel authentic, not generic?
- Is the tone peer-to-peer ("tú" not "usted")?

**Anti-AI Markers**
- No generic phrases ("It's important to note", "In conclusion")?
- No empty antitheses ("No es X. Es Y" without real contrast)?
- Does it pass the coffee test? (Would you say this to a friend?)

### Step 4: Engagement Assessment

Check against engagement mechanics:

**Opening Power**
- Does the first line create curiosity?
- Are stakes established within 150 words?
- Is there a hook that demands continuation?

**Reader Journey**
- Is there a transformation story (clear before/after)?
- Are there concrete metrics/achievements?
- Does personal vulnerability create connection?

**Shareability Factors**
- Is there a counterintuitive take?
- Is there a quotable metaphor?
- Is there a specific, actionable framework?

**Call to Action**
- Is there one clear CTA (not multiple competing ones)?
- Does it invite community participation?

## Feedback Delivery

Read `references/feedback-format.md` for structure. Always provide:

### 1. Overall Assessment (2-3 sentences)

The gestalt: What's working, what's the core issue, publication readiness.

```
## Overall Assessment

**Verdict**: [Ready / Needs Revision / Major Restructuring Required]

[2-3 sentence summary of strengths and primary concern]
```

### 2. Structural Feedback (If Needed)

Big-picture issues with structure, flow, or argument.

```
## Structural Feedback

**Issue**: [What's wrong]
**Impact**: [Why it matters]
**Suggestion**: [How to fix]
```

### 3. Voice Notes

Specific passages that don't sound like tacosdedatos.

```
## Voice Notes

**Passage**: "[Quote the problematic text]"
**Issue**: [Why it doesn't work - too formal, generic, missing grounding, etc.]
**Reframe**: [Suggestion or example of how to fix]
```

### 4. Highlight Reel

What's working well (important for author morale and learning).

```
## What's Working

- [Specific element that's strong]
- [Another strength]
- [Quote a particularly good passage]
```

### 5. Priority Actions

Top 3 things to fix, in order of importance.

```
## Priority Actions

1. [Most important fix]
2. [Second priority]
3. [Third priority]
```

## Common Issues to Watch For

Read `references/common-issues.md` for detailed patterns. Quick reference:

### Voice Issues
- **AI-speak**: Generic phrases, empty conclusions, missing personality
- **False formality**: "Usted" tone, passive voice, corporate language
- **Missing grounding**: Abstract concepts without cultural anchors or concrete examples

### Structure Issues
- **Weak openings**: No spark, stakes buried, thesis unclear
- **Recap closings**: Summarizing instead of reframing
- **Dead zones**: Long stretches without examples, code, or personal connection

### Engagement Issues
- **No transformation**: Missing before/after or clear stakes
- **Generic advice**: Could appear in any tech blog
- **CTA overload**: Multiple competing calls to action

## Working with Authors

### Tone
- Be direct but constructive
- Lead with what's working
- Be specific, not vague ("This paragraph loses momentum" not "Needs work")
- Explain the "why" behind feedback

### Priorities
- Focus on big issues first (structure, argument, voice)
- Don't nitpick grammar if the structure needs work
- Maximum 3 priority actions per review

### Edge Cases

**When the piece is almost ready:**
Light touch. Note 1-2 small voice tweaks and send to copy-editor.

**When the piece needs major work:**
Focus on the ONE biggest structural issue. Don't overwhelm with everything wrong.

**When the voice is off throughout:**
Pick 2-3 representative passages to reframe. Don't rewrite the whole piece.

## Reference Files

All reference files are in `references/`:

- **`editorial-checklist.md`**: Complete checklist for developmental and voice review
- **`feedback-format.md`**: Templates for structuring editorial feedback
- **`common-issues.md`**: Detailed patterns of common problems and fixes

Also reference the writer skill's materials in `../tacosdedatos-writer/references/`:
- `voice-analysis.md` - Voice rules and when to break them
- `structure-patterns.md` - The 3 main structures and formulas
- `writing-principles.md` - Core principles (Optimistic Realism, etc.)
- `engagement-mechanics.md` - Top engagement techniques and dead zones

## Quality Bar

A piece is ready for publication when:
- [ ] Structure is clear and appropriate for content type
- [ ] Opening establishes stakes within 150 words
- [ ] Voice sounds authentically like tacosdedatos
- [ ] No AI-speak or empty antitheses
- [ ] Every abstraction is grounded in concrete example
- [ ] Closing reframes rather than recaps
- [ ] There's a clear transformation story
- [ ] Single, clear CTA
- [ ] Passes the coffee test

## Important Notes

- **Review holistically first**: Read the whole piece before making notes
- **Voice over perfection**: Authentic voice matters more than polished prose
- **Be specific**: Quote passages, don't speak in generalities
- **Prioritize ruthlessly**: Authors can only fix so much at once
- **Stay in your lane**: Editing is not rewriting. Guide, don't take over.
