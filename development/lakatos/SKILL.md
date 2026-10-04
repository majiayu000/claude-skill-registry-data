---
license: Apache-2.0
name: lakatos
description: Philosophy of science methodology examining how research programs evolve through proofs and refutations
category: Research & Academic
tags:
  - philosophy-of-science
  - methodology
  - research-programs
  - falsification
  - epistemology
---

# SKILL.md: Proofs and Refutations — The Logic of Discovery

license: Apache-2.0
```yaml
name: proofs-and-refutations
version: 1.0
source: "Proofs and Refutations: The Logic of Mathematical Discovery — Imre Lakatos"
description: >
  A framework for reasoning under uncertainty, handling counterexamples,
  refining concepts iteratively, and understanding how knowledge actually
  grows through conjecture-refutation dialectics rather than accumulation
  of certified truths.
activation_triggers:
  - debugging complex systems where errors are ambiguous or hard to localize
  - designing ontologies, schemas, or type systems
  - handling edge cases, boundary conditions, or unexpected inputs
  - evaluating whether a proof, argument, or reasoning chain is sound
  - deciding how to respond to falsification or refutation of a hypothesis
  - building systems that must learn or improve from failure
  - coordinating across disagreement about definitions or success criteria
  - any situation where "is this really a counterexample?" is a live question
```

---

## When to Use This Skill

Load this skill when:

- **A system or argument fails** and you need to decide whether the failure invalidates the whole approach or just a sub-component
- **Edge cases appear** that don't fit existing categories — and you must decide whether to expand definitions, exclude the case, or revise the conjecture
- **Definitions are contested** — when what counts as X is genuinely unclear and the answer matters for the conclusion
- **You're tempted to redefine terms** to make a problem go away rather than solve it
- **Someone presents a "proof"** and you need to assess what it actually establishes vs. what it assumes
- **Ontologies or schemas are being designed** and there's pressure to finalize them before adequate testing
- **A reasoning chain reaches a wrong answer** and you need to extract value from the failure rather than just discarding it
- **A system appears to be learning** but may actually be progressively narrowing its success criteria

---

## Core Mental Models

### 1. Proofs Decompose, They Don't Certify

A proof does not establish truth — it **breaks a conjecture into sub-conjectures (lemmas)**, each independently criticizable. Even a proof of a *false* conjecture is productive: it maps the hidden assumptions and creates new targets for inquiry. The "failed" reasoning chain is a diagnostic, not just waste.

> **Operational implication**: When a reasoning chain produces a wrong answer, don't discard it — trace which lemma failed. The map of failure is often more valuable than the original goal.

### 2. Monster-Barring vs. Genuine Learning

When a counterexample appears, there are fundamentally different responses:
- **Monster-barring**: Redefine terms to exclude the counterexample by fiat ("that's not a *real* polyhedron") — preserves the conjecture but hollows it out
- **Lemma-incorporation**: Absorb the counterexample's lesson into a refined conjecture with explicit conditions
- **Surrender**: Abandon the conjecture as genuinely false

Monster-barring *feels* like clarification but is concept-contraction driven by the desire to protect a result. Systems that keep redefining success criteria to exclude inconvenient cases appear to learn while becoming more brittle.

### 3. Local vs. Global Counterexamples

A counterexample can attack:
- **A lemma (local)**: The argument is flawed, but the conjecture may still be true — *repair the proof*
- **The conjecture itself (global)**: The claim is wrong — *revise or abandon*

Conflating these causes two failure modes: (a) abandoning good conjectures because a sub-argument failed, or (b) defending bad conjectures by patching sub-arguments indefinitely.

> **Triage rule**: Before deciding what a counterexample *means*, first determine what it *hits*.

### 4. Definitions Are Products of Inquiry, Not Preconditions

The right definition of a concept cannot be determined at the outset — it **emerges from pressure applied by counterexamples**. Every boundary case is an opportunity to discover what the concept actually needs to be. Initial ontologies are provisional hypotheses, not fixed infrastructure.

> **Operational implication**: Treat schema freeze dates with suspicion. The concepts that matter most will be the ones that haven't been stress-tested yet.

### 5. The Dialectic Cannot Be Shortcut

The "Perfect Definition" move — define the domain as exactly the set of things for which the conjecture holds — collapses inquiry into triviality. Progress requires **maintaining tension** between conjecture and domain. Any architecture too eager to resolve ambiguity, lock down schemas, or close open questions will systematically prevent learning that only happens at the boundary between what works and what doesn't.

---

## Decision Frameworks

### When a Failure Appears

```
Is the failure in the argument or the claim?
├── Attack on a lemma (local) → Repair the proof; conjecture survives
│   ├── Can the lemma be rescued? → Revise sub-argument
│   └── Lemma is genuinely false → Weaken the conjecture's conditions (lemma-incorporation)
└── Attack on the conjecture (global) → Revision required
    ├── Is the counterexample a "monster"? → Check: am I excluding it to protect the conjecture?
    │   ├── Yes (monster-barring) → Dangerous; examine what you're giving up
    │   └── No (genuinely outside scope) → Narrow domain explicitly and document why
    └── Counterexample is legitimate → Revise conjecture or surrender
```

### When Encountering a Counterexample

