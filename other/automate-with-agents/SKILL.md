---
name: automate-with-agents
description: "Use when the user wants GoMarble to keep doing a job on a schedule: a daily brief, anomaly or spend alerts, a weekly creative fatigue check, a search term cleanup every Monday, budget pacing, competitor monitoring, or a recurring report by email or Slack. Covers creating, listing, editing, pausing, running and deleting GoMarble agents with manage_agents, including write agents that propose changes for approval."
---

# Automate with agents

GoMarble agents run a standing job on a schedule in GoMarble's cloud, whether or not the chat app is open. Each run investigates what changed and delivers the result by email or Slack. An agent can be read-only (watch and report) or have write access (propose changes, applied only after approval by default).

"Agent" and "schedule" mean the same thing. Everything goes through one tool: `manage_agents`.

## When to use

- "Every morning, tell me how yesterday went across my accounts."
- "Alert me when ROAS drops below 2 or spend spikes."
- "Check my ads for creative fatigue every week."
- "Clean up search terms every Monday and propose the negatives."
- "Send the team a performance report every Monday at 9."
- "Pause my agents", "what agents do I have?", "run the daily brief now".

For a one-off analysis, don't create an agent. Answer directly, then offer to put it on a schedule.

## Workflow

### 1. See what already exists

Call `manage_agents` with `action: "list"`. If an existing agent already covers the job, such as a daily brief, offer to update it rather than creating a duplicate.

### 2. Agree on the job

Settle these in one short exchange. Don't ask about anything the user already told you.

| Setting | How to decide |
|---|---|
| **The job** | What to watch, which thresholds matter, what to do about it, and what the output should look like. Base it on a starter agent below when one fits. |
| **Accounts** | Use account IDs exactly as the list tools return them (`facebook_list_ad_accounts`, `google_ads_list_accounts`, `tiktok_list_ad_accounts`, and so on). Account names in the prompt don't count as scope. |
| **Cadence** | `daily`, `weekly` or `monthly`, matched to the job. Don't over-notify. Convert the user's local time to a UTC `cronExpression` and pass their IANA `timezone`. |
| **Delivery** | This is the user's choice, so ask. Email (`gmail` + `emailRecipients`) works for everyone. Slack (`slack` + `slackChannels`) needs Slack connected at apps.gomarble.ai/settings/apps (on a plan that includes it) and a channel the GoMarble bot can see. If they have no preference, propose email to their own address. Never default to Slack. Each method needs its destination in the same call, or the agent runs and delivers nothing. |
| **When to notify** | `notificationMode: "always"`, or `"conditional"` with a `notificationCondition` such as "ROAS dropped below 1x". |
| **Read or write** | Monitoring, briefs, fatigue flags, competitor watch and alerts are read-only (the default). Only a job that should act on the account needs `permissions: { accessLevel: "write", writeMode: "ask_approval" }`. Write agents must include at least one Meta Ads or Google Ads account and need a GoMarble plan with write actions. **From here, always use `writeMode: "ask_approval"`**: the agent prepares each change and it waits for someone to approve it in GoMarble. Never set `writeMode: "auto_apply"`. If the user wants changes applied without approval, explain that a workspace owner or admin can set that up in the GoMarble web app, where it comes with guardrails such as budget-change caps. |
| **Guardrails** | For write agents, offer `guardrails`: `allowedActions` (for example only `status_toggle` and `budget_change`) and `maxBudgetChangePct` (for example 20). These need the agent-governance plan feature. `accountScopeStrict: true` locks the agent to its accounts; ask before setting it. |

### 3. Create it as a draft

Call `manage_agents` with `action: "create"`, `type: "prompt"`, `promptTitle`, `prompt`, `scheduleType`, `cronExpression`, `timezone`, `deliveryMethods` and destinations, plus the settings above.

A new prompt agent is a **draft** by default: saved and editable, but nothing runs or delivers until the user activates it. Tell the user it's a draft. Activate it with `action: "resume"` only after they confirm. Pass `isDraft: false` only when the user explicitly asked for it to go live right away.

