---
name: governance-pfp
description: "Gate PFP and Symbol Game work: isolated answers, strict schemas, replay custody, budgets, and independent judges."
operad_source_colours: ["Code", "Paper"]
operad_target_colour: "Receipt"
operad_arity: 2
operad_residual: neutral
families: [governance, pfp, symbol-game, testing, clean-architecture]
---

# governance-pfp

AuthorityEffect: None.

## Current delivery and discovery direction

The primary goal is the simplest cost-effective, repeatable PFP procedure:
demonstrate one useful task, explain its prompt/response contract and checking
step, and collate the actual outcome and cost. Reuse the shared implementation.
The former fixed pilot grid, quotas and mandatory scaling waves are retired.
Catalogs and dimensions offer choices, not instructions to run every combination.

The secondary goal is targeted discovery of LLM and system failure modes,
antibodies and useful patterns. Name each experiment's question and cost/stop
limit; follow unexpected results with another small experiment when useful.
Apply learning to existing typed guidance, concrete prompt attachments or code.
An antibody needs its failure trigger, prompt/operation attachment, reproducer
and a benign control. Discovery observations are not statistical efficacy claims.

PFP is work in progress. Determine engineering needs from observed failures and
practical use. Add hieroglyphic rewrites, variable templates, modes, stages,
loops and alternate operation orders when they answer a concrete question.
Historical recipes below are optional research profiles, not quotas or universal
prerequisites. Use matched baselines for improvement claims, rather than forcing
every exploratory run into a campaign. Preserve existing historical evidence.

## The Single Constitutional Rule

> All Proposal Fidelity Protocol (PFP) operations, pilot campaigns, and structure transformation bouts must strictly decouple deterministic verification from untrusted model proposals, enforce fail-closed SPK-001 schemas with zero answer leakage, preserve cryptographic replay integrity, enforce fail-closed cost reservations, and ground empirical claims in verified offline replayed calculations on explicitly selected tasks and experimental conditions.

---

## 1. What Governance-PFP Must PREVENT (The Twelve Invariant Anti-Patterns)

Directly mined from the comprehensive audit review of 338 registered entries and 1,260 pilot files (`df84a596`):

1. **PREVENT Answer Leakage & Prompt Output Injection (`RULE_PFP_ZERO_ANSWER_LEAKAGE_001`, F01)**
   - *Prohibition:* Never serialize expected answers, prime lists, determinants, or schema examples containing outputs into participant prompts (`live_evaluator.py:255`).
   - *Seed Sanitization:* Never allow seed definitions to encode pre-computed `output` blocks identical to expected outcomes (`pilot_00049`â€“`00074`).
   - *Contamination Preservation:* Historical answer-leaking runs must be preserved with contamination annotations (`STATUS: CONTAMINATED_AUDIT`), never discarded, and never cited as clean evidence.
2. **PREVENT Permissive Grading & Soft Type Coercion (`RULE_PFP_FAIL_CLOSED_TYPING_001`, F02)**
   - *Prohibition:* Never apply loose type coercions (`int()`, `bool()`, `str()` parsing) that convert fractional floats (`3.9`) to integers (`3`), truncate prime lists, or map `true` to `1`.
   - *Envelope Mandatory:* Never accept bare JSON lacking the declared `SPK-001` envelope.
   - *No Model Impersonation:* Never construct synthetic `parsed_response` objects or policy stamps that the model did not generate.
   - *Fail-Closed Fallback:* Unregistered checker IDs must fail closed with `UNREGISTERED_CHECKER_ID`.
3. **PREVENT Stored Answer Equality Bypassing Domain Gates (`RULE_PFP_GENUINE_DOMAIN_EVALUATORS_001`, F04)**
   - *Prohibition:* Never route checkers to generic fallbacks comparing outputs to stored seed answers (`seed.expected_outcome.answer`).
   - *Candidate Witnesses Required:* Echoing `phi_1: 0` without candidate potential vectors, cochains, dual circulation witnesses ($d_0^T w = 0, \|w\|_\infty \le 1$), or algebraic certificates must be rejected.
   - *Domain Scoping:* Cohomology formulas apply only to declared cochain complexes; other arenas require typed domain predicates.
4. **PREVENT Blind Cache Reuse & Tampered Acceptance (`RULE_PFP_CRYPTOGRAPHIC_REPLAY_INTEGRITY_001`, F05)**
   - *Prohibition:* Never trust cached mode/status fields without verifying cryptographic bindings against raw response bytes.
   - *Tamper Refusal:* Mutating a single byte of a cached raw reply must break the SHA-256 digest and trigger `RECEIPT_DIGEST_MISMATCH`.
   - *Spec Drift Refusal:* Reject executions where stored responses cite different model IDs from the running specification.
