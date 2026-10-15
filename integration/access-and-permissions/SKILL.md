---
name: access-and-permissions
description: "Use when a GoMarble tool is denied or the user asks about access: 'I don't have access to this account', account_access_denied, a scope or permission upgrade (606), read-only connections, plan limits (403 / 600), the TikTok beta, agent permissions, or team roles. Explains GoMarble's role-based access control (owner, admin, member; View vs Act per account; OAuth scopes), tells the user exactly who can fix it and where, and never tries to work around a denial."
---

# Access and permissions

GoMarble controls what each person, and each AI app connected on their behalf, can reach. Access works in three layers, and a tool call has to pass all three.

1. **The team role** decides which ad accounts a person can reach.
2. **Per-account access** (for members) decides whether they can view an account or also act on it.
3. **The connector's permissions** (OAuth scopes) decide what the connected AI app may do for that person.

No GoMarble tool changes roles, access or scopes. When access is missing, explain it, say who can fix it and where, and continue with what is allowed. Never retry a denied call in a different way to get around it.

## Roles and account access

| Role | Can reach | Can also |
|---|---|---|
| **Owner** | Every account | Everything an admin can, plus billing, transferring ownership and deleting the team |
| **Admin** | Every account | Invite and remove members, promote admins, connect and remove data sources, set members' account access, change team settings |
| **Member** | Only the accounts granted to them | Nothing admin-level |

A member's access to each account is one of:
- **View:** read tools (reports, insights, lists).
- **Act:** also make changes, **including dry-run proposals**. Any tool that isn't read-only needs Act.
- **None:** no access. Access is denied unless it was granted.

Per-account access applies to Meta Ads, Google Ads, GA4, TikTok, Microsoft Ads and LinkedIn Ads. Other team connections (Shopify, Klaviyo, Search Console, Pages, Instagram, Snowflake, the ad library, MCP connectors) are shared with everyone on the team.

Act can only be granted where the connection allows writing: Meta and Google Ads (and TikTok with a write connection). Everything else is View only.

**Where it's managed:** owners and admins set access at **apps.gomarble.ai/settings/team-management**. They click the member's access chip, pick None, View or Act per account, and toggle **Can build agents**. The same access shows per account under **Settings → Integrations**. Changes take effect within about a minute.

**Team context.** The connection acts in the team the user currently has selected in the GoMarble web app. If accounts look missing or wrong, check the team switcher there. Connector sign-ins last 30 days; after that the user reconnects GoMarble in their AI app.

## When a tool is denied

Read the response, match it below, and relay the fix. Show any link **exactly as given**, never edited.

| What you see | What it means | Who can fix it, and how |
|---|---|---|
| `account_access_denied`, or "You don't have (permission to use / access to) ad account …" with a `level` | The user is a member without View (to read) or Act (to change or propose) on that account | An owner or admin grants it at Settings → Team management → the member's access chip. Say which level is needed. If the account isn't in GoMarble yet, an admin must add it first (`accounts-and-connections`). Don't suggest reconnecting the platform; that won't help. |
| `error_code: 606`, `scope_upgrade_required`, `missing_scope`, `reauth_url` | The AI app's connection wasn't granted that permission when it was set up | The user opens `reauth_url` while logged in to GoMarble, approves, then retries. No reconnection is needed. Exceptions: `tiktok_ads:write` and `google_sheets:*` can't be granted to AI app connections today, so say so and suggest the GoMarble web app for that action. |
| "Can't perform write actions on a read-only connection…" or "… has read-only access and was added by …" | The platform connection was set up read-only | The owner of that connection, or an admin, switches it to Read & Write in Settings → Integrations (Google Ads doesn't need a re-login; Meta and TikTok reconnect). Relay the message's options as written. Members can't use connect or reconnect links; they get "Ask your team admin". |
| "The ad account … only has read access … Analyst (read-only) … in Meta Business Manager" | The person's own Meta role on that account is read-only | They need a higher role on the account in Meta Business Manager. GoMarble can't change it. |
| "The … connection has expired and was added by …" | The platform token expired, and only its owner can reconnect it | Ask that person, or an admin, to reconnect it in Settings → Integrations. |
| `error_code: 403` with `feature_key` such as `fb-ads-account-limit` or `ad-spend-limit`, and `upgrade_url` | Adding this account would pass the plan's account or ad-spend limit | Explain which limit was reached. The workspace owner manages the plan in GoMarble, and plan details are at gomarble.ai/pricing; or an admin removes an unused account. Don't share the `upgrade_url` and don't retry until the limit changes. |
| `error_code: 600`, `quota_error`, `feature_key: agent-mode` | The plan's allowance for applying changes is used up | Explain that the plan's allowance for applying changes is used up; the workspace owner manages the plan in GoMarble, and plan details are at gomarble.ai/pricing. Don't share the `upgrade_url`. Blocked changes were not applied: the user can apply the recommendation in the ad platform, or propose it again once the allowance resets or the plan changes. |
| "Global token quota exceeded" or "reached your limit for competitor ad insights" | Credits for creative analysis or the ad library are used up | Explain that the plan's credits for this feature are used up; the workspace owner manages the plan in GoMarble (plan details: gomarble.ai/pricing). Don't share billing, checkout or upgrade links. Continue with the tools that don't use those credits. |
| "… is part of the TikTok tools beta and is not enabled for this account" | That TikTok tool is in a beta the account isn't in | Contact GoMarble support to join. The non-beta TikTok tools still work. |
| "You don't have permission to manage agents … turn on 'Can build agents'" | A member without the agent permission tried to create or change an agent | An admin turns on **Can build agents** in the member's access chip. |
| `error_code: 607`, `governance_blocked` | A team policy blocked an agent's action (kill switch, allowed actions, or budget cap) | A team admin or the agent's owner changes the agent's limits in GoMarble. This applies to GoMarble's scheduled agents, not normal chat requests. |
| 401 "Authentication failed" | The sign-in expired, or the user was removed from their selected team | Reconnect GoMarble in their AI app, or switch to a team they belong to in the web app. |

## What the connected AI app may do (OAuth scopes)

- By default an AI app connection can **read** Meta, Google, TikTok, LinkedIn and Microsoft Ads, GA4, Search Console, Shopify, Klaviyo, Facebook Pages, Instagram, Snowflake, the ad library and impact.com.
- **Changes are opt-in per platform:** `meta_ads:write` and `google_ads:write`. Without them the model can still make **dry-run** proposals; the `mode: "live"` step returns 606 with the link to add the permission.
- Agents, skills, memory, connector discovery and the account-list tools need no scope.
- TikTok changes and the built-in Google Drive tools (`google_drive_*`) can't be enabled for AI app connections today. Drive files are still reachable through a Drive connector the team adds (the `gdrive-*` tools).

## Answering "what can I do?"

1. Call the list tool for the platform (see `get-started`). Its `configured_accounts` shows the accounts this user can use in GoMarble. For members, that's only the accounts granted to them.
2. If an account the user expects is missing, it's either not added to GoMarble or not granted to them. Both are fixed by an owner or admin (`accounts-and-connections`, or Team management).
3. Say plainly what they can do now (view or act, which platforms) and what needs an admin.
