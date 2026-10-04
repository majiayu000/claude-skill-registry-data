---
name: heroku-slack-agents
description: Build and deploy Slack agents and bots on Heroku with an inspection-first workflow. Use when the agent needs to review or deploy a Slack Bolt for JavaScript app on Heroku, choose between HTTP Request URLs and Socket Mode, prepare a Procfile and env vars, configure Slack app manifests or request URLs, or verify Slack bot operations on Heroku.
description: Build and deploy Slack Bolt for JavaScript or TypeScript agents on Heroku with an inspection-first workflow. Use when the agent needs to review or deploy a Slack Bolt JS or TS app on Heroku, choose between HTTP Request URLs and Socket Mode, prepare a Procfile and env vars, configure Slack app manifests or request URLs, or verify Slack bot operations on Heroku.
---

# Heroku Slack Agents

Build and deploy Slack Bolt JavaScript or TypeScript agents on Heroku without assuming that every project should use the same Slack transport or Heroku process model.

## Start with inspection

Resolve this installed skill's directory first. Do not assume the current workspace contains the skill source repository.

Run the bundled helper from this skill's `scripts/` directory:

```bash
python3 /path/to/heroku-slack-agents/scripts/project_snapshot.py
```

Use the output to identify:

- whether the Heroku CLI is installed and authenticated
- whether the repo appears to use `@slack/bolt` in a JS or TS codebase
- whether a `Procfile` already exists and whether it declares `web` or `worker`
- whether the repo already references `SLACK_SIGNING_SECRET`, `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, or `/slack/events`
- whether a Slack manifest file already exists

If the repo does not look like a Bolt JS or TS app, stop and say that this skill is the wrong fit rather than forcing the Heroku Bolt workflow onto another Slack stack.

## Choose the Slack transport intentionally

For Heroku-hosted production apps, prefer HTTP Request URLs when the app needs a stable public endpoint:

- distributed apps or Slack Marketplace paths
- slash commands, interactivity, and Events API over HTTPS
- a normal Heroku `web` dyno that listens on `process.env.PORT`

Use Socket Mode when the app should avoid public inbound Slack Request URLs and a worker process is acceptable:

- internal bots or development-first setups
- a `worker` dyno instead of a `web` dyno
- `SLACK_APP_TOKEN` in addition to the bot token

Do not mix the two casually. Confirm the intended transport before changing process types, app manifest settings, or Heroku scaling.

## Preferred workflow

1. inspect the repo and detect whether this is a Bolt JS or TS app or another Slack stack
2. confirm whether the deployed app should use HTTP Request URLs or Socket Mode
3. verify the startup contract:
   - HTTP mode needs a `web` process and port binding
   - Socket Mode usually needs a `worker` process instead
4. confirm required Heroku config var names before deployment:
   - HTTP: `SLACK_SIGNING_SECRET`, `SLACK_BOT_TOKEN`
   - Socket Mode: `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, and often `SLACK_SIGNING_SECRET`
   - do not dump all app config vars into the transcript just to check presence
5. deploy with the existing Heroku app workflow instead of inventing a parallel one:
   - `heroku git:remote -a <app>`
   - `git push heroku <branch>:main`
6. scale only the correct process type:
   - `heroku ps:scale web=1 -a <app>` for HTTP
   - `heroku ps:scale worker=1 -a <app>` for Socket Mode
7. if using HTTP, update Slack configuration to the deployed `https://<app>.herokuapp.com/slack/events` URL for:
   - Events API request URL
   - Interactivity request URL
   - slash command request URLs that should hit the same receiver
8. verify with bounded logs, app info, and one harmless Slack event or command

## Guardrails

Ask for confirmation before:

- creating a new Heroku app for a Slack bot
- changing a Slack app manifest, bot scopes, or installed app settings
- rotating or replacing Slack credentials
- switching between HTTP and Socket Mode
- scaling a new process type or disabling the currently serving process

Never print Slack tokens or signing secrets into logs or summaries. If the framework is Bolt, rely on Bolt's request verification instead of bypassing signature checks.

## References

- Read `references/slack-agent-workflows.md` for transport selection, Procfile examples, manifest fields, security notes, and source links.
