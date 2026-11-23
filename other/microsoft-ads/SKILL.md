---
name: microsoft-ads
displayName: "AdKit for Microsoft Ads (Bing Ads): Campaigns, Ad Groups, Ads and Reports"
description: >
  Read and change Microsoft Advertising (Bing Ads) campaigns from an AI agent through the
  AdKit MCP connector, using the official Microsoft Advertising API v13. Every change is saved
  as a draft that the user approves before it goes live. Use when the user wants to run,
  change, or check Microsoft or Bing ads. Not for Microsoft Ads strategy or ad copy advice.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://adkit.so/features/ads-mcp/microsoft
triggers:
  - microsoft ads
  - microsoft ads mcp
  - bing ads
  - bing ads mcp
  - microsoft advertising
  - microsoft ads campaign
  - microsoft ads report
  - bing ads api
---

# Microsoft Ads with AdKit

This skill tells you how to read and change Microsoft Advertising (Bing Ads) campaigns through AdKit. It covers the steps, not the strategy.

AdKit connects Microsoft Advertising accounts and sends your requests to the official Microsoft Advertising API v13. AdKit has no `campaigns`, `ad-groups`, or `ads` entities for Microsoft yet, so you write Microsoft API requests directly.

## Connect AdKit

AdKit is one MCP connector for Meta, Google, TikTok, LinkedIn, Microsoft, Reddit, X, and Pinterest ads.

- **Claude, ChatGPT, and most AI apps:** add a custom connector with the address `https://mcp.adkit.so`, then sign in.
- **Claude Code:** `claude mcp add --transport http adkit https://mcp.adkit.so`

For other AI apps, see how to set up the [AdKit MCP server for Microsoft Ads](https://adkit.so/features/ads-mcp/microsoft). If the AdKit tools are not available, tell the user how to connect. Then stop.

The user must also turn on Advanced Platform Access in AdKit's Agent Permissions. Without it, the requests below fail.

## What AdKit can do on Microsoft Ads

- **Accounts:** `accounts` list, available, connect, disconnect.
- **Campaigns, ad groups, ads, keywords, and reports:** through Microsoft Advertising API v13 requests.
- **Reads** (`POST` requests to `.../Query...` paths) run immediately, with no draft. **Writes** save a draft.
- **Blocked:** billing, audience uploads, and the whole Customer Management service.

## Steps

In this skill, `accounts` `connect` means an `adkit_manage` call with `entity: "accounts"` and `action: "connect"`.

1. **Project:** call `adkit_projects` and get the `projectId`. Every call needs it.
2. **Account:** call `adkit_status`. If no Microsoft account is connected, call `adkit_setup` with `platform: "microsoft"` and give the user the link. After they sign in, use `adkit_manage` with `platform: "microsoft"`: `accounts` `available`, then `accounts` `connect`.
3. **Read** what exists. The request format is in How to write a request, below.
4. **Change** things with the same kind of request. Each write saves a draft.
5. **Review:** `adkit_manage` with `entity: "drafts"`, `action: "get"`, or give the user the link `https://app.adkit.so/manage/drafts?open=<draftId>`. Show them what will change.
6. **Publish:** `drafts` `publish`, only after the user says yes.

To build a new campaign, go from the top down: campaign, then ad group, then ads and keywords. Publish each level before you create the next one, and use the ID that Microsoft returns as the parent. A draft ID never works as a parent ID.

## How to write a request

Every request is one `adkit_manage` call:

```json
{
  "projectId": "<projectId>",
  "entity": "platform-api-request",
  "action": "mutate",
  "data": {
    "platform": "microsoft",
    "accountId": "<accountId>",
    "endpoint": "https://campaign.api.bingads.microsoft.com/CampaignManagement/v13/Campaigns/QueryByAccountId",
    "method": "POST",
    "payload": { "AccountId": "<accountId>", "CampaignType": "Search" },
    "description": "List Search campaigns"
  }
}
```

- `endpoint` is the **full** `https` URL. Microsoft spreads its API across several hosts (`campaign`, `reporting`, `bulk`, and others under `.api.bingads.microsoft.com`), so there is no short path.
- The HTTP method sets the operation:
  - `POST` to `.../Campaigns` adds.
  - `PUT` updates.
  - `DELETE` with a JSON body of IDs deletes.
  - Reads are `POST` requests to `.../Query...` paths.
- In the list request above, `CampaignType` is optional. Without it, Microsoft returns Search campaigns only.
- `action` is always `mutate`, also for reads.
- `description` is required. The user sees it when they review the draft.
- Check every path and field in the [Microsoft Advertising API docs](https://learn.microsoft.com/advertising). Do not use AdKit field names here.

## Examples

Only the `data` part changes. These follow the Microsoft Advertising API v13 reference.

**Pause a campaign.** `Status` is `Active` or `Paused`.

```json
{
  "platform": "microsoft",
  "accountId": "<accountId>",
  "endpoint": "https://campaign.api.bingads.microsoft.com/CampaignManagement/v13/Campaigns",
  "method": "PUT",
  "payload": {
    "AccountId": "<accountId>",
    "Campaigns": [{ "Id": "<campaignId>", "Status": "Paused" }]
  },
  "description": "Pause campaign <campaignId>"
}
```

## Microsoft Ads rules

- New campaigns start paused unless you set `Status`. Microsoft also pauses a campaign when its budget runs out.
- Reports and bulk downloads run as jobs. A successful response only means the job started. Check the job status as the Microsoft docs describe. Report results only when the job is done.
- If the user needs something AdKit blocks, tell them, and report it with `adkit_feedback`.

## Other platforms

The same AdKit connector runs [Meta Ads](https://adkit.so/features/ads-mcp/meta), [Google Ads](https://adkit.so/features/ads-mcp/google), [TikTok Ads](https://adkit.so/features/ads-mcp/tiktok), [LinkedIn Ads](https://adkit.so/features/ads-mcp/linkedin), [Reddit Ads](https://adkit.so/features/ads-mcp/reddit), [X Ads](https://adkit.so/features/ads-mcp/x), and [Pinterest Ads](https://adkit.so/features/ads-mcp/pinterest) ads. Each platform has its own skill in this repo, for example `meta-ads` and `google-ads`.
