---
name: form
description: |
  SOP for formal mathematical domain modeling.
  Trigger when:
  - Creating new formal models or applying mathematical lenses to analyze existing specifications.
  - Navigating phases: Identify, Select, Construct, Validate, Record, Connect.
  - Prompt contains: /form, form workflow, categorical, coalgebraic, linear logic, information-theoretic, validation.
---

# FORM Protocol v2.0 (Control-Theoretic Modeling)

**Identify → Select → Construct → Validate → Record → Connect**

This workflow defines the C.O.R.E. Modeling phase. The objective is to define the formal structural representation of a domain, establishing the state space, transition relationships, and coalgebraic dynamics. This serves as the structural foundation from which normative constraints and test invariants are derived.

---

## Philosophy

Formal models are the bridge between empirical observations and proof. An olog, a coalgebra, a session type specification — each makes implicit relationships explicit and mathematically verifiable. Without formal models, sequence trajectories are guided by anthropomorphic verbal descriptions that cannot be checked or formally composed.

FORM provides the procedure for constructing these structural representations. The `sdma` skill defines a foundational toolkit of categorical, coalgebraic, and information-theoretic isomorphisms. The principle of **minimal representation** governs selection: choose the simplest mathematical formalism that faithfully captures the domain's structure, and use it to map the state space for subsequent verification loops.

---

## Scope