| Response | What it does | When it's legitimate | When it's a trap |
|---|---|---|---|
| **Surrender** | Abandons conjecture | Global counterexample is valid | Counterexample was only local |
| **Monster-barring** | Redefines to exclude | Genuinely outside intended scope | Protecting conjecture from real falsification |
| **Exception-barring** | Restricts domain explicitly | Principled scope limitation | Scope kept shrinking to preserve result |
| **Lemma-incorporation** | Adds condition to conjecture | Local failure, fixable | Used to hide unresolvable problems |
| **Concept-stretching** | Expands definition to cover case | Genuine generalization | Forces alien cases into concept |

### When Designing a Schema or Ontology

```
Is there pressure to finalize definitions before boundary cases are tested?
└── Yes → Treat current definitions as v0 hypotheses; document known gaps
    
Are there cases the current schema handles awkwardly?
└── Yes → These are not "edge cases to handle later" — they are diagnostic pressure
    └── What would the concept need to be for these to fit naturally?
        └── That question is more valuable than patching the current schema
```

### When Evaluating a Proof or Argument

```
What does this proof actually establish?
1. List the lemmas (explicit and implicit)
2. Which lemmas are independently verified vs. assumed?
3. If a lemma fails, does the conjecture fall or just the argument?
4. What domain assumptions are embedded silently?
```

---

## Reference Files

| File | When to Load |
|---|---|
| `references/proofs-as-decomposition-not-certification.md` | When evaluating what a proof or reasoning chain actually establishes; when extracting value from a "failed" argument; when assessing implicit assumptions in a chain of reasoning |
| `references/monster-barring-and-concept-stretching.md` | When a counterexample appears and there's temptation to redefine terms; when a system seems to be "learning" by progressively narrowing its success criteria; when definitions keep shifting after failures |
| `references/local-vs-global-counterexamples-error-triage.md` | When triaging a failure — deciding whether it invalidates the whole approach or just a sub-component; when doing root cause analysis; when deciding whether to abandon or repair an approach |
| `references/definitions-as-products-not-preconditions.md` | When designing or freezing ontologies, schemas, or type systems; when initial categories are failing under boundary cases; when asked to specify definitions before testing |
| `references/the-dialectic-of-conjecture-and-refutation.md` | When understanding the overall arc of how knowledge grows; when a system's learning process needs to be evaluated or designed; foundational framing for most other references |
| `references/the-problem-of-concept-extension-and-boundary-cases.md` | When boundary or edge cases are accumulating and need a principled treatment; when deciding whether to expand, restrict, or revise a concept under pressure |
| `references/the-social-structure-of-rigorous-inquiry.md` | When coordinating across agents or team members who disagree; when a single reasoner is making all calls without challenge; when epistemic role distribution matters |
| `references/the-gap-between-knowing-and-proving.md` | When a conjecture is highly credible but unproven; when deciding whether to act on an unproven hypothesis; when distinguishing justified confidence from formal proof |

---

## Anti-Patterns

These are the failure modes Lakatos most directly warns against:

**1. Monster-Barring by Drift**
Redefining terms incrementally after each counterexample, so no single redefinition looks unreasonable, but the cumulative effect is that the "theorem" now applies to almost nothing. The warning sign: each revision feels like a clarification.

**2. Treating Schema Freeze as Progress**
Locking down definitions and ontologies before they've been stress-tested by boundary cases. The result is a system that handles everything it was tested on and fails badly at everything it wasn't.

**3. Conflating Proof Failure with Conjecture Failure**
Abandoning a correct conjecture because a particular argument for it failed. The argument failing is information about the argument, not necessarily the claim.

**4. The Trivializing Perfect Definition**
Defining the domain as exactly the set of things for which the result holds, then claiming the theorem is proven. This is the death of inquiry dressed as rigor.

**5. Missing the Value in Failed Reasoning**
Discarding a reasoning chain that reached a wrong conclusion instead of tracing which lemma failed. Failed proofs are maps; throwing away the map is waste.

**6. Concept-Stretching Under Pressure**
Forcing genuinely alien cases into an existing concept rather than admitting the concept needs revision or a new concept is needed. Produces categories that are simultaneously too broad and too narrow.

**7. Solo Epistemics**
A single agent making all decisions about what counts as a counterexample, what counts as monster-barring, and whether a proof is sound — without structures that enable genuine challenge. Lakatos's dialogue format is itself an argument about process.

---

## Shibboleths

*How to tell if someone has actually internalized this book vs. just read the summary:*

**They have internalized it if they:**
- Spontaneously ask "is this a local or global counterexample?" before deciding how to respond to failure
- Treat a wrong-answer reasoning chain as *diagnostic* rather than just discarding it
- Become suspicious when their definitions keep getting refined in the wake of counterexamples — and can say *why* that's suspicious
- Recognize the "perfect definition" move as a trap and can name what's lost
- Talk about proofs as *programs of decomposition* rather than as certificates
- Ask "what hidden lemmas is this argument relying on?" when evaluating someone else's reasoning
- Treat the boundary cases as *the interesting part* of a problem, not the annoying part

**They have only read the summary if they:**
- Use "monster-barring" as a generic insult for any definitional refinement, rather than a specific failure mode with specific conditions
- Think the lesson is "be open to counterexamples" — too vague, misses the precise taxonomy
- Think "definitions emerge from inquiry" means "don't define things upfront" — it means definitions are *hypotheses* that should be tested, not avoided
- Cannot distinguish between when lemma-incorporation is legitimate versus when it's covering for a fundamentally broken conjecture
- Treat the social/dialogic structure as stylistic rather than as a substantive claim about what rigorous inquiry requires

---

*Load reference files on demand as specific situations arise. The dialectic of conjecture and refutation cannot be shortcut — neither can reading these references selectively based on what the situation actually requires.*