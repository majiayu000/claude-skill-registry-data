---
name: esphome
description: "Applies safe ESPHome rules for YAML, lambdas, sensors, switches, relays, boot behavior, fail-safes, and validation."
---

# Skill: esphome

## Purpose

Apply safe, maintainable rules to ESPHome YAML, lambdas, sensors, switches, relays, and ESPHome integrations.

## Safety First

ESPHome often controls real hardware. Bugs are not just failed unit tests with extra plastic smell.

Be careful with:

- relays;
- heaters;
- boilers;
- pumps;
- locks;
- gates;
- fans;
- mains-connected devices;
- battery charging;
- high-current loads.

Use failsafe defaults where appropriate.

## Inspect First

Before changing ESPHome config, inspect:

- existing YAML structure;
- substitutions;
- packages/includes;
- board type;
- framework;
- pins/GPIO usage;
- IDs;
- secrets references;
- boot behavior;
- reconnect behavior;
- existing lambdas;
- Home Assistant entities linked to the node.

Do not invent pins, wiring, voltage/current limits, or board behavior.

## YAML Rules

- Preserve existing IDs unless explicitly changing them.
- Avoid duplicate entity IDs.
- Use `!secret` for sensitive values.
- Avoid hardcoded Wi-Fi credentials.
- Keep YAML structure valid.
- Prefer substitutions/packages for repeated configuration when already used.
- Avoid excessive update intervals.
- Consider flash wear.
- Keep lambdas small and readable.
- Avoid blocking lambdas.

## Boot and Failsafe Behavior

Consider:

- relay default state;
- restore mode;
- boot priority;
- Wi-Fi loss;
- API/MQTT reconnect;
- safe state after reboot;
- sensor unavailable states;
- brownouts.

For relays controlling dangerous loads, default-off is usually safer unless project requirements prove otherwise.

## Lambdas

- Keep lambdas short.
- Avoid hidden state unless necessary and documented.
- Avoid blocking delays.
- Handle NaN/unavailable values.
- Prefer named IDs and clear calculations.
- Move complex logic into custom components only when justified.

## Validation

Prefer:

```bash
esphome config <file.yaml>
esphome compile <file.yaml>
```

Only run commands that are available and appropriate for the project.

Report exact commands and results.
## Shared Cross-Ecosystem Style


Apply the shared engineering style from:

- `../../engineering/05_design_principles.md`
- `../../engineering/06_responsibility_model.md`
- `../../engineering/07_complexity_budget.md`
- `../../engineering/12_naming_bible.md`

Language-specific idioms control syntax and ecosystem details, but they must not weaken the core rules: small cohesive units, explicit boundaries, honest validation, no dumping grounds, and no fake placeholders.
