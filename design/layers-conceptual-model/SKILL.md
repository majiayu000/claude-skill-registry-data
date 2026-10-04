---
name: layers-conceptual-model
description: Defines the product's objects, relationships, states, and vocabulary independently of any interface — the most load-bearing layer
---

# /layers-conceptual-model

*Assumes `/layers-intro` has been loaded for framework context.*

The conceptual model is the most neglected load-bearing layer. It defines the objects the product recognises, their relationships, what states they can be in, and the vocabulary used for everything. It lives in the solution space: it is not a capture of users' existing mental models (which are contradictory and messy — that's the domain layer's job), but a deliberate design decision about how the product will model its domain.

**What it is — and isn't:**
- A **design decision** that resolves the messy domain into a coherent, opinionated structure
- **Not a database schema** — engineers make their own data decisions, but the gap between this model and what they build matters. A large, unexamined gap is both UX debt (users encounter a product that contradicts the model) and technical debt (the system is harder to evolve).
- **Not a wireframe or flow** — no screens, no navigation. Those belong to the layers above.
- **Not neutral** — every naming decision, every relationship boundary, every included or excluded object reflects a point of view.

**Decisions this layer needs to make:**
- What objects will this product recognise, and what are their boundaries?
- How do those objects relate to each other?
- What can users do with each object?
- What states can each object be in, and what transitions matter?
- What is the product's vocabulary — one name per concept, chosen and committed to?

**Methods:**

| Method | When |
|---|---|
| **Noun foraging + OOUX** (Sophia Prater) | Default when you have research or domain notes to mine. Extracts objects from naturalistic language. |
| **Semantic IxD / action grammar** (Daniel Rosenberg) | When you have many actions across many objects and want to audit verb consistency and precision. |
| **Event storming — commands/policies phase** (Brandolini) | Domain has complex processes. Start from what happens, work backwards to objects involved. |
| **Card sorting** | Vocabulary is unclear or contested across users or teams. |
| **DDD bounded context mapping** | Multiple user types use the same words differently — surfaces where the model has natural seams. |
| **Walking the existing product** | Redesigning. The current UI reveals the implicit model — compare it to how users actually think. |

Default: **noun foraging and object definition**.

**Quality signals — what good looks like:**
- Every object is independently meaningful to the user — not a UI element, not a vague abstraction
- Relationship roles are explicitly named when an object can play multiple roles
- Attributes that are really relationships have been challenged and converted
- No speculative additions — every object, attribute, and relationship traces to a user need
- State transitions are defined for objects whose status materially changes what users can do
- Temporal decisions are addressed: deletion semantics, relationship temporality, history
- Ubiquitous language is established: one name per concept, one concept per name

---

## Guided session

*Tell me what product or feature you're defining a model for, or say "guide me" to start noun foraging and object definition.*

Ask: *"Where should I capture the work from this session?"* (see `/layers-intro` for options)

Check what the designer has from the problem space — domain notes, research, user needs. If nothing: proceed but flag that a model built without domain knowledge often reflects assumptions more than users' reality.

If redesigning: *"Describe the current model, even informally — what implicit model does the existing product have?"*

---

**Phase 1 — Frame the scope**

1. What product or feature are we defining a conceptual model for?
2. What's the core job users are trying to do with it?
3. What material are you working from?

**Phase 2 — Discover objects**

*From research or domain notes:* Extract every noun — things, people, roles, documents, places, states, concepts, events. Cast wide; don't filter yet. Present the raw list, then ask: missing nouns? Same things with different names?

*From an existing product:* Walk it together. *"What is a user looking at here? What is this thing called?"*

*From first principles:* *"If a user could reach in and hand something to a colleague, what would they hand?"*

Sort into:
- **Objects** — things that persist, have their own attributes, and matter to the user in their own right
- **Attributes** — properties that describe an object, not objects themselves
- **Set aside** — UI elements, vague abstractions, actions dressed as nouns

A true object must be independently meaningful to the user, not just a property of something else.

**Phase 3 — Define each object**

Work through each core object:

```
Object: [Name]
What it is: [one sentence from the user's perspective]
Attributes: [properties a user knows or cares about]
Relationships: [connections to other objects — cardinality and role names]
Actions (CTAs): [what a user can do to or with this object]
```

**Four discipline checks:**

1. *Relationship roles:* When a relationship connects to an object that can play multiple roles (e.g. a User who is both referrer and referred), name the role explicitly: "belongs to one User (as referrer)" not "belongs to one User."

