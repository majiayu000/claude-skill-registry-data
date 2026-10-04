---
name: ship
description: Run the DegenExus pre-merge GO/NO-GO gate with schema-checkable evidence and specialist routing.
disable-model-invocation: true
argument-hint: "[scope or PR target]"
---

# Ship Workflow

Canonical `/ship` workflow. Use this skill instead of duplicating merge-gate prose in commands.

## Sources of Truth

- Routing contract: `.claude/rules/synergy-contract.yml`
- Evidence schema: `.claude/rules/evidence-schema.yml`
- Human routing overview: `.claude/rules/02-agent-synergy.md`
- Release evidence pack: `.claude/skills/release-evidence-pack/SKILL.md`
- Live smoke template for internals changes: `.claude/skills/claude-config-audit/references/live-smoke-template.md`

## Required Gate

1. Resolve changed files and scope from the prompt/current diff.
2. Run `python .claude/hooks/validate-claude-config.py` when `.claude/**`, `CLAUDE.md`, `AGENTS.md`, or agent memory changed.
3. Run `python -m compileall -q .claude/hooks` when hooks changed.
4. Run runtime checks appropriate to the diff, normally `python -m compileall -q src/` and `python -m pytest tests/ -v`.
5. Run `pip-audit -r requirements.txt` when dependency manifests changed or release policy requires it.
6. Confirm no `.env*`, `secrets/**`, `*.pem`, `*.key`, `*.db`, `*.db-wal`, or `*.db-shm` files were added.
7. Route specialists from `.claude/rules/synergy-contract.yml`; always include `code-reviewer`, `security-auditor`, and `test-engineer` for merge readiness, then add domain owners by changed-file surface.
8. Collect each specialist fenced `yaml` evidence block and run `python .claude/hooks/validate-evidence-payload.py <payload>` when shell execution is available. Report schema validation as `PASS`, `WARNING`, or `FAIL`. Reject any specialist output missing `verdict`, `scope_reviewed`, `source_of_truth`, or `findings` unless the specialist explicitly marks `NEEDS_INFO` with a remediation owner.
9. Require live smoke evidence from `references/live-smoke-template.md` only when `.claude/**`, `CLAUDE.md`, or `AGENTS.md` changed; otherwise note `NOT_RUN` with reason.

## Final Output

Emit `.claude/rules/evidence-schema.yml` fields plus a clear `GO` or `NO-GO` decision. Any Critical finding, High security/prompt/risk/SoT finding, or missing required evidence without an environment limitation is `NO-GO`.
