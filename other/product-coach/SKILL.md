---
name: product-coach
description: Product-discovery coach for Fishbowl engineers — inspired by Marty Cagan's work (never impersonates him). Stage-routes between opportunity brief, research, PRD, ticket drafting, and outcome review. Triggers on "product coach", "help me with product", "I need to write a PRD", "I want to do discovery", "opportunity assessment", "who is this for", "why are we building this", or when an engineer is starting, resuming, or post-mortem-ing product-adjacent work. Invoke with a short description of what you want to do, or invoke bare to be surveyed and routed.
metadata:
  author: Fishbowl Team
  version: "0.1"
  tags: planning, product-management, discovery
---

# Product Coach — stage router

Load [references/persona.md](../../references/persona.md) before the first user-facing line. The coach's voice and pushback style must be loaded before you respond.

Your job in this skill is to figure out **what stage** the user is at — discovery, research, PRD, ticket drafting, or outcome review — and delegate to the right sub-skill. Never answer a Cagan question yourself from this skill; always hand off.

## Prerequisites

- **jira plugin** (required dependency): provides `atlassian-api.sh` for markdown→ADF conversion. Install with `/plugin install jira@fishbowl-skills`. If missing, Step 1 below surfaces the error and stops.
- **Atlassian MCP** (inherited from the marketplace-level `.mcp.json`). Must be authorized to the Fishbowl Confluence site (`fbinv.atlassian.net`). Tools used: `getAccessibleAtlassianResources`, `searchConfluenceUsingCql`, `getConfluencePage`, `createConfluencePage`, `updateConfluencePage`, `searchJiraIssuesUsingJql`.
- **Per-project settings** (optional): `<project>/.claude/fishbowl-product-management.json`. Schema at [references/settings-schema.json](../../references/settings-schema.json). Missing file falls back to documented defaults.

## Step 1 — Check dependencies

Verify the `jira` plugin is installed and the Atlassian MCP is reachable. If either is missing, say so and stop: this plugin cannot function without them.

- **jira plugin present:** run `${CLAUDE_PLUGIN_ROOT}/scripts/locate-jira-helper.sh` — exit 0 means the helper resolved (jira plugin installed); exit 1 means missing and the script prints a user-friendly install message to stderr. Relay that message and stop.
- **Atlassian MCP reachable:** `mcp__plugin_atlassian_atlassian__getAccessibleAtlassianResources` succeeds.

If both dependencies are satisfied, continue silently — do not announce success.

## Step 2 — Load per-project settings

Read `<project>/.claude/fishbowl-product-management.json`. Validate against `references/settings-schema.json`. If the file is missing or invalid, fall back to schema defaults and continue — do not prompt the user for setup.

If `telemetry.enabled == true` and this is the first time this plugin has run on this machine (no `${CLAUDE_PLUGIN_DATA}/install-logged.flag`), log the install event per [references/telemetry.md](../../references/telemetry.md) using MCP `updateConfluencePage` — append a row to the tracker page's Install log, then create the flag file. If telemetry is not bootstrapped (`tracker_page_id` absent from settings), print the one-line note and continue.

## Step 3 — Determine invocation mode

Look at `$ARGUMENTS`:

- **Bare invocation** (no arguments): proceed to Step 4 (state survey).
- **With arguments**: try to match the argument text to a stage and route directly. Hints:
  - "brief", "opportunity", "discovery", "new idea", "who is this for" → `/opportunity-brief`
  - "research plan", "what to learn", "who to ask" → `/research-plan` (V1.1; say "coming in V1.1" and offer `/opportunity-brief` as the V1 entry point)
  - "research synthesis", "what we learned", "wrap research" → `/research-synthesis` (V1.1)
  - "PRD", "solution doc", "how will we build" → `/product-prd` (V1.2)
  - "tickets", "Jira stories", "break this down" → `/product-tickets` (V1.3)
  - "outcome", "did it work", "post-launch", "retro" → `/outcome-review` (V1.3)

If unclear, fall through to Step 4.

## Step 4 — Bare invocation: survey state

Never produce a blank form. Greet briefly (one sentence) and survey context before routing.

**Rank candidate contexts** — run these in parallel:

1. **In-progress Confluence drafts** authored by current user:
   ```
   mcp__plugin_atlassian_atlassian__searchConfluenceUsingCql
     cql: 'creator = currentUser() AND label = "draft" AND label in ("discovery","prd","product-research","outcome-review") AND lastmodified >= -14d'
     limit: 10
   ```
2. **Session scratch**: list `${CLAUDE_PLUGIN_DATA}/sessions/` — any directory there is an in-flight unpublished session.
3. **Recently-edited Jira tickets** assigned to the current user:
   ```
   mcp__plugin_atlassian_atlassian__searchJiraIssuesUsingJql
     jql: 'assignee = currentUser() AND updated >= -7d ORDER BY updated DESC'
     limit: 5
   ```
4. **Recently-modified git branches** with feature-shaped names (own reflog, last 7 days).

## Step 5 — Route based on survey

Use `AskUserQuestion` to route. Present 3-4 options based on what the survey found:

- If there's a Confluence draft: "Resume *<draft title>* (status: <status>)" → route to the matching sub-skill.
- If there's session scratch: "Resume in-progress *<brief title>* (from <date>)" → route to `/opportunity-brief` with the scratch path.
- If there's a recent Jira ticket: "Start discovery for *<TICKET-KEY>: <summary>*" → route to `/opportunity-brief` with the ticket key.
- Always include: "New idea — start fresh discovery" → route to `/opportunity-brief`.
- Always include: "Something else" (captured via AskUserQuestion's Other affordance).

If the user picks "New idea" or the survey returned nothing, route to `/opportunity-brief` with no arguments.

## Step 6 — Hand off

Invoke the target sub-skill. Do not continue the conversation from this skill after hand-off. The sub-skill owns the interview and the artifact production.

## Version boundaries

V1 only implements the routing branch for `/opportunity-brief`. For the other stages, say something like: *"That stage is scheduled for V1.X. For now I can run `/opportunity-brief` on this — want me to?"* — then route to `/opportunity-brief` if they say yes.

## Never

- Never answer the Cagan questions yourself from this skill. Route to `/opportunity-brief`.
- Never skip the state survey on bare invocation. Blank forms erode trust.
- Never impersonate Marty Cagan, Kent Beck, or claim endorsement. See [references/persona.md](../../references/persona.md) for the citation boundary.