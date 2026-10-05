---
name: refine
description: |
  SOP for the automated refinement loop (/refine) workflow.
  Trigger when:
  - Exhaustively auditing and optimizing pre-existing codebase artifacts.
  - Applying iterative contraction mapping to reduce code entropy.
  - Prompt contains: /refine, refinement loop, contraction mapping, fixed-point sweep.
---

# REFINE Protocol v1.0: Contraction Mapping & Fixed-Point Convergence

**Absorb → Audit → Iterate → Sweep → Report**

This workflow defines the `/refine` execution loop. The objective is to guide sequence token generation through a series of discrete state transitions (Absorb, Audit, Iterate, Sweep, Report) to systematically reduce the entropy of pre-existing artifacts. The process is modeled as an iterative contraction mapping that halts only when a stable fixed point is verified.

---

## Philosophy & Mathematical Model

Refining an existing artifact is modeled as finding the unique fixed point $\mathbf{S}^*$ of a state-space contraction mapping. Let $\mathcal{X}$ be the space of artifact configurations, and let $d: \mathcal{X} \times \mathcal{X} \rightarrow \mathbb{R}_{\ge 0}$ be a metric proportional to the residual entropy and count of latent/active flaws. The refinement operator $R: \mathcal{X} \rightarrow \mathcal{X}$ is a contraction if:

$$d(R(\mathbf{A}), R(\mathbf{B})) \le q \cdot d(\mathbf{A}, \mathbf{B})$$

for all $\mathbf{A}, \mathbf{B} \in \mathcal{X}$ and some contraction factor $0 \le q < 1$. By the Banach Fixed-Point Theorem, repeated application of $R$ converges to the unique fixed point:

$$\mathbf{S}^* = \lim_{k \rightarrow \infty} R^k(\mathbf{S}_0)$$

### CyberCorrect & Computable Loop Dynamics
To evaluate convergence in real-time, the error metric $e_k$ is computed using a **computable proxy metric** $d_p(\mathbf{S}_k)$, defined as the count of unresolved (`PENDING` or `IN_PROGRESS`) items in `REF_LEDGER`. The convergence rate is defined as:

$$\rho_k = \frac{d_p(\mathbf{S}_k)}{d_p(\mathbf{S}_{k-1})}$$

For a true contraction, $\rho_k \le q < 1$. If $d_p(\mathbf{S}_k) \to 0$, the system is Cauchy-convergent. In practical autoregressive generations:
1. **Unstable Oscillations (Limit Cycles):** If $\rho_k \ge 1$ (active only when $d_p(\mathbf{S}_{k-1}) > 0$ and $d_p(\mathbf{S}_k) > 0$) or if codebase states exhibit exact tracked workspace file hash equality with any prior loop state ($\mathbf{S}_k = \mathbf{S}_j$ for $0 \le j < k$ stored in `TRACKED_WORKSPACE_HASHES`), the loop has entered an unstable cycle. The system must adapt search parameters (lower generation temperature, inject explicit negative examples, or alter subagent critique rubrics) or execute the rollback protocol to break the attractor basin.
2. **Diminishing Returns & Stochastic Cascades:** Self-correction exhibits sublinear convergence, where functional errors are corrected early, but sequential, identical sweeps on unchanged code accumulate stochastic LLM noise (false positive critiques). To prevent these cascades, sweep angles must execute in parallel, and any new subagent finding on unchanged code must be ignored unless backed by a deterministic test or static linter failure.

### Prefix-Induced Attractor Basin Bias
Autoregressive Large Language Models do not generate tokens in a vacuum; they traverse a sequence probability landscape where each token step is conditioned on the historical prefix $\mathbf{S}_t$. When the same agent that modified the code also reviews it, the prefix $\mathbf{S}_t$ contains the refiner's internal steps, design rationale, and implicit assumptions. This warps the landscape to construct a deep **attractor basin** around the refiner's localized choices, mathematically biasing the walk to reinforce its own decisions.

To break this self-congratulatory lock-in and achieve a non-delusional fixed point $\mathbf{S}^*$, validation must execute under **Multi-Boundary Subagent Sweeps (MBSS)**. We project the artifact's state space onto orthogonal axes of critique using independent subagents primed with distinct Initial Boundary Conditions (IBCs) that are completely blind to the refiner's internal trajectory history and to each other's active rubrics or findings, preventing any collusive context leakage.

### The Refine/Review Dialectic: Constructive Tension
Refinement is not a process of compliance-driven submission; it is a collaborative, asynchronous synthesis between two expert viewpoints with a single shared goal: **offering a genuinely compelling improvement to the codebase that is worth maintaining.**

