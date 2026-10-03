---

name: leeway-skill-orchestrator

description: Graph-based orchestration layer that composes LeeWay skills and tool capabilities into an Ambient Capability Field, Task Capability Weave, and bounded Focal Execution Set. Connects skills by primitives, requirements, support, verification, fallback, conflict, transfer, and tool ownership without making MCPs the center of the architecture.

license: MIT

metadata:

  authority: Creator/Human Authority > LeeWay Standards

  mode: graph-skill-orchestration

  stage: post-resilience-pre-focal-execution

  kernel: skills/leeway-universal-capability-kernel/SKILL.md

  resilience: skills/leeway-capability-resilience/SKILL.md

  gateway: skills/leeway-tool-gateway/SKILL.md

  lifecycle: skills/leeway-skill-lifecycle-governance/SKILL.md

---

# LeeWay Skill Orchestrator

## Universal portability gate

Apply `config/portability-contract.md` throughout the capability weave. Express needs as logical capabilities and select authorized, qualified host adapters. No skill may require a particular machine path, OS, device or model as LeeWay core identity. OS/provider-specific instructions apply only to the selected adapter. Preserve the task across equivalent local/remote adapters; report a missing capability precisely when no authorized route exists. Distinguish portable contract, implemented adapter and tested platform in verification.

## Purpose

Turn the governed skill/tool universe into one coordinated capability organism. The Universal Capability Kernel defines the capability-manifold model; this skill operationalizes graph construction, composition, ownership, prerequisites, verification, and focal execution selection.

## Skill/tool graph

Every governed node should declare or derive when evidence permits: PROVIDES, REQUIRES, SUPPORTS, USES_TOOL, TOOL_OWNED_BY, VERIFIES, FALLBACK_FOR, CONFLICTS_WITH, SUPERSEDES, SHARES_PRIMITIVE_WITH, TRANSFERS_PATTERN_TO, OUTPUTS_TO, INPUTS_FROM.

MCP is only one possible provider type. Prefer abstract capability identity over provider identity.

## Orchestration levels

1. CONSTITUTIONAL_CORE — always-on identity/governance.

2. AMBIENT_CAPABILITY_FIELD — lightweight metadata/primitives for every verified skill/tool.

3. TASK_CAPABILITY_WEAVE — all materially useful skills/primitives for the current objective.

4. FOCAL_EXECUTION_SET — only skills/tools requiring full instructions or execution.

5. VERIFICATION_SET — independent skills/tools required to test/criticize/verify.

6. RECOVERY_SET — fallbacks/rollback/repair capabilities if focal execution fails.

A substantive plan is incomplete if it identifies execution but no applicable verification/recovery path.

## Formula/context probes

For each task weave and each material node ask:

1. What are we not discovering?

2. What needs enhancement?

3. What skill is missing?

4. What tool is missing?

5. What orchestration level is missing?

6. What execution level is missing?

7. What other skills can compose with this skill?

8. How does this skill connect upstream/downstream?

9. Which tools does it own/use, and which skill governs each tool?

10. Which verifier and recovery capability closes the loop?

Feed discoveries back through Capability Resilience / Skill Factory rather than silently leaving graph holes.

## Composition procedure

intent → acceptance gate → context/formula → capability demand → graph query → task weave → resolve dependencies/conflicts → focal execution set → verification set → recovery set → execute → verify → evidence → learn

When multiple skills share a primitive, compose at the primitive level where possible rather than loading redundant full instructions.

When a tool lacks a governing skill owner, classify it ORPHAN_TOOL until assigned, wrapped, deprecated, or quarantined.

When a registry skill path has no canonical artifact, classify it REGISTRY_DRIFT; do not count it as a verified live skill.

## Execution truth

listed != governed; governed != executable; executable != executed; executed != verified.

Tool presence in source is not proof of runtime availability.

## Output

For audits, produce a graph/matrix with canonical skills, tools/resources, ownership, relationships, gaps, duplicates/conflicts, missing skills/tools, missing orchestration/execution/verification/recovery levels, proposed compositions, and evidence state. For ordinary tasks, use the graph silently and expose only the materially useful weave.

## Verification and recovery closure

Build VERIFICATION_SET using `leeway-veritas` and domain-specific verifiers. After verification route evidence through `leeway-receipt-authority`, then admit only verified learning through `leeway-learning-ledger`. Build RECOVERY_SET using `leeway-capability-resilience`, `leeway-host-commander`, device/platform fallbacks, rollback skills, or domain recovery capabilities as applicable.


## Parallel execution handoff

When the TASK_CAPABILITY_WEAVE contains independent work units, hand bounded jobs to `leeway-parallel-workplane`. The parent retains conversation, authority, acceptance gate and merge responsibility. Serialize conflicting canonical mutations.


## Company context

Before finalizing a substantive TASK_CAPABILITY_WEAVE, consult `leeway-company-capability-fabric` for affected departments, role/tier perspectives, decision rights, upstream/downstream dependencies, and parallel program lanes. Focal execution must not silo the ambient field. Use `leeway-centered-skill-metrics` only with evidence-bound measurements and explicit targets.


