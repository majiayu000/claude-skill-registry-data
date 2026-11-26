---
name: aizee
description: Sovereign AI engineering control plane — governed CLI + MCP tools that enforce policy, budget, guardrails, and audit on every agent action. Use when an agent needs enforcement (not advice) over LLM traffic, tool calls, memory, and workflows.
license: MIT
---

# aiZee — governed agent operations

aiZee is a policy layer for AI coding agents. It is NOT an LLM, code
generator, or CI/CD replacement — it sits on the action path and enforces
rules so agents cannot bypass them.

## When to use

- Before writing/modifying code: check policy via `aizee check <action>`.
- Before calling an LLM: route through `aizee gateway serve` (failover +
  enforced gates on the traffic path).
- When exploring a codebase: `aizee find "<need>"` and `aizee goal "<obj>"`
  map natural language to skills/workflows/steps.
- When diagnosing the environment: `aizee doctor` (CLI) or `aizee_doctor`
  (MCP) returns `verdict` + ordered `next_steps`.
- When tracking a change: `aizee spec propose <name>` creates an
  OpenSpec-style change folder (proposal/design/tasks); `aizee spec
  archive <name>` lands it.

## Command surface

| Command | Purpose |
|---|---|
| `aizee doctor [--json]` | Structured health verdict + `Run:`/`Guidance:` steps |
| `aizee check <action>` | Policy + budget pre-flight for one action |
| `aizee find <query>` | NL search over skills/workflows/tech-stack |
| `aizee goal <objective>` | Map goal → best workflow + steps |
| `aizee config show` | Masked settings snapshot |
| `aizee config apply <file> --check` | Validate a settings file (no write) |
| `aizee spec propose|changes|archive` | Change-folder lifecycle |
| `aizee gateway serve|init` | Governed LLM proxy (failover + gates) |
| `aizee models` | Model routing catalog (tiers + cost) |
| `aizee work poll` | Poll GitHub for assigned work via `gh` |
| `aizee memory ingest [--watch]` | Consume folders into memory banks |
| `aizee skill link` | Install this SKILL.md into agent harnesses |
| `aizee skill lint [--json]` | Description quality + trigger-collision report over `skills/` |
| `aizee skill scan [--json]` | Prompt-injection / exfiltration scanner for skill files |
| `aizee abstract generate|show` | L0/L1/L2 tiered context (sidecar abstracts in `abstracts/`) |
| `aizee hooks install|uninstall` | Session-start briefing + telemetry hooks for agent harnesses |
| `aizee session from-curl|from-har` | Replayable governed API session from a captured request |
| `aizee inventory [--report]` | Plain-fact install inventory (skills/memory/plugins counts) for prompt injection |
| `aizee plugin enable|disable <name>` | Toggle plugins in plugins.yaml under a serialized transaction |

## MCP tools

The MCP server (`aizee_mcp/aizee_server.py`) exposes ~40 tools.
`aizee_doctor`, `aizee_find`, and `aizee_goal` return the stable envelope
`{schema_version, ok, result, error, meta}` — branch on `error.code`
(`POLICY_DENIED`, `NEED_SETUP`, `UPSTREAM_BROKEN`, `VALIDATION_FAILED`, ...),
never on message text.

## Verification dial

`Kernel.act(..., verify="off|final|checkpoints|strict")` controls optional
extra verification layered on the mandatory gates — the six gates
(Probity → Guardian → Policy → LoopDetector → Budget → Audit) always run;
the dial only adds plan-diff and supply-chain checks on top.
