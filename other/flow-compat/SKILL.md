---
name: flow-compat
description: Route supported legacy PWDEV Code command intent to canonical PWDEV Flow skills. Use when the user mentions old /pwdev-code:* commands, asks for PWDEV Code compatibility, or wants to adopt an existing .planning workspace without losing history.
---

# Route PWDEV Code Intent to PWDEV Flow

Read [migration](../../references/migration.md) before routing legacy initialization or project adoption. Read [fleet](../../references/fleet.md) and [delegation](../../references/delegation.md) before routing their respective operational commands.

## Supported routing

| Legacy intent | Canonical skill |
|---|---|
| `init`, `session` | `$flow-init` |
| `quick` | `$flow-quick` |
| `discover` | `$flow-discover` |
| `design` | `$flow-design` |
| `plan` | `$flow-plan` |
| `execute` | `$flow-execute` |
| `review` | `$flow-review` |
| `verify` | `$flow-verify` |
| `product` | `$flow-product` |
| `memory` | `$flow-memory` |
| `simplify` | `$flow-simplify` |
| `health` | `$flow-health` |
| `maintenance` | `$flow-maintenance` |
| `audit` | `$flow-audit` |
| `fleet` | `$flow-fleet` |
| `delegate` | `$flow-delegate auto` |
| `codex` | `$flow-delegate` with explicit provider `codex` |
| `opencode` | `$flow-delegate` with explicit provider `opencode` |
| `kimi` | `$flow-delegate` with explicit provider `kimi` |
| `gemini` | `$flow-delegate` with explicit provider `gemini` |
| `kiro` | `$flow-delegate` with explicit provider `kiro` |

## Procedure

1. Parse only the legacy command name and user-supplied arguments. Use automatic provider selection only for `delegate`; preserve the explicit provider for provider-named routes.
2. Report `ROUTE: <legacy> -> <canonical>`.
3. Follow the canonical skill completely, including its inspection, safety, approval, artifact, and verification rules.
4. Keep all new portable and operational state under `.planning/flow/`; never translate Flow output back into `.planning/fleet`, `.planning/delegation`, or any other legacy layout.
5. When `init` or `session` finds `.planning/config.json` without `.planning/flow/config.json`, invoke the `$flow-init` migration route and stop for approval after the read-only plan.

## Constraints

- Compatibility never expands user authorization or bypasses canonical approval gates.
- Do not migrate files, enable audit, change Git, launch a fleet, install tools, or call external providers merely because a legacy command previously did so. Follow the routed skill's exact confirmation gates.
- Do not reuse legacy fleet bookkeeping, Docker projects, tmux sessions, branches, delegation output, or locks.
- Do not create one-off aliases or hidden compatibility state.

## Output

Return `ROUTE`, `COMPATIBILITY: SUPPORTED`, the canonical skill result, and `NEXT`.