Optional settings:
- `intelligenceLevel`: `instant`, `medium` (default) or `high` for deeper reasoning.
- `memoryMode`: `auto` (default), `on` or `off`. When on, the agent follows up on its own earlier recommendations.

### 4. Manage existing agents

| User wants to | Call `manage_agents` with |
|---|---|
| See their agents | `action: "list"` (optionally `type: "prompt"` or `"report"`) |
| Change the prompt, cadence, delivery or accounts | `action: "update"`, `scheduleId`, and only the fields that change |
| Stop it for now | `action: "pause"`, `scheduleId` |
| Start it (or take a draft live) | `action: "resume"`, `scheduleId` |
| Run it once now | `action: "run"`, `scheduleId` |
| Remove it | `action: "delete"`, `scheduleId`, only after the user confirms. Deleting can't be undone; pausing can. |

Report agents (`type: "report"`) re-run a report saved in the GoMarble app and need its `reportId`. To schedule a report built in this conversation, create a prompt agent whose prompt describes the report (see the `build-reports` skill).

## Writing a good agent prompt

- Name the accounts, the comparison windows (for example yesterday vs the trailing 7-day average, or 3-day vs 7-day), and the thresholds.
- Say what counts as noise. "Default to HOLD" and "ignore entities changed in the last 48 hours" prevent over-reacting.
- Say what to deliver: a maximum number of bullets, a table, or "only message me when something needs action".
- For write agents, say exactly which changes it may propose and the limits (for example "budget changes of at most 20%").

## Starter agents

These are based on GoMarble's own agent templates. Adapt them to the user's accounts and targets.

| Agent | Platforms | Cadence | Access | The job |
|---|---|---|---|---|
| CMO daily brief | All connected | Daily | Read | Yesterday vs 7-day average for spend, ROAS and CPA per channel, plus GA4 sessions by channel and Klaviyo revenue. At most 5 bullets. |
| Performance analyst | Meta, Google | Daily | Read | Flag the one or two account changes that deserve attention, with the likely driver and next step. |
| Creative fatigue monitor | Meta, TikTok | Weekly | Read | Frequency up and CTR down more than 20% (first vs last 7 days of 28) = fatigued; 15–20% = creeping in. |
| Search term analyzer | Google, Microsoft | Weekly | Read or write | Pareto the search terms driving 80% of spend and flag wasteful ones. With write access, propose negatives for approval. |
| Budget pacing / optimizer | Meta, Google | Daily | Read or write | Default to HOLD. Use 3-day and 7-day ROAS trends. With write access, propose budget moves of at most 20%. |
| Impression share tracker | Google | Weekly | Read | Lost IS (budget) vs lost IS (rank) on profitable campaigns: raise budget, improve rank, or do nothing. |
| Bids optimizer | Google, Microsoft | Weekly | Read or write | Align tCPA/tROAS targets with actual performance. Never change strategy under 30 conversions a month or move targets more than 20%. |
| Competitor radar | Ad library | Weekly | Read | New and scaling competitor ads, grouped by angle, with the gaps worth testing next. |
| Monthly budget reallocation memo | All connected | Monthly | Read | Four weeks of cross-channel efficiency trends and a one-page recommendation for next month's split. |
| CAC vs LTV tracker | Ads + Shopify + Klaviyo | Monthly | Read | Blended CAC, 90-day LTV per cohort and LTV:CAC by month. |

## Permissions

- Team members need the **Can build agents** permission to create or change agents. If `manage_agents` says they don't have it, an owner or admin turns it on in Team management (see `access-and-permissions`).
- An agent shared with the user as a viewer can be read but not changed. Only an agent's owner can delete it or change its permissions and guardrails.
- An agent can only reach accounts its creator can reach.

## Guardrails

- Never create, update, activate or delete an agent the user didn't ask for.
- Never turn on write access without the user saying so, and never set `writeMode: "auto_apply"` from here, even if asked (see Read or write above).
- Confirm the final settings in one short summary before creating: title, job, accounts, cadence (in the user's time zone), delivery, read or write.
