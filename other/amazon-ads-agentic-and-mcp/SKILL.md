---
name: amazon-ads-agentic-and-mcp
description: Drive Amazon Ads with the Amazon Ads MCP Server and the in-console Ads Agent for natural-language campaign, reporting, and account work, with every spend or live change human-gated. Use when the user says "Amazon Ads MCP", "Amazon Ads MCP Server", "MCP server for Amazon Ads", "Ads Agent", "Amazon Ads AI agent", "natural language Amazon campaign", "connect an agent to Amazon Ads", "let the agent build my Amazon campaign", "AMC natural language query", or asks whether an agent can safely change Amazon campaigns. Covers what the MCP Server exposes, how it differs from the Ads Agent, the access model, and the guardrails that keep an agent from spending without approval.
---

# Amazon Ads agentic and MCP

Wire an AI agent to Amazon Ads through the Amazon Ads MCP Server, or use the in-console Ads Agent, and keep both inside guardrails so no spend or live change happens without a human approving it. The MCP Server (open beta, February 2, 2026) is a translation layer that turns natural-language prompts into structured Amazon Ads API calls, so an agent can create, read, update, and delete campaigns, run reports, manage account settings, and read billing data. The in-console Ads Agent (unBoxed 2025, announced November 11, 2025) is Amazon's own assistant inside Campaign Manager that pre-drafts audience strategies and answers natural-language questions against Amazon Marketing Cloud.

This skill is about the mechanics of running Amazon Ads through an agent and the safety rails, not about how to read a report or design an audience. For KPI math and definitions (CPM, CPC, ROAS, ACOS), see the `programmatic-foundations` skill. For the underlying API mechanics, auth, and the safe-to-automate matrix for DSP, see `amazon-dsp-api-and-automation`. For AMC query design and the privacy model behind the natural-language AMC feature, see `amazon-marketing-cloud`. For onsite Sponsored Products and Sponsored Brands strategy, see `retailmedia-onsite-sponsored-products`.

## When to use this skill

- "Connect an agent to Amazon Ads." / "Set up the Amazon Ads MCP Server."
- "Can the agent build my Amazon campaign?" / "Let the agent launch Sponsored Products."
- "What can the Amazon Ads MCP Server do?" / "What is the difference between the MCP Server and the Ads Agent?"
- "Use the Ads Agent to draft an audience strategy." / "Ask AMC a question in plain language."
- "Is it safe to let an agent change Amazon campaigns?" / "How do I stop the agent from spending?"
- "Expand my campaign to a new country with one prompt." / "Pull an Amazon report through the agent."

Boundaries with sibling skills:
- API auth, Login with Amazon, the profile and advertiser model, and the full safe-to-automate matrix: `amazon-dsp-api-and-automation`.
- DSP report metrics, dimensions, and how to read the numbers: `amazon-dsp-measurement-and-reporting`.
- AMC query design, aggregation thresholds, and clean-room privacy: `amazon-marketing-cloud`.
- Onsite Sponsored Products and Sponsored Brands keyword and bid structure: `retailmedia-onsite-sponsored-products`.
- Audience strategy and segment selection: `amazon-dsp-audiences`.
- KPI definitions and shared math: `programmatic-foundations`.

## Quick reference

Pick the surface first. The MCP Server is for wiring your own agent to Amazon Ads; the Ads Agent is Amazon's assistant inside the console.

| You want | Use | Why |
| --- | --- | --- |
| Your own agent to run Amazon Ads through natural language | Amazon Ads MCP Server | It maps prompts to Amazon Ads API calls, so your agent gets the full API surface behind pre-built tools |
| Amazon's built-in assistant to draft strategy and query AMC in plain language | In-console Ads Agent | It lives in Campaign Manager, pre-drafts audience strategy, and answers natural-language AMC questions with no code |
| A ready-to-launch campaign a human reviews before it spends | MCP Server pre-built campaign tool | It bundles the multi-step create flow and stops at review and approval |
| To pull a report or expand to a new country by prompt | MCP Server pre-built tool | Report generation and locale expansion ship as first-class tools |
| To read what an agent can touch on DSP versus what stays managed-service | `amazon-dsp-api-and-automation` | Access is granted per solution and per account, not by the MCP Server itself |

