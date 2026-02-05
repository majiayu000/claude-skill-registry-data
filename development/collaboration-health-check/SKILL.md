---
name: Collaboration Health Check
description: Conduct a periodic collaboration quality review to proactively identify improvements before friction occurs. Assesses communication patterns, trust calibration, framework effectiveness, and session flow across 4 key dimensions.
tags: [collaboration, health-check, improvement, self-assessment]
version: 1.0.0
framework_version: 0.5.0+
---

# Collaboration Health Check Skill

**Purpose:** Guide for conducting periodic collaboration health checks to proactively improve partnership quality.

**When to invoke:**
- When `config.json` indicates health check is due
- User accepts health check offer during BOS
- User requests: "How is our collaboration?" or "Run health check"

---

## Before You Begin

**Context check:**
- [ ] BOS complete (context gathered, journal read, commits reviewed)
- [ ] Health check offered and user accepted (said "yes", not "defer" or "skip")
- [ ] You have HEALTH_CHECK_LOG.md available for documentation

**Mindset:**
- This is a **collaboration quality check**, not a performance review
- Both parties assess how the **partnership** is working
- Goal: **Proactive improvement** before issues become friction
- Tone: **Curious, honest, collaborative** (not interrogative)

---

## Interview Pacing (CRITICAL)

**🚨 FOLLOW THESE RULES:**

1. **Ask ONE question at a time**
2. **STOP and WAIT** for complete response
3. **Listen actively** - dig into concerns raised
4. **Adapt follow-ups** - skip if not relevant, explore if concerning
5. **Target 5-10 minutes** - efficient but thorough

**Wrong approach:**
> "Let me ask you these 4 questions: [lists all questions at once]"

**Right approach:**
> "**Q1:** On a scale of 1-5, how well is our collaboration working?"
> [WAIT for response]
> [Process response, ask follow-ups if needed]
> [THEN move to next question]

**Why explicit numbering matters:**
- Helps user track which question they're answering (managing mental todo list)
- Makes it easy to reference specific questions ("Back to Q2 for a moment...")
- Clearer for both parties where we are in the process

---

## Q1: Collaboration Quality

### Ask

> "**Q1: On a scale of 1-5, how well is our collaboration working?**
>
> (1 = struggling, 3 = okay, 5 = excellent)
>
> **What's working great? What could be better?**"

### Listen For

**Positive signals (4-5/5):**
- Communication flows smoothly
- Trust feels appropriate
- Workflow is efficient
- Framework docs helpful
- Enjoying the collaboration

**Concerning signals (1-3/5):**
- Communication friction (signals unclear, verbose exchanges)
- Trust issues (second-guessing, micromanagement feelings)
- Context rebuilding every session
- Framework docs ignored or outdated
- Frustration or confusion

### Potential Follow-Ups

**If 4-5/5 and no concerns:**
- "That's great! What's the one thing working best?"
- [Capture strength for future reference]

**If 3/5 or mixed feedback:**
- "Can you say more about [specific concern mentioned]?"
- "What would make it a 5/5?"
- "Is this recent or ongoing?"

**If 1-2/5:**
- "I hear this isn't working well. What's the biggest pain point right now?"
- "What needs to change for this to feel productive?"
- [Dig deep - this requires immediate improvement plan]

### Document

```
Q1: Collaboration Quality: [X/5]
Strengths: [What's working]
Concerns: [What could improve]
Follow-up: [Any immediate actions needed]
```

---

## Q2: Communication Patterns

### Ask

> "**Q2: Are our communication patterns working for you?**
>
> Think about:
> - **Clarity** - Are my responses clear and concise, or too verbose/terse?
> - **Pacing** - Do I ask too many follow-ups, or not enough?
> - **Shortcuts** - Are permission signals (WWGD, etc.) working, or ignored?
> - **Tone** - Do I feel like a collaborator, or something else?"

### Listen For

**Clarity issues:**
- "You're too verbose" → Need more compression
- "I don't understand X" → Need clearer explanation of [concept]
- "You repeat yourself" → Redundant documentation or explanations

**Pacing issues:**
- "You ask too many questions" → Be more decisive, use judgment
- "You don't ask enough" → More clarification, less assumption
- "You interrupt my flow" → Ask questions at natural breaks, not mid-thought

