---
name: heroku-config-vars
description: Manage Heroku config vars safely across environments. Use when the agent needs to inspect, compare, set, remove, or audit Heroku config vars, check `.env` parity, or reason about runtime versus build-time configuration on Heroku.
---

# Heroku Config Vars

Manage configuration without treating variable changes as harmless.

## Start with inspection

Inspect the current state before proposing edits:

- `heroku config -s -a <app>` when the user explicitly wants a full key inventory
- `heroku config:get <KEY> -a <app>` for focused checks
- local `.env`, `.env.example`, or deployment docs for expected parity

Assume that changing config vars may create a new release and restart dynos.

## Safe workflow

1. identify the target app and environment
2. inspect only the keys or inventory that are actually needed
3. compare with local expectations
4. group related changes so the user can approve them together
5. apply only the approved keys
6. verify the resulting release and app behavior

Prefer `config:set` for explicit updates and `config:unset` only with confirmation.

## Modeling guidance

- Keep secrets out of command history when possible.
- Prefer targeted `config:get` checks over broad config dumps when the task only concerns a few variables.
- Treat build-time variables and runtime variables as separate concerns.
- Do not paste secret values back into summaries unless the user explicitly needs them.
- Explain whether a variable is expected to affect build output, release behavior, or runtime behavior.

## Guardrails

Ask for confirmation before:

- adding new secrets
- changing production config
- unsetting existing keys
- bulk updates that could affect multiple dynos or review apps

## References

- Read `references/config-vars.md` for command catalogs, comparison patterns, and source links.
