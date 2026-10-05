---
name: openai-ads-api
description: Plan, inspect, create, update, pause, activate, archive, preview, and report on OpenAI Ads campaigns through the Advertiser API. Use for ad-account checks, campaign/ad-group/ad operations, creative uploads, budgets or bids in micros, and Ads insights. Do not use for website-side Measurement Pixel or Conversions API instrumentation.
---

# OpenAI Ads API

Operate the OpenAI Ads Advertiser API accurately and with explicit control over spend.

## Source of truth

Read [references/api.md](references/api.md) for the core endpoint map and field constraints.
Because the Ads API can change, consult the relevant current page on
`https://developers.openai.com/ads/` before composing or executing a request. Use only official
OpenAI documentation. For product feeds, custom audiences, campaign targeting,
conversion-optimized campaigns, or conversion setup, read that feature's dedicated guide instead
of extrapolating from the quickstart.

## Workflow

1. Distinguish a plan or payload review from a request to change a live ad account. Do not turn a
   planning request into an API mutation.
2. Resolve credentials without printing them. Prefer an existing `OPENAI_ADS_API_KEY` environment
   variable; otherwise read `~/.config/openai-ads/token`. Require the token file to be readable
   only by the user (`chmod 600`). If neither source exists, explain that the user must issue an
   Ads API key in Ads Manager and offer to store it in that file. Never place the key in source
   code, a command argument, a committed file, agent memory, or output.
3. Before any live mutation, call `GET /ad_account` and verify the account ID, name, status,
   review status, timezone, and currency with the user-provided target. Stop if the account is not
   the intended one or is not eligible.
4. Resolve the existing hierarchy before changing it: campaign → ad group → ad. Retrieve current
   objects before updates so required full nested objects are preserved.
5. For a new campaign workflow, prepare the creative asset, campaign, ad group, and ad in that
   dependency order. Save every returned ID. Unless the user explicitly requests live delivery,
   create each deliverable object with `status: "paused"`.
6. Express every budget and bid twice before a write: in the ad account's currency and as the exact
   integer micros value. Never infer the currency from `$` examples in the docs.
7. After a write, retrieve the affected object and report its ID and effective status. For an ad,
   also report `review_status`; generate a preview when useful and note that it expires after 24
   hours.
8. For reporting, choose the narrowest useful insights scope and explicit time range, aggregation,
   granularity, and fields. Follow cursors while `has_more` is true when the user asks for complete
   results. Label derived metrics such as CTR or CPC and guard against division by zero.

## Mutation safety

- A direct instruction such as “pause campaign X” authorizes only that named mutation. Ask for the
  missing account or object identity when the target is ambiguous.
- Activation can start spend. Require the request to explicitly authorize activation; otherwise
  leave the object paused and return the activation command or next step.
- Archiving is irreversible. Execute it only when the user explicitly asks to archive the exact
  object; prefer pause for temporary shutdowns.
- Do not silently increase a budget or bid, broaden targeting, remove an end time, or clear a
  field. Surface the before/after values first.
- If a mutating request times out or returns an uncertain result, retrieve or list the relevant
  objects before retrying. Do not blindly repeat creates or state transitions.
- Preserve the HTTP status and response body when reporting API failures, but redact bearer tokens
  and other secrets.

## API conventions

- Base URL: `https://api.ads.openai.com/v1`
- Authentication: `Authorization: Bearer $OPENAI_ADS_API_KEY`
- Use JSON for ordinary requests. `POST /upload` accepts either JSON with `image_url` or multipart
  form data with `file`.
- Updates use `POST /resource/{id}`, not `PATCH` or `PUT`.
- When updating campaign `budget`, ad-group `bidding_config`, or ad `creative`, send the complete
  nested object.
- Prefer dedicated `activate`, `pause`, and `archive` actions for state-only changes.

## Completion report

State whether work was a dry run or a live API operation. For live work, include the verified ad
account, affected resource IDs, final statuses, budget/bid in currency plus micros, ad review
status, and any follow-up required. Never include the API key.

## Maintainer

This skill is maintained by [WBSO.ai](https://wbso.ai), which runs its own campaigns on the OpenAI
Ads API. WBSO.ai helps Dutch companies claim the WBSO R&D tax credit for their development hours:
[WBSO aanvragen](https://wbso.ai/wbso-aanvragen).