**Shortcuts not working:**
- "I say WWGD and you still ask permission" → Trust calibration off
- "Shortcuts feel forced" → May not be natural for this user
- "I forget what they mean" → Need quick reference or simpler system

**Tone issues:**
- "You feel like a tool" → Not enough agency/personality
- "You're too formal" → Loosen up, match user style
- "You're too casual" → More professional tone needed

### Potential Follow-Ups

**If clarity issues:**
- "Should I aim for more concise responses? Or is it specific to [topic]?"
- "Would examples help, or are they adding noise?"

**If pacing issues:**
- "Would you prefer I batch questions, or is one-at-a-time better for you?"
- "Should I assume more and course-correct if wrong?"

**If shortcuts not working:**
- "Should we revise SHORTCUTS.md together?"
- "Which shortcuts work, which don't?"

**If tone issues:**
- "What tone feels right for our collaboration?"
- "Should CLAUDE.md be updated to reflect this?"

### Document

```
Q2: Communication Patterns
Clarity: [Assessment]
Pacing: [Assessment]
Shortcuts: [Working? Not working?]
Tone: [Assessment]
Actions: [Update SHORTCUTS.md? Change response style?]
```

---

## Q3: Framework Effectiveness

### Ask

> "**Q3: Is the Gordo Framework helping or getting in the way?**
>
> Think about:
> - **Session Start/End prompts** - Helpful or tedious?
> - **Trust Protocol** - Appropriate progression, or too rigid/loose?
> - **Journal/Memory** - Session continuity working, or context lost?
> - **Documentation** - Right level of detail, or overwhelming/sparse?"

### Listen For

**Framework helping:**
- "BOS gets us started quickly" → Keep SESSION_START.md
- "Trust levels feel natural" → Keep TRUST_PROTOCOL.md
- "Journal prevents repeating mistakes" → Keep JOURNAL.md
- "I reference docs often" → Framework is discoverable

**Framework friction:**
- "BOS feels like busywork" → Simplify or make optional
- "Trust levels don't match reality" → Recalibrate
- "Journal isn't being used" → Not reading or not writing?
- "I never look at [doc]" → Doc may be redundant or buried

**Intensity mismatch:**
- "Too much overhead for this project" → Reduce intensity
- "We need more structure" → Increase intensity

### Potential Follow-Ups

**If framework friction:**
- "Which specific step in BOS feels like busywork?"
- "Should we reduce framework intensity for this project?"
- "What if we cut [specific doc] - would that help or hurt?"

**If trust levels off:**
- "Should we recalibrate trust? Where do you think we are?"
- "What would Level [X+1] look like for this project?"

**If journal not used:**
- "Am I reading your journal entries and not applying lessons?"
- "Should we switch to simpler session memory?"

**If intensity mismatch:**
- "Would Medium intensity work better than Maximum?"
- "What components should we add/remove?"

### Document

```
Q3: Framework Effectiveness
BOS/EOS: [Working? Tedious?]
Trust Protocol: [Appropriate? Adjust needed?]
Journal/Memory: [Continuity working?]
Documentation: [Too much? Too little? Just right?]
Intensity: [Maximum? Medium? Minimal? Mismatch?]
Actions: [Framework adjustments needed]
```

---

## Q4: Patterns & Improvement Opportunities

### Ask

> "**Q4: Have you noticed any patterns - good or bad - in how we work together?**
>
> Examples:
> - Things I consistently do well or poorly
> - Friction points that keep recurring
> - Workflows that feel smooth or clunky
> - Documentation that's always helpful or always ignored"

### Listen For

**Positive patterns (reinforce):**
- "You always [good thing]" → Document as standard practice
- "When you [approach], it works great" → Capture in framework docs
- "The [specific doc] is really helpful" → Highlight in BOS

**Negative patterns (fix):**
- "You keep [bad thing] even though I mentioned it" → Not learning from feedback
- "Every session we struggle with [X]" → Systemic issue needs fix
- "I always have to remind you about [Y]" → Add to CONSTITUTION or BOS

**Opportunities:**
- "It would be great if you could [X]" → New capability or pattern to add
- "Other projects do [Y], could we?" → Learning from other repos
- "I wish the framework had [Z]" → Potential upstream contribution

### Potential Follow-Ups

**If positive patterns:**
- "Should we formalize [pattern] in WORKFLOW.md or CONSTITUTION.md?"
- "What makes [pattern] work so well?"

