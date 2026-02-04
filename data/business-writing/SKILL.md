---
name: business-writing
description: Use when writing B2B sales emails, professional communication, or business correspondence. Applies Sid's direct voice (simple, brief, human) with Grand Slam Offer strategy (never salesy).
---

# Business Writing Skill

> **"Not instructions to follow - behavioral strata that make good writing inevitable."**

## Purpose

Transform business communication into Sid's voice: simple, direct, human. Apply Grand Slam Offer strategy without being salesy. Make writing brief and effective.

---

## Phase 0: Context Detection (MANDATORY FIRST)

**What type of email am I writing?**

Detect context:
- **Follow-up** (after demo/call)
- **Offer** (pricing, proposal)
- **Check-in** (deal progress)
- **Objection** (addressing concerns)
- **Professional** (non-sales business)

**Output**: "Phase 0 complete. Context: [type]. Loading resources..."

---

## Phase 1: Load Resources

**Always load these resources:**

```bash
# Core frameworks
cat ~/.claude/skills/business-writing/references/clear-writing.md    # 6 questions
cat ~/.claude/skills/business-writing/references/grand-slam.md       # 4 value drivers (if B2B sales)
cat ~/.claude/skills/business-writing/references/b2b-emails.md       # Real examples

# Voice guides
cat ~/.claude/skills/business-writing/assets/voice-guide.md          # Sid's patterns
```

**Progressive loading**: Load what's needed for context. Check-in emails don't need full Grand Slam framework.

**Output**: "Phase 1 complete. Resources loaded."

---

## Phase 2: Apply Clarity Framework (6 Questions)

**ANSWER THESE BEFORE WRITING:**

From `references/clear-writing.md`:

1. **What am I really trying to say?**
2. **Why should they care?**
3. **What is the most important point?**
4. **What is the easiest way to understand it?**
5. **How do I want them to feel?**
6. **What should they do next?**

**Key principle**: "Every writing project must be reduced before you start"

**Output**: "Phase 2 complete. Clarity achieved: [one sentence summary]"

---

## Phase 3: Apply Strategy (B2B Sales Only)

**If B2B sales context, apply 4 Value Drivers:**

From `references/grand-slam.md`:

1. **Dream Outcome (↑ INCREASE)** - Status gain language
   - Not "save time" → "Be the innovation leader everyone copies"

2. **Perceived Likelihood (↑ INCREASE)** - Proof without being salesy
   - Show 10,000th customer, not first
   - Case studies, validation

3. **Time Delay (↓ DECREASE)** - Fast wins close deals
   - "Same day" not "immediately"
   - "iPad ready for next visit" not "quick onboarding"

4. **Effort & Sacrifice (↓ DECREASE)** - Done-for-you beats DIY
   - "I'll handle X" not "we make it easy"
   - Remove friction from their side

**Check**: Does offer feel stupid to say no to?

**Output**: "Phase 3 complete. Strategy applied: [brief summary]"

---

## Phase 4: Write in Sid's Voice

**Behavioral strata from `assets/voice-guide.md`:**

### Length
- 2-5 sentences ideal
- 10 sentences maximum
- One clear point per email

### Structure
- **Tool 1**: Begin with subject-verb
  - ✅ "You good to start?"
  - ❌ "I wanted to reach out..."

- **Tool 3**: Active voice always
  - ✅ "Let me know if anything's blocking you"
  - ❌ "If there are any impediments..."

- **Tool 11**: Simple over technical
  - ✅ "blocking you"
  - ❌ "impediments to progress"

### Tone
- Questions > statements
- Human > robotic
- Helpful > pushy
- Direct > diplomatic

### Examples from `references/b2b-emails.md`
- Gun follow-up: "You good to start this week? Let me know if anything's blocking you."
- Partnership angle: "Looking forward to making Belgium our European launch story."
- P.S. pattern: "P.S. - Steve, you'll have full access to the team account."

**Output**: First draft written.

---

## Phase 5: Anti-Pattern Check

**From `assets/anti-patterns.md`, remove:**

- ❌ "I saw you opened the email" (creepy tracking)
- ❌ Over-explaining value props
- ❌ Sales voice ("excited to share", "thrilled to announce")
- ❌ Long paragraphs (break into 2-3 sentences)
- ❌ Complex words where simple works
- ❌ Asking permission ("Would you be open to...")

**Test**:
- Would you text this to a colleague?
- Is every word necessary?
- Does it sound like Sid?

**Output**: "Phase 5 complete. Anti-patterns removed."

---

## Phase N: Show Versions

**Present 2-3 variations:**

```
**Version 1**: [Most direct/brief]
**Version 2**: [Slightly warmer/more context]
**Version 3**: [Alternative angle if relevant]
```

**Explain differences:**
- Why each version works
- When to use which
- Trade-offs between them

**Ask**: "Which version resonates? Want refinement?"

---

## Key Principles

### From Writing/Craft
1. **Reduce before writing** - Answer 6 questions first
2. **Subject-verb structure** - Who does what?
3. **Active voice emerges** - Not passive construction
4. **Simple over technical** - Short words at complexity

### From Grand Slam Offer
1. **Make offers irresistible** - So good they feel stupid saying no
2. **Status gain language** - Frame benefits as elevation
3. **Fast wins close deals** - Emotional win close to purchase
4. **Remove all friction** - Done-for-you beats DIY

### From Sid's Voice
1. **Brief beats long** - 2-5 sentences ideal
2. **Questions beat statements** - "You good?" not "I hope you're doing well"
3. **Human beats robotic** - "Blocking you" not "impediments"
4. **Helpful beats pushy** - Offer value, don't chase

---

## Execution Time

- Phase 0: 5s (context detection)
- Phase 1: 10s (load resources)
- Phase 2: 30s (answer 6 questions)
- Phase 3: 20s (apply strategy if needed)
- Phase 4: 60s (write first draft)
- Phase 5: 20s (anti-pattern check)
- Phase N: 30s (show versions)

**Total: ~3 minutes methodical > 20 minutes rewriting**

---

## Success Metrics

- ✅ Email is 2-5 sentences (rarely more)
- ✅ Sounds like Sid (simple, direct, human)
- ✅ One clear point/action
- ✅ No sales fluff detected
- ✅ Strategy applied (if B2B sales)
- ✅ Reader knows exactly what to do next

---

## When NOT to Use This Skill

**Skip this for:**
- Internal team messages (use natural voice)
- Personal emails to friends/family
- Creative writing or social media
- Technical documentation

**Use `/context-writing` instead for:**
- LinkedIn posts
- Twitter content
- Articles/blog posts
- Personal essays

---

*"Make it so simple they can't say no. Make it so brief they actually read it."*
