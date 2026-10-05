---
name: core
description: |
  SOP for the micro-execution C.O.R.E. phase.
  Trigger when:
  - Implementing plan steps, managing code changes at commit boundaries, and verifying incremental progress.
  - Navigating states: Absorb, Clarify, Plan, Execute.
  - Prompt contains: /core, core workflow, absorb, clarify, execution invariants, commit boundary, verify assertion.
---
 
# C.O.R.E. Protocol: Micro-Execution under the Verification Dual

**Context → Obstacles → Resolution → Execution**
 
This workflow defines the C.O.R.E. micro-execution phase. It guides a localized plan segment through a series of discrete state transitions (Context, Obstacles, Resolution, Execution), closing each step against the [Verification Dual](../../rules.md) before committing: every step carries a deterministic evaluator (the symbolic path — test, compiler, linter) that must reach $\Delta E = 0$, and each commit boundary meets the [Commit Gate](../../rules.md) (§3). C.O.R.E. is the task-scale instance of the Dual's symbolic path: drive a candidate edit to its evaluator's fixed point, then authorize the change through the ledger gate.
 
---
 
## Scope
 
> [!IMPORTANT]
> C.O.R.E. maps a localized plan segment (typically 2-3 commit boundaries) and manages the execution trajectory. It is execution, not strategy: high-level planning and the exploration of design alternatives are standing dispositions — the [Planning Invariants](../../ambient.md#planning-invariants) and the [Sketch Principle](../../ambient.md#the-sketch-principle) — not steps inside this workflow. If the sequence begins exploring design alternatives or modifying the architecture, it has exited C.O.R.E. space; the walk must immediately halt.
 
## Grammar
 
```yaml
# 1. TRAJECTORY METADATA
STATUS: [ABSORB | CLARIFY | PLAN | EXECUTE]
CONTROL_MODE: [MANUAL | AUTOMATIC] # MANUAL: halt at boundaries; AUTOMATIC: autocommit and continue if tests pass.
 
# 2. CONTEXT (The Initial Boundary Condition)
CTX:
  GOAL: "User's objective (quoted verbatim)"
  CONSTRAINTS:
    - "Boundary condition 1"
  FILES:
    - path/to/target/file
 
# 3. OBSTACLES (Divergence Vectors)
# Populated in CLARIFY status; forces sequence freeze
OBSTACLES:
  - "Uncertainty / contradiction 1"
 
# 4. TRAJECTORY PLAN (Discrete TDD Optimization Steps)
# Populated in PLAN/EXECUTE status
PLAN:
  RATIONALE: "Mathematical / control rationale for this trajectory"
  STEPS:
    - ID: 1
      INVARIANT: "Test assertion or property contract (TDD constraint)"
      TEST_TARGET: "tests/test_file.py::test_name"
      IMPL_TARGET: "src/file.py::function_name"
      IMPL_DELTA: "Implementation edit to satisfy the invariant"
      VALIDATOR: "pytest tests/test_file.py"
      COMMIT: true # Marks a commit boundary
```
 
---
 
## Trajectory Verification & Commit Gates
 
### 1. Closed-Loop Verification Loop (TDD-First)
For each step in the plan, execute a local optimization loop:
- **TDD Formulation**: Formulate and write the test assertion mapping to `INVARIANT` in `TEST_TARGET` conforming to [robust-testing](../robust-testing/SKILL.md) instructions:
   - **Specification Mapping:** If a specification or model exists, the tests MUST directly verify its constraints and state transitions to ensure meaningful surface coverage.
   - **Verification Method Selection:** Select the verification method based on domain complexity:
     - Use **Property-Based Testing (PBT)** if the domain has non-trivial algebraic properties (e.g., round-trip, commutativity, idempotency) and target language support is mature.
     - Use **Fuzz Testing** to validate security and serialization boundaries for untrusted inputs.
     - Use **Metamorphic Testing** if the expected output is complex/expensive to calculate or lacks a simple oracle.
     - Use **Integration/E2E Testing** for multi-module boundaries, asserting global liveness/safety while isolating external APIs via deterministic mocks.
- **Baseline Check**: Run `VALIDATOR` to obtain the baseline error differential $\Delta E_0$. The baseline check MUST verify test failure ($\Delta E_0 \neq 0$) to confirm the test is non-trivial and does not pass on empty/unimplemented code.
- **Generation**: Implement code edits at `IMPL_TARGET` to satisfy `IMPL_DELTA`.
- **Deterministic Evaluation**: Execute `VALIDATOR`.
   - If tests/compilation pass ($V(\mathbf{S}_k) = 0$), proceed to the Refinement Check.
   - If tests/compilation fail ($V(\mathbf{S}_k) \neq 0$), apply a corrective edit $\Delta \mathbf{S}_{k+1}$ designed to minimize the error feedback vector $\Delta E_k$. Repeat up to a cap of 3-5 iterations. If no convergence occurs, transition to `CLARIFY` and halt.
 
### 2. Iterative Refinement Loop
Before concluding work at any commit boundary, contract the diff toward its fixed point. This is one loop — a contraction mapping that re-enters itself until it stops moving, not a second machine bolted onto the verification loop above. Each pass is an application of the refinement operator $R$; the loop halts at the fixed point $R(\mathbf{S}^*) = \mathbf{S}^*$ — the pass that finds nothing left to correct. (The full Banach contraction model is the reference content of [refine](../refine/SKILL.md); `/core` runs the same loop at task scale.)

Each pass:
- Audit the generated diff against code simplicity (Hickey complecting check), volatility alignment (Lowy temporal check), test completeness, and style guidelines.
- **One-Shot Skeptical Audit**: If a plan step converges in exactly 1 iteration (`LOOPS: 1`), you must perform an explicit adversarial audit of the diff. Validate that the baseline failure check was genuine, analyze whether any hidden assumptions were left unverified, and run spatial/temporal checks to ensure no structural complexity was introduced. Document this audit in the `REVIEW` block under `SKEPTICAL_AUDIT`.
- **Deterministic grounding (no additive drift).** A correction enters this loop only when it is grounded — it maps to a reproducible evaluator failure (linter, compiler, failed assertion) or a localized, in-scope specification contract, verified by actually running the tool. Subjective or stylistic critiques do not spawn corrections; they would only accrete complexity the loop is meant to shed. Self-correction is additively biased, so each pass must also *prune* — fold, merge, or delete anything a prior pass added that no longer serves the goal. This bound is what makes the loop a contraction ($q < 1$) rather than a divergent accumulation; it is the [Cutting Imperative](../../rules.md) applied to the diff.
- Update the active sketch (rubric and evaluators, constraint ledger, unknowns ledger, and standards checklists) in the `.ledger/log/[topic].md` flight recorder to track compliance states in real-time, per [the Sketch Principle](../../ambient.md#the-sketch-principle). Log any dynamic shifts or refinements to the rubric goals for human reporting.
- If the quality score is less than 1.0 or any standard/constraint is violated, formulate a corrective refactor, apply it, re-run verification, and **re-enter this loop**. The boundary is reached only when a pass produces no grounded correction.
 
### 3. Commit Gates
At each commit boundary (or phase completion):
- **Commit Gate Invariant:** Every commit passes the [Commit Gate](../../rules.md) (§3) — the conventional message validates mechanically (`commit-hygiene`) and the [ledger gate](../../ledger/gate/README.md) (`ledger/gate/ledger-validate.sh`) authorizes the change — before executing any commit in any repository.
- If `CONTROL_MODE: AUTOMATIC` (and credentials/command permissions are active):
  1. Record the updated active sketch (rubric, constraints, unknowns, standards, commit ID) in `.ledger/log/[topic].md`, and commit it within the `.ledger/` sub-repository.
  2. Output the `REVIEW` block, `JUSTIFICATION` block, and conventional commit message.
  3. Execute `git add [modified files]` and `git commit -m "[message]"` directly.
  4. Automatically proceed to the remaining PLAN steps without halting.
- If `CONTROL_MODE: MANUAL` (or not specified):
  1. Output in this order, then **HALT**:
     - REVIEW block (structured output of self-review findings: SCORE, ITERATIONS, and FINDINGS per the REVIEW Block Format)
     - Sketch update instructions (re-stating the active sketch updates, compiling any rubric adjustments or goal additions)
     - JUSTIFICATION block
     - Conventional commit message conforming to [commit-hygiene](../commit-hygiene/SKILL.md)
     - REMAINING STEPS
  2. **Wait for human confirmation** before proceeding.
 
### 4. REVIEW Block Format
The `REVIEW` block must be output as a structured YAML block containing:
```yaml
REVIEW:
  SCORE: 1.0                              # Qualitative self-audit score [0.0 - 1.0]
  ITERATIONS:
    - STEP_ID: 1                          # Links to the trajectory plan step ID
      BASELINE_FAIL: "Verified diagnostic baseline error / test fail output"
      LOOPS: 3                            # Exact number of verification loops executed (1-5)
      CORRECTIONS:
        - LOOP: 1
          ERROR: "Error output details"
          CORRECTION: "Applied changes to fix"
      VERIFICATION: "Pass evidence / test execution summary"
      SKEPTICAL_AUDIT: "Adversarial audit detail (Mandatory if LOOPS: 1)"
  FINDINGS:
    - ID: F1
      SEVERITY: [LOW | MEDIUM | HIGH | CRITICAL]
      ACTION: "Simplicity / volatility alignment correction applied"
      DETAIL: "Trace audit context"
```

---
 
## Prime Directives
 
1. **STATE_OVER_SCRIPT:** Define the desired state declaratively in the plan grammar. The PLAN must specify atomic TDD steps and verification constraints.
2. **AMBIGUITY_GATE:** If context is missing, conflicting, or weak, token generation for implementation is forbidden ([Halt over assumption](../../rules.md)). Transition to CLARIFY, populate OBSTACLES, and halt until they are resolved.
3. **VERIFICATION_FIRST:** Every PLAN step requires a testable assertion closed by its evaluator (the Verification Dual's symbolic path). A task is incomplete without verification.
4. **TOKEN_MINIMALISM:** Eradicate conversational filler. Output only the plan grammar during planning.
5. **HANDSHAKE_PROTOCOL:** Transition to EXECUTE is forbidden without explicit human approval (unless continuing on a fully automated `CONTROL_MODE: AUTOMATIC` run).
6. **PREDICATE_AWARENESS:** Maintain conformance with active workspace skills.
7. **SCHEMA_RIGIDITY:** Permitted fields in the plan grammar are strictly constrained to: STATUS, CONTROL_MODE, CTX, OBSTACLES, PLAN.
8. **DEBT_TRANSPARENCY:** Suboptimal compromises must be documented in `JUSTIFICATION.DEBT` and recorded in the plan's `## Technical Debt` section.
9. **DEVIATION_RECORDING:** Deviations from the plan must be recorded in the plan's `## Deviation Log` section at commit boundaries.
 
### Protocol Violations (FORBIDDEN)
 
| Violation | Why It's Wrong |
| :--- | :--- |
| Adding fields not listed in SCHEMA_RIGIDITY | Violates grammar constraints. |
| Skipping commit message | Breaks repository history standards. |
| Executing `git commit` without authorization | User commits manually unless `CONTROL_MODE: AUTOMATIC` is active and authorized. |
| Proceeding past commit boundary without human confirmation | Each boundary is a halt gate (unless `CONTROL_MODE: AUTOMATIC`). |
| Continuing after verification failure | Must run the Closed-Loop Verification Loop to fix, or halt if it fails to converge. |
| Proceeding past COMMIT without updating sketch | Destroys decision logs. |
| Implementing code changes without writing the test invariant first | Violates TDD constraints. |
 
---
 
## State Transitions & Definitions
 
```
ABSORB ──→ CLARIFY (if OBSTACLES exist)
       └─→ PLAN    (if no OBSTACLES remain)
 
CLARIFY ──→ PLAN   (once OBSTACLES resolved)
 
PLAN ──→ EXECUTE  (on "APPROVED")
     └─→ CLARIFY  (if new ambiguity discovered)
 
EXECUTE ──→ CLARIFY (if verification fails to converge)
         └─→ ABORT   (if target state space is unreachable)
```
 
**ABSORB:** Ingest input, map target attractor basin. Before leaving this state, run the [DISCOVERY](../../ledger/contracts/discovery.ncl) sub-procedure ([architecture §DISCOVERY](../../docs/predicate-architecture.md#discovery--the-keystone-sub-procedure)) and deposit its footprint into the active `.ledger/log/[topic].md` flight recorder. Scale by stakes: a trivial, localized, reversible edit need not run all five steps; a non-trivial task always does.
 
**CLARIFY:** Halt generation; emit obstacles to resolve uncertainty.
 
**PLAN:** Construct the discrete state trajectory mapping transitions to TDD targets and invariants.
 
**EXECUTE:** Formulate test invariants, check baseline, run candidate code generation, run verification, minimize the error differential, and apply commit gates.
 
**ABORT:** Halt and exit the trajectory walk when the target state space is proven unreachable.
 
---
 
## Lexicon Translation Matrix

> See the canonical Invariant Translation Mapping in [rules.md](../../rules.md) §1 for the full mapping between psychological heuristics and control-theoretic operations.