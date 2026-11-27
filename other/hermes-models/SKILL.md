---
name: hermes-models
description: >-
  Configure Hermes model providers, relay endpoints and pins for interactive sessions, delegation or
  profiles. When a profile uses the wrong API key, a model returns 404, or reasoning effort, vision
  or image generation is wrong, verify the effective route with a real request and session record.
  Not for hermes-updates.
metadata:
  revision: "11"
  areas: "software-development"
  targets: "hermes"
  summary: "configure Hermes providers, transports and routing; prove every route with live signals, not `config get`"
  summary_zh: "配置 Hermes provider、传输与路由；用实时信号证明路由，而非 `config get`"
  kind: "entry"
---

# Hermes Models & Providers

## Gates

- Back up before changes; use `hermes config set`, not patch/write tools for protected
  `config.yaml`. For dotted IDs, use whole-map JSON and parse YAML on read-back.
- Writing `model.provider` clears `model.base_url` and `model.api_mode`; set them after the
  provider. Reorder any self-fallback in the same pass.
- **Prove the route with three signals**, never `config get`: a real one-shot, the per-home
  session row, and resolved reasoning configuration.
- `agent.reasoning_effort` is global; use per-model overrides and confirm the surface before
  aligning tiers. Test transport and effort variants before editing configs.
- Assume drift: distinguish deliberate overrides, read back every write, regenerate the
  config snapshot. Verify per-home provider, catalog and credentials before pinning; never
  accept a same-provider fallback or a green doctor as proof of vision.
- Name the routing layer first. Inventory all seven layers and every cron store for a full
  audit; do not count `no_agent` pins or infer a live harness catalog from its config.
- Use `-t clarify` for text-only probes; empty `-t` enables the full toolset. Wait on background
  generation events without blocking on foreground sleeps. Prove inertness before batch use.
- For any gateway restart, check real traffic first and obtain explicit approval; do not
  restart while another session is writing.
- Treat a provider outage as a fleet cutover. Inventory before changes, keep the old catalog
  entry, edit generator sources rather than generated homes, preserve independent routes and
  verify per surface. Back up, validate all targets, and review dry-run diffs before applying.
  Stop on unknown/empty targets or concurrent writers. Writes, restarts, commits, pushes and
  rollback require their own authorization; leave binding publication to the sync owner.

## Install-side hooks (the check is required, the script is not)

`$HERMES_HOME/scripts/*.py` in these docs names a hook the install may ship — a config snapshot
(`config-snapshot.py`), an install-facts snapshot (`snapshot-install-facts.py`), a fleet-switch adapter
(`model-switch.py`), catalog sync/smoke helpers, and the fleet verification pair
(`profile-layer-reconcile.py`, `contract-drift-check.py`). What matters is the outcome each one
verifies (the route is live, the metadata resolves, the generated layer agrees with its source), not the
filename. Resolve the command from the install or from this skill's config keys; when the install ships
none, say the check is **unavailable** instead of implying it passed.

<!-- install-root: `$HERMES_HOME` below means the install root; it defaults to `~/.hermes` -->

Substitute provider keys from your install's `providers:` block.

## When to Use

| You hear / see | Load |
|---|---|
| fleet cutover (including planning, inventory, drift checks and dry runs), or same-provider ID swap at any scope | rule 20 below |
| 换默认模型 | rules below + [model switching](references/model-switching.md) |
| 加 provider、某模型 404、`does not support the responses endpoint` | [custom providers](references/custom-providers.md) for provider shape, transport probes and reasoning budgets |
| 加 alias / 换 endpoint 或 API key / 网关认证失败 | [provider rotation](references/provider-rotation.md) before changing an alias, URL or key; `.env` edits require owner confirmation |
| Add or rotate a provider across root and profiles; verify per-home catalogs, aliases, fallbacks or account availability | [fleet provider rollout](references/fleet-provider-rollout.md); for cutovers or same-provider ID swaps, rule 20 still applies |
| "让 subagent 用便宜点的模型" | `references/delegation-routing.md` |
| "routing 机制怎么运作" / "能不能按任务自动选模型" | rules 6 + 16 + 18, `references/delegation-routing.md` |
| profile 里模型/密钥不生效、只有 root 能用 | `references/delegation-routing.md` → per-profile provider |
| 配置在 root 和 profile 之间漂移 | `references/config-drift.md` |
| "review 全部 model routing" / 审计整条路由策略 | rules 16 + 18, `references/config-drift-audit.md` |
| vision / image_gen 报错、`auto` 路由 | `references/config-drift.md` |
| 给模型声明 context_length / 元数据 | `references/provider-metadata-audit.md` |
| 某 relay 的 effort/成本/流式行为异常 | `references/model-endpoint-matrix.md` |

