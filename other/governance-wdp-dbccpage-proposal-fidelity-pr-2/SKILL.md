---
name: governance-wdp
description: "Consolidated Witnessed Difference Programme (WDP) governance gate across CODA 9-layer stack, DDC operations, Algorithm Prime stages, and Research Atlas totality."
operad_source_colours: ["Code", "Paper", "State", "Proof"]
operad_target_colour: "Receipt"
operad_arity: 4
operad_residual: neutral
families: [governance, wdp, coda, ddc, prime-algos, atlas, mathematical-solvers]
---

# Governance WDP: Witnessed Difference Programme

**AuthorityEffect:** None.  
**Consolidation Notice (2026-10-12):** This sovereign governance skill consolidates and supersedes 14 legacy specialist skills:
- `governance-coda`, `coda-atlas-lake-totality-sync-guard`, `coda-research-atlas-reconcile`, `coda-semigroup-action-defect-falsifier-harness`, `coda-spine-search-pipeline`
- `governance-ddc`, `ddc-exact-repair`, `ddc-scale-descent`, `ddc-structural-lift`, `ddc-tape-parser`, `ddc-typed-refusal`
- `governance-prime-algos`, `theoria-algorithm-prime-000`, `techne-prime-pipeline-stage-evaluator`

---

## 1. Core Mathematical Foundations of WDP

The **Witnessed Difference Programme (WDP)** establishes the continuum-free, relational mathematics governing discrete complexes, coboundary defects, and exact quotient repairs across the engine:

1. **Zero-Authority Substrate:**  
   Markdown specifications carry `AuthorityEffect: None`. Truth resides strictly in verified executable code (compiled Rust in `engine/crates_rs/core_wdp/` and formal Lean 4 kernels in `coda_atlas`).
2. **Tripartite Semantic Separation:**  
   Agents must never conflate the three fundamental difference primitives:
   - **Difference ($\Delta$):** The raw algebraic or combinatorial disagreement between two cochain states.
   - **Residual ($r$):** The projected cochain remnant after contraction onto a declared subspace ($r = x - P(x)$).
   - **Defect ($d$):** The failure of an exact sequence, closure, or boundary condition ($d = \delta^k \omega \ne 0$).
3. **Exact Rational Geometry:**  
   All valid theorem-grade certifiers operate over exact rational arithmetic ($\mathbb{Q}$) using `num_rational::BigRational`. Floating-point implementations are relegated to proposal diagnostics and explicitly gated with `AuthorityEffect: None`.

---

## 2. CODA 9-Layer Stack Architecture

All work interacting with the CODA application pipeline must comply with the canonical 9-layer sequence defined in `coda_*_rules.yaml`:

```text
Layer 1: FOC   (Finite Obstruction Calculus)
Layer 2: MUR   (Meta & Universal Re-Presentation)
Layer 3: CS    (Continuum Shadow)
Layer 4: CS-Q  (Continuum Shadow to Continuum Bridge)
Layer 5: Q     (The Continuum)
Layer 6: A     (Sentinel)
Layer 7: OR    (Omniversal Re-Presentation)
Layer 8: FDA   (Finite Descent Authority)
Layer 9: GTLA  (General Theory of Layered Authority)
```

The names and application order above follow `operads/rules/coda/rl_coda_and_prime_algorithms_discipline.md` and `engine/crates_rs/core_wdp/src/coda/pipeline.rs`. Names identify components; the actual layer functions and their declared premises determine executable scope. A layer record does not establish external authorization.

### Key Invariants:
- **Layer 5 Identity:** Layer 5 is strictly named **"The Continuum"** (`Q`). Hallucinated legacy names such as "Quantum Enclosure" are rejected by automated gates.
- **Duality Zero Gap:** Every optimal $L^1$ quotient repair must be accompanied by an exact dual cocycle certificate verifying zero duality gap ($\text{primal} = \text{dual}$).
- **FDA Role Split:** The component proposing an algebraic mutation or repair step cannot authorize its admission.
- **GTLA Cryptographic Gate:** External root authority cannot promote unverified speculative candidates into theorem-grade statuses.

---

## 3. Discrete Deformation Calculus (DDC)

DDC provides the dynamic state-transition calculus across discrete state spaces, tracked via action tapes (`ddc.jsonl`).

