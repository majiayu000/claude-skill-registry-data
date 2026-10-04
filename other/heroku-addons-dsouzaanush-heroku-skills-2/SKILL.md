---
name: heroku-addons
description: Manage Heroku add-on resources and attachments safely. Use when the agent needs to create, inspect, plan, attach, detach, upgrade, wait on, open, or destroy Heroku add-ons, or reason about attachment aliases, shared resources, config-var side effects, and add-on lifecycle guardrails.
---

# Heroku Add-ons

Use this skill for generic add-on lifecycle management that is broader than any one specialized service.

## Read-only-first flow

Start with:

- `heroku addons:info <addon>`
- `heroku addons:plans <service>`
- `heroku addons:open <addon>` when the user needs vendor console access

Use inspection to determine:

- which resource is being managed
- which app attachments already exist
- whether the operation should happen at the resource level or attachment level

## Resource and attachment model

Keep these distinctions explicit:

- `addons:create` creates a resource
- `addons:attach` attaches an existing resource to an app, often creating config vars
- `addons:detach` removes an attachment but may leave the underlying resource running
- `addons:destroy` destroys the resource itself

Prefer attachments and aliases when the goal is controlled sharing rather than a new resource.

## Confirm-first operations

Ask for confirmation before:

- `addons:create`
- `addons:attach`
- `addons:detach`
- `addons:upgrade`
- `addons:destroy`

Call out config-var side effects and aliasing behavior before executing attachment changes.

## References

- Read `references/addons-lifecycle.md` for aliasing, sharing behavior, and source links.
