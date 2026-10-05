---
name: ha:quick
description: Implement small Home Assistant changes without planning — add config-flow validation, update a platform, fix a config-flow step, create a config-entry migration. Use for single-file edits under 50 lines.
effort: low
---

# Quick Mode

Skip the planning ceremony. Get working code fast.

## Usage

```bash
/ha:quick Add a battery sensor to the coordinator
/ha:quick Fix the reauth flow redirect
/ha:quick Add a diagnostics dump to the integration
```

## Arguments

`$ARGUMENTS` = What to implement

## How It Differs

| Normal Mode | Quick Mode |
|-------------|------------|
| Spawn research agents | No agents |
| Create plan document | Mental model only |
| Parallel review | Optional single review |
| Multiple iterations | Single pass |

## Workflow

1. **Understand** - Read relevant files (max 3)
2. **Implement** - Write code directly
3. **Verify** - Quick typecheck + hassfest
4. **Done** - No ceremony

## Iron Laws

1. **NEVER skip verification** — run `mypy homeassistant/components/<domain>/` after every change, even in quick mode
2. **DO NOT touch files outside the stated scope** — quick mode means minimal blast radius; if a fix requires changes across multiple integrations or platforms, escalate to `/ha:plan`
3. **NEVER bypass security checks for speed** — config-flow input validation, secret handling, and no-secrets-in-logs rules apply regardless of change size
4. **UI changes ALWAYS go through the `impeccable` skill** — even in quick mode: if the change touches ha-frontend UI (Lit components, templates, styling), invoke `impeccable` first when it's in the available-skills list; if it isn't installed, prompt the user to install it before proceeding

## Rules in Quick Mode

### Still Enforced (Iron Laws)

- ✓ No custom polling loop when a `DataUpdateCoordinator` fits (PS3)
- ✓ No blocking I/O on the event loop — no sync library calls in `async def` (P4)
- ✓ Coordinator owns the fetch — entities read `coordinator.data`, no I/O in entity properties (P11)
- ✓ Security basics (validate at the config-flow boundary, never log secrets)
- ✓ Run `ruff format .`

### Skipped

- ✗ Parallel agent research
- ✗ Written plan document
- ✗ Multiple review passes
- ✗ Documentation updates

## When to Use

**Good for:**

- Bug fixes with clear solution
- Small features (<100 lines)
- Refactoring with tests
- Adding an entity / attribute to an existing platform
- Frontend (ha-frontend) tweaks

**Not for:**

- New config flows / OAuth / reauth flows
- Multi-version config-entry data migrations
- New integrations from scratch
- Architectural changes
- Anything touching security

## Quick Patterns

### Add Entity

```bash
/quick Add a battery sensor to the coordinator
```

→ `SensorEntityDescription` + entity in `sensor.py` + `strings.json` + `icons.json`

### Fix Bug

```bash
/quick Fix: sensors not updating after a cloud account reload
```

→ Find issue + fix + verify

### Add Service Action

```bash
/quick Register a "refresh" service action
```

→ voluptuous schema + handler in `services.py` + `services.yaml` + `strings.json`

## Escape Hatch

If quick mode hits complexity:

```
This needs more planning. Switching to normal mode.
Run /ha:plan [task] for full analysis.
```

## Verification

After quick implementation:

Run `mypy homeassistant/components/<domain>/`. If you changed the config-entry
data shape or bumped the entry `version`/`minor_version`, add/adjust
`async_migrate_entry` and its test. Run `ruff format .` and
`python3 -m script.hassfest --domain <domain>`, then
`pytest tests/components/<domain>/test_<module>.py` for affected tests.

## Example Session

```
User: /ha:quick Add a config-entry migration to move hostname into host

Claude:
1. Reading homeassistant/components/example/__init__.py...
2. Adding async_migrate_entry...

# homeassistant/components/example/__init__.py
async def async_migrate_entry(hass: HomeAssistant, entry: ExampleConfigEntry) -> bool:
    if entry.version == 1:
        new_data = {**entry.data}
        new_data[CONF_HOST] = new_data.pop("hostname")
        hass.config_entries.async_update_entry(entry, data=new_data, version=2)
    return True

3. Bumping VERSION in the config flow...

# homeassistant/components/example/config_flow.py
class ExampleConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 2

4. Verifying...
$ ruff format . ✓
$ mypy homeassistant/components/example/ ✓
$ python3 -m script.hassfest --domain example ✓

Done. Run `pytest tests/components/example/` to verify.
```