### The 8-Letter Trace Alphabet:
Each DDC step uses one of these eight operation labels and carries an execution log or an explicit refusal outcome:
- **`E` (Exact Repair):** Discharges the declared defect; the host checks zero reported residual and diagnostics on the same carrier.
- **`R` (Residual Projection):** Carries the remaining residual; the host preserves reported obstruction diagnostics on the same carrier.
- **`C` (Context Exposure):** Changes the declared carrier/window; the host rejects a decrease in reported obstruction diagnostics.
- **`I` (Integration):** Records integration with a receipt declaration; the host requires the diagnostic state to remain unchanged.
- **`Λ` (Structural Lift):** Extends the carrier under a lift trigger and licence declaration. A trigger alone is not a licence.
- **`D` (Descent / Re-index):** Changes the carrier with a loss-ledger declaration.
- **`M` (Refusal):** Emits a typed refusal reason without mutating the diagnostic state.
- **`T` (Terminalization):** Records terminalization without mutating the diagnostic state or minting authority.

These meanings follow `engine/crates_rs/core_wdp/src/ddc/ddc_alphabet.rs` (`DdcOp`) and the host checks in `engine/crates_rs/core_symbol_game/src/ddc.rs` (`step_violations`). The host consumes declared diagnostics and witness booleans; this conditional verification does not independently establish a supplied receipt, loss ledger, lift licence, or detector adequacy.

### Action Tape Protocol (`ddc.jsonl`):
- The inspected host action enumerates the submitted steps in order and constructs a SHA-256 receipt chain over their canonical payloads.
- `verify_tape` checks its implemented letter/control laws against declared states and witness fields. Unknown letters return `UnknownLetter`; malformed requests or exact scalars may return parsing errors.
- This request schema does not carry an existing tape's entry hashes or step indices. The returned chain does not independently authenticate supplied artifacts, execution, or external witness objects.

---

## 4. Algorithm Prime Triad & Protocol Stages

Algorithm Prime governs protocol execution, preventing infinite loops, stalling, and spurious nocebo-to-placebo oscillations:

1. **Stage 1: Declaration Order (Preflight & Setup):**  
   Declare finite carrier sets, coordinate bases, and boundary matrices before execution. Dynamic allocation of undeclared coordinates during descent is prohibited.
2. **Stage 2: Adapter Descent (Optimization & Repair):**  
   Execute bounded descent steps. Every step must strictly decrease the declared Lyapunov obstruction potential ($\Phi(s_{t+1}) < \Phi(s_t)$) or terminate.
3. **Stage 3: Continuation Law (Confluence & Handoff):**  
   Verify the normal form chase confluence. If the obstruction is quenched ($\Phi = 0$), emit an accepted receipt; if a non-zero obstruction persists and no valid descent exists, emit a typed refusal.
4. **Anti-Cheat Halting Bounds:**  
   Every iterative run is capped by a strict fuel parameter. Exhausted fuel yields an explicit `BudgetExhausted` refusal, never an unverified partial solution.
5. **Protocol vs. Domain Type Discipline:**  
   Prime stages are behavioral protocol operations. Domain types live in `core_wdp` and `core_types`; stage wrappers must never re-declare parallel domain structs.

---

## 5. CODA Research Atlas, Lake Totality & Spine Search

The **CODA Research Atlas** (`atlas/coda_atlas/`) stores the canonical repository research monographs, claim ledgers, and formal proofs.

1. **EADC Decimal Classification (`EA:FFF.SSS.BBB`):**  
   All chapters and monographs follow the EADC addressing schema:
   - `FFF`: Field (e.g., `001` Finite Obstruction Calculus, `004` General Relativity, `006` Finite QM).
   - `SSS`: Subfield.
   - `BBB`: Book / Monograph.
2. **Lake Proof Totality Gate:**  
   Lean 4 formalizations in `lean4/genx/` and `coda_atlas/` must compile with 0 errors, 0 warnings, 0 `sorry` tokens, and 0 custom synthetic axioms.
3. **Semigroup Action Defect Falsification:**  
   Dynamic suites must distinguish true physical projected motion from discrete semigroup action defects ($\delta_{\text{semigroup}} = T(s_1 + s_2) - T(s_1) T(s_2)$).
4. **Spine Search Pipeline:**  
   Atlas reconciliation maintains SQLite FTS5 full-text indexing and vector embeddings over canonical monographs, ensuring verifiable bibliographic lineage.

---

## 6. Verification Harness & Operator Tooling

To run the consolidated source checks and fixed examples across WDP, CODA, DDC, and Prime algorithms, use the scripts in `scripts/`:

```bash
# Run the consolidated WDP checks:
python operads/skills/governance-wdp/scripts/check_wdp.py

# Run individual component checks:
python operads/skills/governance-wdp/scripts/check_coda.py
python operads/skills/governance-wdp/scripts/check_ddc.py
python operads/skills/governance-wdp/scripts/check_prime_algos.py
```

A passing run confirms only the checks implemented by these scripts, including selected source checks and fixed arithmetic examples. It is not a Rust build, Lean replay, proof of paper/runtime equivalence, or independent verification of supplied witness declarations.
