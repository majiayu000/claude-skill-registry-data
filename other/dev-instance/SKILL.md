---
name: ha:dev-instance
description: "Home Assistant dev instance runtime tools — debugging, smoke testing, live state inspection, registry inspection, log analysis. Use when verifying integration behavior against a running Home Assistant instance."
effort: low
user-invocable: false
---

# Home Assistant Dev Instance

Runtime intelligence for Home Assistant integrations via a local dev instance
(`hass -c config`). Prefer exercising the integration through the real core
APIs of a running instance — reload the config entry, call its service
actions, watch the log — over guessing runtime behavior from source alone.

## Iron Laws — Never Violate These

1. **DEV ONLY** — Never debug against a production or home instance with real devices/data. The dev instance's `config/` is disposable; treat it that way
2. **PREFER THE DEV INSTANCE OVER GUESSING** — reloading the entry and reading `config/home-assistant.log` > speculating about setup behavior; Developer Tools → Actions > a throwaway script poking the library directly
3. **CHECK AVAILABILITY FIRST** — confirm `script/setup` has been run (venv present) and `config/configuration.yaml` exists (created on first `hass -c config` run), or a devcontainer is available
4. **`.storage` IS READ-ONLY** — inspect `config/.storage/*` registries with Read/jq only; NEVER hand-edit them (core holds registries in memory and overwrites the files — edits corrupt or silently vanish). https://developers.home-assistant.io/docs/entity_registry_index
5. **EXACT VERSIONS** — the venv's `site-packages/<pkg>` reflects YOUR checkout's `requirements` pins (manifest.json for integration libraries), not latest — point docs lookups at the installed version, not the PyPI "latest" tab

## Quick Reference

| Task | Dev instance | Fallback |
|------|--------------|----------|
| Get docs | Read `.venv/lib/python*/site-packages/<pkg>/` or `https://pypi.org/pypi/<pkg>/json` | `WebFetch developers.home-assistant.io` (ha-docs-fetcher skill) |
| Exercise code | Developer Tools → Actions (call the service), reload the config entry | `python3 -m homeassistant --script check_config -c config` |
| Evaluate expressions | Developer Tools → Template: `{{ states('sensor.x') }}` | Read the entity source directly |
| Inspect live state | Developer Tools → States (filter by domain) | `grep '<domain>' config/home-assistant.log` |
| Find source | `grep -rn "class .*Coordinator" homeassistant/components/<domain>` | `grep -rn "async_setup_entry"` |
| Inspect DOM (Lit) | Browser devtools — select the `ha-*` custom element, inspect its properties | Manual browser inspection |
| List entities/registries | `jq` over `config/.storage/core.entity_registry` (READ-ONLY) | Developer Tools → States |
| Read logs | `tail -f config/home-assistant.log` | Settings → System → Logs in the UI |

## Detection

```bash
# Mirrors hooks/scripts/detect-hass-dev.sh (SessionStart) — file-based, because
# the dev instance is started on demand, not an always-on endpoint
[ -f config/configuration.yaml ]        # ✓ dev instance initialized
[ -f .devcontainer/devcontainer.json ]  # ○ devcontainer tasks available, no config/ yet
[ -d .venv ]                            # script/setup has been run (venv present)
```

The SessionStart hook reports one of three core-checkout states: "✓ HA dev
instance config detected (config/)", "○ Devcontainer detected but no config/
dir", or "○ Core checkout without a dev instance". For custom integrations it
checks for a `configuration.yaml` next to `custom_components/`; for
ha-frontend it points at `yarn develop` + a core instance with
`frontend: development_repo`.

## Essential Patterns

### Smoke-Test an Integration Immediately

```text
# Against the running dev instance (hass -c config)
1. Settings → Devices & Services → Add Integration → <name>   (UI config flow)
2. Developer Tools → States — filter by the domain, verify entities + values
3. grep -i "error\|warning" config/home-assistant.log | tail -20
```

### Verify a Config Entry Migration