5. **PREVENT Unsafe Cost Accounting & Hidden Retries (`RULE_PFP_FAIL_CLOSED_COST_ACCOUNTING_001`, F03, F09)**
   - *Prohibition:* Never default missing `usage.cost` to $0.00.
   - *Monotonic Attempts:* Never collapse multi-attempt retries into single call counts.
   - *Pre-Dispatch Holds:* Never bypass pre-dispatch ledger reservations.
   - *Fee Verification:* Never treat `:free` model suffixes as verified zero-billing receipts; live parameters, fees, and provider rate limits must be validated and snapshotted.
6. **PREVENT Synthetic Passes & File-Presence Metamorphism (`RULE_PFP_EMPIRICAL_MEASUREMENT_INTEGRITY_001`, F08)**
   - *Prohibition:* Never emit literal `PASSED` status dictionaries from constant code blocks without evaluator or model execution (as in Track 09).
   - *Inventory vs Measurement:* File-presence flags (`scored`, `passed`) are inventory metadata, not empirical measurements.
   - *Disjoint Terminals:* Every row must resolve to one of: `PLANNED`, `FIXTURE_VERIFIED`, `PROVIDER_COMPLETED`, `HOST_ACCEPTED`, `TYPED_REFUSAL`, `INFRASTRUCTURE_ERROR`, `CHECKER_DEFECT`.
7. **PREVENT Permutation Conflation with Independent Trials (`RULE_PFP_PERMUTATION_DECOUPLING_001`, F10, F12)**
   - *Prohibition:* Never report check-only or relabeling variations of a single model response as independent model trials.
   - *Registry Partitioning:* Check variations are partitioned as `PERMUTATION_EVALUATION`; only independently rendered requests or fresh provider dispatches count as `INDEPENDENT_MODEL_TRIAL`.
8. **PREVENT Reusable Orchestration Scattering (`RULE_PFP_ARCHITECTURE_DEDUPLICATION_001`, F06)**
   - *Prohibition:* Never duplicate helper AST groups (atomic writes, SHA-256 calculators, run-bundle persistence, budget gates) across pilot folders (23 repeated AST groups).
   - *Provider Port Exclusivity:* Never allow direct HTTP calls from individual pilot scripts; all network calls must route through the canonical PFP application provider port.
9. **PREVENT Merging Independent Judges (`RULE_PFP_INDEPENDENT_JUDGE_SEPARATION_001`, F06)**
   - *Prohibition:* Never homogenize or merge independent mathematical judges, formal verifiers, or frozen paper snapshots into single monolithic checkers.
   - *Separation:* Shared app infrastructure handles transport, persistence, and budget accounting; mathematical verification judges remain strictly independent.
10. **PREVENT Budget Policy Drift & Unidentified Models (`RULE_PFP_MODEL_BUDGET_CONFINEMENT_001`, F09)**
    - *Prohibition:* Never allow runaway per-pilot or per-arm spending ($0.10â€“$5/arm); default campaigns must target $0 spend on open-weights/free tiers, with micro-budgets capped at < $0.005/run.
    - *No Unidentified Models:* Never deploy unidentified exploratory models (`stealth/space-bunny-alpha`) in governed campaigns.
11. **PREVENT Prompt Agency & Self-Authorizing Extraction (`RULE_PFP_PROMPT_AGENCY_PROHIBITION_001`, F11)**
    - *Prohibition:* Never attribute enforcement authority to prompts ("forces intermediate derivations", "ensures model checks equations"). Prompts request; host code parses, checks, and rejects.
    - *Mining Fence:* Model-extracted components remain unverified candidate material until admitted by host review or automated gates.
12. **PREVENT Prompt Family Acceptance Conflation (`RULE_PFP_PROMPT_FAMILY_EQUIVALENCE_001`, F12)**
    - *Prohibition:* Never group rule-withholding refusal controls into the primary task prompt family. Distinct acceptance predicates require partitioning into an associated adversarial-test family.
    - *Witness Naming:* Use `DERIVATION_WITNESS` for checkable artifacts rather than mentalistic `SCRATCHPAD_WITNESS`.

---

## 2. What Governance-PFP Must PROMOTE (The Six Coalescence Pillars)

