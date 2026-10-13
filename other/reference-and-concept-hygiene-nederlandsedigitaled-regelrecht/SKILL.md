---
name: reference-and-concept-hygiene
description: >
  Builds and audits a concept-ontology for a regelrecht corpus to decide and verify reference
  types — cross-law source-binding vs intra-law source-binding vs open-norm leaf vs external-fact
  leaf — and to catch concept conflation across laws. Core principle: a value's reference type is
  fixed by WHO derives it, and a binding is sound only when producer and consumer denote the SAME
  concept; the lexical surface (the word in the text) is not the concept. Detects false friends
  (one term, different concepts — e.g. a register-based vs a factual "naar de omstandigheden"-based
  residence/ingezetene concept), orphan plain-params (a value a regulation actually derives, modeled
  as a brute input), negation/complement re-entry (¬X modeled as an independent leaf next to X), and
  duplication (one concept re-entered as several independent leafs, losing the single-source-of-truth
  invariant). Produces a law-level glossary and a stelsel-level concept map with sound same-concept
  binding edges and flagged lexical-match-but-concept-mismatch edges. Use when deciding whether a
  value should be cross-law/intra-law/leaf, when the same term means different things across laws,
  or when a binding might silently conflate concepts.
allowed-tools: Read, Write, Bash, Grep, Glob, WebFetch, WebSearch, AskUserQuestion
user-invocable: true
---

# Cross-law Concept & Binding Ontology

Two recurring questions in a cross-law model: (1) what **reference type** should a value be —
a cross-law source-binding, an intra-law source-binding, an open-norm leaf, or an external-fact
leaf — and (2) is a given **binding sound**, given that the same term can denote a *different
concept* in a different law. This skill answers both by building a concept-ontology and auditing
references against it.

## Core principle — type follows derivation, soundness follows concept identity

> The reference type of a modeled value is fixed by **who derives it**. A source-binding is sound
> only when the producer and the consumer denote the **same concept**. The lexical surface — the
> word in the `text:` — is **not** the concept: two laws can use one word for different concepts
> (false friends), or different words for one concept (synonyms). The engine runs a conflated
> binding without complaint; only concept analysis catches it.

## Reference-type decision procedure

For each modeled value, ask in order:
1. **Does another regulation derive it** (an endpoint computes it)? → **cross-law source-binding**.
2. **Does the same regulation derive it** in another article? → **intra-law source-binding**.
3. **Does the law delegate the determination** to a factual or discretionary judgment ("naar de
   omstandigheden te beoordelen", "naar het oordeel van", "zo nodig geschat" — an open norm)? →
   **open-norm leaf** (an injected judgment; the legislator opened the slot).
4. **Brute fact** that no regulation derives and the law does not delegate as an open norm? →
   **external-fact leaf**.

Anti-patterns to flag:
- **Orphan plain-param** — a value that a regulation actually derives (1 or 2) modeled as a brute
  input. Smell: a leaf whose name matches an existing endpoint, or a value the text grounds in
  "vastgesteld op grond van [andere regeling]".
- **Negation/complement re-entry** — a value that is the logical complement of an existing
  determination (¬X) modeled as an *independent* leaf, so the model permits X ∧ ¬X. Derive it from
  the single determination instead.

## The ontology — cluster by concept, not by word

The discriminator is the **determination-mode**, not the lexeme. For each term the corpus reckons
with, tag its mode:
- **computed-rule** — derived by an endpoint;
- **register/administrative** — an inschrijving in a register; a formal act;
- **factual open-norm** — "naar de omstandigheden"; a weging of facts;
- **composite** — a status = a factual core **+** a qualifier (e.g. *lawful*-X = factual-X + a
  legality predicate);
- **brute fact**.

Then cluster surface forms into **canonical concepts** by mode + legal referent, not by spelling:
- **False friends** — one lexeme, different concepts. A residence/ingezetene term that is
  register-based in statute A but a factual "naar de omstandigheden"-weging in statute B is a
  *different concept*. Binding A's predicate to B's endpoint is a conflation even though the words
  match and the engine runs.
- **Synonyms** — different lexemes, one concept → a binding is appropriate.
- **Composites** — never bind a composite to one of its parts (lawful-resident ↛ factual-resident);
  decompose into the part-bindings.

## Binding-soundness audit

For each existing source-binding `P (law A) ← E (law B)`:
- **Same canonical concept** (mode + referent)? If not → **CONFLATION** (false friend); flag.
- Is the consumer a **composite** and the producer one of its **parts** (or vice versa)? →
  **PART/WHOLE mismatch**; decompose.

Across the corpus:
- Is one concept **re-entered as several independent leafs**? → **DUPLICATION**; lost
  single-source-of-truth and lost mutual-exclusion invariant. Derive the rest from one determination.
- Does a **plain-param** correspond to something a regulation derives? → **ORPHAN**; rebind.

## Classification of each finding

| Bucket | Meaning | Action |
|---|---|---|
| **structural-fix** | the reference type or binding is mechanically wrong vs the derivation/concept facts | rebind / derive from one source / decompose |
| **concept-question (jurist)** | whether two concepts are *legally equivalent* is a normative call (e.g. "do we accept a register as proxy for a factual open norm?") | jurist decides; document the proxy-with-rationale or reject |
| **accept-with-rationale** | a deliberate proxy (e.g. a register as best machine-readable indicator of a factual norm) | keep — but model the register as an **indicator that feeds** the open-norm weging, never as its silent **replacement**; annotate |

**Cardinal rule:** a register may *inform* a factual open-norm determination but must not silently
*replace* it — that substitution is the canonical conflation (mirrors the standard "naar de
omstandigheden te beoordelen" + "een enkele inschrijving is niet voldoende"-doctrine). Keep the model
**symmetric**: if one side of a stelsel models a concept factually, the mirror side must too, unless a
documented decision says otherwise.

## Output

- **Law-level glossary** (per law): `term → canonical concept → determination-mode → reference-type →
  endpoint/leaf id`.
- **Stelsel-level concept map**: concepts as nodes; sound same-concept binding edges; and a flagged
  list of false-friend edges (lexical match, concept mismatch), orphan plain-params, complement
  re-entries, and duplications.
- A **reference-hygiene report** classifying each finding (structural-fix / concept-question /
  accept-with-rationale), with a jurist-question per concept-equivalence call.

## Verification (no hunches)

Confirm a "derived" claim by locating the producing endpoint; confirm a conflation by showing the
**determination-modes differ**, not by the wording. After a rebind/derive/decompose: schema-validation
and cross-law-integriteit stay green, and end-to-end outcomes are unchanged where the concept was
already equivalent (anti-masking: flip a source fact, see the outcome move). A rebinding that changes
outcomes means the concepts were genuinely different — that is a finding, not a regression.

## Relation to other skills

- `law-letter-fidelity-audit` — is the model faithful to the **letter** (vs toelichting / desired
  outcome)? Orthogonal to this skill, which asks whether the **references** are the right type and
  whether bindings respect **concept identity**. Run fidelity first (terms letter-true), then this
  (terms wired and clustered right).
- `law-generate` — the placement/binding mechanics (`source` under `input:`, not `parameters:`). This
  skill decides *which* binding type and *whether* a binding is conceptually sound.
- `regelrecht-stelselanalyse` — cross-law-integriteit (dangling / plain-param) is the **mechanical**
  layer; this skill adds the **conceptual** layer on top (same-concept binding, false-friend
  detection).
