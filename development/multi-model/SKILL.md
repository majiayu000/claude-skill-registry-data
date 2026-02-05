---
name: multi-model
description: Coordinate multiple models for routing, ensembling, or fallback strategies.
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
Design model routing and orchestration playbooks with clear guardrails and observability.

## Trigger Conditions
- **Use this skill when:** Need model selection, fallback, or ensemble flows across providers.
- **Reroute when:** If limited to single provider, use its dedicated skill.

## Guardrails (Inherited from Skill-Forge + Prompt-Architect)
- Structure-first: every platform skill keeps `SKILL.md`, `examples/`, and `tests/` populated; create `resources/` and `references/` as needed. Log any missing artifact and fill a placeholder before proceeding.
- Confidence ceilings are mandatory in outputs: inference/report 0.70, research 0.85, observation/definition 0.95. State as `Confidence: X.XX (ceiling: TYPE Y.YY)`.
- English-only user-facing text; keep VCL markers internal. Do not leak internal notation.
- Adversarial validation is required before sign-off: boundary, failure, and COV checks with notes.
- MCP tagging for runs: `WHO=multi-model-{session}`, `WHY=skill-execution`, namespace `skills/platforms/multi-model/{project}`.

## Execution Framework
1. **Intent & Constraints** — clarify task goal, inputs, success criteria, and risk limits; extract hard/soft/inferred constraints explicitly.
2. **Plan & Docs** — outline steps, needed examples/tests, and data contracts; confirm platform-specific policies.
3. **Build & Optimize** — apply platform playbook below; keep iterative checkpoints and diffs.
4. **Validate** — run adversarial tests, measure KPIs, and record evidence with ceilings.
5. **Deliver & Hand off** — summarize decisions, artifacts, and next actions; capture learnings for reuse.

## Platform Playbook
- **Workflow patterns:**
  - Define routing policies by task, cost, and latency
  - Implement fallback chains with health checks
  - Log decisions and outcomes for continuous tuning
- **Anti-patterns to avoid:** Routing without telemetry, Infinite fallback loops without stop conditions, Mixing models without normalizing prompts
- **Example executions:**
  - Route generation to cost-effective model with quality checks
  - Blend embeddings from multiple providers for robustness

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