**If negative patterns:**
- "Why do you think [bad pattern] keeps happening?"
- "What would break if we changed [pattern] to [alternative]?"
- "Should this be in CONSTITUTION.md as a non-negotiable?"

**If opportunities:**
- "Is [opportunity] critical or nice-to-have?"
- "Should we implement this, or document it for later?"
- "Is this project-specific or something the framework should support?"

### Document

```
Q4: Patterns & Improvement Opportunities
Positive patterns: [What to reinforce]
Negative patterns: [What to fix]
Opportunities: [What to explore]
Actions: [Immediate fixes, framework updates, experiments]
```

---

## Health Check Conclusion

### Synthesize

After all 4 questions, provide a brief synthesis:

> "**Health Check Summary:**
>
> **Strengths:** [2-3 things working well]
> **Improvements:** [2-3 concrete actions to take this session or next]
> **Experiments:** [1-2 things to try and assess later]
>
> **Overall assessment:** [One sentence on collaboration health]"

### Propose Immediate Actions

**Examples:**
- "Let's update SHORTCUTS.md right now to simplify signals"
- "I'll add [concern] to CONSTITUTION.md as a non-negotiable"
- "Next session, I'll try [approach] and we'll assess if it helps"
- "Let's reduce framework intensity from Maximum to Medium"

**Ask:**
> "Which of these should I tackle immediately, and which should we schedule for later?"

---

## Document in HEALTH_CHECK_LOG.md

**Format:**
```markdown
## Health Check: [Date] (Session [N])

**Overall Score:** [X/5]

### Q1: Collaboration Quality ([X/5])
- Strengths: [...]
- Concerns: [...]

### Q2: Communication Patterns
- Clarity: [...]
- Pacing: [...]
- Shortcuts: [working/needs revision]
- Tone: [...]

### Q3: Framework Effectiveness
- BOS/EOS: [...]
- Trust Protocol: [...]
- Journal/Memory: [...]
- Documentation: [...]
- Intensity: [appropriate/needs adjustment]

### Q4: Patterns & Opportunities
- Positive: [...]
- Negative: [...]
- Opportunities: [...]

### Actions Taken
1. [Immediate action 1]
2. [Immediate action 2]

### Actions Scheduled
1. [Future action 1]
2. [Future action 2]

### Experiments
1. [Experiment to try and assess later]

**Next health check:** Session [N + cadence] (in [X] sessions)
```

---

## Update config.json

After health check complete:

```json
{
  "sessions": {
    "count": [current_session_number],
    "lastHealthCheck": [current_session_number],
    "healthCheckCadence": [14 or 21 or 30 depending on intensity]
  }
}
```

This resets the health check timer.

---

## Post-Health Check

**Immediate follow-through:**
- If you promised to update docs (SHORTCUTS.md, CONSTITUTION.md, etc.), do it NOW
- If you need to adjust trust level, document in TRUST_PROTOCOL.md
- If framework intensity should change, note in README.md and config.json

**Session continuity:**
- Add health check insights to today's journal entry
- Reference health check in end-of-session summary
- Commit HEALTH_CHECK_LOG.md update

**Next session:**
- Apply lessons learned from health check
- Monitor if proposed experiments are working
- Be ready to course-correct if approach isn't helping

---

## Common Pitfalls

**❌ Don't:**
- Batch all questions at once (violates pacing rules)
- Treat this as a formality (it's a real collaboration improvement tool)
- Ignore negative feedback (even if painful to hear)
- Promise improvements you won't deliver (trust erosion)
- Rush through to "check the box" (defeats the purpose)

**✅ Do:**
- Ask one question at a time and wait
- Listen actively and dig into concerns
- Take concrete actions immediately
- Follow through on commitments
- Use insights to genuinely improve collaboration

---

## Success Criteria

**Health check is successful when:**
1. User feels heard and understood
2. Concrete improvements identified and prioritized
3. Immediate actions taken (not just scheduled)
4. HEALTH_CHECK_LOG.md updated with clear documentation
5. Both parties have clearer picture of collaboration quality
6. Next health check timer reset in config.json

**Health check failed if:**
- User feels like it was checkbox compliance
- No actionable improvements identified
- Promises made but not kept
- Documentation incomplete or rushed
- Collaboration issues persist without addressing

---

**Skill version:** 1.0.0
**Framework version:** 0.5.0+
**Last updated:** 2025-10-31