1. **Multidimensional Parameter Matrix Architecture (`RULE_PFP_MULTIDIMENSIONAL_MATRIX_001`)**
   - Knobs span orthogonal dimensions defined in [`dimension_register.yaml`](../../../workflows/library/pilot_estate/dimensions/dimension_register.yaml):
     - **Open Task Family Universe:** The task universe is unbounded and coextensive with all problems that can be posed as text prompts (symbolic manipulation, combinatorial search, graph theory, automated reasoning, constraint satisfaction, code generation, cochain defect verification, semantic parsing, formal refutation, etc.). An initial finite seed suite (e.g. `linear_algebra`, `graph_facts`, `graph_repair`, `refusal`, `cochain_defect`, `magma_associativity`) serves solely as a Phase 1 calibration fixture slice for baseline failure-boundary benchmarking, not a closed domain boundary.
     - **Multi-Rung Difficulty Scaling:** Difficulty rungs (e.g. Rungs 1â€“5 and beyond) calibrated to baseline model failure boundaries where unstructured prompt-response loops break down.
     - **Representation Rewrites:** Encodings across representations and syntax styles (`raw_prose`, `structured_spans`, `ebnf_wire_v1`, `sn_wire_v2`, `mss_boundary_v1`, `hieroglyphic_glyphs`, or domain ASTs).
     - **Operational Modes:** Structured protocol execution modes across functional clusters (e.g. direct proposals, verified roundtrips, multi-turn descent, typed refusal).
     - **Model Tiers:** Open weights (8B, 70B) and free-tier routes on OpenRouter.
   - *Extensional Problem Ingress:* Task instances are generated or ingested from modular problem generators and domain evaluators rather than maintained as static, duplicated script folders.
2. **Single Prompt Standard (`SPK-001`) Ingress Pipeline (`RULE_PFP_SPK001_INGRESS_PIPELINE_001`)**
   - Compiles raw stimulus $P$ into typed prompt packet $P^*$ and decomposition tree $\{p_i\}$ under `SPK-001`.
   - Preserves verbatim bytes in `raw_reply`; non-schema commentary is accounted for as Structure Leakage Debt in `residual_text_ledger.json`.
   - Strict Pydantic V2 schema validation on all incoming responses before evaluation.
3. **Cryptographic Replay Manifest & Hermetic Offline Verification (`RULE_PFP_REPLAY_MANIFEST_INTEGRITY_001`)**
   - `ReplayManifestV1` cryptographically binds:
     - `prompt_sha256`: SHA-256 of rendered prompt payload.
     - `raw_reply_sha256`: SHA-256 of verbatim provider response bytes.
     - `decoding_config`: Pinned temperature, top_p, max_tokens, seed.
     - `checker_digest`: SHA-256 of sovereign checker source and dependencies.
     - `receipt_digest`: SHA-256 of the resulting evaluation receipt.
   - Offline replay sweeps must run completely disconnected (`--offline`) re-executing checkers against stored raw bytes. Tampering with any byte must trigger fail-closed `RECEIPT_DIGEST_MISMATCH`.
4. **Pre-Dispatch Budget Reservations & Monotonic Accounting (`RULE_PFP_PREDISPATCH_BUDGET_RESERVATION_001`)**
   - Compulsory ledger reservation before initiating network transport.
   - Monotonic sequence numbering and discrete attempt logging for all retries.
   - Automatic halt and reservation lock on missing cost metadata (`UNRECONCILED_COST`).
5. **Paired Experimental Protocols & Structure Delta (`RULE_PFP_PAIRED_CONTROLS_STRUCTURE_DELTA_001`)**
   - For an improvement claim, compare PFP with a matched plain baseline and the same independent checker. Discovery experiments instead state the failure question they probe; no fixed arm or repetition count applies.
   - Measure Structure Delta: $\Delta S = S_{\text{created}} - S_{\text{removed}}$.
   - Track calibrated abstention: models must cleanly refuse out-of-distribution inputs under explicit contract clauses.
6. **Four-Artifact Pilot Standardization & Decisive Mutations (`RULE_PFP_FOUR_ARTIFACT_STANDARDIZATION_001`)**
   - Retained legacy pilot bundles use the following anatomy. New demonstrations reuse the shared runner and need not create a directory per experiment:
     1. `spec.yaml`: Task parameters, knobs, schema IDs, budget limits.
     2. `run.py`: Canonical execution entrypoint routing through `PilotLabService`.
     3. `tests/test_pilot.py`: Focused regression checks for demonstrated defects; no fixed mutation count.
     4. `README.md`: Concise problem specification and mathematical invariant description.