Two things to keep straight:
- The MCP Server does not grant new access. It rides your existing Amazon Ads API credentials, so it can only do what those credentials already allow. See `amazon-dsp-api-and-automation` for the access model.
- Write is real. The MCP Server can create, update, and delete campaigns and change account settings, so the guardrails below are not optional.

## Core process

1. Confirm eligibility and credentials, because the MCP Server rides existing access and grants nothing new. The MCP Server is open to Amazon Ads partners with active API credentials (Login with Amazon plus an allowlisted developer application). If you cannot call the Amazon Ads API today, wiring the MCP Server changes nothing. Confirm the account has the solution scope you need (Sponsored Products, DSP, AMC) per `amazon-dsp-api-and-automation`.
2. Decide MCP Server versus Ads Agent, because they solve different problems. Build your own agent against the MCP Server when you want to orchestrate Amazon Ads inside a larger workflow (a nightly optimizer, a cross-platform report, your own reviewer). Use the in-console Ads Agent when you want Amazon's assistant to pre-draft an audience strategy or answer an AMC question without leaving Campaign Manager.
3. Scope the tools to read-first, because read tools cannot spend. Start any agent integration with reporting and account-read tools. Prove the agent pulls the right numbers and names the right entities before you enable any create, update, or delete tool.
4. Put a human gate on every write, because the MCP Server can create, update, and delete campaigns and change billing-adjacent settings. Route every write through a review step. The pre-built campaign tool already stops at a ready-to-launch state that "only needs review and approval"; hold that line and never auto-approve.
5. Constrain the blast radius, because one prompt can span three or more API operations. Limit the agent to a named advertiser or campaign, cap the budget it can propose, and require an explicit confirmation before launch, budget change, bid change, or delete.
6. Log every action, because you need an audit trail when an agent touched a live account. Capture the prompt, the resolved API calls, the entity IDs, and who approved the write. Reconcile agent-made changes against the account daily.
7. Verify in the account, because a natural-language layer can misread intent. After any approved write, confirm the created or changed entity in the console or through a read call. Do not trust the agent's own success message alone.

## Decision rules and thresholds

### MCP Server versus in-console Ads Agent

- Use the MCP Server when the work belongs in your own pipeline: scheduled reporting, a custom optimizer, a cross-platform workflow, or an agent that has to touch systems beyond Amazon. It exposes the Amazon Ads API through natural-language tools, so it is the right layer for anything you build and control.
- Use the in-console Ads Agent when the work is inside Campaign Manager and Amazon's own drafting is enough: pre-drafting an audience strategy or asking AMC a question in plain language. It does not require you to build or host anything.
- The two are not mutually exclusive. A team can use the Ads Agent for in-console drafting and the MCP Server for programmatic orchestration on the same account.

### What must always be human-gated

Never let an agent execute these without an explicit human approval:
- Launching a campaign, ad group, or ad (turns on spend).
- Any budget increase or bid increase (raises spend).
- Deleting or archiving a live campaign, ad group, target, or creative (destroys delivery and history).
- Account-level settings changes and anything touching billing or financial data (the MCP Server can read billing and financial data; treat any change here as the highest gate).
- Country or locale expansion, because a single prompt can spin up delivery in a new market.

Read-only work (pulling reports, listing entities, reading settings) can run unattended once you trust the agent's output, because it cannot spend.

### Budget and blast-radius caps

- Scope credentials to the smallest advertiser set the job needs. Do not point a broad-access token at a single-advertiser task.
- Set a hard ceiling on any budget the agent can propose (for example, no proposed daily budget above 120 percent of the current daily budget without a second approval).
- Require a two-person or two-step approval for deletes and for any change above the ceiling.
- Rate-limit writes. A runaway agent that loops on "update budget" can move real money fast; cap writes per run and per hour.

### When not to use an agent at all

- High-stakes launches (tentpole events, large reserved DSP flights) where a misread prompt is expensive. Build these by hand and use the agent only to draft and to report.
- Managed-service-only accounts that cannot write through the API. The MCP Server cannot create a write path that the account does not have; see `amazon-dsp-api-and-automation`.
- Any workflow where you cannot log and reconcile the agent's actions. No audit trail, no autonomous write.

