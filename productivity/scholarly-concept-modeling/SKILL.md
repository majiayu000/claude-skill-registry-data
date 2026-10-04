---
name: scholarly-concept-modeling
version: 1.3.0
description: Use during paper design or novel concept definition to build a domain model dictionary (DDD Ubiquitous Language) and prevent terminological confusion
---

# Scholarly Concept Modeling Skill

## Purpose
Apply Domain-Driven Design (DDD) principles—specifically Ubiquitous Language and Bounded Contexts—to define, structure, and disambiguate core domain concepts (e.g., *agency*, *subjectivity*, *sovereignty*, *inflation*, *consensus*) in paper writing.

## Trigger Conditions
- When creating a thesis outline or chapter structure
- When introducing a new major concept or analytical framework
- When a reviewer notes terminological ambiguity
- When drafting or revising a chapter (warrant-check for definitional claims)

## Workflow

### Step 1: Create Concept Inventory
Extract core domain terms into `docs/design/domain-concepts.md`:

```markdown
### Concept: [e.g. Agency]
- **Definition in Paper**: The capacity of individual actors to act independently within structural constraints.
- **Bounded Context**: Chapters 2 through 4 (Sociological Analysis).
- **Disambiguation**: Distinct from *Free Will* (philosophical) and *Behavior* (empirical psychology).
- **Contrast with Prior Literature**: Diverges from Smith (2018), who defines agency purely as a structural effect.
- **Contrast with Prior Empirical Claims**: When peer-reviewed disagreement exists not over the definition but over an empirical proposition involving the concept (e.g., "X promotes Y"), record the camps and representative papers (e.g., proponent camp Smith 2018 vs. opponent camp Jones 2020). Keep consistent with the Contestation Status column of `literature-matrix.md`.
```

### Step 1.2: Practice-Check for Modal Claims (v1.2.0)

If a draft definition contains strong modal claims ("impossible", "must", "only", "always"), perform the following before fixing it as SoT:

1. **Flag**: enumerate the modal claims.
2. **Check with the author**: ask one question per claim — "Does your practical experience contain a counterexample to this claim?"
3. **Record relaxations**: if a claim is relaxed, record both the original and the relaxed form (to preserve the theoretical trajectory).

Agents tend to generate strong modal claims from theoretical coherence, but the author's practical knowledge may supply counterexamples (e.g., "map design cannot be externalized" → relaxed to "provision is externalizable, internalization is not" based on practice knowledge of borrowing established methodologies).

### Step 1.5: Idea Explosion Capture
If the user mentions tangential ideas, hypotheses, or inspirations during concept definition dialogue, the agent must not discard them. Instead, append them to the end of `docs/<paper-id>/design/domain-concepts.md` (or `docs/design/domain-concepts.md`) in the following format:

```markdown
## Unsorted Idea Pool
- [timestamp] Summary of user's remark (emerged during definition of Concept X)
- [timestamp] ...
```

This safely captures ideas overflowing from working memory without disrupting the main task (concept definition). Implements [Cognitive Scaffolding Rule S2](../../../rules/en/cognitive-scaffolding-rule.md).

### Step 2: Automated Term Consistency Check
During drafting and review, the AI Agent verifies `docs/<paper-id>/design/domain-concepts.md` (or `docs/design/domain-concepts.md`) to check that:
1. Defined concepts are not used with meanings that conflict with their definitions.
2. Near-synonyms are not unconsciously substituted for defined terms.
3. The agent reflects the user's recent statements back ("You're using this term to mean X, correct?") and checks for discrepancies with the definition (S2: Metacognitive Mirroring).
4. **Warrant check for definitional claims (v1.3.0)**: when the prose states a definitional decision ("this paper defines X as…", "Y is not part of the definition"), the reason attached in the same paragraph must match the concept entry (definition, disambiguation, relaxation record). Do not attach a nearby citation or scope-limit as if it were the warrant for the definitional change. Keep the citation's introduction and the definitional decision in separate sentences.

Immediately before writing a definitional sentence:
1. Re-read the relevant concept entry
2. Match the definitional sentence to the entry's definition
3. Match the reason sentence to the entry's warrant (including any relaxation record)
4. If a nearby citation is a different point (scope, a three-part core, etc.), keep it independent — do not glue it to the definitional decision

## Cognitive Scaffolding
All interactions in this skill must follow the [Cognitive Scaffolding Rule](../../../rules/en/cognitive-scaffolding-rule.md) (S1–S4). Concept definition dialogues are particularly prone to thought divergence, so S2 (Metacognitive Mirroring) takes priority.

## Outputs
- `docs/design/domain-concepts.md` (Single Source of Truth for Domain Concepts)
