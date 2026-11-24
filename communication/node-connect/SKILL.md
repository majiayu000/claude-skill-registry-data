---
name: node-connect
description: "Diagnose a paired node's connection failures step by step."
version: 1.0.0
author: External Agent contributors, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [nodes, gateway, diagnostics, messaging]
    category: messaging
    related_skills: [telegram-client, telegram-visualize, telegram-widgets, telegram-rich-messages]
---

# Node Connect Skill

Diagnose why one paired node will not connect, then prove the fix with a fresh probe. One exact node against one exact gateway home: lock the target, classify the node, run one probe, read the first failed step, fix that step, and show the result as a connection flow in the DM. Ported from External Agent `skills/node-connect/SKILL.md`; the lanes are Hermes' own — there is no node-initiated connection, no QR code, and no browser lane here. Pairing is owner-registered and the probe is one real invoke against the node's own endpoint.

## When to Use

- The user says a node will not connect, shows as disconnected, or a pairing is stuck.
- After any pairing, token, or endpoint change, to prove the node connects again.
- When a node went stale (`connected` is false because nothing has been seen from it in 300 seconds).
- Do not use for a node that answers but returns wrong data — that is the node's own behaviour; call `nodes` invoke directly and read what it returned.
- Do not use for a gateway-wide outage — that is the gateway's problem, not one node's connection.

## Prerequisites

- The `nodes` tool is available in this conversation. It is owner-only: the telethon adapter hides it from every non-owner sender, and tenant sessions never see it. Diagnosis runs in the owner's DM.
- `telegram_client` is available for the presentation. `widget_show` routes itself: a widget in a DM, the same content as a rich message anywhere else.
- A node is identified by its id or its unique display name; a pairing request by its exact request ID.
- The node's bearer token is password-equivalent. The operator supplies the endpoint and token out of band; pass the token straight to `nodes` request and never write it anywhere else — never in chat, the diagnosis, the widget, or a file. The registry never logs it and strips it from every record it returns.

## How to Run

1. **Lock the target.** Note the profile/home, run `nodes` status and `nodes` pending, and confirm they describe the same node before changing pairing or auth.
2. **Classify the node** from status and pending: paired, pairing pending, or never paired.
3. **Run `nodes` diagnose on the node.** One probe, four steps: route → auth → pairing → reconnect.
4. **Read the first failed step and fix that step only** (see the verdict table). A failure further down the flow is not proven until the step before it passes.
5. **Re-run diagnose after the change.** Success is a fresh probe proving all four steps — an approval, a paired count, or a ping proves only one transition.
6. **Present it once** with the script below and one `telegram_client` `widget_show`. **Never retry a show**: a timeout can mean the server accepted it — a retry duplicates the delivery. Read the error first.

## Quick Reference

### Verdicts

| Verdict | Failed step | What it means | Fix |
| --- | --- | --- | --- |
| `healthy` | none | The node answers the probe | Nothing — it connects |
| `unreachable` | route, reconnect | The probe never reached the node | Check the route from the host: DNS, TLS, or the node being down |
| `auth_failed` | auth | The node rejected the token (HTTP 401/403) | Re-pair with a fresh token: new request, then approve it |
| `node_error` | reconnect | The node answered but refused the probe | Fix it on the node side, then diagnose again |
| `pairing_pending` | pairing (pending) | A request waits for approval | Approve the exact request ID |
| `not_paired` | pairing (failed) | No request exists for this node | Open a pairing request, then approve it |

### Step states

`ok`, `failed`, `pending`, `skipped`, `unknown`. A step is `skipped` when an earlier step makes it meaningless (reconnect before auth passes; reconnect before pairing exists), and `unknown` when it was never tested (auth on a node the probe never reached).

### Probe facts

- The probe is one real `device.status` invoke: `POST {endpoint}/invoke` with the node's bearer token, 10 seconds by default (`timeoutMs` overrides it).
- A node that answers refreshes `lastSeenAt`, exactly like a successful invoke — so a stale node that answers the probe is reconnected by the probe itself.
- `connected` is a liveness heuristic from `lastSeenAt` (within 300 seconds), not a socket. A stale node is not proof of a dead route until the probe fails.

## Procedure

### Lock the target

```json
{"action": "status"}
{"action": "pending"}
```

Record the profile/home, the node's id, name, platform, and endpoint, and any pending request for that name. If status and pending disagree about which node this is, stop — do not approve anything until they agree.

### Classify the node

- **Paired:** status lists it. Go to Diagnose.
- **Pairing pending:** pending lists a request with this node's name. Go to the pairing lane.
- **Never paired:** neither lists it. Go to the pairing lane with a fresh request.

### Diagnose

```json
{"action": "diagnose", "node": "phone-1"}
```

