---
name: operational-safety
description: Progressive-disclosure operational-safety-depth modules for the work-loop. Holds failure-mode-keyed checklists the quality-engineer reviewer reasons from (state-and-idempotency, blast-radius, environment-isolation, cost-and-teardown, drift-and-rollback, observability-and-smoke), plus cloud-implementation-craft, the module also inlined into the implementer's EXECUTE brief. Each is grounded in standing operational taxonomy (AWS Well-Architected, Google SRE, the Terraform/Pulumi Day-1/Day-2 split). The orchestrator loads only the matching modules and inlines them into the reviewer's REVIEW brief — and cloud-implementation-craft into the implementer's EXECUTE brief — when infra/destructive work is detected; the subagent never self-discovers this skill. Not a reviewer prompt itself — it is the depth library the reviewer and implementer reason from. Carves against security-checklists on the reliability-vs-security lens.
---

# Skill: operational-safety

This skill is the **depth library** behind the `quality-engineer` agent for
infrastructure and destructive operational work. The reviewer's body carries
the *universal method* (its testability / observability / reliability /
maintainability lens, the severity rubric, the report format). The
*shape-specific depth* — what to actually check at each operational failure
mode — lives here, in the per-failure-mode `references/<module>.md` modules (reviewer
checklists plus `cloud-implementation-craft`, the EXECUTE-craft module — see
below), so the agent prompt stays lean and the depth scales without bloat. It
is the operational-lens twin of
[`security-checklists`](../security-checklists/SKILL.md), built on the same
orchestrator-loaded, table-routed mechanism — **no new reviewer** (the CHARTER
three-reviewer ceiling; ADR-0023), no executable code (ADR-0031).

## How it loads (orchestrator-driven, not self-discovered)

**The orchestrator drives loading; the subagent does not.** There is no
mechanism to force a subagent to invoke a skill, skill discovery is
model-invoked and adapter-variable, and the `quality-engineer`'s `tools:` list
does not include a Skill tool. So depth must not depend on the reviewer finding
this library itself.

Concretely, at the work-loop's REVIEW `quality-engineer` step, when the change
is infra/destructive (the destructive/irreversible risk trigger routed it to
full mode, and the diff touches IaC / deploy config / a stateful migration),
the orchestrator:

1. Detects which **operational failure modes** the diff or spec crosses.
2. Loads **only the matching modules** via the deterministic failure-mode→module
   routing authority — this skill's [Module index](#module-index) below (the
   `work-loop` REVIEW `quality-engineer` bullet dispatches against it rather than
   carrying its own copy).
3. **Inlines the selected modules' content** into the `quality-engineer`
   subagent's brief — so the reviewer receives a focused checklist as prompt
   text, never a path to resolve. The **same three steps** also run at
   `work-loop`'s EXECUTE step for `cloud-implementation-craft`, inlining it into
   the *implementer's* brief (the EXECUTE-consumer extension below).

Loaded per this skill's Module index — only the modules the change raises, never a
flat march through every module. Where an
adapter *does* support subagent skill auto-discovery, that is a redundant
convenience layered on top — never the load-bearing mechanism.

**The EXECUTE-consumer extension (`cloud-implementation-craft`).** ADR-0031
established this library as a REVIEW-only depth source for `quality-engineer`.
One module — `cloud-implementation-craft` — is **also** inlined into the
**implementer's EXECUTE brief** on infra-flavored work, by the same
orchestrator on the same Module index, so its golden practices
(least-privilege-but-sufficient permissions, timing/retry, packaging,
externalized config) shape the build, not only the review (ADR-0034). The
mechanism is unchanged — the orchestrator inlines; the subagent does not
self-discover — only the *consumer* is extended from the reviewer to the
implementer. `quality-engineer` still loads it at REVIEW to check the craft
against deployed reality.

## The reliability-vs-security carve (load-bearing)

This library and [`security-checklists`](../security-checklists/SKILL.md) split
infrastructure review along one clean line, and the split must stay clean both
ways:

- **`security-checklists` owns *security* config.** Over-broad IAM, public
  exposure, secrets in state, unencrypted-at-rest, metadata SSRF, CORS — the
  security failure classes. Its `config-misconfig` module is the IaC-security
  home.
- **`operational-safety` (this skill) owns *reliability / ops* config.**
  Idempotent convergence, blast radius, environment isolation, cost/teardown,
  drift/rollback, observability/smoke — the operational failure classes.