```bash
# READ-ONLY inspection of the config entry store after a version bump
jq '.data.entries[] | select(.domain=="<domain>")
    | {version, minor_version, unique_id, source}' \
  config/.storage/core.config_entries
```

### Debug a Lit Component (ha-frontend, with the element handle from devtools)

```js
// Browser devtools console — reactive state lives directly on the element
// instance; there's no separate process to attach to.
const el = document.querySelector('home-assistant').shadowRoot
  .querySelector('home-assistant-main');  // walk shadow roots to your ha-* element
el.shadowRoot.innerHTML;     // rendered output
Object.keys(el).filter(k => !k.startsWith('_')); // reactive property names
el.hass;                     // the hass object every ha-* component receives
```

## Setup Requirements

```bash
# Core checkout — https://developers.home-assistant.io/docs/development_environment
script/setup                    # creates .venv (uv), installs deps + prek hooks
source .venv/bin/activate
hass -c config                  # config/ is created on first run; UI at localhost:8123
hass -c config --debug          # verbose startup + debug diagnostics
```

```bash
# Devcontainer: use the preconfigured "Run Home Assistant Core" task
# (postCreateCommand already ran script/setup; F5 debugging works out of the box)

# Custom integration repo without a core checkout:
pip install homeassistant && hass -c config   # symlink custom_components into config/
```

```yaml
# config/configuration.yaml — debug logging for the integration under work
# https://www.home-assistant.io/integrations/logger/
logger:
  default: warning
  logs:
    homeassistant.components.<domain>: debug
```

## Reliability Guards

**Worktree/port check (FIRST, in multi-worktree setups)**: only one instance
can bind port 8123 — a second `hass` in another worktree fails or you end up
inspecting the wrong one. Before trusting any observation, confirm the running
process belongs to THIS checkout: the log's first lines print the config
directory path, and `ps aux | grep 'hass -c'` shows which checkout launched it.

**Registry introspection BEFORE acting**: never guess entity IDs or unique
IDs. Check Developer Tools → States (or jq the entity registry) before writing
service calls or assertions against entities you haven't confirmed this
session. A guessed-entity_id failure costs more than the lookup.

**Output-size guard**: runtime output is unbounded. Always cap it —
`tail -n 100` / `grep -i error` on `config/home-assistant.log`, `jq` filters
on `.storage` files (never `cat` a whole registry), state filters in
Developer Tools. Re-query narrower rather than dumping wide.

**UI fallback**: if you can't reach the UI at localhost:8123, don't stall —
verify server-side instead: `config/home-assistant.log` for setup results,
`.storage` for registry effects, `python3 -m homeassistant --script
check_config -c config` for config validity, or a pytest run with the `hass`
fixture. If the instance won't even boot, safe mode loads core without custom
integrations (https://www.home-assistant.io/docs/configuration/troubleshooting/).

**QA walkthrough pattern**: after a feature completes, run a short checklist
against the dev instance: add (or reload) the config entry, fetch the new
entities' states, call the main service action, tail the log for errors.
Report each step's pass/fail — not just "smoke test passed".

## Proactive Runtime Checks

Don't just use the dev instance reactively. **Query runtime state at
workflow checkpoints** automatically:

- **After code edits**: restart/reload and tail `config/home-assistant.log` (catch setup crashes — ConfigEntryNotReady loops, ImportError, "Detected blocking call" warnings)
- **After features complete**: UI-flow smoke test (behavioral check)
- **Before planning**: jq the config-entry + entity registries (concrete context)
- **When investigating**: Auto-capture log errors before asking user
- **Frontend UI bugs**: inspect `ha-*` element state via browser devtools before editing components

See `${CLAUDE_SKILL_DIR}/references/proactive-patterns.md` for full integration points.

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/proactive-patterns.md` - Push-like runtime patterns at workflow checkpoints
- `${CLAUDE_SKILL_DIR}/references/tool-examples.md` - Complete tool usage examples
- `${CLAUDE_SKILL_DIR}/references/validation-checklist.md` - Runtime validation patterns
