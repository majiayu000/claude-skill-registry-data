---
name: platform-access
description: Use to manage how people, apps and services reach a Platform org, with machine tokens, org secrets, webhooks, and connected services such as GitHub, Notion, Google and RunPod.
---

# Access and connections

## Tokens

- `access.tokens`: active tokens with name, kind, scopes and dates. Never values.
- `access.create_token` (confirm): a new token gets only scopes the calling token has. The value is in the result once. Hand it to the person and do not keep it.
- `access.revoke_token` (confirm): revoke by id.

Give each app or agent its own token with the fewest scopes it needs.

## Secrets

- `access.secrets`: names, whether each is set, who set it when. Never values.
- `access.set_secret` (confirm) replaces a value. `access.delete_secret` (confirm) removes it.
- An app's pod env reads secrets named `app_<app>_<key>` through its manifest's `secret_env`.

Never echo a secret value, in chat or in a tool argument you show.

## Webhooks

- `access.webhooks`: destinations, the events to pick from, and the org's feeds. URLs are never returned.
- `access.save_webhook` adds or changes one. `access.test_webhook` sends a test now. `access.delete_webhook` needs confirm.

## Connections

The org's own accounts on other services. Their tools show up in the tool list under the service name, such as `github.*` or `notion.*`.

- `connections.list`: each service, its fields, and whether the org set them.
- `connections.save` (confirm) sets fields. `connections.test` checks the keys with one call.
- `connections.disconnect` (confirm) signs out of a service connected with a sign-in.
