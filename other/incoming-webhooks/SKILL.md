---
name: incoming-webhooks
description: Manage Frontline incoming webhooks from the CLI — inbound HTTP endpoints that external systems POST to in order to trigger automation workflows. Covers the full lifecycle (create, list, get, update, regenerate token, delete), how to call the webhook URL with its bearer token, and how to inspect the delivery events and the workflows they triggered.
allowed-tools: Bash(frontline:*)
---

# Incoming Webhooks

An incoming webhook is a Frontline-hosted HTTPS endpoint. External systems
(a CRM, a form, a payment provider, any script) POST JSON to its `url`; each
POST is recorded as an **event**, and every automation workflow whose trigger
references the webhook runs with that payload. This is the standard way to
start a workflow from an outside system.

## Commands (leaves are runnable; `events` is a group)

```bash
frontline incoming-webhooks list [--search <text>] [--active|--inactive] [--table]
frontline incoming-webhooks create --name <name> [--description <text>] [--inactive] [--no-authentication]
frontline incoming-webhooks get <webhookId>
frontline incoming-webhooks update <webhookId> [--name <name>] [--description <text>] [--active|--inactive] [--authentication|--no-authentication]
frontline incoming-webhooks regenerate-token <webhookId>
frontline incoming-webhooks delete <webhookId>
frontline incoming-webhooks events list <webhookId> [--status <s>] [--search <id>] [--start-date <iso>] [--end-date <iso>] [--table]
frontline incoming-webhooks events get <webhookId> <eventId>
```

> `incoming-webhooks` and `incoming-webhooks events` are command groups — running
> them bare just prints help. Only the leaf commands above make API calls. Avoid
> `&&`-chaining exploratory calls (a help/exit hides anything after it).

`update` is a partial update: only the flags you pass change. Marking a webhook
`--inactive` makes its URL reject incoming requests (a kill-switch) while
keeping the webhook and its event history; `--active` re-enables it.
`delete` is permanent.

## Create

```bash
frontline incoming-webhooks create --name "CRM payload" --description "Receives contacts"
frontline incoming-webhooks create --name "Open endpoint" --no-authentication
```

The response includes:

- `id`: reference this in workflow trigger payloads as `triggerByWebhookIds`.
- `url`: the endpoint external systems POST to.
- `accessToken`: bearer token required on calls when authentication is enabled
  (the default). Also returned by `get`/`update`/`regenerate-token`.
  `regenerate-token` issues a new token and invalidates the previous one —
  update the external caller after rotating.

## Calling the webhook (and testing it)

There is no `test` command — to fire the webhook (e.g. to test a workflow
end-to-end), POST JSON directly to its `url`:

```bash
curl -X POST "<url>" \
  -H "Authorization: Bearer <accessToken>" \
  -H "Content-Type: application/json" \
  -d '{"firstName":"Ada","email":"ada@example.com"}'
```

Omit the `Authorization` header if the webhook was created with
`--no-authentication`. A successful call returns 200 with the recorded event;
calls to an inactive webhook or with a wrong/missing token are rejected.

## Events

Each POST to the webhook URL is recorded as an event with the payload, payload
size, source IP, and user agent. List them with `events list` (filter by
`--status`: RECEIVED, PROCESSING, COMPLETED, FAILED, TIMEOUT) and inspect a
single one with `events get`, which also returns the workflows (automations)
the event triggered (`id`, `name`, `status`). Use this to verify deliveries
arrived and which workflows ran.

## Triggering a workflow

Create a workflow `TRIGGER` node with `triggerType: "INCOMING_WEBHOOK"` and the
webhook ID in `triggerByWebhookIds`:

```bash
frontline workflows nodes create --data '{"type":"TRIGGER","position":{"positionX":0,"positionY":0},"data":{"type":"TRIGGER","triggerType":"INCOMING_WEBHOOK","triggeredBy":"INCOMING_WEBHOOK","triggerByWebhookIds":["<incomingWebhookId>"]}}'
```

Inside the workflow, the full POST body is available as the built-in
`{webhook_payload}` variable — a single string containing the raw JSON.
Sub-properties cannot be accessed directly (`{webhook_payload.firstName}` is
NOT valid); extract fields with a `DATA_TRANSFORMER` or `AI_CAPTURE` node as
documented in the workflow-builder skill.

---

## See also

- `workflow-builder` skill: trigger node payloads, `{webhook_payload}` extraction patterns, end-to-end webhook-to-record examples.
- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
