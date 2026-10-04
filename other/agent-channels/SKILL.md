---
name: agent-channels
description: View Frontline channel integrations (WhatsApp, Instagram, Messenger) from the CLI and bind a number/account/page to an agent. Use when the user wants to see which messaging channels are connected, change which agent answers a WhatsApp number / Instagram account / Messenger page, register or disconnect a WhatsApp number, or read a WhatsApp number's business profile. Distinct from `agents settings` channel config. Does NOT connect new channels (that needs the in-app OAuth flow).
allowed-tools: Bash(frontline:*)
---

# Agent channels

Agent channels are the messaging surfaces an agent answers on: **WhatsApp** numbers, **Instagram**
accounts, and **Messenger** pages. This skill operates on **already-connected** integrations and
controls which agent each one is bound to.

This is **not** the same as `frontline agents settings <agentId> <channel>`, which configures how a
given agent _behaves_ on a channel (livechat/whatsapp/instagram/messenger appearance + behavior).
Agent channels here are the account-level integrations themselves and their agent bindings.

**Connecting a channel is not available from the CLI** — it requires the OAuth / embedded-signup
flow in the app (Meta tokens). The CLI can view connected channels, bind/unbind them to agents,
and run WhatsApp number maintenance (register / disconnect / read profile).

Requires a USER API key (same key as conversations, playbooks, knowledge bases). Output is JSON
by default; add `--table` (or `--pretty`) for a human-readable view.

## View connected channels

```bash
frontline agent-channels list            # full nested JSON (whatsapp, instagram, messenger)
frontline agent-channels list --table    # flat table: channel, targetId, label, agentId
```

In `--table` mode, `targetId` is the value you pass to the assign/update commands
(WhatsApp uses the `phoneNumberId`; Instagram/Messenger use the numeric account/page id).
`agentId` shows the currently bound agent (blank = unbound). `list` returns `null` if no
channel is connected.

## Assigning a channel to an agent

Every channel binds to exactly one agent. Use `--agent-id <id>` to bind, or `--clear` to unbind.

```bash
# Instagram account -> agent
frontline agent-channels instagram assign <instagramAccountId> --agent-id <agentId>
frontline agent-channels instagram assign <instagramAccountId> --clear

# Messenger page -> agent
frontline agent-channels messenger assign <messengerPageId> --agent-id <agentId>

# WhatsApp number -> agent (via update; integrationId + phoneNumberId)
frontline agent-channels whatsapp update <integrationId> <phoneNumberId> --agent-id <agentId>
frontline agent-channels whatsapp update <integrationId> <phoneNumberId> --clear
```

`assign` requires exactly one of `--agent-id` or `--clear`. Resolve `<agentId>` with the
`frontline-agents` skill.

## WhatsApp number maintenance

WhatsApp `update` doubles as profile editor + agent assignment. Provide only the fields you
want to change; omitting `--agent-id`/`--clear` leaves the binding untouched.

```bash
# Read the live business profile
frontline agent-channels whatsapp info <phoneNumberId>

# Edit profile fields (any subset)
frontline agent-channels whatsapp update <integrationId> <phoneNumberId> \
  --about "We reply within minutes" --website "https://example.com" \
  --email support@example.com --category OTHER

# Register the number with Meta (generates a PIN and completes registration)
frontline agent-channels whatsapp register <integrationId> <phoneNumberId>

# Disconnect a single number
frontline agent-channels whatsapp disconnect <integrationId> <phoneNumberId>
```

`<integrationId>` and `<phoneNumberId>` both come from `frontline agent-channels list`.

## Not available here

- Connecting/creating a channel (WhatsApp embedded signup, Instagram/Messenger OAuth).
- Uploading a WhatsApp profile picture (multipart upload).
- Instagram/Messenger disconnect (manage from the app).

## See also

- Resolving an agent's `<agentId>`: the `frontline-agents` skill.
- Configuring how an agent behaves on a channel: `frontline agents settings`.
- Authentication and profiles: the `auth-and-profiles` skill.
- Full reference: <https://docs.getfrontline.ai/cli>.