> [!IMPORTANT]
> FORM produces formal model documents — either creating new ones from `templates/MODEL.md` or scrutinizing existing documents (protocol specs, whitepapers, design docs) through the SDMA lens. It is structural analysis, not planning, exploration, or implementation: strategic planning and exploration are the standing [Planning Invariants](../../ambient.md#planning-invariants) and [Sketch Principle](../../ambient.md#the-sketch-principle), and implementation is `/core`. If you find yourself writing code or redesigning architecture, you've left FORM territory.

---

## Dual-Mode Operation

MODEL operates in two modes, determined by context:

### Create Mode

**Trigger:** No existing document specified. The human requests a formal model for a domain or problem.

**Flow:** Produce a new model document from `templates/MODEL.md`, committed to `docs/models/`.

**Output:** A complete model document with all five template sections filled.

### Apply Mode

**Trigger:** An existing document is specified (protocol spec, whitepaper, design doc, etc.).

**Flow:** Scrutinize the existing document through the SDMA lens. Identify which formalisms apply, what structure is implicit, where rigor is missing, and what the formal model reveals.

**Output:** Either annotations/refinements to the existing document, or a companion model document in `docs/models/` that formalizes the document's domain.

> [!NOTE]
> In Apply mode, the target document may not need all SDMA formalisms. The Decision Matrix (SDMA §6) determines which tools are relevant. Don't force a formalism where none is warranted.

---

## Grammar

```yaml
# 1. STATE METADATA
STATUS: [IDENTIFY | SELECT | CONSTRUCT | VALIDATE | RECORD | CONNECT]

# 2. CONTEXT
CTX:
  MODE: [CREATE | APPLY]
  DOMAIN: "Problem domain being modeled"
  TARGET: "path/to/existing/doc.md" # Apply mode only
  SCOPE: "What aspect of the domain to model"

# 3. FORMALISM SELECTION (populated in SELECT)
FORMALISM:
  PRIMARY: "Selected representation (from Decision Matrix)"
  SUPPORTING: ["Additional formalisms if layered"]
  RATIONALE: "Why this formalism fits the domain"

# 4. MODEL (populated in CONSTRUCT)
MODEL:
  TYPE: "Olog | Coalgebra | Session Type | LinRel | Hyperdoctrine | ..."
  COMPONENTS: ["Key structural elements of the model"]

# 5. VALIDATION (populated in VALIDATE)
VALIDATION:
  CHECKS:
    - CHECK: "What was verified"
      RESULT: [PASS | FAIL | PARTIAL]
      DETAIL: "Specifics"
```

---

## Procedure

### Step 1: IDENTIFY

Characterize the problem domain and determine what needs formal modeling.

**Create mode:**

- Absorb the domain description from the human
- Identify the core structural characteristics (state, resources, protocols, constraints, metrics)
- Frame the modeling question: "What would a formal model of this domain reveal?"
- **Premise check:** Is the domain as the user describes it, or as the user *believes* it to be? If the user says "this is fundamentally a state machine problem," verify that independently before allowing the framing to constrain formalism selection.

**Apply mode:**

- Read the target document thoroughly
- Identify implicit structure: What entities exist? What relationships? What invariants?
- Identify structural weaknesses: Where is the document vague, ambiguous, or inconsistent?
- Frame the analysis: "What does the SDMA lens reveal about this document's domain?"

### Step 2: SELECT

Choose the appropriate formalism(s), starting from the Decision Matrix (SDMA §6) but not constrained by it.

**Both modes:**

- Apply the Decision Matrix as a starting point for formalism selection
- If the domain is well-served by an SDMA formalism, use it — the SDMA covers the most critical isomorphisms in computer science
- If the domain requires a formalism outside the SDMA toolkit, select it — the SDMA is a bedrock to build from, not a closed set
- Apply the **principle of minimal representation**: choose the simplest formalism that faithfully captures the domain's essential structure
- If multiple characteristics are present, determine the layering strategy
- Document the rationale for selection and alternatives considered
- **Independence check:** Would you have selected this formalism if the user hadn't suggested or implied a direction? If the user said "I think this is categorical," verify that claim against the domain's actual structure rather than accepting it as a constraint. If competing formalisms have genuinely comparable merit and the stakes are high, escalate to the [Dialectic Principle](../../ambient.md#the-dialectic-principle) — cross-model sampling for a decorrelated second opinion.

> [!IMPORTANT]
> **HALT after SELECT.** Present the formalism selection and rationale to the human before constructing the model. Wrong formalism choice cascades into wasted work.

### Step 3: CONSTRUCT

Build the formal model.

**Create mode:**

- Construct the model using the selected formalism
- Follow the SDMA guidelines for the chosen tool (olog construction rules, coalgebra observer patterns, session type definitions, etc.)
- Ensure the model captures the domain's essential structure without unnecessary complexity

**Apply mode:**

- Extract the formal structure implicit in the target document
- Construct the model that makes this structure explicit
- Note where the target document's claims are supported or contradicted by the formal model

### Step 4: VALIDATE

Verify the model's internal consistency, external adequacy, and framing assumptions.

- **Internal consistency:** Does the model satisfy its own structural constraints? (Diagram commutativity for ologs, bisimulation closure for coalgebras, session type duality, etc.)
- **External adequacy:** Does the model capture the domain faithfully? Are there domain properties that the model cannot express?
- **Minimality:** Is the model unnecessarily complex? Could a simpler formalism capture the same properties?
- **Assumption independence:** Revisit the framing from IDENTIFY. Now that the model is constructed, does the domain's actual structure confirm the assumptions that guided formalism selection? A model can be internally consistent yet built on an unchallenged framing error — the formalism "works" because the wrong question was asked precisely.
- **Upstream coherence:** Does the validated model contradict any upstream strategic artifact — the governing IBC's goal, a plan's assumptions, or an existing ADR's rationale? If the model reveals that an upstream premise is false, emit an ESCALATION block per the **Strategic Escalation** invariant in [ambient.md](../../ambient.md#planning-invariants) and HALT. A valid model that contradicts the IBC is a discovery, not an error.

Document all validation checks and their results.

### Step 5: RECORD

Commit the model as a durable artifact.

**Create mode:**

- Fill all five sections of `templates/MODEL.md`
- Commit to `docs/models/<domain-name>.md`

**Apply mode:**

- Either produce a companion model document in `docs/models/`, or integrate findings directly into the target document (human's choice)
- If companion: use `templates/MODEL.md` with the Source Document field populated
- If integrated: annotate the target document with formal observations

> [!IMPORTANT]
> **Template discipline.** Create mode documents MUST use `templates/MODEL.md`. Ad hoc formats are a protocol violation. Apply mode companion documents also use the template; integrated annotations follow the target document's format.

### Step 6: CONNECT (State Transition Verification Mapping)

Link the formal model to the verification pipeline:

- **Generate Transition Assertions**: Map the model's state-space transitions and algebraic properties to executable assertions or mock transition traces.
- **Link to TDD Suite**: Feed these trace assertions into the project's verification test suite, ensuring the implementation's state machine is verified deterministically.
- Update the sketch with modeling findings.
- Cross-reference related models in `docs/models/`.
- Cross-reference related specifications in `docs/specs/` to verify that the model's state space conforms to the specification constraints.
- If the model reveals design flaws, structural complecting (spatial issues), or temporal volatility conflicts, flag them explicitly.

---

## State Transitions

```
IDENTIFY ──→ SELECT     (domain understood, characteristics identified)
         └─→ ABORT      (domain not suitable for formal modeling)

SELECT ──→ CONSTRUCT    (formalism chosen, human approved)
       └─→ IDENTIFY     (wrong scope — need to reframe)

CONSTRUCT ──→ VALIDATE  (model built)
          └─→ SELECT    (formalism doesn't fit — need different tool)

VALIDATE ──→ RECORD     (model passes validation)
         └─→ CONSTRUCT  (validation failures require model revision)

RECORD ──→ CONNECT      (artifact committed)

CONNECT ──→ DONE        (context linked, implications noted)
```

---

## MANDATORY HALT Points

You MUST stop and await human input at:

1. **After SELECT:** Formalism choice must be approved before construction
2. **After VALIDATE (if failures):** Human decides whether to revise or accept partial model
3. **Before RECORD (Apply mode):** Human chooses companion document vs. integrated annotations

---

## Model Storage

```
docs/
└── models/
    └── <domain-name>.md    # formal model artifact
```

Model filenames should be descriptive of the domain being modeled, not the formalism used. Example: `docs/models/payment-protocol.md`, not `docs/models/session-type-1.md`.

---

## Integration with Sketch Lifecycle

If a sketch exists for the current workstream:

- IDENTIFY findings are written to the sketch
- SELECT rationale is written to the sketch
- VALIDATE results are written to the sketch
- Each sketch update is committed immediately

The sketch captures the _modeling journey_; the model document captures the _outcome_.

---

## Position in the Workflow Chain

FORM is a domain-specific structural-analysis tool, not a pipeline stage:

```
explore (ambient Sketch Principle)  →  understand the problem space
                                        ↓
/form    →  formalize domain understanding (can be invoked from any phase)
         ↓
/spec    →  declare normative constraints over the model (→ what MUST hold)
         ↓
/core    →  regulate state (guided by model, constrained by spec)
```

FORM can be invoked standalone or from within any other workflow. A model produced while exploring informs the strategy that follows; a model produced during `/core` validates implementation decisions. The formal model is a structural analysis tool available at any point. Strategy itself is governed by the ambient [Planning Invariants](../../ambient.md#planning-invariants), not a discrete planning workflow.
