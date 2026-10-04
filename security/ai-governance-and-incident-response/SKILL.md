---
name: ai-governance-and-incident-response
description: Review an AI system for weak model version control, missing rollback plans, unsafe guardrail change workflows, inadequate regulated audit trails, and incident response gaps specific to LLM and agentic failures.
last_reviewed: 2026-04-27
---

# AI Governance and Incident Response

## First Principle

**You cannot respond to an AI incident if you do not know which model version, prompt version, and policy version produced the bad output.**

The foundational requirement for AI governance is reproducibility. When a model produces harmful output, takes an unauthorized action, or exhibits unexpected behavior in production, the first question is always: "What exactly did this system run?" If you cannot answer that question precisely — the exact model artifact, the exact prompt template version, the exact tool policy set, the exact data sources — you cannot diagnose the problem, fix it reliably, or demonstrate to regulators that you have controlled the risk.

Governance is not process for its own sake. It is the operational infrastructure that makes every other security control auditable, reversible, and defensible.

## Attack Mental Model

AI governance failures are not primarily attacker-driven — they are organizational failures that attackers exploit or that cause self-inflicted harm:

1. **Unknown production state** — teams cannot identify which model or prompt version is currently running, so they cannot scope the impact of a discovered vulnerability or pull the exact version producing bad output
2. **Ungoverned change velocity** — prompt templates, guardrail rules, and tool policies change frequently without review, creating unaudited regressions in safety or security behavior
3. **Audit trail inadequacy** — logs exist but do not capture the right fields; incident response requires reconstructing what happened, and the evidence is either missing (too sparse) or inadmissible (too raw, containing PII or secrets)
4. **Playbook absence** — teams apply generic web-service incident response to AI failures; AI-specific containment steps (rollback model version, quarantine memory, disable specific tools) are not pre-planned and take too long under time pressure

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Model release metadata, prompt changes, policy changes, exception approvals, and audit events are validated by the release workflow before they reach any environment. |
| **Scope** | Change authority is bounded by role and environment. Who can change models, prompts, guardrails, and data access policies — and which environments those changes may reach — is explicitly defined. |
| **Isolate** | Staged rollout, rollback capability, and environment separation ensure a release failure cannot become a fleet-wide outage or security incident. |
| **Enforce** | Signed release records, approval workflows, immutable audit trails, and incident runbooks are implemented in tooling — not in tribal knowledge or informal coordination. |

## GOV.1 Model and Guardrail Change Governance

**The core vulnerability:** Without versioning and approval workflows, every prompt edit, guardrail change, and model swap is an uncontrolled experiment in production. Any of these can silently degrade safety or security behavior.

### Check

- Is every production artifact — model ID, prompt template, guardrail rules, tool policy set — tracked as a versioned, immutable record tied to a release?
- Do guardrail relaxations, model swaps, and tool policy changes require explicit approval before reaching production?
- Is there a defined, tested rollback procedure that can restore a known-good model and policy state within a defined time window?

### Action

- **Version every production artifact.** Create a release record for each deployment that captures:

```yaml
release_id: "rel_2026-04-27-003"
deployed_at: "2026-04-27T14:00:00Z"
deployed_by: "deploy-service"
approved_by: "security-lead"
artifacts:
  model_id: "claude-sonnet-4-6"
  model_sha256: "a3f..."
  prompt_template_id: "chat-v2.3"
  prompt_template_hash: "sha256:b7c..."
  guardrail_policy_id: "policy-v4.1"
  tool_policy_id: "tools-v1.8"
  data_source_config_id: "sources-v2.0"
environments: ["production-us-east"]
rollback_to: "rel_2026-04-20-001"
change_rationale: "Updated refusal policy for medical content per legal review"
test_evidence_ids: ["eval-run-4521", "security-eval-4519"]
```

- **Require approval for high-risk changes.** Define a risk tier for each change type. Policy relaxations, model swaps, and new tool exposure are high-risk — require documented approval. Wording improvements to prompts with no policy change are low-risk — require peer review. No unilateral production changes for any tier.
- **Staged rollout and rollback.** High-risk changes roll out to 5% of traffic first. Rollback is a first-class operation with a documented procedure and a tested time-to-restore target (e.g., under 15 minutes for a model rollback).

### Failure Modes

- A prompt template is edited to improve tone. The edit removes a guardrail phrase. The change ships without review. Safety regressions are discovered 3 weeks later.
- An emergency model swap bypasses evaluation. The new model has subtle tool-calling behavior differences that are not caught until production incidents accumulate.
- A developer cannot tell which prompt version was running during the incident window because template changes are not versioned.

## GOV.2 AI Incident Response and Regulated Audit Readiness

**The core vulnerability:** Generic incident response playbooks do not cover AI-specific containment steps. When a prompt injection, model regression, or memory poisoning event occurs under time pressure, teams improvise — slowly.

### Check

- Does the organization have AI-specific incident playbooks covering: prompt injection, data leakage, unauthorized tool execution, model regression, and memory poisoning?
- Do audit trails capture enough structured evidence for forensic reconstruction — without exposing raw sensitive content?
- Have playbooks been exercised — tabletop drills, replay drills, or simulation runs — in the past 6 months?

### Action

- **Define AI-specific incident runbooks** for the most common failure modes. Each runbook must specify:
  1. Detection signal (what does this incident look like in logs and alerts?)
  2. Immediate containment (disable specific tool? roll back model version? quarantine memory store? rate-limit to zero?)
  3. Evidence preservation (which log streams, memory snapshots, and request records to capture before they expire or are overwritten)
  4. Communication chain (who is notified, in what order, with what initial information?)
  5. Post-incident review (what minimum structured evidence is required for the review record?)

- **Minimum audit log fields for regulated environments.** Every request that could be subject to review must produce a structured audit record containing: model version, prompt template ID and version, retrieval source IDs (not content), tool calls with authorization outcome, user/tenant context, and policy decision. This is the evidence set that regulators and auditors expect.

- **Test the playbooks.** Run a tabletop exercise for each major incident type at least once per quarter. A playbook that has never been exercised is a plan that has never been validated. Use the playbook gaps discovered in exercises to drive the next iteration.

### Minimum Deliverable Per Review

- [ ] Release inventory: all versioned production artifacts with approval, test evidence, and rollback pointer
- [ ] Approval workflow definition: who can approve what change type, for which environments
- [ ] Rollback procedure: documented, tested, with a measured time-to-restore
- [ ] Incident playbooks: one per major AI failure mode, with detection, containment, evidence, and communication steps
- [ ] Audit log field requirements by use case: operational debugging vs. security forensics vs. regulatory compliance

## Quick Win

**Write one AI incident playbook this week — for prompt injection.** It should cover: what a prompt injection looks like in your logs, what the immediate containment action is (e.g., which feature to disable, which tool to revoke), and which log fields you need to capture. A single tested playbook is worth more than five untested ones.

## References

- Base logging and runtime controls → [system-infrastructure-security/SKILL.md](../system-infrastructure-security/SKILL.md)
- Model provenance and promotion controls → [model-supply-chain-security/SKILL.md](../model-supply-chain-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