This process rests on a dialectical balance between the refiner (worker) and the reviewers (maintainers) who operate using opposite methods but a unified purpose:
1. **Instructing Agents as World-Class Experts:** Neither the refiner nor the maintainer reviewers are limited in capability. They are world-class experts who have absolute confidence in their respective domains, but possess the humility to concede and adapt when a superior design, cleaner implementation, or stronger evidence-backed argument is offered. They are the best at what they do and act with confidence and mutual respect.
2. **Defending Choices vs. Resubmitting Bias (The Worker's Stand):** Maintainers, by their nature, conduct myopic reviews constrained to their specific rubrics (e.g., modular coupling, allocation count, naming conventions). The refiner, holding the macro context, may see a cohesive piece of the puzzle that the subagents and reviewers missed. In such moments, the refiner must **take a stand** and defend its design choices. It must resist submissive over-engineering or compliant "fixes" that compromise the overall goal. However, just as crucially, the worker **cannot resubmit its own bias** back into the equation after that bias has been deferred or challenged. It must remain objective and humble.
3. **Meticulous Note-Keeping for Self-Preservation:** To keep the higher-level goal on track in long sessions and ensure the worker itself cannot forget what has occurred during refinement, the worker is coached and structurally required to take **meticulous progress notes** in the active sketch file. The sketch is the refiner's memory; it guards against context loss, prevents prefix-induced self-bias from creeping back into justifications, and documents why specific design choices were defended.
4. **Humility to Leverage Reviewer Experience:** The maintainers have deep experience and know their codebase's motivation better than anyone. They do not accept lazy hacks or "BS" code. They want help solving problems, and their experience is invaluable to raising code and documentation to the repository's highest standards. The refiner must recognize when maintainer feedback is a genuine avenue for improvement and concede when a better path is offered.
5. **API Stability and Project Objectives:** High-level project objectives and API stability override individual nits. Once API stability is reached, compromises must be made to preserve the public API surface. Prioritizing API stability before a release/milestone is reached is premature and counterproductive; design soundness takes precedence early on.

### The Accuracy-Correction Paradox (SCoRe Trajectory Guardrails)
To prevent the system from degrading correct artifacts or entering overcorrection loops, we enforce strict **Deterministic Grounding**:
- **Verifier Grounding:** Any critique, issue, or ledger item generated by a subagent MUST be rejected unless it can be mapped directly to a deterministic evaluator failure (such as a linter warning, a failed test execution, a syntax error, or a documented spec violation). Reject any subagent finding that does not include a stdout/stderr trace or specific file/line location. Purely subjective or stylistic criticisms are banned from the ledger (see Prime Directive 4).
- **Socratic Verification Gate:** Socratic checks (e.g., assessing code elegance) may guide human-in-the-loop iterations but cannot spawn ledger entries unless they are converted into concrete, reproducible test assertions or compiler checks.
- **Sieving & Cutting Pruning Invariant:** Counter the additive bias of self-correction loops. The agent MUST actively evaluate and prune superfluous structures, redundant variables, comments, or dependencies introduced in follow-up iterations that no longer serve the target goal (see Section 3 for procedural details).
- **Regression Invariance:** Every iteration step must verify that previous working test suites continue to pass. If a change breaks a regression test, the edit is immediately discarded, the state rolled back, and the correction re-attempted.
- **Git History Invariance:** The use of history-altering git commands is strictly prohibited. All history must remain linear and immutable (see Prime Directive 9).
- **Core Premise Verification (The "Turd-Polishing" Guardrail):** Before optimizing or polishing any target artifact, the agent must challenge the underlying design. If a core premise is found to be flawed, the agent MUST log the premise failure in the sketch and transition to `HALT` (see Section 3 for procedural details).

### Loop Bounds and Exit Metrics
To ensure sequence generations converge to $\mathbf{S}^*$ rather than terminating in local sub-optimal minima, the workflow enforces three control-theoretic bounds that scale dynamically based on the complexity of the task (assessed during `ABSORB`):

1. **Minimum Execution Loops ($N_{min}$):** The loop MUST execute at least $N_{min}$ iterations, even if no issues are initially visible.
   *Convergence Shortcut:* If the initial audit finds $d_p(\mathbf{S}_0) = 0$ and the first parallel sweep phase yields zero findings, the artifact is declared converged, and the system bypasses $N_{min}$ to transition directly to `REPORT`.
   > [!IMPORTANT]
   > The Convergence Shortcut still requires executing the full `SWEEP` phase. The refiner MUST spawn the independent subagents to verify there are zero findings. Transitioning directly to `REPORT` from `AUDIT` without running the sweep is a protocol violation.
2. **Consecutive Clean Sweeps ($M_{sweep}$):** Once the active refinement ledger is empty, the agent must perform $M_{sweep}$ consecutive adversarial sweeps.
3. **Divergence Boundary ($K_{max}$):** To prevent infinite limit cycles or chaotic oscillations, we define a loop limit $K_{max}$.

The exact parameter bounds are initialized in the `ABSORB` phase based on task complexity (see Section 1). Only when $M_{sweep}$ consecutive sweeps find zero new issues on the final, static codebase state can the system declare convergence ($R(\mathbf{S}^*) = \mathbf{S}^*$) and proceed to the `REPORT` phase. Transitioning to `REPORT` directly from `ITERATE` or `AUDIT` is strictly prohibited. Any code modification resets `CONSECUTIVE_CLEAN_SWEEPS` to `0`, requiring a full reset of the sweep phase.

---

## Scope

> [!IMPORTANT]
> `/refine` is for **optimizing and polishing pre-existing artifacts**. It is NOT for implementing new features (that's `/core`) nor for drafting high-level architecture; that strategic work is governed by the [Planning Invariants](../../ambient.md#planning-invariants), not this loop. If the sequence begins adding new functional scopes or diverging from the initial target artifact, the walk must halt and return control to the human.

---

## Grammar

```yaml
# 1. METADATA
TOPIC: "topic-slug"            # Topic slug for the refinement session
STATUS: [ABSORB | CLARIFY | AUDIT | ITERATE | SWEEP | REVIEW | REPORT | HALT]

# 2. CONTEXT
CTX:
  TARGET_ARTIFACTS:
    - "path/to/target/file"
  TEST_FILES:
    - "path/to/test/file"
  SPECIFICATION_FILES:
    - "path/to/specification/file"
  ARCHITECTURAL_DOCS:
    - "path/to/architectural/doc"   # Mapped architectural docs (README, ADR, etc.)
  GOAL: "Verbatim objective statement"
  MODE: [INTERACTIVE | AUTONOMOUS]  # Interactive requires human gates; Autonomous runs under /goal
  PREMISE_BYPASS: [TRUE | FALSE]     # If TRUE, bypass premise verification halts (defaults to FALSE)
  WORKTREE_PATH: "path/to/worktree"  # Path to the isolated git worktree
  AGENT_BRANCH: "branch_name"        # Current active agent branch attempt (e.g., agent/refine-<topic>-attempt-1)
  ASSUMPTIONS: []            # Hypotheses logged during autonomous CLARIFY resolution
  CONSTRAINTS:
    N_MIN: 4                 # Adaptive loop limit scaled to task complexity
    M_SWEEP: 4               # Adaptive sweep limit scaled to task complexity
    K_MAX: 12                # Adaptive divergence boundary
    REVIEW_BUDGET: 3         # Max maintainer review cycles before halting
    SIBLING_SKILLS:          # Sibling skills loaded and consulted during audit
      - robust-testing
      - engineering
      - prior-art

# 3. DYNAMIC REFINEMENT LEDGER
# Track all optimization targets identified during AUDIT or SWEEP phases.
# All items must be RESOLVED before entering the final SWEEP validation gates.
REF_LEDGER:
  - ID: R1
    AXIS: [CORRECTNESS | API_SUFFICIENCY | COMPLIANCE | EDGE_CASES]
    TARGET: "symbol_or_line_or_file"
    STATEMENT: "Description of the target improvement"
    STATUS: [PENDING | IN_PROGRESS | RESOLVED]
    EVIDENCE: "Verification results / test run outputs"

# 4. DYNAMIC REVIEW LEDGER (PR REVIEW)
# Track all nitpicks and design critique targets identified during the REVIEW phase.
# All items must be RESOLVED before human sign-off and merge.
REVIEW_LEDGER:
  - ID: N1
    AXIS: [CORRECTNESS | API_SUFFICIENCY | COMPLIANCE | EDGE_CASES]
    MAINTAINER: [maintainer-architecture | maintainer-complexity | maintainer-documentation]
    TARGET: "symbol_or_line_or_file"
    STATEMENT: "Nitpick/critique details"
    STATUS: [PENDING | RESOLVED]
    RESOLUTION: "commit_hash or text justification"
    RE_REVIEW_STATUS: [REJECTED | APPROVED]

# 5. ADVERSARIAL SWEEP SYSTEM (MBSS)
# Track the dynamically identified adversarial review angles and subagent sessions.
MBSS_PLAN:
  META_AUDITOR_STATUS: [PENDING | APPROVED | BYPASSED_AUTONOMOUS]  # Bypassed in autonomous mode if programmed criteria met
  ANGLES:
    - ID: A1
      NAME: "e.g., security-sandbox"
      RUBRIC: "Search for specific resource leak or sandbox escape"
      SUBAGENT_ID: "conv-uuid"
      STATUS: PENDING          # [PENDING | PASS | FAIL]

# 6. ITERATIVE TRACE
# Live execution metrics updated at each loop boundary
TRACE:
  CURRENT_LOOP: 0              # Current iteration index (k)
  INITIAL_STATE_COMMIT: "sha256_hash"  # The commit hash of S0 before any modifications
  CONSECUTIVE_CLEAN_SWEEPS: 0  # Number of consecutive clean sweeps completed
  REVIEW_CYCLE_COUNT: 0        # Current maintainer review cycle index
  ROLLBACK_RETRY_COUNT: 0      # Consecutive rollbacks at current state (resets on progress, capped at 3)
  TOTAL_ROLLBACK_COUNT: 0      # Cumulative rollbacks executed during the entire run
  LAST_RESTORED_LOOP: 0        # Loop index j of the last restored state (defaults to 0)
  JUST_RESTORED: null          # Optional: transient loop index j just restored from (defaults to null)
  FILTERED_CRITIQUES:          # Track critiques discarded by verifier/spec triage filters
    - SUBAGENT_ID: "conv-uuid"
      CRITIQUE: "Subjective styling suggestion"
      REASON: [REJECTED_SUBJECTIVE | REJECTED_OUT_OF_SCOPE | REJECTED_FAKE_FAILURE | REJECTED_CASCADE_GUARD]
  LOOPS:
    - LOOP: 1
      RESTORED_FROM_LOOP: null # Optional: loop index j restored from on rollback (defaults to null)
      TARGETS_ADDRESSED:
        - R1
      ERROR_METRIC: 0          # Proxy error count d_p(S_k)
      CONVERGENCE_RATE: 0.0    # Computed convergence rate rho_k
      TRACKED_WORKSPACE_HASHES: # Content hashes of target, test, and modified files only
        "path/to/file": "sha256_hash"
      VERIFICATION: "Compiler/linter/test outputs"
      COMMITS:
```

## State Transitions & Definitions

```
ABSORB ──→ CLARIFY   (if goal/scope ambiguity exists)
       └─→ AUDIT     (if no ambiguity remains)

CLARIFY ─→ AUDIT     (once ambiguity resolved)
        └─→ HALT     (if ambiguity cannot be resolved in autonomous mode)
 
AUDIT  ──→ ITERATE   (if ledger has PENDING items)
       ├──→ CLARIFY   (if unexpected environment/dependency ambiguities occur mid-run)
       ├──→ HALT      (if core premise verification fails in any mode, or loop budget/oscillation is detected in interactive mode)
       ├──→ AUDIT      (if loop budget/oscillation is detected and autonomous rollback succeeds)
       └─→ SWEEP     (if ledger is empty)
 
ITERATE ─→ AUDIT     (once all ledger items are RESOLVED and (CURRENT_LOOP - LAST_RESTORED_LOOP <= K_MAX or CONSECUTIVE_CLEAN_SWEEPS > 0))
        ├──→ CLARIFY   (if unexpected environment/dependency ambiguities occur mid-run)
        └─→ HALT     (if CURRENT_LOOP - LAST_RESTORED_LOOP > K_MAX and CONSECUTIVE_CLEAN_SWEEPS == 0, loop oscillation is detected, or rollback fails)
 
SWEEP  ──→ AUDIT     (if a sweep discovers new issues, or if sweeps pass but limits not met)
       └─→ REVIEW    (once CONSECUTIVE_CLEAN_SWEEPS = M_SWEEP and CURRENT_LOOP >= N_MIN, or via Convergence Shortcut)

REVIEW ──→ ITERATE   (if review findings require code/doc modifications; resets sweep counters)
       ├──→ HALT     (if review budget is exceeded or oscillation detected)
       └─→ REPORT    (once all maintainers approve, leading to human final merge decision)
```

### 1. ABSORB
Ingest the target artifact, the optimization goals, and any relevant specs or test suites. Setup the tracking ledger in the active sketch file.
- **Mode Selection:** Set `CTX.MODE` to `AUTONOMOUS` if executing under a long-running background worker (e.g. `/goal`), otherwise default to `INTERACTIVE`.
- **Ambiguity Gate:** If there is ambiguity in the goal or scope, transition to `CLARIFY` and do not proceed to `AUDIT` until it is resolved ([Halt over assumption](../../rules.md)).
- **Architectural Documentation Mapping:** Locate and map all relevant design/architectural documents (e.g., `README.md`, ADRs, docs in `docs/`) and log their relative paths in `CTX.ARCHITECTURAL_DOCS`.
- **Worktree Setup:** 
  Initialize a dedicated git worktree at `.worktrees/refine-<topic>` based on the active HEAD and create a private branch attempt:
  ```bash
  git worktree add -b agent/refine-<topic>-attempt-1 .worktrees/refine-<topic> HEAD
  ```
  Ensure `.worktrees/` is added to the main `.gitignore` file to prevent untracked file pollution in the user's view. Set `CTX.WORKTREE_PATH` to `.worktrees/refine-<topic>` and `CTX.AGENT_BRANCH` to `agent/refine-<topic>-attempt-1`.
  *Note:* All subsequent code modification, linter checking, and test runs MUST execute inside the worktree directory, leaving the user's active working directory completely isolated and undisturbed.

**Adaptive Parameter Bounds Initialization:**
Evaluate the complexity of the target artifact and goal. Scale the limits dynamically:
- *Simple (local edits, docs):* Set $N_{min}=3$, $M_{sweep}=3$, $K_{max}=8$, $REVIEW\_BUDGET=2$.
- *Medium (single-module refactors, test suite updates):* Set $N_{min}=4$, $M_{sweep}=3$, $K_{max}=10$, $REVIEW\_BUDGET=3$.
- *Complex (core logic changes, protocol designs, multi-file refinements):* Set $N_{min} \ge 4$, $M_{sweep} \ge 4$, $K_{max} \ge 12$, $REVIEW\_BUDGET \ge 3$.

Log these parameters and their complexity rationale in the sketch.

### 2. CLARIFY
Halt sequence generation. Surface obstacles or questions regarding the target artifacts or goals.
- **Interactive Mode:** Wait for human validation before resolving the ambiguity and transitioning to `AUDIT`.
- **Autonomous Mode:** Formulate a conservative, logical hypothesis/assumption that maximizes system safety and preserves existing behavior. Record this hypothesis under an `ASSUMPTIONS` section in the sketchpad and proceed with execution. Only trigger a hard `HALT` if the ambiguity prevents compilation, linting, or test execution (e.g., a missing library or fatal syntax error).

### 3. AUDIT
Exhaustively analyze the artifact across four dimensions to identify how to achieve its **minimal representation** (optimal articulation of the problem space without superfluous complexity). 
At the start of the audit phase:
1. Increment `CURRENT_LOOP` by 1 (representing a new loop cycle $k$) at the start of every audit phase (except when returning from `CLARIFY` within the same loop).
2. Run audit tools and populate `REF_LEDGER` with all discovered targets.
3. **Architectural Documentation Audit:** Audit the codebase modifications against the mapped `CTX.ARCHITECTURAL_DOCS`. If code changes introduce architectural drift (e.g., public API modifications, new module coupling, changed invariants), the refiner MUST log documentation tasks (e.g. `R_DOC_1`) in the `REF_LEDGER` to update the documents during `ITERATE`.
4. Update the `TRACE.LOOPS` list in the active sketch file. If `TRACE.JUST_RESTORED` is not null, set `RESTORED_FROM_LOOP` of the current loop entry to `TRACE.JUST_RESTORED` and then reset `TRACE.JUST_RESTORED` to `null` in the active sketchpad. To ensure mathematical correctness and avoid blind convergence calculations, metrics MUST be calculated and recorded at the END of the AUDIT phase (after all findings are populated in the ledger, but before transitioning to ITERATE or commencing edits):
   - **ERROR_METRIC ($d_p$):** Record the proxy error metric $d_p(\mathbf{S}_k)$ defined as the count of unresolved (`PENDING` or `IN_PROGRESS`) items in `REF_LEDGER`.
   - **CONVERGENCE_RATE ($\rho_k$):** Calculate and record the convergence rate $\rho_k = \frac{d_p(\mathbf{S}_k)}{d_p(\mathbf{S}_{k-1})}$. If $k = 1$, $d_p(\mathbf{S}_{k-1})$ refers to the initial state error $d_p(\mathbf{S}_0)$. If $k = 1$ or if $d_p(\mathbf{S}_{k-1}) = 0$, set $\rho_k = 0.0$ if $d_p(\mathbf{S}_k) = 0$, and $\rho_k = \infty$ (or `N/A`) if $d_p(\mathbf{S}_k) > 0$.
   - **ROLLBACK_RETRY_COUNT Reset:** If $d_p(\mathbf{S}_k)$ < $d_p(\mathbf{S}_{k-1})$ and `TRACE.LOOPS[CURRENT_LOOP].RESTORED_FROM_LOOP` is null, progress has been made; reset `ROLLBACK_RETRY_COUNT` to 0.
   - **TRACKED_WORKSPACE_HASHES:** Compute and record the SHA-256 hashes of target files (`CTX.TARGET_ARTIFACTS`), test files (`CTX.TEST_FILES`), and any files modified in the current branch attempt (resolved using `git diff --name-only TRACE.INITIAL_STATE_COMMIT HEAD`). If a file exists on the filesystem, record its SHA-256 hash. If a file has been deleted in the working tree, record its hash as the sentinel value `"ABSENT"`.
   - **CORE_PREMISE_VERIFICATION:** Challenge the underlying design before continuing. If a design choice is determined to be fundamentally flawed ("stupid"), log the premise failure in the sketch, and immediately transition to `HALT` (in both interactive and autonomous modes) to prevent turf-polishing via automated assumptions.

**Sibling Skills Consultation:**
You are required to actively consult the workspace's sibling skills to think more broadly:
- Mapped tests MUST be checked against the guidelines in [robust-testing](../robust-testing/SKILL.md).
- Code safety and type boundaries MUST conform to the procedural directives in [engineering](../engineering/SKILL.md).
- Architectural designs and abstractions MUST be compared against patterns in [prior-art](../prior-art/SKILL.md) to ground decisions in proven implementations.
- API surface designs must be evaluated against complection and decoupling rules in [api-audit](../api-audit/SKILL.md), [hickey](../hickey/SKILL.md), and [lowy](../lowy/SKILL.md).

**Socratic Purpose Checklist:**
Evaluate the implementation by asking:
- *Is this solution a toy, a superficial prop, or genuine production-grade art?*
- *What is the higher-level goal, and what is truly necessary to achieve it to the optimal degree?*
- *Are we ignoring or glossing over hidden complexities to finish quickly?*

**Sieving & Cutting Check (Discriminative Pruning):**
Counter the additive bias of self-correction loops. LLMs tend to over-engineer solutions by continually adding redundant code, helper parameters, or verbose logic to patch reviewer critiques. Auditing requires active, discriminative pruning:
- *What has been added in previous iterations that is superfluous to the goal?*
- *Can we fold, merge, or completely delete these additions to achieve a cleaner, simpler representation?*
- *Note:* Pruning applies aggressively to any agent-added complexities. Do not delete pre-existing public API surfaces unless explicitly requested by `CTX.GOAL` or verified as completely unused by downstream code.
- **Grounded Ledger Invariant:** You must only add targets to the `REF_LEDGER` that are deterministically grounded. Socratic checks and sibling skill reviews (e.g., Hickey simplicity, Lowy volatility) may guide design reasoning, but cannot spawn ledger entries unless they are converted into concrete, reproducible test assertions, spec contract requirements, or compiler/linter rules. Any target added to the ledger by the refiner must be actively verified by executing the compiler, linter, or test runner in the workspace; unverified or hypothesized tool errors are strictly prohibited.

If no targets are found in `REF_LEDGER`, transition to `SWEEP` (transitioning directly to `REVIEW` or `REPORT` from `AUDIT` is strictly prohibited under any circumstances, even if the initial audit was completely clean). Otherwise, transition to `ITERATE`.

### 4. ITERATE
At the start of `ITERATE`, reset `CONSECUTIVE_CLEAN_SWEEPS` to `0` (since codebase modifications are about to occur).
For each ledger item:
1. Apply the local closed-loop verification loop inside the isolated worktree (`CTX.WORKTREE_PATH`):
   - **For code artifacts:** Apply TDD validation (write/update tests, verify baseline failure, implement changes, verify success).
   - **For non-code artifacts (e.g. documentation, specifications):** Apply rigorous linting, link checking, style alignment audits (e.g. [documentation](../documentation/SKILL.md)), and structural completeness checks. Verify baseline deficiency before correction.
2. Commit the change using conventional commits conforming to [commit-hygiene](../commit-hygiene/SKILL.md) inside the worktree directory, and record the conventional commit hash and message in `TRACE.LOOPS[CURRENT_LOOP].COMMITS`.
3. Update the ledger item status to `RESOLVED` with evidence.
4. Update the active sketch in `.ledger/log/` and commit it within the `.ledger/` sub-repository. To automate updating and committing sketch files, you can use the synchronization script from the main repo root:
   ```bash
   ./skills/refine/scripts/sync_sketch.py [optional custom message]
   ```
   Transition to `AUDIT` once all ledger items are `RESOLVED`.

### 5. SWEEP
Once the ledger is empty, the refiner MUST execute parallel validation sweeps using independent adversarial subagents. Self-auditing, self-certification, or skipping subagent creation based on the refiner's confidence or the minor size of edits is strictly prohibited and constitutes a fatal protocol violation.
Once the ledger is empty:
1. **Dynamic Angle Identification:** The refiner analyzes the scope of modifications and lists the relevant **Adversarial Audit Angles** (dimensions of the state-space) that must be audited in parallel. These must span every conceivable risk category for the modification (e.g., security, edge cases, UX, concurrency, performance, schema safety).
2. **Spawn Meta-Auditor:** Spawn an independent subagent with a clean context, passing the goal, constraints, final code/diff, and the proposed audit angles.
   - **Role:** Meta-Auditor
   - **Goal:** Audit the proposed review angles for completeness. Check for structural blind spots. Refine and sharpen the subagent prompts to ensure they are highly critical and target real vulnerability boundaries.
   - **Grounded Critique Invariant:** The Meta-Auditor MUST programmatically append the following constraint to all generated subagent prompts:
     `"You must only report findings that can be demonstrated with a concrete, reproducible test scenario, a compiler error, a specific linter rule violation, or a documented specification contract violation. Banish all stylistic, aesthetic, or subjective suggestions."`
   - **Interactive Gate:** The sweep cannot proceed until the human approves the angles list and sets `META_AUDITOR_STATUS: APPROVED`.
   - **Autonomous Gate:** The Meta-Auditor's critique and updated angles are accepted programmatically. The system updates the angle definitions, sets `META_AUDITOR_STATUS: BYPASSED_AUTONOMOUS`, and transitions immediately.
3. **Execute Isolated Subagent Audits:** For each approved angle, the refiner spawns an independent subagent in a mutually isolated context:
   - **IBC Setup:** Initialize the subagent with the specific custom prompt/persona approved by the Meta-Auditor, including the Grounded Critique Invariant. The subagent MUST remain completely blind to the existence, active rubrics, or findings of all other parallel sweep angles to prevent cross-reviewer influence or collusive group-think.
   - **Task:** Critically review the modified files against its specific rubric and return findings in a strict machine-readable format:
     ```yaml
     status: [PASS | FAIL]
     findings:
       - axis: [CORRECTNESS | API_SUFFICIENCY | COMPLIANCE | EDGE_CASES]
         target: "symbol_or_line"
         statement: "Description of the issue"
         evidence: "Linter error, failed test, or spec contract section"
     ```
4. **Evaluate Findings:**
   - If *any* subagent reports findings:
     - **Verifier Grounding Filter:** Filter all subagent findings against the strict Verifier Grounding rule. Any finding that cannot be mapped directly to a deterministic compiler error, linter warning, test failure, or documented specification violation must be rejected as subjective/stylistic and omitted from the active ledger. Reject any finding claiming a compiler error, linter warning, or test failure unless it is verified by actively executing the corresponding tool in the local workspace. If the compiler, linter, or test runner executes cleanly (exit code 0, no errors/warnings on the target), the finding must be classified as `REJECTED_FAKE_FAILURE`, logged under `TRACE.FILTERED_CRITIQUES` in the sketch, and omitted from the active ledger.
     - **Semantic Spec-Violation Triage:** For any subagent finding claiming a specification violation, the refiner must first check if the cited specification file is localized. Specification files checked during triage MUST reside in localized files explicitly mapped to the target package/module directory, be listed in the active sketchpad context under `CTX.SPECIFICATION_FILES`, or be documented directly within the active sketchpad. If the cited specification is not in this localized set, the finding must be classified as `REJECTED_OUT_OF_SCOPE`, logged under `TRACE.FILTERED_CRITIQUES` in the sketch, and discarded. The refiner must verify if the finding explicitly contradicts a statement, constraint, or invariant documented in those localized spec files. If no documented specification contradicts the current implementation, and no automated tool reports a failure, the finding must be classified as `REJECTED_SUBJECTIVE`, logged under `TRACE.FILTERED_CRITIQUES` in the sketch, and omitted from the active ledger.
     - **Stochastic Cascade Guard:** If the codebase has not changed since the previous sweep phase, any new subagent finding that was not identified in the previous sweep is automatically classified as `REJECTED_CASCADE_GUARD`, logged under `TRACE.FILTERED_CRITIQUES` in the sketch, and discarded unless it is backed by an automated compiler, linter, or test runner failure.
     - For accepted findings, merge them into `REF_LEDGER` as `PENDING` items.
     - Reset `CONSECUTIVE_CLEAN_SWEEPS` to 0.
     - Reset `META_AUDITOR_STATUS` to `PENDING`.
     - Transition to `AUDIT`.
   - If *all* subagents report `PASS`:
     - Increment `CONSECUTIVE_CLEAN_SWEEPS` by 1.
     - Reset `ROLLBACK_RETRY_COUNT` to 0.
     - **Convergence Shortcut:** If this is loop 1 (`CURRENT_LOOP` = 1), the initial audit was clean, and all subagents pass, the codebase has converged. Transition directly to `REVIEW` (bypassing `N_MIN`).
     - If `CONSECUTIVE_CLEAN_SWEEPS` < `M_SWEEP` or `CURRENT_LOOP` < `N_MIN`:
       - Transition to `AUDIT` to run another sweep cycle. Reset `META_AUDITOR_STATUS` to `PENDING`. To ensure diversity on unchanged code, the Meta-Auditor must choose different audit angles or perturb/alter the subagent personas (e.g. increase temperature or change persona roles).
     - If `CONSECUTIVE_CLEAN_SWEEPS` >= `M_SWEEP` and `CURRENT_LOOP` >= `N_MIN`:
       - Transition to `REVIEW`. (Transition to `REVIEW` is strictly forbidden if any code or documentation changes have occurred since the last sweep pass, or if `CONSECUTIVE_CLEAN_SWEEPS` has been reset to `0`).

### 6. REVIEW (Hostile Maintainer PR Review)
This state models a formal Pull Request review under extremely strict and hostile maintainers.
1. Increment `REVIEW_CYCLE_COUNT` by 1.
2. **Spawn Hostile Maintainers:** Spawn 3 independent subagents initialized with specific, critical reviewer personas representing codebase owners. Both the worker and the reviewers must be instructed as world-class experts who are the best at what they do, possessing confidence in their judgment but enough humility to concede when superior work or reasoning is offered.
   - **Maintainer 1 (`maintainer-architecture`):**
     - *Role:* Architecture & API Coherence Cop.
     - *Rubric:* Critique module coupling, boundary cleanliness, naming consistency, adherence to Hickey simplicity (complection) and Lowy volatility (axes of change). Reject redundant classes/functions and leaky boundaries. Reject lazy hacks or sub-standard code, but act constructively to help solve problems.
   - **Maintainer 2 (`maintainer-complexity`):**
     - *Role:* Complexity & Performance Auditor.
     - *Rubric:* Critique line counts, cognitive overhead, redundant loops/conditions, over-engineering, unnecessary allocations. Reject "BS" code and complexity bloat while remaining open to elegant, justified solutions.
   - **Maintainer 3 (`maintainer-documentation`):**
     - *Role:* Quality & Documentation Custodian.
     - *Rubric:* Critique documentation alignment (README, ADR, etc.), test coverage, edge cases, type-safety coverage. Ensure the repository's highest quality and documentation standards are met.
   - **Isolation Invariant:** Spawns must operate in mutually isolated context windows. They cannot see the refiner's internal thinking trace or each other's rubrics or findings.
3. **Evaluate Maintainer Feedback:**
   - Maintainers output their findings in structured format. The refiner merges these findings into `REVIEW_LEDGER` as `PENDING`.
4. **Address Ledger Items:** For each comment, the refiner (acting as an expert holding the macro architectural context) must evaluate the nit. The refiner must either:
   - **Commit Fix:** Edit code or architectural docs in the worktree directory, run linters/tests, commit changes, and record the commit hash in the ledger item `RESOLUTION`. This is the appropriate action when reviewer feedback is valuable for improving the code/docs up to high repository standards.
   - **justification:** Provide a formal, evidence-backed text explanation in `RESOLUTION` explaining why the code/architecture must be maintained in its current form. Use this when the refiner must **take a stand** and defend its choices because the reviewer or subagent misses the bigger, cohesive picture in their myopic review. The refiner must keep the higher-level goal on track, relying on its meticulous progress notes to prevent context loss. Crucially, the refiner **cannot resubmit its own bias** back into the equation if that bias was previously deferred or challenged.
   - **API Compromise:** If API stability has been reached, project goals and stability override individual nits. The refiner and reviewers must make compromises to preserve the public API surface. (Prior to stability, premature API lock-in is counterproductive, and design soundness overrides).
   - **Triage Transition Rules:**
     - If *any* code or documentation modification is made, the refiner MUST transition back to `ITERATE` (resetting all sweep counters) to compile, check lint, and run the adversarial validation sweeps (`SWEEP`) on the updated codebase state before returning to `REVIEW`.
     - If *only* text justifications are written, the refiner remains in the `REVIEW` state and requests re-evaluation from the maintainers.
5. **Re-Review Gate:** Maintainers review the updates. If they accept the fix or the justification, they mark the comment as `APPROVED`. If they reject, it stays `PENDING` and the refiner must attempt a new resolution.
6. **Cycle Budget Gate:** If `REVIEW_CYCLE_COUNT` > `CTX.CONSTRAINTS.REVIEW_BUDGET` and unresolved ledger items remain, transition to `HALT` and log a review budget exhaustion report.
7. Once all items in `REVIEW_LEDGER` are marked `APPROVED` by all maintainers, transition to `REPORT`.

### 7. AUTONOMOUS BACK-TRACKING & OSCILLATION RECOVERY
If at any loop boundary `CURRENT_LOOP` - LAST_RESTORED_LOOP exceeds $K_{max}$ (and `CONSECUTIVE_CLEAN_SWEEPS` == 0), or if oscillation is detected (k >= 2 and $\rho_k \ge 1$ when $d_p(\mathbf{S}_{k-1}) > 0$ and $d_p(\mathbf{S}_k) > 0$ and TRACE.LOOPS[k].RESTORED_FROM_LOOP is null, or if codebase states exhibit exact tracked workspace file hash equality $\mathbf{S}_k = \mathbf{S}_j$ for any prior loop state $1 \le j < k$ stored in `TRACKED_WORKSPACE_HASHES` when `CONSECUTIVE_CLEAN_SWEEPS` == 0 and j != TRACE.LOOPS[k].RESTORED_FROM_LOOP):
- **Interactive Mode:** Halt and transition to `HALT`.
- **Autonomous Mode:**
  1. Identify the target loop index $j$ (an integer, where $j < k$) in `TRACE.LOOPS` where all regression tests passed. If the codebase starts with pre-existing test failures that the agent is trying to resolve, select the target loop index $j$ that achieved the lowest proxy error metric $d_p(\mathbf{S}_j)$, or default to `0` (representing the initial state $S_0$ before any modifications). Resolve the target commit hash by selecting the last commit hash recorded in the `COMMITS` list of the `TRACE.LOOPS` entry where `LOOP == j`, or default to `TRACE.INITIAL_STATE_COMMIT` if $j = 0$. If the `COMMITS` list is empty for loop $j$ (e.g. it was a clean sweep pass), search backwards for the most recent preceding loop entry (where `LOOP < j`) containing a valid commit hash, or default to `TRACE.INITIAL_STATE_COMMIT` if none exists.
  2. Compute the next branch attempt index `N = TOTAL_ROLLBACK_COUNT + 2`.
  3. Inside the worktree directory (`CTX.WORKTREE_PATH`), clean up the workspace and check out a new branch attempt from the target stable commit hash:
     ```bash
     git restore :/
     git clean -fd
     git checkout -b agent/refine-<topic>-attempt-N <stable-commit-hash>
     ```
     This completely isolates the new attempt and preserves the entire history of the previous attempt branch (`-attempt-(N-1)`) for complete workspace auditability, satisfying global history invariants.
  4. Update `CTX.AGENT_BRANCH` to `agent/refine-<topic>-attempt-N` in the active sketch file.
  5. Set `TRACE.LAST_RESTORED_LOOP` to $j$ and set `TRACE.JUST_RESTORED` to $j$ in the active sketchpad, and reset `CONSECUTIVE_CLEAN_SWEEPS` to `0` in the sketchpad. Run the sketch synchronization script from the main repo to commit this state update:
     ```bash
     ./skills/refine/scripts/sync_sketch.py "docs(sketch): rollback to loop j via branch attempt N"
     ```
  6. Increment both `ROLLBACK_RETRY_COUNT` and `TOTAL_ROLLBACK_COUNT` in the active sketchpad.
  7. If `ROLLBACK_RETRY_COUNT` > 3, or if no rollback target state can be resolved from `TRACE.LOOPS`, transition to `HALT` and log a failure report.
  8. Apply Reflective Attempt Mutation (GEPA-inspired): Analyze the execution trace, modified diffs, and failures of the discarded branch attempt(s). Formulate an explicit list of "what not to do" (negative exemplars) and target modifications, documenting this reflection in the new loop entry. Perturb the Initial Boundary Condition (IBC) for the next attempt: lower the generation temperature, inject the negative exemplars into the reasoning context, or modify the subagent critique personas.
  9. Transition to `AUDIT` and resume.

### 8. HALT
Freeze the execution trajectory immediately. Record a failure report detailing the cause of the halt (unresolved ambiguity, budget exhaustion, rollback failure, review budget exhaustion, or loop oscillation) and return control to the human developer for manual intervention.
- **Cleanup Invariant:** Before completing the transition to `HALT`, clean up and remove the git worktree to leave the host environment in a pristine state:
  ```bash
  git worktree remove --force .worktrees/refine-<topic>
  ```

### 9. REPORT
Before generating the final report, execute a post-mortem review of the refinement process itself:
1. **Spawn Post-Mortem Process Auditor:** Spawn a final, independent adversarial review subagent:
   - **Role:** Adversarial Process Auditor
   - **Task:** Retrieve and analyze the entire parent conversation history (`transcript.jsonl` under `<appDataDir>/brain/<conversation-id>/.system_generated/logs/`) and git commit history of the refinement run. Critically evaluate the process: where did the refiner overcorrect, loop inefficiently, deviate from scope, or miss structural simplifications? What could have been done better?
   - **Output:** Return a structured critique outlining process inefficiencies and retrospective recommendations.
2. **Human Approval Gate:** Present the finalized sign-off, approvals, and diffs to the human developer (nrd).
   - If approved by the human:
     - Merge the final successful agent branch (e.g. `agent/refine-<topic>-attempt-N`) back into the active main branch, or format it as a single, clean conventional commit.
     - Clean up and remove the git worktree:
       ```bash
       git worktree remove --force .worktrees/refine-<topic>
       ```
     - Compile and output the final report using the template at `templates/REFINE.md`. Embed the maintainer review results and the post-mortem findings.
     - Record a final trace entry in `TRACE.LOOPS` for loop $k+1$ (the final state $\mathbf{S}^*$) with $d_p(\mathbf{S}^*) = 0$ and `VERIFICATION: "Fixed-point reached. Consecutive clean sweeps verified."` to demonstrate complete convergence.
   - If rejected by the human:
     - Clean up and remove the git worktree:
       ```bash
       git worktree remove --force .worktrees/refine-<topic>
       ```
     - Transition to `HALT`.

---

## Prime Directives

1. **FIXED_POINT_RIGOR:** Never declare completion without executing the minimum $N_{min}$ loops and satisfying the $M_{sweep}$ consecutive clean sweeps constraint, unless the convergence shortcut applies.
2. **ATOMIC_REFINEMENTS:** Every refinement commit must be logically atomic. Do not bundle unrelated refactorings or style updates into a single transaction.
3. **ORTHOGONAL_SWEEPS:** Every sweep MUST execute Multi-Boundary Subagent Sweeps (MBSS) in parallel. Spawning specialized, isolated review subagents approved by an independent Meta-Auditor is mandatory. Self-auditing, self-certification, or skipping subagent execution is strictly forbidden, regardless of refiner confidence or change size.
4. **DETERMINISTIC_GROUNDING:** Banish subjective criticisms. Every item entered in the refinement ledger must map directly to a verified failure of a linter, compiler, test assertion, or specification contract. Reject any finding without a concrete failure trace.
5. **SKETCH_SYNCHRONIZATION:** The active sketch in `.ledger/log/` must be updated and committed in the `.ledger/` sub-repository at every loop boundary. Do not bundle multiple loops of code modifications and sketch pad updates into a single commit. Automate commits using `./skills/refine/scripts/sync_sketch.py`.
6. **COMMIT_HYGIENE:** All commits must strictly conform to [commit-hygiene](../commit-hygiene/SKILL.md).
7. **OSCILLATION_BREAKING:** Detect and break limit cycles autonomously using target file hash matches. If in autonomous mode, check out a new attempt branch from the last stable commit in the isolated worktree and perturb prompt parameters before retrying. In interactive mode, halt immediately.
8. **EXIT_GATE_INVARIANCE:** Transitions to `REPORT` are strictly forbidden unless initiated from a passing `REVIEW` state where all maintainers have approved all items in the `REVIEW_LEDGER`, followed by the human final merge decision.
9. **GIT_HISTORY_INVARIANCE:** History-altering git commands (such as `reset`, `rebase`, or `commit --amend` on any commit in any user-facing branch) are strictly forbidden across both the main repository and the `.ledger/` sub-repository. Backtracking via attempt branches preserves the linear history of all attempts and satisfies global history invariance.
10. **PREMISE_CHALLENGING:** Never refine a design without challenging its core premises and assumptions first. If the design is fundamentally flawed or over-engineered, halt execution immediately instead of polishing a "turd."
11. **TIGHT_WORKTREE_LIFECYCLE:** The git worktree MUST be cleaned up and removed using `git worktree remove --force .worktrees/refine-<topic>` on any exit path (`REPORT` or `HALT`), leaving the host repository clean and undisturbed.
12. **HOSTILE_MAINTAINER_REVIEW:** You are required to submit changesets to a panel of independent, critical maintainer subagents representing codebase owners. They review code design, simplicity, and documentation. All comments in `REVIEW_LEDGER` must be resolved (via commits or justified rebuttals) and marked `APPROVED` before presenting the PR to the human.
13. **DOCUMENTATION_ALIGNMENT:** Manage architectural documentation actively. You must audit code modifications against mapped `CTX.ARCHITECTURAL_DOCS` to identify and resolve document drift, committing documentation updates in the same attempt branch.
