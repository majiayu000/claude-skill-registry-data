---
name: skill-router
description: Route non-trivial Codex tasks to the right local execution lane and capability set. Use when Codex needs to decide between direct execution, a local skill, an enabled plugin, or an MCP/tool surface; when the user asks which skill or workflow to use; when you want to inspect the local Codex inventory; or when a task needs a compact lane + capability + verification recommendation before work begins.
---

# Skill Router

Use this skill to make Codex routing environment-aware instead of guess-based.

## Quick Start

1. Classify the task into a lane:
   - `direct`
   - `broken`
   - `build`
   - `operate`
   - `review`
   - `plan`
2. Run `scripts/scan_codex_inventory.py` to inspect local skills, plugins, and MCP servers.
3. Match the task against the most specific local capability first.
4. Return a compact recommendation using the routing contract in `references/routing-contract.md`.

## Lane Selection

| Lane | Examples | Default Reasoning | Default Thinking |
|------|----------|-------------------|------------------|
| `direct` | trivial read, one command, factual answer | fast | none |
| `broken` | bug, regression, crash, failing test, broken build | standard | think |
| `build` | new feature, component, integration, workflow | standard | think |
| `operate` | refactor, automate, configure, document, deploy | standard | none |
| `review` | code review, risk review, security review | standard | think-hard |
| `plan` | broad, ambiguous, multi-stage, scope decisions | frontier | **ultrathink** |

Escalate to `frontier` reasoning + `ultrathink` for: production incidents,
auth/permissions changes, architecture decisions where rollback is expensive.

If a task spans multiple lanes, choose the first critical lane and note the downstream chain.

## Capability Resolution

Prefer, in order:

1. repo instructions already in force
2. local Codex skills
3. enabled plugins
4. configured MCP/tool surfaces
5. direct execution

Rules:

- prefer one strong local capability over a long chain
- prefer the most specific capability over the most famous one
- fall back to direct execution if no strong local match exists
- do not search the internet for skills by default
- do not auto-install anything silently

## Inventory Scan

Use the bundled script:

```bash
python3 scripts/scan_codex_inventory.py
python3 scripts/scan_codex_inventory.py --query deploy
python3 scripts/scan_codex_inventory.py --json
```

Use the inventory scan when:

- you need to know which local capability is actually present
- multiple possible skills might match
- the task mentions a tool or platform and you want to confirm availability

## Output Contract

Always return:

- lane
- chosen capability or fallback
- reasoning tier: `fast`, `standard`, or `frontier`
- verification plan
- short notes only if needed

See `references/routing-contract.md` for the canonical shape.

## Named Chains (Optional)

If `AGENTS.md` declares saved chain sequences, check them BEFORE computing
fresh from the lane tables. Match by substring on the user's prompt; first
match wins.

```yaml
# in AGENTS.md
chains:
  - name: ship-feature
    when: ["ship the feature", "lets implement"]
    chain: writing-plans → frontend + db
    thinking: think
```

Per-step models / agents resolve from the lane tables unless `chain.model`
or `chain.thinking` overrides globally, or `steps[].model` overrides per
step.

## Dispatch Protocol — Per-Step Model Enforcement

When a chain step needs a different model than the parent session, dispatch
that step as a Codex sub-task with `model:` set explicitly. Steps that
match the parent model run inline.

```
For each step in the chain:
  IF step.model == parent_model AND not parallel-fan-out:
      → run inline
  ELSE:
      → spawn sub-task with model=<step.model>, agent=<step.agent>
  Parallel steps (`+`) launch concurrently.
```

## Thinking Depth

Each lane row carries an optional `Thinking` value: `none / think /
think-hard / ultrathink`. Pre-pend the keyword to the dispatch prompt to
allocate extended-thinking budget. Production incidents and architecture
decisions default to `ultrathink`; mechanical work to `none`.

## Codex-Specific Notes

- this skill is local-first
- this skill is for routing and orchestration, not governance
- for enterprise governance, policy, and proof of judgment, use Sentigent instead of expanding this skill into a control plane

## Resources

### `scripts/`

- `scan_codex_inventory.py`: inspect installed local Codex skills, enabled plugins, and configured MCP servers

### `references/`

- `routing-contract.md`: required output shape for recommendations
- `product-boundary.md`: product boundary and audience definition for the Codex version
