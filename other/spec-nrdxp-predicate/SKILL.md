---
name: spec
description: |
  SOP for normative specification and behavioral contracts.
  Trigger when:
  - Defining invariants, permitted transitions, and forbidden states.
  - Navigating steps: Identify, Formalize, Verify, Record, Connect.
  - Prompt contains: /spec, spec workflow, normative constraint, invariant, BCP 14.
---

# SPEC — Normative Specification Workflow

**Identify → Formalize → Verify → Record → Connect**

**Verification Dual — symbolic path.** SPEC produces the normative constraint artifacts that are checked by the symbolic half of the [Verification Dual](../../rules.md#2-prime-invariants): every constraint this workflow formalizes becomes a deterministic evaluator target (a test invariant, a type-level proof obligation, or a model-checker input) that closes a condition on the symbolic path. Routed at the moment of specifying invariants and behavioral contracts ([rules.md §5](../../rules.md#5-skill-routing)).

This workflow defines the C.O.R.E. Specification phase. The objective is to define high-density normative constraint vectors (behavioral contracts) that prune the phase-space of valid trajectories during code generation. Where `/form` describes the system's states and transitions (coalgebraic dynamics), `/spec` declares what MUST hold (modal specification) and translates these constraints into test invariants.

---

## Philosophy

A model is a representation. A specification is a contract.

Models are descriptive — they map the state-space and operational dynamics. Specifications are normative — they declare invariants that must remain stable and transition conditions that are permitted. This distinction maps precisely to the behavior/specification duality formalized in SDMA §11 (Stone duality: coalgebraic dynamics ↔ modal specification).

Without explicit specifications, sequence walks rely on stochastic priors. Every corrective feedback loop caused by trajectory drift is the cost of a missing specification. SPEC minimizes this drift by establishing explicit, deterministic constraints before execution, translating them into executable test suites.

---

## Scope

> [!IMPORTANT]
> SPEC produces **normative constraint artifacts** — declarations of what a system MUST, SHOULD, MUST NOT, and MAY do. It is NOT structural modeling (that's `/form`) and NOT implementation (that's `/core`); strategic planning and exploration are the standing [Planning Invariants](../../ambient.md#planning-invariants) and [Sketch Principle](../../ambient.md#the-sketch-principle), not workflows you switch into. If you find yourself describing ontology without constraints, you're in `/form` territory. If you find yourself evaluating approaches rather than declaring constraints, you've left SPEC for strategy.

---

## Normative Language

Specifications use normative keywords as defined in [BCP 14](https://www.rfc-editor.org/info/bcp14) (RFC 2119, RFC 8174):

> The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in specification documents produced by this workflow are to be interpreted as described in BCP 14 when, and only when, they appear in all capitals.

This convention is not ceremonial — it is the single most effective mechanism for eliminating behavioral ambiguity. An agent client interpreting "the system must validate input" will treat it as a recommendation. An agent client interpreting "the system MUST validate input" treats it as a non-negotiable requirement.

---

## Dual-Mode Operation

Like `/form`, SPEC operates in two modes, determined by context:

### Create Mode

**Trigger:** No existing system specified. The human requests a behavioral specification for a new domain.

**Flow:** Produce a new specification artifact from `templates/SPEC.md`, committed to `docs/specs/`.

**Output:** A complete specification with all template sections filled.

### Apply Mode

**Trigger:** An existing system, document, or implementation is specified.

**Flow:** Extract and formalize the normative constraints implicit in the system's design. Surface unwritten assumptions, missing invariants, and behavioral gaps.

**Output:** Either a standalone specification in `docs/specs/` or annotations integrated into the target document (human's choice).

> [!NOTE]
> Apply mode is where /spec often delivers the most value — surfacing the behavioral rules that everyone assumes but nobody has written down.

---

## Formalism Selection

SPEC is **notation-agnostic**. The formalism scales with the system's criticality, mirroring how `/form` selects formalisms via the SDMA Decision Matrix (SDMA §6).

| System Criticality                        | Specification Notation                                              | Verification Method                                |
| :---------------------------------------- | :------------------------------------------------------------------ | :------------------------------------------------- |
| **Low** (internal tools, scripts)         | Structured prose with explicit INVARIANT / MUST / MUST NOT blocks   | Agent self-verification                            |
| **Medium** (libraries, APIs, protocols)   | Alloy (structural constraints), TLA+ (behavioral/temporal)          | LLM-integrated formal verification or model finder |
| **High** (cryptographic, safety-critical) | Full Alloy + TLA+ with proof obligations, optionally Lean/Coq proof | Dedicated model checker, proof assistant           |

> [!IMPORTANT]
> **Verification is mandatory at every tier.** A specification that hasn't been checked for internal consistency is not a specification — it's a wish list. The verification method scales with the notation, but verification itself is never optional.

### Selecting the Right Level

Use these heuristics:

- If the constraints are simple enough to express as "X MUST/MUST NOT Y" → Tier 1 (prose)
- If the constraints involve state transitions, concurrent access, or relational structure → Tier 2 (Alloy/TLA+)
- If correctness failures have security, financial, or safety implications → Tier 3 (with proof)

When in doubt, err toward more formalism. The cost of over-specifying is ceremony; the cost of under-specifying is implementation bugs.

### Domain Conventions

Criticality is not the only axis. Many domains have **established specification traditions** with their own formats, conventions, and tooling. When a domain convention exists, prefer it over a generic notation — it carries decades of community-tested structure and will be more natural for both human reviewers and agents trained on that corpus.

Common domain-specific specification formats:

| Domain                   | Established Format                                       | When to Use                                                |
| :----------------------- | :------------------------------------------------------- | :--------------------------------------------------------- |
| Network protocols        | IETF RFC format with ABNF grammars (RFC 5234)            | Specifying wire formats, message sequences, state machines |
| APIs                     | OpenAPI / AsyncAPI                                       | Specifying REST/event-driven API contracts                 |
| Data validation          | JSON Schema / XML Schema                                 | Specifying structural constraints on data interchange      |
| Programming languages    | EBNF grammars + operational/denotational semantics       | Specifying syntax and evaluation rules                     |
| Requirements engineering | IEEE 830 / ISO/IEC/IEEE 29148                            | Specifying system-level requirements for large projects    |
| Cryptographic protocols  | Formal security models (UC framework, game-based proofs) | Specifying security properties and adversary models        |

These formats are not alternatives to the SPEC.md template — they complement it. The SPEC.md template captures the **predicate-internal normative layer** (invariants, transitions, forbidden states, verification tags). Domain-specific formats live inside the template's **Formal Specification** section, providing the domain-standard representation alongside the predicate-internal constraints.

> [!TIP]
> If the domain has an established specification format, use it. The SPEC.md template's "Formal Specification" section is designed to host domain-standard notation. The constraint sections above it provide the pipeline-internal normative layer; the formal specification section provides the domain-standard layer.

---

## Procedure

### Step 1: IDENTIFY

Determine what needs constraining. Sources of normative constraints:

- **The model** (if one exists): What states, transitions, and observers does it define? What structural properties must hold?
- **The governing IBC** (if one exists): What strategic non-goals impose behavioral bounds?
- **Domain knowledge**: What invariants are assumed but unwritten? What "everyone knows" but nobody has documented?
- **Failure modes**: What MUST NEVER happen? What would constitute a critical failure?
- **Existing implementations**: What behavioral rules are encoded in code but not documented?

**Create mode:** Absorb the domain description, identify the behavioral boundaries.

**Apply mode:** Read the target system thoroughly. Identify every implicit invariant, every assumed pre-condition, every unwritten "this should never happen."

### Step 2: FORMALIZE

Express constraints using the notation appropriate to the system's criticality tier.

**All tiers require:**

- **Named constraints**: Every constraint has a unique, descriptive identifier (e.g., `no_empty_completion`, `session_required_for_spawn`)
- **Typed references**: Constraints reference typed entities — either from the model's ontology or declared inline. Untyped prose ("the system should be fast") is an aspiration, not a constraint.
- **Normative keywords**: Use BCP 14 keywords (MUST, MUST NOT, SHOULD, MAY) with their defined meanings.
- **Verification tags**: Each constraint carries a `VERIFIED` tag indicating its verification status (populated in VERIFY).

**Tier 2+ additionally requires:**

- Formal notation (Alloy signatures/facts/predicates, TLA+ state predicates/actions/temporal properties)
- Explicit proof obligations (what needs to be verified and at what level)

> [!IMPORTANT]
> **HALT after FORMALIZE.** Present the specification to the human before verification. Wrong constraints verified are worse than unverified correct constraints — challenge the constraints before investing in verification.

### Step 3: VERIFY

Verify the specification at the appropriate level. Verification has three sub-tiers:

1. **Consistency**: Is the specification internally coherent? No contradictions between invariants, no unreachable states, no vacuous constraints (constraints trivially satisfied by every state — meaning they constrain nothing).
2. **Conformance** (if model exists): Does the model's state space satisfy the specification? Can the model reach a state that violates a constraint?
3. **Proof** (Tier 3 only): Can we formally prove that the model satisfies the specification? This is where Lean, Coq, or Alloy's exhaustive model finding applies.

Tag each constraint with its verification result:

- `VERIFIED: proof` — formally proven (Lean, Coq, exhaustive model check)
- `VERIFIED: machine` — machine-checked for consistency (Alloy Analyzer, TLC)
- `VERIFIED: agent-check` — agent self-verification (weakest guarantee)
- `UNVERIFIED` — not yet verified, with rationale for deferral

> [!CAUTION]
> Do NOT mark a constraint as `VERIFIED: machine` when it was actually `VERIFIED: agent-check`. The distinction matters — downstream consumers rely on the tag to know where the specification's guarantees have teeth and where they have only aspiration.

### Step 4: RECORD

Commit the specification artifact.

**Create mode:**

- Fill all sections of `templates/SPEC.md`
- Commit to `docs/specs/<domain-name>.md`

**Apply mode:**

- Either produce a standalone specification in `docs/specs/`, or integrate findings into the target document (human's choice)
- If standalone: use `templates/SPEC.md` with the Target System field populated
- If integrated: annotate the target document with normative constraint blocks

> [!IMPORTANT]
> **Template discipline.** Create mode documents MUST use `templates/SPEC.md`. Ad hoc formats are a protocol violation.

### Step 5: CONNECT (Test Invariant Mapping)

Link the specification constraints to execution-level verification targets:

- **Generate Test Invariants**: For every named constraint, define a test invariant specification (e.g. mock assertions, property tests, or trace boundaries).
- **Assemble Verification Suite**: Map these invariants to specific test cases in the project's test suite, creating the deterministic evaluator $V(\mathbf{S})$ for execution.
- Cross-reference any form artifact in `docs/specs/` — the spec constrains the form's state space.
- Link constraints to downstream execution, ensuring they become non-negotiable step verification assertions when `/core` regulates state against them.
- If the spec reveals model inadequacies, flag them for `/form` revision.
- Update the sketch with specification findings.

---

## State Transitions

```
IDENTIFY  ──→ FORMALIZE   (constraints identified)
          └─→ ABORT       (nothing worth specifying)

FORMALIZE ──→ VERIFY      (human approves constraints)
          └─→ IDENTIFY    (wrong scope — need to reframe)

VERIFY    ──→ RECORD      (spec passes verification)
          └─→ FORMALIZE   (verification failures require revision)

RECORD    ──→ CONNECT     (artifact committed)

CONNECT   ──→ DONE        (context linked)
```

---

## MANDATORY HALT Points

You MUST stop and await human input at:

1. **After FORMALIZE:** Constraints must be human-approved before verification begins
2. **After VERIFY (if failures):** Human decides whether to revise or accept partial verification
3. **ESCALATION:** If the spec contradicts the model or an upstream strategic frame, emit ESCALATION per the **Strategic Escalation** invariant in [ambient.md](../../ambient.md#planning-invariants) and HALT

---

## Specification Storage

```
docs/
└── specs/
    └── <domain-name>.md    # specification artifact
```

Specification filenames should be descriptive of the domain being constrained, not the formalism used. Example: `docs/specs/identity-protocol.md`, not `docs/specs/alloy-spec-1.md`.

---

## Specification Rot Prevention

Specifications are living artifacts. Rot prevention uses existing pipeline infrastructure:

- **Model changes** → spec re-verification required (surfaced by `/form`'s CONNECT step)
- **Execution deviates from spec** → ESCALATION fires per the **Strategic Escalation** invariant in [ambient.md](../../ambient.md#planning-invariants)
- **`/core` discovers spec is wrong** → empirical invalidation: emit an ESCALATION block and HALT for the human to choose the response (re-frame, dialectic, or descope), per the same [Strategic Escalation](../../ambient.md#planning-invariants) invariant

---

## Position in the Workflow Chain

```
explore → frame → /form → /spec → /core
(ambient dispositions)  (what)  (must)  (do)
                          ↑        ↓
                          └─ cross-reference ─┘
```

Exploring and framing are standing dispositions — the [Sketch Principle](../../ambient.md#the-sketch-principle) and the [Planning Invariants](../../ambient.md#planning-invariants) — not workflows you switch into. SPEC can be invoked standalone or from within any other workflow. A specification produced while exploring informs the strategy that follows; one produced during `/core` validates implementation decisions. The specification is a _normative tool_ available at any point.

**Where it fits:**

- **After `/form`**: The natural position. The form defines the ontology; the spec constrains it. Execution then operates within those constraints.
- **Without `/form`**: Valid. Not every system needs a formal model, but many need behavioral contracts. `/spec` can be invoked with inline type declarations instead of model references.
- **During `/core`**: Valid. If `/core` discovers undocumented behavioral requirements, invoking `/spec` mid-execution captures them as normative artifacts rather than ad hoc code comments.

---

## Integration with Sketch Lifecycle

If a sketch exists for the current workstream:

- IDENTIFY findings are written to the sketch
- FORMALIZE rationale is written to the sketch
- VERIFY results are written to the sketch
- Each sketch update is committed immediately

The sketch captures the _specification journey_; the spec document captures the _normative outcome_.

---

## Prime Directives

1. **VERIFICATION_MANDATORY:** Every constraint must carry a `VERIFIED` tag. Untagged constraints are protocol violations. Deferred verification is acceptable with explicit rationale; silent omission is not.

2. **NORMATIVE_NOT_DESCRIPTIVE:** If you're describing structure without declaring what must hold, you're modeling, not specifying. Every statement in a specification should use normative language (BCP 14 keywords).

3. **TYPED_CONSTRAINTS:** Constraints MUST reference typed entities. "The system should be reliable" is not a constraint. "Service uptime MUST NOT fall below 99.9% over any rolling 30-day window" is.

4. **FORMALISM_SCALES:** Use the simplest formalism that provides adequate verification. Don't force Alloy on a config validation check. Don't use prose for a cryptographic protocol.

5. **HALT_ON_CONTRADICTION:** If verification reveals contradictions between constraints, you are FORBIDDEN from proceeding to RECORD. Surface to human.

6. **TEST_INVARIANT_MAPPING:** Every normative constraint MUST map to an executable test invariant in the verification suite. Sourcing code edits without compiling the corresponding test invariant is forbidden.

### Protocol Violations (FORBIDDEN)

| Violation                                           | Why It's Wrong                                          |
| :-------------------------------------------------- | :------------------------------------------------------ |
| Constraints without `VERIFIED` tags                 | Downstream consumers can't distinguish rigor levels     |
| `VERIFIED: machine` on an agent-checked constraint  | Misrepresents the verification guarantee                |
| Untyped normative claims                            | Aspirations masquerading as constraints                 |
| Specification without normative keywords            | Descriptions masquerading as specifications             |
| Modifying spec without committing                   | Breaks changelog; decision history is lost              |
| Proceeding to RECORD with unresolved contradictions | Incoherent spec cascades into incoherent implementation |
| Constraints without explicit test invariant mapping | Implementation loses its deterministic verification validator |