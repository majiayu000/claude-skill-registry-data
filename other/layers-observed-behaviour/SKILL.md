---
name: layers-observed-behaviour
description: User research planning and synthesis at the observed behaviour layer — produces candidate job stories with confidence ratings
---

# /layers-observed-behaviour

*Assumes `/layers-intro` has been loaded for framework context.*

The observed behaviour layer is the closest we can get to reality. It is raw material — what users actually do, not what we think they do or wish they would do. Everything above it is interpretation; this layer is the source.

**Decisions this layer needs to make:**
- What specific questions do we most need to answer about our users?
- What evidence already exists, and how reliable is it?
- How do we gather what's missing?
- What patterns emerge — and what can we claim with confidence vs. what remains assumption?

**Methods:**

| Method | When |
|---|---|
| **JTBD interviews** | Understanding triggers, motivations, and anxieties. Interview about a real past experience, not hypotheticals. |
| **Contextual inquiry / observation** | When what users say differs from what they do. Watching real work reveals tacit behaviour. |
| **Diary studies** | When the behaviour is distributed over time or infrequent — users self-report as events occur. |
| **Support ticket / review analysis** | Existing product with accumulated signal. Good for identifying pain points at scale without recruiting. |
| **Analytics review** | What users do (not why). Complements qualitative; doesn't replace it. |
| **Usability observation** | Where do people struggle or succeed with an existing product? |

**Quality signals — what good looks like:**
- Observations are specific and close to raw data, not summarised into conclusions
- Job stories are grounded in something seen or heard, not inferred from team beliefs
- Confidence levels are marked: observed / inferred / assumed
- Research gaps are named explicitly, not papered over
- Workarounds are flagged — a need real enough to motivate improvisation is a strong signal

This skill works in two modes. Detect which applies and state it clearly:
- **Plan mode** — no research yet; help design a study
- **Synthesise mode** — existing research material; help make sense of it

If they have partial research, start in Synthesise mode with what exists, then shift to Plan mode to identify gaps.

---

## Guided session

*Tell me what you're working on — what question you most need to answer about your users — or say "plan" or "synthesise" to start a guided session.*

Ask: *"Where should I capture the work from this session?"* (see `/layers-intro` for options)

Ask: *"Do you have existing research — interviews, session recordings, support tickets, analytics — or do we need to plan research from scratch?"* State the mode clearly once you know.

---

### Plan mode

**Phase 1 — Define the learning goal**

Help the designer articulate what they most need to understand. Push past vague goals:
- Not "understand users better" but "understand what triggers someone to refer a friend, and what makes them hesitate"

Write out 2–3 specific research questions.

**Phase 2 — Identify participants**

Who has the behaviour we need to observe? Push on assumptions:
- Existing users, potential users, or churned users?
- Is the behaviour something they do currently, or something they'd do in a new situation?
- How many participants for meaningful signal? (Qualitative interviews: 6–10 usually reaches saturation)

**Phase 3 — Design the study**

Choose the right method based on the learning goal. If running JTBD interviews, generate an interview guide:

*Opening:* "Tell me about the last time you [relevant behaviour]. Walk me through what was happening at that point."

*Timeline:* "What triggered that? What did you try first? What made you keep going / give up / switch?"

*Motivations:* "What were you hoping would be different after doing this? What were you worried about? What almost stopped you?"

*Closing:* "Is there anything I haven't asked that would help me understand this better?"

Remind the designer: listen for nouns (candidate domain objects) and the language users use naturally — this feeds the domain layer.

**Phase 4 — Plan synthesis**

Before going to research: agree on how findings will be captured and organised. One observation per note, tagged with the research question it speaks to. Raw quotes over summaries.

---

### Synthesise mode

**Phase 1 — Take stock**

Ask the designer to share what they have — transcripts, notes, data summaries, whatever form. Ask: how was this collected, what questions was it designed to answer, how confident are you in its quality?

**Phase 2 — Extract observations**

Pull out concrete observations — things users said, did, or felt. Stay close to raw data; no interpretation yet.

If working from memory rather than documents, elicit by asking:
- *"What was the most surprising thing a user did or said?"*
- *"What kept coming up across different users?"*
- *"What did users struggle with that you didn't expect?"*

**Phase 3 — Identify patterns**

Group observations by theme:
- Recurring situations that trigger the behaviour
- Common motivations — underlying goals that keep appearing
- Shared anxieties — hesitations that show up across users
- Workarounds — what users do when the product doesn't serve the job

**Phase 4 — Draft candidate job stories**

From the patterns: *When [situation], I want to [motivation], so I can [expected outcome].*

For each: is the "When" specific enough? Is the "I want to" a motivation or a solution? Mark confidence: observed / inferred / assumed.

**Phase 5 — Flag research gaps**

What questions do the observations not yet answer? What would a designer need to know that this research doesn't tell them? These become input for a follow-up Plan mode session.

---

### Completion

Produce:
1. **Key observations** — significant raw findings
2. **Patterns** — grouped themes with supporting observations
3. **Candidate job stories** — with confidence ratings
4. **Research gaps** — questions still unanswered

Close with: *"These job stories are ready to refine at the user needs layer. Run `/layers-user-needs` to work through them."*
