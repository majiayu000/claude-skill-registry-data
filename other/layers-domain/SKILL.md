---
name: layers-domain
description: Maps domain concepts, terminology conflicts, and bounded contexts — produces a noun harvest for the conceptual model layer
---

# /layers-domain

*Assumes `/layers-intro` has been loaded for framework context.*

The domain layer maps what exists in the real world independently of any product: the concepts, terminology, processes, relationships, and mental models users bring with them. This is observation, not design.

**Critical distinction:** Do not resolve contradictions at this layer. Contradictory, messy, inconsistent domain language is data — it signals where different user communities have diverged, and where the product will need to make deliberate choices. Resolution happens at the conceptual model layer.

**Decisions this layer needs to make:**
- What are the key concepts in this domain, and how do they relate?
- What language do people use — and where does that language conflict or diverge?
- Where are the natural seams where different communities use the same words differently?
- What events and processes structure the domain's activity over time?

**Methods:**

| Method | When |
|---|---|
| **Concept maps / bubble diagrams** | Domain is complex and poorly understood. Informal nodes-and-lines show how concepts relate without forcing premature structure. |
| **Domain event storming** (Brandolini) | Domain is process-heavy. Start from significant things that happen (past tense) — events reveal natural seams. |
| **Expert interviews** | Domain knowledge lives in people, not documents. Conversations reveal tacit knowledge and contested terminology. |
| **Document and artefact analysis** | Domain produces artefacts (contracts, forms, invoices) that reveal natural structure and vocabulary. |
| **Competitive analysis** | Entering an established domain. Existing products reveal how others have modelled it — and where they disagree. |
| **Shadowing** | Domain involves workflows hard to articulate. Watching people work reveals what they actually do. |

Default: **concept mapping and terminology audit**.

**Quality signals — what good looks like:**
- Contradictions are documented, not resolved
- Synonyms are recorded (same thing, different names)
- Polysemy is flagged (same name, different things in different contexts)
- Bounded contexts are named where communities use language coherently within their group but inconsistently across groups
- The noun harvest is a complete raw candidate list — not filtered, not pre-organised into objects and attributes

---

## Guided session

*Tell me what domain you're mapping and what you know about it, or say "guide me" to start a structured session.*

Ask: *"Where should I capture the work from this session?"* (see `/layers-intro` for options)

Ask: *"Are you working from research and domain expertise, or from what the team currently believes about the domain?"* If mapping beliefs, flag throughout that what's being captured is the team's model, not necessarily how users experience the domain.

---

**Phase 1 — Frame the domain**

1. What domain are we mapping? (The real-world context — not the product.)
2. Who are the people operating in this domain? (Roles, user types, stakeholders.)
3. What are they trying to accomplish, before your product enters the picture?

Keep pushing back toward the real world if answers drift toward product decisions.

**Phase 2 — Surface the concepts**

*"Walk me through how [domain] works. What are the main things, how do they relate, what happens?"*

Listen for nouns (concepts), verbs (processes), and natural vocabulary. Take notes on everything — raw, unfiltered. Then prompt:
- *"What do people actually call these things? Multiple names for the same thing?"*
- *"What rules exist — explicit policies or understood conventions?"*
- *"What changes over time? What has a lifecycle?"*

**Phase 3 — Concept map**

Build a concept map: nodes connected by labelled relationships. Informal — no required hierarchy or orientation; follow what feels natural for the domain. In Mermaid: `graph TD` or `graph LR`.

Ask: *"Does this feel like the domain, or like a database diagram? What's missing or wrong?"*

**Phase 4 — Terminology audit**

For each concept: does everyone in this domain use this word the same way? Are there other words for the same thing? Does this word mean something different in another context?

Document:
```
Concept: [thing]
Names used: [all variants]
Context: [who uses which, and when]
Conflict type: synonyms (same thing, different names) / polysemy (same name, different things)
```

Do not choose a winner.

**Phase 5 — Bounded contexts**

Look at terminology conflicts: are there communities of people who share vocabulary internally but diverge from other groups? Name and describe each. These seams will matter when the conceptual model is defined — the product will need to decide how to navigate or bridge them.

**Phase 6 — Domain events (optional)**

If the domain is process-heavy: *"What are the significant things that happen in this domain? Name them in past tense."*

List events on a timeline. Ask what triggers each, and what happens as a result. Objects with significant events around them are likely to need state transition diagrams at the conceptual model layer.

**Phase 7 — Noun harvest**

Compile all nouns surfaced in the session. Mark each:
- **Potential object** — independently meaningful, may have attributes and relationships
- **Potential attribute** — a property of something else
- **Unclear** — needs more thought

Don't filter aggressively. The conceptual model layer does the sorting.

---

### Completion

Produce:
1. **Concept map** — Mermaid `graph TD`
2. **Terminology conflicts** — documented name variants and bounded contexts
3. **Domain events** — if explored, key events timeline
4. **Noun harvest** — complete candidate list

Close with: *"This domain map is raw material for your conceptual model. Run `/layers-conceptual-model` to define objects, relationships, and vocabulary — the noun harvest is your starting point."*