## Orchestration precedence

`leeway-skill-orchestrator` owns capability selection/composition and the TASK_CAPABILITY_WEAVE. `leeway-parallel-workplane` owns delegated worker lanes, interrupt/retool state and parent conversation sovereignty. `multi-agent-orchestration` is a domain implementation skill for designing/building multi-agent systems and messaging architectures; it does not supersede the parent LeeWay orchestrator. `workflow-orchestration` is a domain implementation skill for DAG/state-machine/business workflow construction, retries and compensation; it does not own Agent Lee identity or skill selection. One parent control plane; subordinate orchestration capabilities compose beneath it.


## Maximum-capability probes

At material architecture/capability reviews also ask:
11. **What would a world-class specialist department know that we have not encoded?**
12. **What capability are we postponing merely because an external product/provider currently supplies it, and can LeeWay learn and own the underlying method or native path?**

Do not defer a reasonably specifiable capability as 'later' merely because it is specialized or difficult. Difficulty is a planning/routing concern, not a reason to lower the target. External systems may provide evidence, architecture patterns or execution, but provider availability must not become the boundary of LeeWay capability thinking.


## Skill House routing
For substantial domain work, consult `config/skill-house-registry.json` before selecting isolated skills. A Skill House is a department-scale capability view over the graph. Activate one or more Houses ambiently, then derive TASK_CAPABILITY_WEAVE and FOCAL_EXECUTION_SET from their member capabilities. Small/local tasks may route directly to a skill when House activation adds no material context.

House activation does not load every member skill at full depth. It guarantees contextual eligibility and exposes department workflow, providers, gates, verification, recovery and cross-House dependencies.

Current promoted Houses: WRITING_PUBLISHING and THREE_D_PRODUCTION. Multiple Houses may compose in one program.


## LeeWay Imagination & Simulation Kernel

For substantive work where pre-execution simulation can materially reduce error, cost or risk, route through `leeway-imagination-simulation-kernel` and `config/imagination-simulation-execution-contract.json` before real mutation.

Required behavior: INTENT → GROUND → REPRESENT → GENERATE → SIMULATE → EVALUATE → REPAIR → SELECT → AUTHORIZE → EXECUTE → OBSERVE → COMPARE → VERIFY → EVIDENCE.

The workspace must keep OBSERVED, CANDIDATE/PREDICTED, EXECUTED and VERIFIED states distinct. A modeled PASS is never execution proof. Failed candidates trigger repair/alternative search until acceptance or a verified blocker. Select task-appropriate models; do not force every problem into geometry. Formula authority may be claimed only after canonical Formula artifact/version/hash/implementation is verified as required by LeeWay standards.

This kernel is disciplined counterfactual planning/execution behavior, not a claim that Agent Lee is conscious, self-aware, subjectively imagines, or literally reproduces human neural mechanisms.


## Formula Epistemic Authority

Before using a Formula/equation as governing evidence, consult `leeway-formula-epistemic-authority`, `config/formula-knowledge-registry-v1.json`, and the applicable epistemic record.

Required distinction: mathematical validity, dimensional validity, domain validity, numerical stability, empirical validity, standards conformance, runtime validation and canonical authority are independent dimensions. Never collapse them into one PASS.

Classify the expression/model before use. A heuristic/project target/standard-bound rule/empirical hypothesis cannot be promoted to universal mathematical law. Candidate equations remain subordinate to verified canonical LeeWay Formula authority. PASS and FAIL evidence are both retained. If canonical Formula authority is claimed, reverify the canonical artifact/version/hash/implementation as required before comparison/promotion.


## Formula Fabric routing

Formula consumers should request governed Formula capability through `leeway-formula-fabric` and `config/formula-fabric-client-contract-v1.json` rather than creating or carrying independent canonical Formula copies.

Route: consumer → Formula Fabric discovery → authority/self-inspection → compute/lab operation → authority/evidence envelope → Veritas/receipt when consequential.

GitHub Pages/static publication is discovery only and cannot prove or execute Formula runtime. Live authoritative computation requires a verified Formula Fabric runtime bound to canonical Formula implementation evidence. Verified sealed offline bundles are allowed by manifest/version/hash; unverified copied Formula fallback is prohibited.


## Real-Time Voice & Multimodal Infrastructure routing

For live voice, streaming STT/TTS, barge-in, phone/receptionist/avatar voice, read-aloud, WebRTC media, live screen/camera multimodal, or audio-latency work, route through `leeway-real-time-voice-multimodal-infrastructure` as a focal execution skill and apply `config/realtime-voice-heavy-use-routing-v1.json`.

Do not substitute the generic multimodal skill for production real-time media engineering. Use the real-time execution contract, playout ledger, interrupt bus, telemetry and LFEA-qualified profiles. Thresholds are tunable evidence-bound profiles; transport/provider choices remain task-dependent and subordinate to LeeWay authority.
