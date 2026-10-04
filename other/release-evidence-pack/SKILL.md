---
name: release-evidence-pack
description: >
  Assemble merge-readiness evidence for DegenExus PRs: tests, compile checks,
  security scan status, edge cases, changed files, memory updates, and gate verdicts.
disable-model-invocation: true
when_to_use: >
  Invoke explicitly during `/ship`, PR preparation, or docs-memory-curator evidence
  audits.
---

# Release Evidence Pack

Use `.claude/rules/evidence-schema.yml` as the output schema and `.claude/rules/synergy-contract.yml` for specialist routing.


## Workflow

1. Record changed files and classify runtime, test, docs, memory, and `.claude` impacts.
2. Run or collect evidence for `python -m compileall -q src/`, targeted pytest, full pytest when feasible, and `.claude` config validation when relevant. When `.claude/**`, `CLAUDE.md`, or `AGENTS.md` changed, include the live-smoke checklist from `.claude/skills/claude-config-audit/references/live-smoke-template.md`.
3. Summarize security checks, including secrets scan status and dependency audit status if dependencies changed.
4. List at least three edge cases considered.
5. State whether `memory/` files changed and why.
6. Ask routed specialists to emit a fenced `yaml` block matching `.claude/rules/evidence-schema.yml`; when shell execution is available, validate captured blocks with `python .claude/hooks/validate-evidence-payload.py <payload>`.
7. Produce a GO/NO-GO recommendation with blockers separated from recommendations.

## Output Sections

- Scope
- Commands and exact outcomes
- Specialist findings
- Edge cases
- Memory updates
- Remaining risk
- Final verdict

The final pack must include `verdict`, `scope_reviewed`, `source_of_truth`, `commands_run`, `findings`, `edge_cases`, `handoffs`, and `memory_update` fields from `.claude/rules/evidence-schema.yml`, plus `validate-evidence-payload.py` PASS/WARNING/FAIL status for specialist evidence when collection was possible.
