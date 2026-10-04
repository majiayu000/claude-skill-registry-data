---
name: select-design-pattern
kind: skill
status: ready
provenance:
  principles:
  - P008
  - P025
  - P009
  - P013
  claims:
  - C00250
  - C00252
  - C00253
  - C00259
  - C00260
  - C00532
  - C00536
  - C00537
  - C00538
  - C00539
  - C00560
  - C00561
  - C00562
  - C00563
  - C00742
  - C00814
  source_anchors:
  - 0574f24ece08-c0002
  - 0574f24ece08-c0006
  - 5b1b9ca368a5-c0002
  - 5b1b9ca368a5-c0003
  - 5e67c59e0e18-c0003
  authored_from_digest: 01b376ec497ee54f270ae2d9fd89b37269084ae4af04e53080a034e4cb38ee56
---

# Select Design Pattern

## Purpose

Guide the Software Design Reviewer in determining whether a design pattern is warranted and, if
so, which one — acting as a principled gate against speculative pattern use.

A design pattern names and abstracts the key aspects of a common design structure, making it a
reusable solution to a recurring problem within a particular context (PRC-023; clm-073). Each
pattern is fully characterised by four elements: its name, the problem and context in which it
applies, the solution expressed as a general arrangement of collaborating roles, and the
consequences — the trade-offs that applying it entails (clm-074).

Because patterns are not free — one that does not fit its intended problem introduces needless
indirection and complexity rather than removing it (clm-079) — the primary obligation of this
skill is to confirm that a real, recurring structural problem exists before any pattern is
considered, and to recommend the simpler direct design whenever that is sufficient.

## When to use

- A concrete class is tightly coupled to its callers and the concrete type is expected to change
  or vary, making an abstract interface the appropriate decoupling boundary (PRC-022; clm-076).
- A behaviour that must change or be substituted at runtime is being extended through a growing
  class hierarchy; composition over inheritance is being evaluated (PRC-022; clm-077).
- A concept that varies — an algorithm, a creation strategy, a notification routing mechanism —
  has been identified and needs encapsulating behind a stable interface to insulate the rest of
  the system from that variation (PRC-022; clm-078).
- A team is proposing to adopt a named design pattern and needs a principled review before the
  additional structure is committed.

**Do not apply this skill** when no recurring structural problem has been identified. If the
motivation is sophistication, anticipated future extensibility without a present confirmed need,
or familiarity with the pattern rather than structural necessity, this skill issues a refusal
(PRC-007; PRC-023; clm-079).

## Procedure

### Step 1 — Confirm a real recurring problem exists

Before any pattern is considered, the structural problem must be confirmed as real and recurring.

Ask each of the following:

1. **Is the pain concrete?** Can the problem be stated in one precise sentence describing an
   observed or reported structural difficulty — not a generalised desire for extensibility or
   elegance?
2. **Has it recurred?** Has the structural problem arisen more than once in the current design,
   in analogous designs, or in a verified near-term confirmed change? A problem encountered only
   once may be addressed with a targeted direct fix rather than a pattern.
3. **Is it grounded in present requirements?** Is the problem traceable to a real, current
   requirement or to a confirmed change that has already been requested — not to a speculative
   future scenario?

**Decision gate:** if the problem fails any of these three tests, stop and issue the verdict
**"No pattern warranted — problem not confirmed"**, citing PRC-007 and PRC-023. Record which
test failed and why. Do not proceed to pattern selection. Introducing a pattern without a
confirmed recurring problem is speculative complexity (clm-079; PRC-007).

If the problem passes all three tests, write it down in one precise sentence and carry that
statement as the anchor through all remaining steps.

---

### Step 2 — Name the variation point and apply the three decoupling moves

Every pattern addresses a variation point: the concept in the design that changes, has multiple
concrete forms, or must be shielded from callers (PRC-022; clm-078). Naming it precisely is
required before pattern selection can proceed.

**2a. Identify what varies.**
State in one sentence which behaviour, object type, algorithm, structure, or creation strategy
needs to change independently of the rest of the system.

**2b. Apply the three decoupling moves.**
These are the structural principles that any pattern recommendation must satisfy. Work through
each in order:

