---
name: layers-user-needs
description: Elicits and prioritises user needs (needs, pains, desires) as job stories — produces opportunities ready for product strategy
---

# /layers-user-needs

*Assumes `/layers-intro` has been loaded for framework context.*

User needs are what we think users are trying to achieve, and why — an interpretation built on observed behaviour and domain knowledge, not a direct capture of reality. This layer sits between the messy raw material of observation and the deliberate decisions of the solution space.

In OST terms, the outputs here are **opportunities**: needs (what users want to achieve), pains (what's causing friction), and desires (improvements they'd value). All three are valid inputs; elicit all three.

**Decisions this layer needs to make:**
- Who exactly are the users whose needs we're defining — and in what situation?
- What jobs are they trying to do — functional, emotional, and social?
- Which needs are grounded in evidence, and which are assumptions?
- Which needs matter most, and why?

**Methods:**

| Method | When |
|---|---|
| **Job stories** (JTBD) | Default. Situation → motivation → outcome. Keeps solutions out; forces specificity through the "When" clause. |
| **User stories** | Team prefers role-based framing, or integrating with an existing Agile workflow. |
| **Top tasks analysis** (Gerry McGovern) | Large existing user base. Identify which tasks matter most by frequency. Statistical, survey-based. |
| **Persona + scenario** | Communicating to stakeholders who think in archetypes. Good for alignment; less precise for design decisions. |
| **ODI desired outcomes** (Ulwick) | Precise, measurable statements. Format: "Minimize [metric] when [context]." Maps directly to opportunity scoring. |

Default: **job stories**.

**Three types of need — elicit all three:**
- **Functional** — the practical task. Feeds interaction structure and conceptual model directly.
- **Emotional** — how the user wants to *feel* while doing the job. Feeds surface (tone, copy, feedback).
- **Social** — how the user wants to be *perceived* by others in this context. Also feeds surface; sometimes strategy.

Emotional and social needs are chronically under-articulated in briefs and research reports, even when they're genuinely shaping behaviour. Asking for them explicitly is usually what surfaces them.

**Quality signals — what good looks like:**
- The "When" clause is specific enough to picture the moment it happens
- The motivation is a genuine goal, not a solution sneaking in
- Functional, emotional, and social dimensions all explored
- Confidence marked: observed / inferred / assumed
- Workarounds surfaced — a need real enough to motivate improvisation is a strong signal

---

## Guided session

*Tell me who your users are and what you're working on, or say "guide me" to start a structured session.*

Ask: *"Where should I capture the work from this session?"* (see `/layers-intro` for options)

Ask: *"What's the source of the user needs we're working with — user research, domain knowledge, team assumptions, or a mix?"* If working from assumptions, mark them clearly throughout and plan to validate.

---

**Phase 1 — Frame the users**

1. Who are the users whose needs we're defining? Be specific — not "users" but which type, in which situation.
2. What context are they in when the relevant need arises?
3. Is there more than one distinct user type with meaningfully different needs? Work through them separately.

**Phase 2 — Elicit needs**

Work through the needs the designer raises. Format: *When [situation], I want to [motivation], so I can [expected outcome].*

The "When" clause is the most important part — it must be specific enough to picture the moment. Push until it is.

For each need, ask: *"Is there a functional job here, an emotional job, a social job — or all three?"*

Probe each:
- *On "When":* "Could you picture the moment this happens? Is this triggered by an event, a feeling, a rhythm, or a threshold being crossed?"
- *On motivation:* "Is a solution sneaking in? Why does this matter to them? What's at stake if unmet?"
- *On expected outcome:* "What does success look like for the user — not the product?"

**Phase 3 — Surface hidden needs**

- *"What needs do users have that the product currently ignores?"*
- *"What do users do before and after the moment we normally focus on?"*
- *"What do users have to do that they really wish they didn't?"*
- *"What need are users currently meeting with a workaround — a spreadsheet, an email — that a product could serve better?"*

**Phase 4 — Challenge and filter**

Review all needs together. For each:
1. **Need or solution?** "When I need a report, I want to export to CSV" is a solution. Push to the underlying need.
2. **Specific enough to design from?** A need so broad that any feature could serve it is not useful.
3. **Grounded?** Mark: observed / inferred / assumed.
4. **Important?** How frequently does this situation arise? How painful is it unmet?

**Phase 5 — Prioritise**

Rough ordering: highest importance × most poorly currently served. A need that matters a lot and is badly served is a high-value opportunity. A need that matters a lot but is already well served is not.

Don't over-engineer this. Precise prioritisation is strategy work at `/layers-product-strategy`. A rough ranking is enough here.

---

### Completion

Produce:
1. **User needs** — final list, priority order, with confidence ratings (observed / inferred / assumed)
2. **Unprioritised needs** — surfaced but not ranked, so they aren't lost
3. **Gaps** — needs probably real but not yet grounded; research questions to answer
4. **Contradictions** — if different user types have conflicting needs, name them explicitly

Close with: *"These needs are the opportunities for your product strategy. Run `/layers-product-strategy` to build a strategy tree connecting them to business outcomes and solution bets."*

If needs are mostly assumed: *"Several of these are marked as assumed. Before building strategy on them, consider running `/layers-observed-behaviour` to gather evidence."*
