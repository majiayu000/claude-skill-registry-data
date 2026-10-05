---
name: cx-satisfaction-export
description: Use to export CSAT or satisfaction survey responses from a support platform into one canonical shape. Trigger for "export our CSAT data", "pull satisfaction ratings", "get survey responses out of Zendesk/Freshdesk/Gorgias/HubSpot", joining CSAT to tickets, or when a conversation export left the csat field null.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: platform
  platform: multi
---

# Exporting satisfaction responses

Every conversation export in this catalog sets `csat: null` and notes that
satisfaction is a separate resource. **This is that resource.**

It is one skill covering several platforms rather than one skill per vendor,
because the endpoints are the easy part. The hard part is that satisfaction scales
differ between platforms, and on several of them the scale is configured per
account — so there is no correct universal mapping to look up.

## The rule: normalise only where the platform fixes the scale

| Platform | Scale | Normalised? |
| --- | --- | --- |
| Zendesk | `good` / `bad` — fixed by Zendesk | **Yes.** good → 1, bad → 0 |
| Intercom | 1–5 — fixed | Yes, but already captured by `intercom-export-conversations` |
| Freshdesk | Configured per account | No. Raw value + `--scale-map` |
| Gorgias | Configured per account | No. Raw value + `--scale-map` |
| HubSpot | Configured per survey | No. Raw value + `--scale-map` |
| Front | No native CSAT | n/a |
| Five9 | Separate post-call survey report | n/a |

Where the scale is account-configurable the script emits the **raw value** plus a
distribution of what it saw, and refuses to invent a mapping. A guessed mapping
produces a number that looks like CSAT, is plotted like CSAT, and is not CSAT.
Supply `--scale-map` once you know your account's configuration and the same
export becomes normalised.

**Zendesk's `offered` and `unoffered` are not scores.** They record that a survey
was or was not sent. They are exported with `score: null` and
`is_response: false`. Mapping them to 0 fabricates dissatisfaction — a real and
common error, because they arrive in the same field as the actual scores.

## Usage

```bash
node scripts/export-satisfaction.mjs --platform zendesk --start 90d
```

**Arguments**

- `--platform <zendesk|freshdesk|gorgias|hubspot>` — required.
- `--start <when>` — ISO date, epoch seconds, or a relative window (`90d`).
- `--out <dir>` — default `./out/<platform>-satisfaction`.
- `--scale-map <path>` — JSON mapping raw values to a 0–1 fraction, e.g.
  `{"103": 1, "102": 0.75, "-103": 0}`. Values must be between 0 and 1.
- `--max-pages <n>` — stop early. Use to sample.

**Sample first and read the raw distribution.** That output is how you learn what
your account's scale actually is, which is the information you need to write the
`--scale-map`:

```bash
node scripts/export-satisfaction.mjs --platform freshdesk --start 30d --max-pages 1
```

Credentials are the same environment variables the matching conversation export
skill uses, so if you have already run one of those, this works without further
setup.

## Output

```
satisfaction.jsonl
```

| Field | Notes |
| --- | --- |
| `source` | Platform |
| `conversation_source_id` | **Join key to `conversations.jsonl`** |
| `response_source_id` | The rating's own id |
| `customer_id`, `assignee_id` | Where the platform provides them |
| `created_at` | |
| `score` | 0–1 fraction, or `null` when unmapped |
| `score_raw` | Always the platform's original value |
| `scale` | `binary` \| `account_configurable` \| `mapped` |
| `is_response` | `false` for offered-but-unanswered |
| `comment` | The verbatim, which is the actually useful part |

`conversation_source_id` is what makes this composable: join it to a canonical
conversation export and you can segment satisfaction by channel, queue, agent, or
contact driver without any per-platform code.

## What this does not give you

- **HubSpot: no conversation or contact link.** Feedback submissions carry no
  association in this export; the associations API is a separate call. Without it,
  responses cannot be joined to conversations, which limits them to a standalone
  trend.
- **Non-respondents.** This is the response set only. Response bias is the dominant
  uncertainty in any survey metric and it cannot be measured from responses alone —
  see `cx-survey-design`, which ships the diagnostic and needs the contacts that
  did *not* respond.
- **Survey definitions.** Question text, scale configuration, and send rules stay in
  the platform. You need them to interpret `score_raw`.
- **Intercom and Five9**, for the reasons in the table above.

## Present results to the user

1. **Whether the export is normalised.** If not, say so before quoting any average,
   and give the raw distribution so the user can build the scale map.
2. **Response count vs record count.** On Zendesk especially, most records may be
   `offered` rather than answered. That difference *is* the response rate.
3. **The raw distribution.** Often the most immediately useful output — it shows the
   real shape of the responses, including bimodality.
4. **That non-respondents are absent**, and that a CSAT figure without a response
   rate is not a finding.
5. **The join key**, and any platform limitation on it (HubSpot).

## Troubleshooting

**403** — satisfaction data is often gated separately from ticket read access. Check
the scope or permission before the credentials.

**404** — surveys may not be enabled on the account, or the resource is not
available on the plan.

**All records have `score: null`** — expected on a configurable-scale platform
without `--scale-map`. Read the raw distribution and write the map.

**No records at all** — check that surveys are actually being sent, and widen
`--start`. Satisfaction volume is a small fraction of contact volume.

**Scores look inverted** — your `--scale-map` may have the polarity backwards.
Freshdesk-style scales use negative numbers for dissatisfaction, which is easy to
transpose.