| Move | Grounding | What it demands |
|---|---|---|
| Program to an interface | PRC-022; clm-076 | Callers depend on an abstract type, not a concrete class; the concrete type is replaceable without modifying callers |
| Favour composition over inheritance | PRC-022; clm-077 | Where behaviour must vary, delegate to a composed object rather than extending a class; composition keeps each class encapsulated and permits substitution at runtime |
| Encapsulate the concept that varies | PRC-022; clm-078 | The variation point identified in 2a is placed behind a stable interface and isolated from the rest of the system |

**2c. Test whether direct decoupling is sufficient.**
If applying the three moves above resolves the confirmed problem without requiring the overhead
of a named catalogue pattern — that is, without multiple prescribed collaborating roles, a
specific object graph structure, or lifecycle control — then a named pattern is not needed.

In that case, issue the verdict **"Direct decoupling is sufficient; no named pattern required"**
and describe the minimal structural change. Do not proceed further.

Only advance to Step 3 if the confirmed problem genuinely requires a named pattern's additional
prescribed structure to be resolved.

---

### Step 3 — Locate candidate patterns by purpose and scope

The pattern catalogue is organised along two axes — **purpose** and **scope** — which together
narrow the search space before individual patterns are examined (clm-075).

**By purpose — which family addresses the confirmed problem?**

| Purpose | What it addresses | Typical variation point |
|---|---|---|
| **Creational** | Decouples clients from the classes they instantiate; controls which concrete type is created and how complex objects are assembled | Which class to create, or how a complex object is built up from parts |
| **Structural** | Composes classes and objects into larger structures; adapts, wraps, or connects interfaces | How objects are connected, adapted, or extended without modifying their definitions |
| **Behavioural** | Distributes responsibility and defines how objects collaborate; controls the flow of requests or algorithms | Which algorithm runs, how a request is routed, or how state changes are communicated |

**By scope — class or object?**

- **Class-scope patterns** fix relationships through inheritance at compile time.
- **Object-scope patterns** fix relationships through composition at runtime. When favouring
  composition over inheritance (clm-077), prefer object-scope candidates.

Identify the one or two families whose purpose aligns with the confirmed problem from Step 1.
For the enumeration of individual patterns within those families, defer to
`../../references/gof-pattern-selection-guide.md`.

---

### Step 4 — Match each candidate against its problem/context and weigh consequences

For each candidate pattern identified in Step 3, evaluate it against all four of the pattern's
essential elements (clm-074):

**4a. Match the problem/context.**
Compare the pattern's stated applicability conditions to the confirmed problem from Step 1. The
match must be substantive — the pattern's reason for existing must correspond to the structural
difficulty that was confirmed, not merely share surface vocabulary with it. A superficial
resemblance is not a match.

**4b. Verify the solution fits.**
Check that the pattern's prescribed arrangement of collaborating roles — interfaces, abstract
classes, concrete implementations, and their relationships — can be introduced within a scope
proportionate to the problem. If adopting the solution requires restructuring far beyond the
problem's blast radius, the pattern is disproportionate.

**4c. Weigh the consequences.**
Every pattern introduces costs alongside its benefits (clm-079). Record the specific
consequences for this candidate:

- How many additional collaborating types does it add?
- Does it reduce or increase coupling between affected components?
- Does a reader need prior familiarity with the pattern to follow the code locally?
- Does it constrain or open up future change relative to the current design?

**4d. Record the verdict for this candidate:** *strong match*, *partial match* (applies but costs
are disproportionate to the problem), or *no match*.

---

### Step 5 — Recommend or decline

Synthesise Steps 1–4 into a single recommendation.

**Recommend the pattern when all of the following hold:**

- The problem from Step 1 is confirmed and recurring.
- The pattern's problem/context is a strong match (Step 4a).
- The solution can be introduced within a scope proportionate to the problem (Step 4b).
- The structural benefit — reduced coupling at the variation point, reduced future change
  amplification — outweighs the indirection and additional complexity the pattern introduces
  (Step 4c; clm-079).

**Recommend direct decoupling when:**

