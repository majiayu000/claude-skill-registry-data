---
name: agentdb-advanced
description: Advanced AgentDB deployment patterns, multi-tenant controls, and durability hardening.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
model: sonnet
x-version: 3.2.0
x-category: platforms
x-vcl-compliance: v3.1.1
x-cognitive-frames:
  - HON
  - MOR
  - COM
  - CLS
  - EVD
  - ASP
  - SPC
---




## Purpose
Design and operate resilient AgentDB clusters with governance, quotas, and observability baked in.

## Trigger Conditions
- **Use this skill when:** Need guardrails for multi-tenant AgentDB, backups, or compliance-focused deployments.
- **Reroute when:** If only doing basic local prototyping, use the base agentdb skill.

## Guardrails (Inherited from Skill-Forge + Prompt-Architect)
- Structure-first: every platform skill keeps `SKILL.md`, `examples/`, and `tests/` populated; create `resources/` and `references/` as needed. Log any missing artifact and fill a placeholder before proceeding.
- Confidence ceilings are mandatory in outputs: inference/report 0.70, research 0.85, observation/definition 0.95. State as `Confidence: X.XX (ceiling: TYPE Y.YY)`.
- English-only user-facing text; keep VCL markers internal. Do not leak internal notation.
- Adversarial validation is required before sign-off: boundary, failure, and COV checks with notes.
- MCP tagging for runs: `WHO=agentdb-advanced-{session}`, `WHY=skill-execution`, namespace `skills/platforms/agentdb-advanced/{project}`.

## Execution Framework
1. **Intent & Constraints** — clarify task goal, inputs, success criteria, and risk limits; extract hard/soft/inferred constraints explicitly.
2. **Plan & Docs** — outline steps, needed examples/tests, and data contracts; confirm platform-specific policies.
3. **Build & Optimize** — apply platform playbook below; keep iterative checkpoints and diffs.
4. **Validate** — run adversarial tests, measure KPIs, and record evidence with ceilings.
5. **Deliver & Hand off** — summarize decisions, artifacts, and next actions; capture learnings for reuse.

## Platform Playbook
- **Workflow patterns:**
  - Provision clusters with backups, encryption, and rotation policies
  - Define tenant-level quotas, namespaces, and authZ
  - Instrument metrics/alerts for latency, recall, and index health
- **Anti-patterns to avoid:** Running production on single-node dev defaults, Sharing credentials across tenants, Skipping periodic compaction or snapshot verification
- **Example executions:**
  - Set up staging and production clusters with nightly snapshot policies
  - Add per-tenant rate limits and API tokens for a hosted AgentDB service

## Documentation & Artifacts
- `SKILL.md` (this file) is canonical; keep quick-reference notes in `README.md` if present.
- `examples/` should hold runnable or narrative examples; `tests/` should include validation steps or checklists.
- `resources/` stores helper scripts/templates; `references/` stores background links or research.
- Update `metadata.json` version if behavior meaningfully changes.

## Verification Checklist
- [ ] Trigger matched and reroute considered
- [ ] Examples/tests present or stubbed with TODOs
- [ ] Constraints captured and confidence ceiling stated
- [ ] Validation evidence captured (boundary, failure, COV)
- [ ] MCP tags applied for this run

Confidence: 0.70 (ceiling: inference 0.70) - Standardized platform skill rewrite aligned with skill-forge + prompt-architect guardrails.
