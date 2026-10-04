---
name: heroku-applink-connections
description: Set up and manage Heroku AppLink org connections and JWT authorizations for Salesforce or Data Cloud. Use when the agent needs to provision the Heroku AppLink add-on, install the AppLink CLI plugin, inspect AppLink connection setup, review connection prerequisites or connection state, connect Salesforce orgs, create JWT authorizations, review trusted org connection security, or reason about environment mapping for AppLink connections on Heroku.
---

# Heroku AppLink Connections

Use Heroku AppLink to establish trusted org connections and JWT authorizations without blurring them with publication workflows, publication state, or exposed endpoints.

## Start with add-on and plugin inspection

Resolve this installed skill's directory first. Do not assume the current workspace contains the skill source repository.

Run the bundled inspection helper from this skill's `scripts/` directory:

```bash
python3 /path/to/heroku-applink-connections/scripts/plugin_status.py
```

Use the output to determine:

- whether the Heroku CLI is installed
- whether the AppLink CLI plugin is installed
- whether AppLink commands are available in the current shell

## Separate connection types clearly

- Use **connections** when the goal is to establish a trusted org relationship that publication flows will later reuse.
- Use **authorizations** when app code needs to act as a specific Salesforce or Data Cloud user.
- Use this skill for connection setup, connection prerequisites, connection troubleshooting, and connection state review.

Do not use authorizations as a substitute for publish-time connections.

## Preferred setup flow

1. provision the add-on with `heroku addons:create heroku-applink -a <app>`
2. install the AppLink CLI plugin if needed with `heroku plugins:install @heroku-cli/plugin-applink`
3. confirm org environment type before connecting production, sandbox, or scratch orgs
4. create a Salesforce connection with `heroku salesforce:connect ...` or `heroku salesforce:connect:jwt ...`
5. add authorizations only when application code needs outbound Salesforce or Data Cloud access
6. verify connection state in the AppLink dashboard, CLI, or API
7. hand publication work off to `heroku-applink-publications` only after the trusted connection is healthy

## Guardrails

Ask for confirmation before:

- provisioning the AppLink add-on
- connecting a production org
- storing JWT-based credentials
- removing connections or authorizations
- mixing sandbox and production orgs on the same app tier

Follow Heroku's guidance to avoid mixing environment types. Prefer staging apps for sandbox orgs and production apps for production orgs.

## References

- Read `references/applink-connections.md` for commands, security notes, and source links.
