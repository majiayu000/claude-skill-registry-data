---
name: idmp-event
description: "IDMP event skill for listing, searching, confirming, resending, annotating, and reading event context through the real unacknowledged-event workflow."
metadata:
  author: "TaosData"
  version: "0.4.0"
  owner_team: "AI"
  requires:
    bins:
      - idmp-cli
  cliHelp: "idmp-cli event --help"
---

# event

**Read [`../idmp-shared/SKILL.md`](../idmp-shared/SKILL.md) first.**

**Before any write:** Follow the [🛑 Destructive op confirmation protocol](../idmp-shared/SKILL.md#-destructive-op-confirmation-mandatory). Read-only commands stay read-only here, but delete / write / patch flows still require the shared yes-gate.


## Recommended shortcuts

| Shortcut | Purpose |
|----------|---------|
| `+list` | List events with paging and element filters. |
| `+search` | Search events globally. |
| `+count` | Read the count of unacknowledged events. |
| `+get` | Read one event in detail. |

## Recommended references

- [`event read flows`](references/event-read-flows.md)
- [`../idmp-workflow-alert-create/SKILL.md`](../idmp-workflow-alert-create/SKILL.md)
- [`../idmp-workflow-alert-debug/SKILL.md`](../idmp-workflow-alert-debug/SKILL.md)

## Missing context to resolve first

| Context | Why it must be resolved before mutation |
| --- | --- |
| Failure boundary | Decide whether you are debugging missing event generation, missing delivery, or both. |
| Event scope | You need an `eventId`, an `analysisId`, or a narrow enough search scope to avoid acting on the wrong event. |
| Operator intent | Confirm whether acknowledgement, resend, or annotation is actually allowed in this session. |
| Verification window | Decide which reread window and filters will prove the event was found, acknowledged, or retried. |

## Constrained live behaviors

- `status=Unack` alone is not always reliable in shared environments; when you already know the producer analysis, reread events with `analysisId` before deciding the event is missing.
- Capture event detail and context before you run `confirm` or `resend`; both commands have operator-visible side effects.
- `resend` retries delivery only. It does not acknowledge or recreate the event.
- A successful `resend` does not guarantee a fresh top-level notification-history row. Delivery history is detail-based, can lag, and can be throttled by the event's minimum notification interval.
- Shared environments can surface stale events whose `event events items` call fails because the linked analysis was already deleted; try a fresher event before assuming the CLI path is wrong.
- Create alert rules from [`../idmp-workflow-alert-create/SKILL.md`](../idmp-workflow-alert-create/SKILL.md), not from this event read workflow.

## Product behavior to preserve

- Start with the unacknowledged-event path: count, list/search, detail, context, confirm or resend, then annotations.
- Treat confirm and batch confirm as the real acknowledgement workflow.
- Use `items` to inspect event context before retrying notifications.
- Use `annotations` to keep operator notes with the event.
- Create alert rules from alert workflows, not from the event read workflow.

## Key commands

```bash
idmp-cli schema event.count.list
idmp-cli event count list

idmp-cli schema event.events.list
idmp-cli event events list --params '{"current":1,"size":20}'

idmp-cli event events search --params '{"keyword":"overcurrent","current":1,"size":20}'
idmp-cli event events get --params '{"eventId":123}'
idmp-cli event events items --params '{"eventId":123}'

idmp-cli event events confirm --ack-risk --params '{"eventId":123}'
idmp-cli event events confirm --dry-run --ack-risk --params '{"eventId":123}'
idmp-cli event confirm create --ack-risk --data '[123,456]'
idmp-cli event confirm create --dry-run --ack-risk --data '[123,456]'
idmp-cli event events resend --dry-run --ack-risk --params '{"eventId":123}'
idmp-cli event annotations list --params '{"eventId":123}'
```

## Exception and failure handling

- If an event disappears from the unacknowledged view after confirm, treat that as expected acknowledgement behavior rather than data loss.
- If `resend` succeeds, expect notification delivery to retry only; it does not acknowledge or rewrite the event.
- If `resend` succeeds but no fresh history row appears, widen the notification-history reread and consider notification throttling before assuming the retry did nothing.
- If `items` or `annotations` is empty, continue with event detail and notification checks instead of repeating confirm/resend blindly.
- If confirm or resend fails, stop retrying and inspect detail, context, and notification history before the next action.
- If list results look noisy, narrow the workflow with count, search, and detail rather than acknowledging from a broad page.

## Validation scenarios

1. Start the unacknowledged workflow with `idmp-cli schema event.count.list` and `idmp-cli event count list`.
2. Read the current queue with `idmp-cli event events list --params '{"current":1,"size":20}'` and `idmp-cli event events search --params '{"keyword":"overcurrent","current":1,"size":20}'`.
3. Inspect one event with `idmp-cli event events get --params '{"eventId":123}'` and `idmp-cli event events items --params '{"eventId":123}'`.
4. Acknowledge a single event with `idmp-cli event events confirm --ack-risk --params '{"eventId":123}'`, then run batch acknowledgement with `idmp-cli event confirm create --ack-risk --data '[123,456]'` or preview it first with `--dry-run`.
5. Preview follow-up actions with `idmp-cli event events resend --dry-run --ack-risk --params '{"eventId":123}'` and `idmp-cli event annotations list --params '{"eventId":123}'`.
