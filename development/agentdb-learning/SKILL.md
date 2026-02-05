---
name: agentdb-learning
description: Learning loops on top of AgentDB for reinforcement, curriculum, and replay buffers.
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
Wire AgentDB into learning systems so agents can store, grade, and reuse experiences safely.

## Trigger Conditions
- **Use this skill when:** Need replay buffers, curriculum storage, or offline evaluation tied to AgentDB.
- **Reroute when:** If doing non-learning retrieval, use agentdb or agentdb-optimization.

## Guardrails (Inherited from Skill-Forge + Prompt-Architect)
- Structure-first: every platform skill keeps `SKILL.md`, `examples/`, and `tests/` populated; create `resources/` and `references/` as needed. Log any missing artifact and fill a placeholder before proceeding.
- Confidence ceilings are mandatory in outputs: inference/report 0.70, research 0.85, observation/definition 0.95. State as `Confidence: X.XX (ceiling: TYPE Y.YY)`.
- English-only user-facing text; keep VCL markers internal. Do not leak internal notation.
- Adversarial validation is required before sign-off: boundary, failure, and COV checks with notes.
- MCP tagging for runs: `WHO=agentdb-learning-{session}`, `WHY=skill-execution`, namespace `skills/platforms/agentdb-learning/{project}`.

## Execution Framework
1. **Intent & Constraints** — clarify task goal, inputs, success criteria, and risk limits; extract hard/soft/inferred constraints explicitly.
2. **Plan & Docs** — outline steps, needed examples/tests, and data contracts; confirm platform-specific policies.
3. **Build & Optimize** — apply platform playbook below; keep iterative checkpoints and diffs.
4. **Validate** — run adversarial tests, measure KPIs, and record evidence with ceilings.
5. **Deliver & Hand off** — summarize decisions, artifacts, and next actions; capture learnings for reuse.

## Platform Playbook
- **Workflow patterns:**
  - Capture episodes with scores and metadata for replay
  - Build curriculum progression queries and freshness windows
  - Automate evaluation runs that write back graded experiences
- **Anti-patterns to avoid:** Mixing training and evaluation data without lineage, Letting replay buffers grow without TTL/compaction, Missing safety checks on auto-labeled data
- **Example executions:**
  - Store RL trajectories with reward signals and filter by scenario
  - Run evaluation sweeps that tag failing episodes for re-training

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