7. **Optional Research Derivation Profiles (`RULE_PFP_PILOT_MODUS_OPERANDI_AND_LIFT_PROTOCOL_001`)**
   - Historical recipe in [`modus_operandi.md`](../../../adversary/tests/pilots/modus_operandi.md) for empirical pilots (`pilot_0000000` through `pilot_0000099`):
     - **Mechanized Paper Claim Grounding:** Advanced pilots (Rungs 2â€“6) must reject trivial toy seeds and ground problems in verified Lean 4 Mathlib theorems and Python certified oracles in `coda_atlas/F004_papers/`.
     - **Root Directory Hygiene:** Pilot roots contain only sovereign specs (`spec.yaml`, `seed.yaml`, `prompt_template.yaml`, `p_star.yaml`, `README.md`, `results/`, `tests/`).
     - **Granular Test Capsules:** Every run is encapsulated in sequential zero-padded folders (`tests/test_00/` through `tests/test_99/`) containing `test_spec.yaml`, `input.yaml`, and `response.yaml`.
     - **3-Stage Empirical Derivation Protocol:**
       1. *Stage 1:* Bare seed + 10 distinct surface dialect rewrites (Tier H, Tier D, Tier S, Matrix/Vector, Category Theory, Discrete Cochains, Channel Masking, S(n) Down-Map, Genesis Relational, Operator Axioms) evaluated without hints or templates.
       2. *Stage 2:* $P^*$ Prompt Template baseline under SPK-001 governance (evaluating compliance, refusal, and structural lift requests on ungrounded/unlicensed operations).
       3. *Stage 3:* DDC Structural Lift contract grant (`governance-wdp`), extending carrier capacity and operational licenses, driving exact certified $\ell^1$ norm derivation.
     - **Zero Overwrites:** Never overwrite earlier prompt generations; maintain immutable lineage records with versioned files (`p_star_rewrite_XX_v2.yaml`).

---

## 3. Retained Core Mathematical Invariants

1. **Discrete Manifold Retraction & Strict Descent**: Proposer-host interaction proceeds strictly through discrete manifold retraction turns verifying Strict Descent on $(\Gamma_2, \Phi_1, \text{defect\_count})$ under the Discrete Deformation Calculus (DDC) 8-letter operational trace alphabet $\mathcal{A}_{\mathrm{DDC}} = \{E, R, C, I, \Lambda, D, M, T\}$. Loose conversational chat is forbidden (`symbol-game-manifold-retraction-guard`).
2. **Exact Rational Cochains & Simplicial Metric Geometry**: Edge weights in $\mathbb{Q}$ (`fractions.Fraction`); Gram matrix $G_{ij} = (d_{0i}^2 + d_{0j}^2 - d_{ij}^2)/2$ must be positive definite for Euclidean embeddability; deficit angle receipts check incident angles; and independent dual circulation witness ($d_0^T w = 0, \|w\|_\infty \le 1$) is required for zero-duality-gap certification (`symbol-game-simplicial-metric-guard`).
3. **Value Object Exact-Type Equality**: All cross-context Value Objects (`TurnKind`, `Disposition`, `Role`, `Budget`) live strictly in `domain/shared_kernel/` with exact-type equality (`type(self) is type(other)`). Subclass masquerading is forbidden (`symbol-game-inward-dependency-guard`).
4. **Stage Opcode Allocation Formula**: Governs internal evaluator dispatch offset $\mathrm{base}(N) = 128 + 8 \times (N - 22)$ for $N \ge 22$ (internal evaluator metadata only; never serialized into MSS wire packets).
5. **Stage Retraction Down-Map Law**: Retraction down-rule $d_N(u_N(x)) = x$ is a conditional lift obligation for future accepted lifts. Newly introduced terms return typed `NON_DESCENT` (`stage_status.py`, `goo-mssn-stage-retraction-gate`).
6. **Delimiter Balancing & $\Sigma_{36}$ Wire Alphabet**: Balanced delimiters (nested brackets/parentheses), $\Sigma_{36}$ alphabet compliance, base distinction `<>` classified as Diff, never Atom (`symbol-game-packet-codec-guard`).
7. **Two-Object Identity & Four Non-Overlapping Domains**: Strict non-conflation of **Object A** (Proposal Fidelity Protocol runtime â€” untrusted neural proposals, packetization, zero authority) and **Object B** (Minimal Symbol System monograph â€” cochains, quotient obstructions, discrete optimization). Partitioned across PFP/SGPP (runtime), MSS-N/$S(n)$ (pure math), CEC (context extension), and Authority/Core (sovereign gate).

---

## 4. Operational Execution & Verification CLI

```bash
# Consolidated PFP invariant verification check
python operads/skills/governance-pfp/scripts/check_pfp.py

# Backward-compatible verification alias
python operads/skills/governance-pfp/scripts/check_symbol_game.py
```

---

## 5. Reference Dispatch Matrix