- The three moves from Step 2b resolve the problem without a named pattern (Step 2c).
- The candidate pattern's costs — additional collaborating types, required pattern-awareness,
  lifecycle complexity — exceed the structural benefit for this specific problem.
- The problem is isolated or unlikely to recur beyond a single instance, making the simpler
  targeted fix preferable (clm-079; PRC-007).

**Issue a refusal when:**

- No confirmed recurring problem was found in Step 1.
- The motivation is sophistication, anticipated future extensibility, or familiarity with the
  pattern rather than a confirmed structural need (PRC-023; clm-079; PRC-007).

**State the verdict explicitly using one of three labels:**

| Verdict | When to use |
|---|---|
| **Pattern recommended** | Name the pattern, cite its problem/context match, state the trade-offs accepted, and describe the bounded structural change required |
| **Direct decoupling sufficient** | Describe the three-move application without a named pattern; no further prescribed structure is needed |
| **No pattern warranted** | State why, citing the governing principle (PRC-007; PRC-023; clm-079); do not propose an alternative pattern as consolation |

## Inputs

| Field | Required | Description |
|---|---|---|
| `artefact` | Yes | The code, design document, or interface description under review |
| `requirements` | Yes | The present known requirements governing this artefact; speculative future needs do not count |
| `reported_problem` | Yes | The concrete structural pain that prompted consideration of a pattern, in the submitter's own words |
| `recurrence_evidence` | No | Concrete examples of the problem occurring more than once; strengthens or weakens Step 1's verdict |
| `lifetime` | No | Anticipated system lifetime; calibrates how much structural investment is proportionate |
| `team_conventions` | No | Legitimate local conventions that may affect whether a pattern is idiomatic in this codebase |

## Output

A structured recommendation containing, in order:

1. **Verdict** — one of *Pattern recommended*, *Direct decoupling sufficient*, or *No pattern
   warranted*, stated as a single sentence with the governing principle cited.
2. **Problem statement** — one sentence restating the confirmed recurring structural problem, or
   stating that none was confirmed and the specific reason why.
3. **Variation point** — the concept that varies, named precisely; present even when the verdict
   is a refusal, if a variation point was claimed by the submitter.
4. **Decoupling-move analysis** — a brief assessment of how the three moves (program to an
   interface, favour composition over inheritance, encapsulate what varies) apply to the problem,
   and whether they are sufficient on their own.
5. **Pattern rationale** *(present only when the verdict is "Pattern recommended")* — the
   pattern's name, its purpose–scope position in the catalogue, the problem/context match, and
   the specific trade-offs accepted.
6. **Bounded structural change** — the minimum set of structural changes required to realise the
   recommendation. No replacement code; a structural sketch or description only.

The minimum useful output is the verdict sentence and one sentence explaining the primary reason
for it.

## References

- [`../../references/gof-pattern-selection-guide.md`](../../references/gof-pattern-selection-guide.md) —
  Concrete pattern catalogue organised by purpose (creational / structural / behavioural) and
  scope (class / object); used in Step 3 to identify candidate families and in Step 4 to check
  each pattern's problem/context and stated consequences for individual patterns.
- [`../../principles/principles.yaml`](../../principles/principles.yaml) —
  PRC-022 (decouple through abstraction: program to an interface, favour composition over
  inheritance, encapsulate the concept that varies);
  PRC-023 (apply design patterns as named, problem-driven solutions with explicit trade-offs —
  selected against the problem they solve and applied judiciously, never gratuitously);
  PRC-007 (reject speculative generality and unneeded abstraction — design only as generic as
  present known requirements demand).

## Provenance

Derived from principles PRC-022 and PRC-023 and their supporting claims clm-073, clm-074,
clm-075, clm-076, clm-077, clm-078, and clm-079, as recorded in `principles/principles.yaml`,
and grounded in source anchors `erich-gamma-richard-80cb534a-h0017`, `h0010`, `h0012`, `h0015`,
`h0016`, `h0018`, and `h0019` from *Design Patterns: Elements of Reusable Object-Oriented
Software*.

**Rights notice:** the source text (`erich-gamma-richard-80cb534a`) is distillation-only. All
content in this skill has been paraphrased into original language; no verbatim runs of source
wording appear anywhere in this file.