2. *Attributes that are really relationships:* If an attribute is just the name or ID of another object in the model, it's a relationship — model it, don't duplicate it as an attribute.

3. *No speculative additions:* Don't add attributes, relationships, or actions not grounded in a stated user need. Scope creep at the conceptual model layer propagates through every layer above.

4. *Implementation vs. design decisions:* When conversation drifts to how something is generated, stored, or computed — redirect: *"How it's generated is engineering. What matters here: can a user change this? What happens to things that already referenced it?"*

5. *Verb precision:* For each action, ask whether the verb tells the user what they'll end up with or what real-world operation they're performing. "Enter a PIN" fails because it implies the PIN already exists — "Create" is precise. More critically: check whether a generic verb (Edit, Delete, Update) is hiding operations with meaningfully different real-world consequences. "Edit address" conflates correcting a typo with recording a house move — two operations where one preserves history and one doesn't, requiring different system behaviour and different user intent. A **deductive** interface uses generic verbs and asks users to map their intent to them; an **inductive** interface names the real-world operation ("Register change of address") and preserves its meaning. When a generic verb could mean different things depending on what the user is actually trying to do, name the operations separately.

**Phase 4 — Object map**

Generate a relational object map: entities as nodes, relationships as labelled lines with cardinality markers. No fixed orientation — follow what makes the relationships most readable. In Mermaid: `erDiagram`.

When presenting, explain cardinality: `||` = exactly one, `o{` = zero or many, `|{` = one or many. The crow's foot is always on the "many" side. Relationship labels read in the direction declared (first entity → second entity).

Ask: *"Does this reflect how you think about these things? Relationships missing, directions reversed, connections that shouldn't be there?"*

**Phase 5 — State transitions and temporal decisions**

For each object where lifecycle or status matters: *"What states can a [Object] be in? What moves it between states? What becomes impossible in each state?"*

Generate a state diagram: states as nodes, transitions as labelled arrows, with a clear start state. Top-to-bottom or left-to-right depending on the number of states. In Mermaid: `stateDiagram-v2`.

Also probe temporal decisions (from `/layers-intro`): intermediate action states, read model lag, relationship temporality, deletion semantics, history. For implementation-entangled questions, don't force a premature answer — articulate the user experience requirement and flag as a named open question for an engineering conversation.

**Phase 6 — Ubiquitous language**

The ubiquitous language covers both nouns (objects, attributes) and verbs (actions). The same principle applies to both: one word per concept, one concept per word.

**Nouns:** List every chosen object and attribute name. For any noun with synonyms or naming conflicts:

```
Term: [chosen name]
Rejected alternatives: [other names that appeared]
Decision: [why this term was chosen]
```

**Verbs — action vocabulary:** Compile all action verbs across all objects. Apply two tests:

*Synonym check:* Are multiple verbs being used for the same operation? "Create" and "Add" for the same action type should be consolidated. Minimising the verb vocabulary reduces what users have to learn — the same verb working identically across all objects (like cut/copy/paste) means users learn once and transfer everywhere. Every synonym is a new thing to memorise.

*Flattening check:* The opposite risk — one verb covering operations that are genuinely different. "Edit address" sounds simple until you realise it conflates two things: correcting a typo (overwrite is fine) and recording a house move (which should create a new record and preserve the old one). The domain treats these differently; the interface shouldn't hide that. For each generic CRUD verb (Edit, Delete, Update, Create), ask: could this cover operations with different real-world consequences — different history implications, different downstream effects, different things the user is actually trying to accomplish? If so, give them separate names. "Register change of address" and "Correct address" are not verbose — they're precise.

```
Verb: [chosen action name]
Applies to: [which objects]
Rejected alternatives: [other verbs considered]
Decision: [why this verb; what real-world operation it names]
```

*"This is your product's ubiquitous language. Use these terms consistently — in the UI, in help text, in API names, in internal conversation. Every inconsistency between this model and the surface creates cognitive load for users."*

---

### Completion

Produce:
1. **Object definitions** — attributes, relationships, and actions
2. **Object map** — `erDiagram`
3. **State transition diagrams** — for objects with meaningful lifecycles
4. **Ubiquitous language** — chosen nouns and verbs with resolved conflicts and decisions
5. **Open questions** — deferred decisions, objects that felt thin, anything flagged but unresolved

Close with: *"The conceptual model defines what exists in this product. Next: design how users interact with those objects. Run `/layers-interaction-flow`."*

If domain work hasn't been done: *"This model was built without domain research — it's a hypothesis. Plan to revisit it once you have evidence."*