## Reference material

- `references/mcp-server-capabilities.md`: the pre-built tool families the MCP Server exposes (campaign create and manage, reporting, account and settings, billing read, locale expansion), which Amazon Ads solutions they reach, the open-beta access requirements, and the read-versus-write split. Read this when scoping which tools to enable for an agent.
- `references/ads-agent-vs-mcp.md`: a side-by-side of the in-console Ads Agent and the MCP Server across surface, who builds it, what it drafts versus executes, AMC natural-language support, and the decision table for picking one. Read this when the user is unsure which to use.
- `references/agent-permission-guardrails.md`: the guardrail model in depth, a human-gate matrix by action, credential scoping, budget and rate caps, a review-and-approve pattern, and an audit and reconciliation checklist. Read this before letting any agent write to a live account.

## Templates and examples

- Read-first reporting agent: enable only the MCP Server reporting and account-read tools. Prompt: "Pull last 14 days of Sponsored Products spend, sales, and ACOS for advertiser A12BC3DEF, broken out by campaign." No write tools enabled, so it cannot spend. Schedule it nightly once the numbers reconcile.
- Human-gated campaign build: enable the pre-built Sponsored Products campaign tool. Prompt: "Draft a Sponsored Products campaign for the 'Summer Hydration' ASIN set, 25 dollars per day, exact-match on our top 20 converting terms." The tool returns a ready-to-launch campaign; a human reviews the terms, the daily budget, and the ASINs, then approves the launch. Never auto-approve.
- Locale expansion with a ceiling: prompt the locale-expansion tool to "replicate campaign CMP-88421 into Canada at the same structure." Require approval before it launches, and cap the proposed Canada daily budget at the source campaign's daily budget until performance is seen.
- In-console strategy draft: in Campaign Manager, ask the Ads Agent to pre-draft an audience strategy for a new streaming TV flight, then hand the draft to a trader to refine and launch. Use the Ads Agent's natural-language AMC query to sanity-check overlap before committing.

## Common pitfalls

- Assuming the MCP Server grants access. It does not. It rides your existing Amazon Ads API credentials, so a token without DSP scope still cannot touch DSP through the server. Confirm access per `amazon-dsp-api-and-automation`.
- Enabling write tools on day one. A create, update, or delete tool can spend or destroy delivery on a wrong prompt. Start read-only, prove the agent, then add writes behind a gate.
- Trusting the agent's success message. A natural-language layer can misread intent and still report success. Verify every approved write in the console or with a read call.
- One prompt, many operations. A single instruction can trigger three or more API calls (the campaign create tool bundles them). Scope the blast radius and confirm before launch so a compound action does not surprise you.
- Auto-approving the ready-to-launch state. The pre-built campaign tool stops at review and approval on purpose. Auto-approving throws away the one gate that keeps a bad campaign from spending.
- Confusing the two products. The in-console Ads Agent drafts and queries inside Campaign Manager; the MCP Server is the layer you wire your own agent to. Do not tell a user to "install" the Ads Agent or to "open" the MCP Server in the console.
- No audit trail. If you cannot log the prompt, the resolved calls, the entity IDs, and the approver, do not let the agent write. Reconcile agent changes against the account daily.

## Sources

- [Amazon Ads MCP Server, now in open beta](https://advertising.amazon.com/library/news/amazon-ads-mcp-server-open-beta) (as of July 2026)
- [unBoxed 2025 recap](https://advertising.amazon.com/library/news/unboxed-2025-recap) (as of July 2026)
- [Amazon Ads unBoxed 2025 AI announcement](https://advertising.amazon.com/library/news/unboxed-ai-announcement) (as of July 2026)
- [Amazon DSP campaign and creative API are now available](https://advertising.amazon.com/resources/whats-new/amazon-dsp-campaign-and-creative-api-are-now-available) (as of July 2026)
- [Campaign analysis with unified reporting](https://advertising.amazon.com/resources/whats-new/unboxed-2025-campaign-analysis-with-unified-reporting) (as of July 2026)