The result carries `verdict`, `steps` (route, auth, pairing, reconnect in order), the `probe` evidence (`answered`, `http_status`, `error`, `payload`), the token-stripped node record, and `next_step`. Read the first step whose state is `failed` — that is the fix. Do not act on a later step until the failed one passes.

### Paired-node lane

- **`unreachable`:** the route is the problem. The endpoint must resolve and answer from the host — check DNS, TLS, and whether the node is up. Do not re-pair: pairing is `ok`, and a new token cannot fix a route.
- **`auth_failed`:** the token is stale. Open a new pairing request with the token the node operator supplies now, then approve it. Never reuse the old token.
- **`node_error`:** the route and the token are fine; the node's own API refused the probe. The fix is on the node side — diagnose again after it.
- **`healthy` after a stale node:** the probe reconnected it. Say so plainly; nothing else changed.

### Pairing lane

```json
{"action": "pending"}
{"action": "approve", "requestId": "<exact request id>"}
```

Re-list pending immediately before the approve — retries can supersede the request. **Never approve by position, age, or similarity**: only the exact request ID, matched against the node name, platform, and endpoint the operator supplied. An approval proves pairing only. Run diagnose right after it: only a fresh probe proves the node connects.

For a node with no request at all, open one first — the operator supplies the endpoint and token out of band:

```json
{"action": "request", "name": "phone-1", "platform": "android", "endpoint": "https://node.example.com", "token": "<operator-supplied token>"}
```

Then approve the returned request ID as above.

### Present the diagnosis

Save the diagnose JSON, build the flow with the helper script, and send it once:

```bash
python skills/messaging/node-connect/scripts/node_diagnosis_flow.py diagnosis.json
```

The script prints the mermaid flow (route → auth → pairing → reconnect, each step labelled with its state) and the `widget_show` params: template `flow`, the node name in the title, the flow as `data.mermaid`, a companion carrying the verdict, the step table, and the next step, plus copy buttons for the diagnosis and — while pairing is pending — the request ID. Call `telegram_client` with `action="widget_show"` and those params, exactly once.

```json
{
  "action": "widget_show",
  "params": {
    "template": "flow",
    "title": "Node connection: phone-1",
    "data": {"mermaid": "flowchart LR\n  R[Route: ok] --> A[Auth: failed] --> P[Pairing: ok] --> C[Reconnect: skipped]"},
    "companion": "<h1>Node connection: phone-1</h1><p><b>Auth failed</b></p><p>Next: re-pair with a fresh token.</p>",
    "buttons": [{"type": "copy", "label": "Copy diagnosis", "value": "phone-1: Auth failed — re-pair with a fresh token."}]
  }
}
```

In a DM this sends the flow as an inline SVG widget (plus the companion message carrying the buttons); in a group it sends the same step table and next step as one rich message. Report the surface plainly: a group never gets a widget, by design.

## Pitfalls

- Never approve by position, age, or similarity — only the exact request ID, re-listed just before approving.
- An approval, a paired count, or a ping proves only one transition. Declare success only after a fresh diagnose made after the final change shows `healthy`.
- A stale `connected: false` is a liveness heuristic, not a route verdict — the probe decides.
- Never put the bearer token in chat, logs, the diagnosis, or the widget. The operator supplies it for the pairing request only.
- Do not mix endpoints: the probe uses the registered endpoint. A different URL is a different node — re-pair it under its own request.
- The flow widget is display-only in this version: a tap on the widget itself gets the empty answer. Put actions on the companion buttons instead of inside the widget.
- Widgets render only in **beta clients** (Android 13.2.0, iOS 13.2, macOS beta 13.1.0). Stable Telegram, Telegram Desktop, and the public Bot API do not render them yet — a reader on stable sees the message without the widget. Say so before showing one. The rich surface renders everywhere.
- Never retry a `widget_show`. A timeout can mean the server accepted it.
- A widget is not a rich message: the flow template builds both surfaces from the same data, so keep them in sync through the script — do not hand-write a second version.

## Verification

- The diagnose result is `ok` with a `verdict` from the table and `steps` listing route, auth, pairing, reconnect in order.
- The script's mermaid parses in the widget kit and the `widget_show` params build a widget within the size limits and a rich message with the same step table.
- The tool result is `ok` with `surface` naming the delivery, `template` `flow`, and a `message_id`. A `pending_confirmation` result is not a send; `widget_show` never returns one.
- In a DM with a beta client the widget renders, each step shows the state the diagnose reported, and the companion carries the verdict, the step table, the next step, and the buttons.
- In a group the rich message carries the same steps and next step.
- After a fix, a fresh diagnose (a new probe made after the change) shows `healthy`. Anything earlier is not proof.
