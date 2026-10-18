---
name: forge-n8n
description: "Forge: building and validating n8n automation workflows: n8n, workflow, webhook, trigger, cron, retry, error branch, credentials, validate_workflow."
---

# Forge playbook — n8n / automation

This domain is **skill + MCP driven, not agent-heavy.** Do **not** spawn a crowd of agents. **Do not duplicate ECC n8n skills — defer to them.**

## Hard rules
- Validate before claiming production-ready: webhook method, input schema, credentials, auth/security, **error branch present**, retry behavior, **test/prod separation**.
- Credentials live in n8n credential store / env — never hardcoded in nodes.
- Imported/new workflows stay **inactive** until the owner approves activation.
- Expressions are null-safe: use optional chaining, `??` for defaults (not `||`, which also replaces 0 and empty text), and `Array.isArray()` before looping.
- Webhook-triggered workflows answer early with a Respond to Webhook node and do slow work afterwards, so the caller never times out.

## Workflow
1. Consult `n8n-mcp-tools-expert` **first** (correct nodeType formats + tool selection).
2. Architecture from `n8n-workflow-patterns`; node setup from `n8n-node-configuration`; expressions from `n8n-expression-syntax`.
3. Code nodes → `n8n-code-javascript` (default) or `n8n-code-python`.
4. **Gate:** run `validate_node` / `validate_workflow` via `n8n-validation-expert`; resolve real errors (it knows the false positives).
5. For custom code/scripts you *may* run `codex-reviewer` (Codex, optional) — advisory, not a blocker.

## Fan-out & flow
L2 fix/extend; L3 new multi-branch workflow. Mostly **serial** (a workflow is one artifact); parallelize only independent sub-workflows.

## Ship-readiness (unique)
`validate_workflow` clean; webhook auth enabled; secrets in credentials (not hardcoded); error + retry paths exist; test vs prod URLs separated; a manual test execution shown. Then run the `ship-readiness` n8n checklist. **Never** claim production-ready without passing validation; no live activation without owner approval.
