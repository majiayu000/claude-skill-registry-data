---
name: reddit-ads
displayName: "AdKit for Reddit Ads: Campaigns, Ad Groups, Ads and Reporting"
description: >
  Create, edit, and report on Reddit ads from an AI agent through the AdKit MCP connector:
  campaigns, ad groups, ads, carousels, account defaults, and results. Every change is saved
  as a draft that the user approves before it goes live. Use when the user wants to run,
  change, or check Reddit ads. Not for Reddit ad strategy or creative advice.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://adkit.so/features/ads-mcp/reddit
triggers:
  - reddit ads
  - reddit ads mcp
  - reddit ads manager
  - reddit campaign
  - reddit ad group
  - reddit promoted post
  - reddit ads report
  - reddit ads api
---

# Reddit Ads with AdKit

This skill tells you how to create, edit, and report on Reddit ads through AdKit. It covers the steps, not the strategy.

## Connect AdKit

AdKit is one MCP connector for Meta, Google, TikTok, LinkedIn, Microsoft, Reddit, X, and Pinterest ads.

- **Claude, ChatGPT, and most AI apps:** add a custom connector with the address `https://mcp.adkit.so`, then sign in.
- **Claude Code:** `claude mcp add --transport http adkit https://mcp.adkit.so`

For other AI apps, see how to set up the [AdKit MCP server for Reddit Ads](https://adkit.so/features/ads-mcp/reddit). If the AdKit tools are not available, tell the user how to connect. Then stop.

## What AdKit can do on Reddit

| Entity      | Actions                                                                             |
| ----------- | ----------------------------------------------------------------------------------- |
| `campaigns` | list, get, create, update                                                           |
| `ad-groups` | list, get, create, update                                                           |
| `ads`       | list, get, create, update (image, video, carousel, or an existing post)             |
| `results`   | list (account, campaign, ad group, or ad level)                                     |
| `accounts`  | list, available, connect, disconnect, update, profiles, pixels, funding-instruments |
| `drafts`    | get, publish (review your changes, then send them)                                  |

AdKit cannot delete Reddit campaigns, ad groups, or ads. Pause them instead with `status: "paused"`.

## Steps

All calls go through `adkit_manage` with `platform: "reddit"`. Before a call you have not made in this session, read its fields with `adkit_help({ path: "manage reddit <entity> <action>" })`. Do not guess field names. In this skill, `campaigns` `create` means `entity: "campaigns"`, `action: "create"`.

1. **Project:** call `adkit_projects` and get the `projectId`. Every call needs it.
2. **Account:** call `adkit_status`. If no Reddit account is connected, call `adkit_setup` with `platform: "reddit"` and give the user the link. After they sign in, use `accounts` `available`, then `accounts` `connect`.
3. **Account defaults:** find the profile, pixel, and funding instrument with `accounts` `profiles`, `accounts` `pixels`, and `accounts` `funding-instruments`. Save them with `accounts` `update`. This change applies immediately, with no draft.
4. **Build from the top down.** Each create saves a draft. For each level, do these steps before you start the next level:
   - Show the draft to the user (`drafts` `get`, or the link `https://app.adkit.so/manage/drafts?open=<draftId>`).
   - Wait for a yes. Then publish it with `drafts` `publish`.
   - Use the Reddit ID that the publish result returns as the parent of the next level. A draft ID never works as a parent ID.

   The levels, in order:
   1. **Campaign:** `campaigns` `create` with a name and an objective. Campaigns start paused, so they spend nothing.
   2. **Ad group:** `ad-groups` `create` with the `campaignId`, the budget, bidding, and targeting.
   3. **Ad:** `ads` `create` with the `adGroupId` and the creative. For an image or video: call `adkit_manage` with `entity: "media"` and `action: "request_upload_url"` (no platform). It returns an upload URL. Send the file to that URL with `PUT`. Put the returned `uploadId` in `creative.media[].id`. A video also needs a thumbnail image. AdKit sends the files to Reddit when the ad is published.

5. **Go live:** `campaigns` `update` with `status: "active"`. Publish that draft only after the user says yes. Then check with `ad-groups` `list` and `ads` `list` that the ad groups and ads are active too.
6. **Results:** `results` `list` with a `level` and a date range (`from` and `to`).

## Reddit rules

- Write support is in beta. When a write fails, read the error and its `retryable` flag. Check your drafts and the existing Reddit objects before you retry, so you do not create the same thing twice. Report unexpected failures with `adkit_feedback`.
- Campaigns start paused. Ad groups and ads start active.
- A lifetime budget on the campaign turns on campaign budget optimization: Reddit splits that one budget across the ad groups. Otherwise, put a daily budget on each ad group.
- AdKit creates the Reddit post behind each ad. Do not create posts yourself.
- Use AdKit field names (camelCase). The entities in the table above ignore raw Reddit API field names.

## Anything else in the Reddit API

For a Reddit feature that AdKit does not cover, use `entity: "platform-api-request"` with `action: "mutate"`. The action is always `mutate`, also for reads. AdKit sends the request to `https://ads-api.reddit.com/api/v3` as it is. The user must turn on Advanced Platform Access in AdKit's Agent Permissions.

- Check every path and field in the [Reddit Ads API docs](https://ads-api.reddit.com/docs/v3/).
- Writes save a draft, like any other change.
- After you use it, report the missing feature with `adkit_feedback`.

```json
{
  "projectId": "<projectId>",
  "entity": "platform-api-request",
  "action": "mutate",
  "data": {
    "platform": "reddit",
    "accountId": "<accountId>",
    "endpoint": "ad_accounts/<accountId>/campaigns",
    "method": "GET",
    "description": "List campaigns"
  }
}
```

## Other platforms

The same AdKit connector runs [Meta Ads](https://adkit.so/features/ads-mcp/meta), [Google Ads](https://adkit.so/features/ads-mcp/google), [TikTok Ads](https://adkit.so/features/ads-mcp/tiktok), [LinkedIn Ads](https://adkit.so/features/ads-mcp/linkedin), [Microsoft Ads](https://adkit.so/features/ads-mcp/microsoft), [X Ads](https://adkit.so/features/ads-mcp/x), and [Pinterest Ads](https://adkit.so/features/ads-mcp/pinterest) ads. Each platform has its own skill in this repo, for example `meta-ads` and `google-ads`.
