---
name: linkedin-ads
displayName: "AdKit for LinkedIn Ads: Campaign Groups, Campaigns, Ads, Targeting and Reporting"
description: >
  Create, edit, and report on LinkedIn ads from an AI agent through the AdKit MCP connector:
  campaign groups, campaigns, ads, targeting search, media upload, and results. Every change
  is saved as a draft that the user approves before it goes live. Use when the user wants to
  run, change, or check LinkedIn ads. Not for LinkedIn ad strategy or creative advice.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://adkit.so/features/ads-mcp/linkedin
triggers:
  - linkedin ads
  - linkedin ads mcp
  - linkedin campaign manager
  - linkedin campaign group
  - linkedin sponsored content
  - linkedin ads targeting
  - linkedin ads report
  - linkedin ads api
---

# LinkedIn Ads with AdKit

This skill tells you how to create, edit, and report on LinkedIn ads through AdKit. It covers the steps, not the strategy.

## Connect AdKit

AdKit is one MCP connector for Meta, Google, TikTok, LinkedIn, Microsoft, Reddit, X, and Pinterest ads.

- **Claude, ChatGPT, and most AI apps:** add a custom connector with the address `https://mcp.adkit.so`, then sign in.
- **Claude Code:** `claude mcp add --transport http adkit https://mcp.adkit.so`

For other AI apps, see how to set up the [AdKit MCP server for LinkedIn Ads](https://adkit.so/features/ads-mcp/linkedin). If the AdKit tools are not available, tell the user how to connect. Then stop.

## AdKit names and LinkedIn names

AdKit uses the same names on every platform, so two of them differ from LinkedIn's:

| AdKit entity | LinkedIn name                             |
| ------------ | ----------------------------------------- |
| `campaigns`  | Campaign Groups                           |
| `ad-groups`  | Campaigns ("Ad sets" in Campaign Manager) |
| `ads`        | Ads (creatives)                           |

When the user says "campaign", they usually mean a LinkedIn Campaign, which is one of the AdKit `ad-groups`. Ask the user which one they mean before you change anything.

## What AdKit can do on LinkedIn

| Entity             | Actions                                                                      |
| ------------------ | ---------------------------------------------------------------------------- |
| `campaigns`        | list, get, create, update                                                    |
| `ad-groups`        | list, get, create, update                                                    |
| `ads`              | list, get, create, update (name and status)                                  |
| `targeting-search` | search (find IDs for locations, job titles, industries, and other targeting) |
| `media`            | upload, get                                                                  |
| `results`          | list                                                                         |
| `accounts`         | list, available, connect, disconnect                                         |
| `drafts`           | get, publish (review your changes, then send them)                           |

## Steps

All calls go through `adkit_manage` with `platform: "linkedin"` and an explicit `accountId`. AdKit does not pick a default LinkedIn account. Before a call you have not made in this session, read its fields with `adkit_help({ path: "manage linkedin <entity> <action>" })`. Do not guess field names. In this skill, `campaigns` `create` means `entity: "campaigns"`, `action: "create"`.

1. **Project:** call `adkit_projects` and get the `projectId`. Every call needs it.
2. **Account:** call `adkit_status`. If no LinkedIn account is connected, call `adkit_setup` with `platform: "linkedin"` and give the user the link. After they sign in, use `accounts` `available`, then `accounts` `connect`.
3. **Build from the top down.** Each create saves a draft. For each level, do these steps before you start the next level:
   - Show the draft to the user (`drafts` `get`, or the link `https://app.adkit.so/manage/drafts?open=<draftId>`).
   - Wait for a yes. Then publish it with `drafts` `publish`.
   - Use the LinkedIn ID that the publish result returns as the parent of the next level. A draft ID never works as a parent ID.

   The levels, in order:
   1. **Campaign group:** `campaigns` `create` with a name and, if needed, a lifetime budget and an end date.
   2. **Targeting:** `targeting-search` `search` to find the IDs for the audience.
   3. **Campaign:** `ad-groups` `create` with the `campaignId`, the objective, the schedule, the daily budget, the targeting, and `status: "draft"`. LinkedIn's `draft` status is not an AdKit draft: the campaign exists on LinkedIn but does not run.
   4. **Media:** `media` `upload`. It returns a URN such as `urn:li:image:...`. Check that it finished processing with `media` `get`.
   5. **Ad:** `ads` `create` with the `adGroupId` and the creative, or `existingPostId` to promote a post that already exists.

4. **Go live:** `ad-groups` `update` with `status: "active"`. Publish that draft only after the user says yes. An active LinkedIn campaign needs at least one location in its targeting.
5. **Results:** `results` `list` with a `level` and a date range (`from` and `to`).

## LinkedIn rules

- The objective, schedule, daily budget, and targeting go on the ad group (LinkedIn Campaign). The campaign (Campaign Group) only takes a lifetime budget.
- On create, status is `active` or `draft`. `paused` is accepted on update only.
- An ad update can only change the name and the status. To change the copy or the image, create a new ad and pause the old one.
- Use AdKit field names (camelCase). The entities in the table above ignore raw LinkedIn API field names.

## Anything else in the LinkedIn API

For a LinkedIn feature that AdKit does not cover, use `entity: "platform-api-request"` with `action: "mutate"`. The action is always `mutate`, also for reads. AdKit sends the request to `https://api.linkedin.com/rest` as it is. The user must turn on Advanced Platform Access in AdKit's Agent Permissions.

- LinkedIn uses Rest.li paths. Check every path and field in the [LinkedIn Marketing API docs](https://learn.microsoft.com/linkedin/marketing).
- Read requests run immediately, with no draft. Writes save a draft, like any other change.
- After you use it, report the missing feature with `adkit_feedback`.

```json
{
  "projectId": "<projectId>",
  "entity": "platform-api-request",
  "action": "mutate",
  "data": {
    "platform": "linkedin",
    "accountId": "<accountId>",
    "endpoint": "adCampaignGroups/(account:urn:li:sponsoredAccount:<accountId>)",
    "method": "GET",
    "description": "List campaign groups"
  }
}
```

## Other platforms

The same AdKit connector runs [Meta Ads](https://adkit.so/features/ads-mcp/meta), [Google Ads](https://adkit.so/features/ads-mcp/google), [TikTok Ads](https://adkit.so/features/ads-mcp/tiktok), [Microsoft Ads](https://adkit.so/features/ads-mcp/microsoft), [Reddit Ads](https://adkit.so/features/ads-mcp/reddit), [X Ads](https://adkit.so/features/ads-mcp/x), and [Pinterest Ads](https://adkit.so/features/ads-mcp/pinterest) ads. Each platform has its own skill in this repo, for example `meta-ads` and `google-ads`.