| Target Reference File | Primary Focus | Task Branch Dispatch Condition |
|:---|:---|:---|
| [`references/pfp_pilot_audit_and_remediation_standards.md`](references/pfp_pilot_audit_and_remediation_standards.md) | 10 vulnerability vectors (F01â€“F10), 5 remediation workstreams, preflight gates. | Consult when reviewing pilot implementations, prompt builders, or replay pipelines. |
| [`references/evidence_learned_antiskills.md`](references/evidence_learned_antiskills.md) | Production mutation gaps (M01â€“M23) and PFP audit anti-skills (Anti-Skills 13â€“22). | Consult when writing regression tests, debugging silent skips, or auditing runner traps. |
| [`references/sn_four_layer_separation.md`](references/sn_four_layer_separation.md) | 4-layer model, epistemic one-way arrow, 4-directory layout. | Consult when reviewing $S(n)$ documentation boundaries or mathematical shadows. |
| [`references/active_obstruction_registers.md`](references/active_obstruction_registers.md) | Dual registers ($W_n^{\mathrm{active}}$ vs $H_n$), retraction $r_N$, simplicial invariants. | Consult when auditing stage obstruction counts, down-maps, or Gram embeddability. |
| [`references/genesis_claim_hygiene_and_taxonomy.md`](references/genesis_claim_hygiene_and_taxonomy.md) | 4-strata evidence, 5 anti-patterns, PFP late-stage receipts. | Consult when verifying derivation claims or PFP tool call 6-tuples. |
| [`references/two_object_identity_and_four_domains.md`](references/two_object_identity_and_four_domains.md) | Object A vs Object B non-conflation, WDP 22 layers, 12 nonclaims. | Consult when demarcating runtime PFP code from pure MSS-N mathematics. |
| [`references/genesis_levels_and_research_estate.md`](references/genesis_levels_and_research_estate.md) | Levels 00â€“21 sealed core vs 22â€“100 post-pin exploratory trees. | Consult when working with Genesis level derivations or open horizon boundaries. |
| [`references/sn_mssn_level_decomposition_and_epochs.md`](references/sn_mssn_level_decomposition_and_epochs.md) | Nine operadic epochs, trans-base dispatch offset $\mathrm{base}(N)$. | Consult when navigating MSS-N level decomposition or operadic dispatch. |
| [`references/universal_cross_domain_playbook.md`](references/universal_cross_domain_playbook.md) | 6-step cross-domain fixture playbook, carrier graphs, ASSERT moves. | Consult when writing or testing domain fixtures, cuts, or graph projection adapters. |
| [`references/manifold_retraction_and_packets.md`](references/manifold_retraction_and_packets.md) | DDC 8-letter trace alphabet, packet envelopes, wire syntax codecs. | Consult when working on wire codecs, envelope serialization, or strict descent. |
| [`references/mssn_tower_grammar_and_stages.md`](references/mssn_tower_grammar_and_stages.md) | Levels 0â€“21 grammars, retraction contracts, stage status lifters. | Consult when auditing stage status, lift proofs, or syntax grammars. |
| [`references/simplicial_geometry_and_cochains.md`](references/simplicial_geometry_and_cochains.md) | Cochains, deficit angles, Gram positive-definiteness, dual circulation. | Consult when implementing exact rational cochain solvers or simplicial embeddings. |
| [`references/pedagogy_and_curriculum.md`](references/pedagogy_and_curriculum.md) | 4-tier cognitive ladder, 4-minute pulses, learning metrics ($P_{\text{diag}}$). | Consult when generating educational materials, student notebooks, or pedagogical exercises. |
| [`references/operational_toolkits_and_frontiers.md`](references/operational_toolkits_and_frontiers.md) | Token frontier EFG licensing, replay terminal ladder, prompt contracts. | Consult when evaluating token generation frontiers, replay ladders, or prompt lints. |

## Typed transport lessons from Pilot 22

For a transformation, name the protected executable query and the equality being
preserved. Type shape, equal summaries and recomputed digests alone do not establish
answer preservation. Use a preserving control and a coherently rebound control that
changes the answer. For composition, state the intermediate version/span identity
rule and whether equality concerns endpoints/maps or also derivation histories.
A different semantic adapter is allowed when its comparison contract is explicit.

Name raw capture, evaluation and output budgets separately. The historical trusted
offline runner's evaluation cap did not cap its raw retention stream; avoid claiming
a total resource bound from the evaluation limit alone.

[Reviewed finite transport contract](../../../_ic/nara/historical/oewas007/research/briefs/pfp_expansion/pilot22_typed_engine/revision2/candidate/README.md).
These controls support the declared finite query, not arbitrary prose equivalence.
