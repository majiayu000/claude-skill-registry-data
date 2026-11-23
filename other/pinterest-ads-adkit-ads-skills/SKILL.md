---
name: pinterest-ads
displayName: "AdKit for Pinterest Ads: Campaigns, Ad Groups, Ads and Reporting"
description: >
  Read and change Pinterest ads from an AI agent through the AdKit MCP connector: campaigns,
  ad groups, ads, and reporting through the official Pinterest API v5. Every change is saved
  as a draft that the user approves before it goes live. Use when the user wants to run,
  change, or check Pinterest ads. Not for Pinterest ad strategy or creative advice.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://adkit.so/features/ads-mcp/pinterest
triggers:
  - pinterest ads
  - pinterest ads mcp
  - pinterest ads manager
  - pinterest campaign
  - pinterest ad group
  - pinterest ads report
  - pinterest ads api
---

# Pinterest Ads with AdKit

This skill tells you how to read and change Pinterest ads through AdKit. It covers the steps, not the strategy.

AdKit connects Pinterest ad accounts and sends your requests to the official Pinterest API v5. AdKit has no `campaigns`, `ad-groups`, or `ads` entities for Pinterest yet, so you write Pinterest API requests directly.

## Connect AdKit

AdKit is one MCP connector for Meta, Google, TikTok, LinkedIn, Microsoft, Reddit, X, and Pinterest ads.

- **Claude, ChatGPT, and most AI apps:** add a custom connector with the address `https://mcp.adkit.so`, then sign in.
- **Claude Code:** `claude mcp add --transport http adkit https://mcp.adkit.so`

For other AI apps, see how to set up the [AdKit MCP server for Pinterest Ads](https://adkit.so/features/ads-mcp/pinterest). If the AdKit tools are not available, tell the user how to connect. Then stop.

The user must also turn on Advanced Platform Access in AdKit's Agent Permissions. Without it, the requests below fail.

## What AdKit can do on Pinterest

- **Accounts:** `accounts` list, available, connect, disconnect.
- **Campaigns, ad groups, ads, and analytics:** through Pinterest API requests under `ad_accounts/<accountId>/`.
- **Reads** (`GET`) run immediately, with no draft. **Writes** (`POST`, `PATCH`) save a draft.
- **Blocked:** billing, business access, Pins, boards, and user-level resources. You cannot create a Pin. An ad must use a Pin that already exists, so ask the user for its Pin ID.

## Steps

In this skill, `accounts` `connect` means an `adkit_manage` call with `entity: "accounts"` and `action: "connect"`.

1. **Project:** call `adkit_projects` and get the `projectId`. Every call needs it.
2. **Account:** call `adkit_status`. If no Pinterest account is connected, call `adkit_setup` with `platform: "pinterest"` and give the user the link. After they sign in, use `adkit_manage` with `platform: "pinterest"`: `accounts` `available`, then `accounts` `connect` with the `accountId` and `integrationId` from the `available` result.
3. **Read** what exists with `GET` requests. The request format is in How to write a request, below.
4. **Change** things with `POST` (create) or `PATCH` (update) requests. Each one saves a draft.
5. **Review:** `adkit_manage` with `entity: "drafts"`, `action: "get"`, or give the user the link `https://app.adkit.so/manage/drafts?open=<draftId>`. Show them what will change.
6. **Publish:** `drafts` `publish`, only after the user says yes.

To build a new campaign, go from the top down: campaign, then ad group, then ad. Publish each level before you create the next one, and use the ID that Pinterest returns as the parent. A draft ID never works as a parent ID.

## How to write a request

Every request is one `adkit_manage` call:

```json
{
  "projectId": "<projectId>",
  "entity": "platform-api-request",
  "action": "mutate",
  "data": {
    "platform": "pinterest",
    "accountId": "<accountId>",
    "endpoint": "ad_accounts/<accountId>/campaigns",
    "method": "GET",
    "description": "List campaigns"
  }
}
```

- `endpoint` is a path relative to `https://api.pinterest.com/v5`. It must start with `ad_accounts/<accountId>/`.
- `action` is always `mutate`, also for reads.
- `description` is required. The user sees it when they review the draft.
- `payload` holds the query fields for a `GET`, or the request body for a `POST` or `PATCH`.
- `POST` and `PATCH` go to the collection path (for example `.../campaigns`) and take an array of objects, even for one item.
- Check every field and value in the [Pinterest API v5 reference](https://developers.pinterest.com/docs/api/v5/). Do not use AdKit field names here.

## Examples

Only the `data` part changes. These follow the Pinterest API v5 specification.

**Account performance by day.** `columns` is a comma-separated string. `start_date` cannot be more than 90 days ago.

```json
{
  "platform": "pinterest",
  "accountId": "<accountId>",
  "endpoint": "ad_accounts/<accountId>/analytics",
  "method": "GET",
  "payload": {
    "start_date": "2026-11-01",
    "end_date": "2026-11-07",
    "granularity": "DAY",
    "columns": "SPEND_IN_DOLLAR,IMPRESSION_1,CLICKTHROUGH_1,CTR"
  },
  "description": "Daily spend, impressions, and clicks for 1 to 7 Nov"
}
```

**Create a paused campaign.** `ad_account_id`, `name`, and `objective_type` are required.

```json
{
  "platform": "pinterest",
  "accountId": "<accountId>",
  "endpoint": "ad_accounts/<accountId>/campaigns",
  "method": "POST",
  "payload": [
    {
      "ad_account_id": "<accountId>",
      "name": "Holiday traffic",
      "objective_type": "CONSIDERATION",
      "status": "PAUSED"
    }
  ],
  "description": "Create the paused campaign Holiday traffic"
}
```

**Pause a campaign.** An update needs `ad_account_id` and `id`.

```json
{
  "platform": "pinterest",
  "accountId": "<accountId>",
  "endpoint": "ad_accounts/<accountId>/campaigns",
  "method": "PATCH",
  "payload": [
    { "ad_account_id": "<accountId>", "id": "<campaignId>", "status": "PAUSED" }
  ],
  "description": "Pause campaign <campaignId>"
}
```

## Pinterest rules

- Structure: campaign, then ad group, then ad. Each ad promotes one existing Pin (`pin_id`).
- Money fields are in micro-currency: 1,000,000 equals 1 unit of the account's currency.
- With campaign budget optimization, Pinterest splits one campaign budget across the ad groups. Set `daily_spend_cap` or `lifetime_spend_cap` on the campaign, never both. Without it, set the budget on each ad group.
- A successful response does not mean that Pinterest created every object. After a create, read the object with a `GET`.
- If the user needs something AdKit blocks, tell them, and report it with `adkit_feedback`.

## Other platforms

The same AdKit connector runs [Meta Ads](https://adkit.so/features/ads-mcp/meta), [Google Ads](https://adkit.so/features/ads-mcp/google), [TikTok Ads](https://adkit.so/features/ads-mcp/tiktok), [LinkedIn Ads](https://adkit.so/features/ads-mcp/linkedin), [Microsoft Ads](https://adkit.so/features/ads-mcp/microsoft), [Reddit Ads](https://adkit.so/features/ads-mcp/reddit), and [X Ads](https://adkit.so/features/ads-mcp/x) ads. Each platform has its own skill in this repo, for example `meta-ads` and `tiktok-ads`.
