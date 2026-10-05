---
name: seo-agentic
description: Use when auditing whether an AI agent can safely understand and complete a web task through the rendered interface, DOM, accessibility tree, forms, authentication, consent, state changes, and documented protocol capabilities such as UCP, ACP, MCP, or A2A; treat this as task readiness and accessibility, not a ranking factor or guaranteed agent usage.
---

# Agentic Web Readiness

Audit whether a permitted agent can perceive, understand, and safely complete a bounded task using the same truthful interface and controls available to users.

Read [agent-task-protocol.md](references/agent-task-protocol.md) before a formal audit.

## Procedure

1. Define one user-authorized task, start/end states, account/access assumptions, locale/device, risk class, owner, and success evidence.
2. Capture screenshot, DOM, accessibility tree, accessible names/roles/states, focus order, form labels/errors, dynamic state, network-independent confirmations, and any approved agent trace.
3. Verify semantic controls, stable identifiers/state, keyboard operation, loading/error recovery, consent, authentication, rate limits, and human-readable confirmation.
4. Require explicit confirmation for purchase, publication, deletion, permission, financial, legal, or other consequential actions. Never weaken security, privacy, bot controls, or anti-abuse systems for convenience.
5. Test task completion with bounded safe inputs in an authorized environment. Record partial completion, blocked access, ambiguity, and irreversible steps; do not simulate success.
6. Evaluate UCP, ACP, MCP, A2A, or similar capabilities only against current specifications and a documented consumer. Record discovery location, operations, authentication, version, fallback, owner, and policy boundary.
7. Route crawl/index concerns to `seo-technical`, commerce data to `seo-commerce`, accessibility remediation to the implementation owner, and search/AI measurement to `seo-performance` or `ai-visibility-monitor`.
8. Package findings as SEO Findings `1.1.0` with `task_flow` or `protocol_capability` targets and `agentic`, `accessibility`, `policy`, `technical`, or `commerce` categories.

## Guardrails

Do not call semantic HTML a ranking factor, protocol support a visibility requirement, or successful automation evidence of universal agent compatibility. Do not bypass authentication, CAPTCHA, consent, rate limits, paywalls, robots, or destructive confirmations.

## Formal evidence handoff

Package only supported observations as SEO Findings `1.1.0`. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout, then run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Keep the handoff provisional until this command passes.

## Output

Return the task contract, perception/state evidence, completion trace, blockers, safety controls, optional protocol assessment, owners, verification, rollback, and limitations—never an agentic SEO score.
