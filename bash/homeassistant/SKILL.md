---
name: homeassistant
description: "Applies safe Home Assistant rules for automations, templates, integrations, entity behavior, startup states, and validation."
---

# Skill: homeassistant

## Purpose

Apply safe, explicit, maintainable rules to Home Assistant automations, scripts, templates, integrations, and configuration.

## Safety First

Do not create automations that can cause unsafe physical behavior.

Be careful with:

- heaters;
- boilers;
- locks;
- gates;
- relays;
- pumps;
- power circuits;
- battery charging;
- high-current loads;
- water valves;
- garage doors;
- alarms.

Use failsafe defaults where appropriate.

## Inspect First

Before changing Home Assistant config, inspect relevant files when present:

- `configuration.yaml`
- `automations.yaml`
- `scripts.yaml`
- `secrets.yaml` references only, not values
- packages
- blueprints
- template sensors
- existing entity IDs
- helpers/input entities
- dashboard files if relevant

Do not invent entity IDs.

Do not hardcode secrets.

## Automation Rules

- Avoid loops caused by state changes.
- Debounce noisy sensors.
- Handle `unknown` and `unavailable`.
- Use explicit conditions.
- Avoid hidden time assumptions.
- Consider restart behavior.
- Consider mode: `single`, `restart`, `queued`, `parallel`.
- Document non-obvious triggers and safety conditions.
- Avoid automations that depend on fragile friendly names.

## Templates

- Handle missing/unavailable states.
- Avoid exceptions from unavailable attributes.
- Prefer explicit defaults.
- Keep templates readable.
- Avoid complex business logic hidden in templates when a helper/script is clearer.

## Entity and Naming

- Preserve existing entity IDs.
- Avoid duplicate entity IDs.
- Use domain-meaningful names.
- Keep related automations/scripts/packages cohesive.

## Validation

Prefer actual validation when available:

```bash
ha core check
```

Or project-specific container/supervisor validation commands.

Report exact commands and results.

If validation cannot be run, explain why.
## Shared Cross-Ecosystem Style


Apply the shared engineering style from:

- `../../engineering/05_design_principles.md`
- `../../engineering/06_responsibility_model.md`
- `../../engineering/07_complexity_budget.md`
- `../../engineering/12_naming_bible.md`

Language-specific idioms control syntax and ecosystem details, but they must not weaken the core rules: small cohesive units, explicit boundaries, honest validation, no dumping grounds, and no fake placeholders.