The routing therefore assigns **IaC-security → `config-misconfig`**,
**IaC-reliability → `operational-safety`**. Do not duplicate security config
into an operational module, and do not migrate operational config out of where
it correctly lives. When a check seems to belong to both lenses, ask which
*failure* it guards against — a leaked credential is security; a half-applied,
non-convergent stack is reliability.

## The three-bucket delegation legend

Every check in every module is tagged so the reviewer knows who owns it —
the same legend `security-checklists` uses, read through the operational lens:

- **`tool`** — scanner / CI-gate-owned. Confirm the gate is *wired*; don't
  re-check by hand. The operational analogs of the security scanners are the
  policy-as-code / CSPM scanner (which also feeds the security pass), the
  cost-diff gate, and the plan-parse destroy/replace counter. If the delegated
  gate is **absent**, do not silently skip: either reason the class best-effort
  and flag it `degraded: no gate`, or state the gap explicitly. A silent skip
  is the worst outcome — it looks like coverage.
- **`hybrid`** — the gate surfaces the signal; *you* judge the fix. A plan
  diff or a drift report points at the change, but whether the apply converges,
  whether the destroy is intended, or whether the rollback path is real is
  reasoning work.
- **`reason`** — reviewer-only. Whether the loop is genuinely idempotent,
  whether proposer≠approver holds for a destructive op, whether a smoke probe
  actually exercises the artifact end-to-end — the classes no scanner sees. The
  highest-value findings live here.

## Module index

This index is the **deterministic failure-mode→module routing authority** — the
`work-loop` REVIEW `quality-engineer` bullet (and, for `cloud-implementation-craft`,
the EXECUTE implementer brief) dispatches against the **Load when** column rather
than carrying its own copy. Match the operational failure mode the infra/destructive
change raises to its module(s). The `> **Grounded in:**` cells pin each module to
its RFC-0041 module-table groundings.

| Module | Load when — the operational failure mode the change raises | Grounded in |
|---|---|---|
| [`state-and-idempotency`](references/state-and-idempotency.md) | provisioning or mutating infra; a stateful migration; any re-runnable write path — covers convergent re-apply, state locking, single-writer | F1.2, F1.3 |
| [`blast-radius`](references/blast-radius.md) | can delete or replace existing infra; a destroy/teardown path; removing a `prevent_destroy` guard — covers destroy/replace gating, proposer≠approver | F3.1, F3.2 |
| [`environment-isolation`](references/environment-isolation.md) | iterating against (or able to touch) production; shared vs throwaway/staging state — covers separate state/accounts | F3.3 |
| [`cost-and-teardown`](references/cost-and-teardown.md) | provisions billable resources; ephemeral/per-iteration infra; teardown path — covers cost-ceiling-as-gate, destroy-on-fail, TTL, no orphans | F3.4, F3.5 |
| [`drift-and-rollback`](references/drift-and-rollback.md) | long-lived infra that can drift; a deploy needing a defined recovery path — covers read-only drift detection, known-good re-apply path | F1.4, F2.6 |
| [`observability-and-smoke`](references/observability-and-smoke.md) | deploys a service / site / endpoint a user reaches; needs smoke + telemetry — covers active end-to-end probe, log access, health, verify-status, symptom→layer log playbook | F2.2; taxonomy follow-up |
| [`cloud-implementation-craft`](references/cloud-implementation-craft.md) | authoring infra / a managed-runtime deployment / live interaction (**also inlined into the implementer's EXECUTE brief**) — **EXECUTE-craft**: least-privilege-but-sufficient permissions, timing/retry, packaging / entrypoint model, externalized config (also REVIEW) | RFC-0044 Author·behavioral + packaging gap |

`state-and-idempotency` (write-path convergence) and `drift-and-rollback`
(divergence detection + recovery) are kept **deliberately separate** — every
major operational taxonomy splits the two (AWS Well-Architected *Change
Management* vs *Failure Management*; Google SRE *Release Engineering* vs
*Incident Response*; Terraform `apply` vs `-refresh-only`; Pulumi Day-1 vs
Day-2). `observability-and-smoke` is its own sixth module, not folded into
reliability prose, because "load the real URL, confirm render, read the logs to
debug a failed smoke" is a distinct active-probe + telemetry concern.
