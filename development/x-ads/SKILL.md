---
name: x-ads
displayName: "AdKit for X Ads (Twitter Ads): Campaigns, Ad Groups, Promoted Posts and Reporting"
description: >
  Create, edit, and report on X (Twitter) ads from an AI agent through the AdKit MCP
  connector: campaigns, ad groups (line items), promoted posts, account defaults, and results.
  Every change is saved as a draft that the user approves before it goes live. Use when the
  user wants to run, change, or check X or Twitter ads. Not for X ad strategy or creative
  advice.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://adkit.so/features/ads-mcp/x
triggers:
  - x ads
  - x ads mcp
  - twitter ads
  - twitter ads mcp
  - x promoted posts
  - x ads line item
  - x ads report
  - x ads api
---

# X Ads with AdKit

This skill tells you how to create, edit, and report on X (Twitter) ads through AdKit. It covers the steps, not the strategy.

## Connect AdKit

AdKit is one MCP connector for Meta, Google, TikTok, LinkedIn, Microsoft, Reddit, X, and Pinterest ads.

- **Claude, ChatGPT, and most AI apps:** add a custom connector with the address `https://mcp.adkit.so`, then sign in.
- **Claude Code:** `claude mcp add --transport http adkit https://mcp.adkit.so`

For other AI apps, see how to set up the [AdKit MCP server for X Ads](https://adkit.so/features/ads-mcp/x). If the AdKit tools are not available, tell the user how to connect. Then stop.

## What AdKit can do on X

| Entity      | X name         | Actions                                                                             |
| ----------- | -------------- | ----------------------------------------------------------------------------------- |
| `campaigns` | Campaigns      | list, get, create, update                                                           |
| `ad-groups` | Line items     | list, get, create, update                                                           |
| `ads`       | Promoted posts | list, get, create, delete                                                           |
| `results`   |                | list (needs `from` and `to` dates)                                                  |
| `accounts`  |                | list, available, connect, disconnect, update, profiles, pixels, funding-instruments |
| `drafts`    |                | get, publish (review your changes, then send them)                                  |

## Steps

All calls go through `adkit_manage` with `platform: "x"`. Before a call you have not made in this session, read its fields with `adkit_help({ path: "manage x <entity> <action>" })`. Do not guess field names. In this skill, `campaigns` `create` means `entity: "campaigns"`, `action: "create"`.

1. **Project:** call `adkit_projects` and get the `projectId`. Every call needs it.
2. **Account:** call `adkit_status`. If no X account is connected, call `adkit_setup` with `platform: "x"` and give the user the link. After they sign in, use `accounts` `available`, then `accounts` `connect`.
3. **Account defaults:** find the profile, pixel, and funding instrument with `accounts` `profiles`, `accounts` `pixels`, and `accounts` `funding-instruments`. Save them with `accounts` `update`. This change applies immediately, with no draft.
4. **Build from the top down.** Each create saves a draft. For each level, do these steps before you start the next level:
   - Show the draft to the user (`drafts` `get`, or the link `https://app.adkit.so/manage/drafts?open=<draftId>`).
   - Wait for a yes. Then publish it with `drafts` `publish`.
   - Use the X ID that the publish result returns as the parent of the next level. A draft ID never works as a parent ID.

   The levels, in order:
   1. **Campaign:** `campaigns` `create` with a name, a budget, and `status: "paused"`. A paused campaign spends nothing.
   2. **Ad group:** `ad-groups` `create` with the `campaignId`, the objective, bidding, and targeting.
   3. **Ad:** `ads` `create` with the `adGroupId` and either `existingPostId` (promote a post that already exists) or a `creative` for a new post. Read `adkit_help({ path: "manage x ads create" })` for the media a new post can use.

5. **Go live:** `campaigns` `update` with `status: "active"`. Publish that draft only after the user says yes. Then check with `ad-groups` `list` that the ad groups are active too.
6. **Results:** `results` `list` with a `level` and a date range (`from` and `to`). X requires both dates.

## X rules

- Write support is in beta. When a write fails, read the error and its `retryable` flag. Check your drafts and the existing X objects before you retry, so you do not create the same thing twice. Report unexpected failures with `adkit_feedback`.
- A daily budget on the campaign means X spreads it across the ad groups, so leave the ad group budgets out. With only a lifetime budget on the campaign, set a budget on each ad group.
- The ad group objective is required, and its optimization goal must match it.
- An ad is the link between an ad group and a post. You cannot pause or edit an ad. Pause its ad group, or delete the ad.
- In results, the ad `platformId` is the ID of the promoted post (the link between the ad group and the post). `postId` is the post itself.
- Use AdKit field names (camelCase). The entities in the table above ignore raw X API field names.

## Anything else in the X Ads API

For an X feature that AdKit does not cover, use `entity: "platform-api-request"` with `action: "mutate"`. The action is always `mutate`, also for reads. AdKit sends the request to `https://ads-api.x.com/12` as it is. The user must turn on Advanced Platform Access in AdKit's Agent Permissions.

- X often uses `PUT` for updates. Check every path and field in the [X Ads API docs](https://docs.x.com/x-ads-api).
- Read requests run immediately, with no draft. Writes save a draft, like any other change.
- After you use it, report the missing feature with `adkit_feedback`.

```json
{
  "projectId": "<projectId>",
  "entity": "platform-api-request",
  "action": "mutate",
  "data": {
    "platform": "x",
    "accountId": "<accountId>",
    "endpoint": "accounts/<accountId>/campaigns",
    "method": "GET",
    "description": "List campaigns"
  }
}
```

## Other platforms

The same AdKit connector runs [Meta Ads](https://adkit.so/features/ads-mcp/meta), [Google Ads](https://adkit.so/features/ads-mcp/google), [TikTok Ads](https://adkit.so/features/ads-mcp/tiktok), [LinkedIn Ads](https://adkit.so/features/ads-mcp/linkedin), [Microsoft Ads](https://adkit.so/features/ads-mcp/microsoft), [Reddit Ads](https://adkit.so/features/ads-mcp/reddit), and [Pinterest Ads](https://adkit.so/features/ads-mcp/pinterest) ads. Each platform has its own skill in this repo, for example `meta-ads` and `google-ads`.