## Rules

1. **Transport:** probe both endpoint types before declaring a capability missing.
2. **Providers:** use top-level `providers:`, normalize `custom:` during drift checks,
   and declare each model's `context_length`.
3. **Switching the default route:** writing `model.provider` **clears** `model.base_url` / `model.api_mode`.
   Order: backup → `model.default` → `model.provider` → `model.api_mode` → `model.base_url` →
   `agent.reasoning_effort`. Takes effect on `/new` or next session start. Promoting a provider that
   already led `fallback_providers` leaves the chain starting with the new default itself — reorder
   the chain in the same pass so entry 1 is a different provider.
4. **Proof:** see the three signals below; a config echo is not live proof.
5. **Effort:** use `agent.reasoning_overrides` for per-model tiers. Read
   [config drift](references/config-drift.md) for surface differences and precedence.
6. **Delegation:** pin per profile; pin values reload on spawn. The schema is built at session
   start; never flip it mid-conversation.
   Verify a real child. For per-task paths, read [delegation routing](references/delegation-routing.md).
7. **Profiles:** provider maps and `.env` are per-home; remove inherited inline keys that win over
   `key_env`, then probe live in that home.
8. **Dotted IDs:** use whole-map JSON (not a dotted key). Verify parsed shape.
9. **Reasoning:** compare usage, not requested effort; size the token budget per relay and model.
10. **Vision:** pin root and every profile and prove each with a real image call.
11. **Drift:** classify differences before mirroring; read back and regenerate the snapshot.
12. **Text-only one-shot:** see [endpoint matrix](references/model-endpoint-matrix.md) for inert invocation.
13. **Aliases and fallbacks:** separate per-home records. Prove the chain and remove the probe alias.
14. **Bounded non-default task:** use an isolated harness CLI (`pi`, then `omp`) before `hermes chat`.
15. **Long generation:** background + notification or one event wait. On truncation, retry with a
    lower tier and explicit stop condition. See [endpoint matrix](references/model-endpoint-matrix.md).
16. **Routing layers:** session default, delegation pin, backend, cron, profile, invocation and
    fallback differ in lifetime. Instructions select a layer; they do not implement resolution.
    Report changed vs instruction-only layers. Read [delegation routing](references/delegation-routing.md).
17. **Protected config:** use `hermes config set` and verify the YAML shape.
18. **Tier policy:** fast pool for the hot path, free pool for background and at least one paired
    lane. Probe each ID before blaming routing config.
19. **Catalog scope:** resolve pins against the actual home's catalog. Probe effort before edits.
20. **Fleet cutover gate:** an outage, retirement or restore moves all affected homes and harnesses;
    an ID swap moves only live references and preserves the old ID. Keep old provider definitions,
    verify generated homes and harness effort metadata. For any fleet cutover or same-provider
    ID swap, even in a single home, read the child before planning, inventory, `--check`, or
    `--dry-run`. Re-read it after compaction. Read-only work does not require mutation approval;
    the Gates above still apply to every mutating step.

    Read `../hermes-models-cutover/SKILL.md` (relative to this skill's directory) and follow it. Do not call the Skill tool for it.

Install the parent and child into the same skills root using the catalog's generated Install row;
an update alone does not install a new skill name.

## Proof

Follow [live proof](references/model-switching.md#proof): enumerate the affected homes, harness
settings, bot bindings and roster tiers. Report uncovered homes. In each changed home get a live
reply, compare the before/after `sessions.model` rows in its own read-only database, and resolve
reasoning effort. Compare the configured provider separately: the sessions table has no provider
column. Batch per-home calls in the background with individual timeouts. Verify delegation with a
real spawn and live transcript; verify vision with one real image call per profile.

## References

- `references/model-switching.md` — switching order, three-signal proof, ghc-proxy deployment, Copilot
  fallback hygiene.
- `references/delegation-routing.md` — layer lifetimes, overrides, pool tiers and profile routing.
- `references/config-drift.md` — drift audit, lettered tier menu, reasoning-effort layers, auxiliary vision.
- `references/provider-metadata-audit.md`, `references/model-endpoint-matrix.md`,
  `references/config-drift-audit.md` — audit detail.
- Only if a script command fails (for example `uv` is not found), read [references/troubleshooting.md](references/troubleshooting.md).
- `references/cases.md` — historical cases: Copilot fallback cleanup, ghc-proxy deployment.
- `scripts/audit-routing-inventory.py` — dumps every routing layer for all homes into JSON
  and flags self-fallbacks and cron coverage.
- `scripts/audit-provider-metadata.py`, `scripts/audit-config-drift.py`,
  `scripts/probe-provider-endpoint.sh` — audit scripts and endpoint probes; `templates/ghc-proxy.service` — unit template.
