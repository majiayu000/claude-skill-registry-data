---
name: codex-supercharge-router
description: >
  Route Codex work to the right supercharged workflow. Use when the user asks
  to improve their Codex setup, choose among skills, combine GitHub repos/MCP
  servers, reduce tokens, build agent workflows, or decide which local
  supercharge skill to invoke next. Use the boundary rules here when requests
  mention agents, evals, costs, guardrails, MCP, daemon/status workflows, or
  safety.
---

# Codex Supercharge Router

Use this first when the request is broad. Pick one primary skill, then add at most
one support skill.

## Routing Table

| User need | Primary skill | Support skill |
|---|---|---|
| "I am running out of context" | `$low-token-context` | `$model-cost-router` |
| "Understand this repo" | `$repo-intelligence-brief` | `$codebase-graph-scout` |
| "Make this repo easier to revisit" | `$repo-to-wiki` | `$agent-memory-ledger` |
| "Use or test an MCP server" | `$mcp-server-lab` | `$mcp-safety-review` |
| "Add MCP CI/conformance gates" | `$auto-skill-build-mcp-conformance-harness` | `$mcp-safety-review` |
| "Is this MCP safe?" | `$mcp-safety-review` | `$sandbox-source-intake` |
| "Clean up MCP config secrets" | `$auto-skill-safety-mcp-secret-guard` | `$mcp-safety-review` |
| "Turn an API into tools" | `$openapi-to-mcp-skill` | `$mcp-safety-review` |
| "Build, redesign, or review frontend UI" | `$open-design-ui-library` | `$low-token-context` |
| "Ship a reliable agent workflow" | `$auto-skill-build-agent-reliability-loop` | `$agent-observability` |
| "Track local agent runs/costs" | `$agent-observability` | `$model-cost-router` |
| "Append or review recent run history" | `$auto-skill-build-agent-run-ledger-dashboard` | `$agent-observability` |
| "Grade Supercharge edits or share status" | `$auto-skill-build-supercharge-feedback-loop` | `$agent-observability` |
| "Run bounded iterative experiments" | `$experiment-loop-runner` | `$agent-memory-ledger` |
| "Choose model tier or cost route" | `$model-cost-router` | `$low-token-context` |
| "Import third-party skill/prompt pack" | `$auto-skill-safety-external-skill-intake` | `$skill-quality-gate` |
| "Create reusable prompt templates" | `$codex-prompt-template-builder` | `$skill-quality-gate` |
| "Create many useful skills" | `$skill-pack-factory` | `$skill-quality-gate` |
| "Audit my skill/plugin pack" | `$skill-quality-gate` | `$low-token-context` |
| "Clone fresh repos safely" | `$sandbox-source-intake` | `$repo-intelligence-brief` |
| "Synthesize patterns across cloned repos" | `$auto-skill-build-source-pattern-synthesis` | `$skill-pack-factory` |
| "Verify GitHub trend or discovery claims" | `$auto-skill-trend-github-discovery-radar` | `$sandbox-source-intake` |
| "Set up a day/week workflow" | `$workflow-launchpad` | `$agent-memory-ledger` |
| "Set up daemon/status/worker control" | `$workflow-launchpad` | `$mcp-safety-review` |

## Boundary Rules

- If the request affects live users, external tools, accounts, data, payments,
  or production budgets, choose the reliability or safety skill before local
  observability.
- If the user asks for CI, release gates, JUnit/XML, conformance, or tool-surface
  diffs, choose `$auto-skill-build-mcp-conformance-harness` over
  `$mcp-server-lab`.
- If the task is one bounded trial with a stop condition, use
  `$experiment-loop-runner`; if it feeds production guardrails or canaries, use
  `$auto-skill-build-agent-reliability-loop`.
- If the task is only model choice or token/cost measurement, use
  `$model-cost-router`; if routing is enforced by gateway budgets or fallback
  policy, use `$auto-skill-build-agent-reliability-loop`.
- If the source is an external skill pack, slash-command pack, hook plugin, or
  prompt catalogue, run `$auto-skill-safety-external-skill-intake` before
  `$skill-pack-factory`.
- If the task creates or adapts reusable Codex prompt templates, use
  `$codex-prompt-template-builder`. If the template pack came from an external
  source, run `$auto-skill-safety-external-skill-intake` first; run
  `$skill-quality-gate` before publishing.
- If the task compares multiple local source clones before deciding what to
  build, use `$auto-skill-build-source-pattern-synthesis` before
  `$skill-pack-factory`.
- If the task uses current popularity, trend, stars, topics, "latest", or public
  launch/discoverability claims, use `$auto-skill-trend-github-discovery-radar`
  before writing README, marketplace, or skill-generation conclusions.
- If the task has daemons, workers, queues, sidecars, task APIs, status/log
  commands, or multi-agent leases, use `$workflow-launchpad` before starting
  processes. Add `$mcp-safety-review` only when the control surface exposes
  side-effecting tools or credentials.
- If the task creates, edits, reviews, grades, or validates Codex Supercharge
  artifacts, append a `$auto-skill-build-supercharge-feedback-loop` batch so
  future sessions and automations can see the latest state.
- If the task turns an OpenAPI/Swagger spec into tools, use
  `$openapi-to-mcp-skill` for the surface plan. Add `$mcp-safety-review` before
  serving or installing any generated bridge when credentials, writes,
  destructive operations, admin actions, or account data are involved.
- If the task is visual/frontend work, use `$open-design-ui-library` for
  design-system selection and craft checks. Use `$workflow-launchpad` only when
  process control, local daemons, or worker lifecycle is the main risk.

## Skip When

- The user has explicitly named the exact skill or plugin to use.
- The task is a narrow code edit with an obvious local workflow.

## Default Policy

- Prefer small, composable workflows over large magic systems.
- Prefer local markdown state over repeated long prompts.
- Prefer shallow clones and README/manifest inspection before installs.
- Prefer source evidence over trend-list claims.
- When a repo is unverified or risky, classify it as inspiration only.

Read `references/source-repos.md` when you need the cloned source inventory.
Read `references/source-pattern-synthesis.md` when comparing source patterns.
Read `references/github-discovery-radar.md` when claims depend on current
GitHub evidence, public repo status, stars, topics, or trend positioning.
Read `references/workflow-control-plane.md` when launching daemon, worker,
status/log, task API, or multi-agent coordination workflows.
Read `references/supercharge-feedback-loop.md` before continuing prior Codex
Supercharge artifact work or handing status to subagents/automations.
Read `references/openapi-tool-surface.md` when converting API specs into MCP or
agent tool surfaces.
Read `references/open-design-ui-library.md` when selecting UI systems,
tokens, or craft checks.
Read `references/prompt-template-system.md` and `prompt-templates/README.md`
when creating or adapting reusable prompt templates.
Read `references/skill-routing-boundaries.md` when routing overlaps.

## Validation

- Choose one primary skill and at most one support skill.
- Escalate safety/reliability before execution when accounts, credentials,
  live users, or destructive tools are involved.
- If routing overlaps, cite the boundary rule used.
