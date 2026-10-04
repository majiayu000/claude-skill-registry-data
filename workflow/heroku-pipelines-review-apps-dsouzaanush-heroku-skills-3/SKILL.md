---
name: heroku-pipelines-review-apps
description: Manage Heroku pipelines and review apps with stage-aware guardrails. Use when the agent needs to inspect or configure Heroku pipelines, connect apps to stages, promote slugs between stages, enable review apps, or reason about `app.json` behavior in Heroku review workflows.
---

# Heroku Pipelines and Review Apps

Operate multi-environment Heroku delivery flows without collapsing staging, review, and production into one step.

## Inspect before changing

Start with:

- `heroku pipelines:info <pipeline>`
- `heroku pipelines:diff -a <upstream-app>`
- `heroku apps:info -a <app> --json`
- local `app.json` and deploy docs

Use inspection to determine:

- whether a pipeline already exists
- which apps are mapped to which stages
- whether review apps are expected to inherit config or add-ons
- whether promotion is safer than a fresh deploy

## Safe workflow

1. identify the pipeline and target stage
2. inspect current stage mappings
3. review `app.json` before touching review apps
4. confirm whether the user wants promotion or a new deploy
5. apply the smallest safe change
6. verify resulting stage or review-app behavior

## Guardrails

Ask for confirmation before:

- creating or destroying a pipeline
- reconnecting apps to different stages
- enabling or disabling review apps with `heroku reviewapps:enable -p <pipeline> -a <app>` or `heroku reviewapps:disable -p <pipeline> -a <app>`
- promoting toward production

Treat production promotion as a release action, not as routine inspection.

## References

- Read `references/pipelines-review-apps.md` for command catalogs, `app.json` notes, and source links.
