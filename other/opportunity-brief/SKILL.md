---
name: opportunity-brief
description: Conduct a Marty-Cagan-style opportunity assessment interview and produce a ~2-page Opportunity Brief in Confluence. Covers business objective, customer, problem, success metric, current alternatives, assumptions/risks, and what we don't know yet. Triggers on "opportunity brief", "opportunity assessment", "discovery brief", "who is this for", "why are we building this", "validate this idea", "product discovery", or any request to frame a feature before implementation. One question at a time. Records accepted research gaps as structured Confluence Decision pages with bidirectional links.
metadata:
  author: Fishbowl Team
  version: "0.1"
  tags: planning, product-management, discovery, opportunity-brief
---

# Opportunity Brief — Cagan interview

## Prerequisites

- **jira plugin** (required, hard dependency): `atlassian-api.sh` handles markdown→ADF conversion AND emits the Page Properties macro that the Decisions log index depends on. Without it, Page Properties render as a plain code block and aggregation in Confluence will not work. Locate the helper path with `${CLAUDE_PLUGIN_ROOT}/scripts/locate-jira-helper.sh` — it prints the absolute path on stdout or exits 1 with a user-friendly install message. Never hardcode the path. **There is no markdown-only fallback; abort if the helper is missing.**
- **Atlassian credentials for the helper** (only needed for commands that hit the network — adding labels, updating pages). If missing, the helper prompts you to run `"$HELPER" setup`, which interactively writes `~/.config/secrets.json` with mode 0600. `markdown-to-adf` (the pure conversion step) works without credentials.
- **Atlassian MCP** (inherited from marketplace-level `.mcp.json`, authorized to `fbinv.atlassian.net`). Tools used: `searchConfluenceUsingCql`, `getConfluencePage`, `createConfluencePage`, `updateConfluencePage`.
- **Git user.email configured** — used to derive the pseudonymous `author_hash` for Page Properties and telemetry.
- **`jq`** — used by helper scripts for JSON parsing. Present on the marketplace's recommended toolchain.

Load these references before the first user-facing line:

- [references/persona.md](../../references/persona.md) — coach voice, pushback style, citation boundaries.
- [references/cagan-methodology.md](../../references/cagan-methodology.md) — the four questions, the four risks, Fishbowl framing.
- [references/interview-tactics.md](../../references/interview-tactics.md) — one-question-at-a-time, AskUserQuestion use, handling "I don't know."
- [references/artifact-templates/opportunity-brief.md](../../references/artifact-templates/opportunity-brief.md) — markdown skeleton for the final artifact.
- [references/confluence-destinations.md](../../references/confluence-destinations.md) — default destinations + per-project overrides.
- [references/decision-log.md](../../references/decision-log.md) — decision page structure + how to link bidirectionally.

## Step 1 — Session setup

Generate a session ID (`uuidgen` or `date +%s`-suffixed) and create the scratch directory:

```
${CLAUDE_PLUGIN_DATA}/sessions/<session-id>/draft.md
```

Initialize the scratch with the artifact-template skeleton. All interview answers accumulate here during the session.

If `$ARGUMENTS` references an existing Confluence draft page ID or a scratch session ID, load that instead and resume.

## Step 2 — Frame the session

One sentence, in-persona:
> *"We'll work through a short set of questions — customer, problem, outcome, and what we know or don't — and turn it into a two-page brief published to Confluence. I'll ask one thing at a time; say 'I don't know' any time and we'll record it as something to learn."*

Then ask Step-3 Question 1.

## Step 3 — The interview

Ask in order. **One question per turn.** Use `AskUserQuestion` when answers enumerate cleanly (see tactics below). Use open text otherwise. After each answer, write it to the scratch file in the appropriate section, then ask the next question.

### Q1 — Business objective

*"What Fishbowl business objective is this work serving?"*

Open text. Listen for: revenue, retention, cost reduction, strategic differentiation, compliance, technical-debt reduction. If the answer is hand-wavy ("it'll be cool"), push back politely: *"That's a reason to build it, but what does Fishbowl get? How does this change the business?"*

### Q2 — Customer (specifically)

*"Who specifically is this for?"*

Multi-choice starting point (AskUserQuestion):
- "A named customer / customer segment I can describe"
- "An internal user role (support, warehouse ops, finance, etc.)"
- "A new market we're not serving yet"
- "I don't know yet — help me think about who"

On "I don't know" → coach per [references/interview-tactics.md](../../references/interview-tactics.md): suggest who might know (customer success, support, sales), record as research next-step, move on.

### Q3 — Problem from the customer's perspective

*"What can't they do today — in their words, not yours?"*

Open text. Listen for workaround descriptions ("they copy-paste data from…", "they call us because…"). If the answer is framed as "they need <feature>," push: *"That's a solution. What's the problem underneath it?"*

### Q4 — Success metric

*"How will we know this worked? What's the metric that should move, by how much, by when?"*

AskUserQuestion:
- "A specific business KPI I can name (revenue, retention, usage rate, etc.)"
- "Leading indicator only (feature adoption, task completion time)"
- "Customer-satisfaction signal (NPS, support tickets)"
- "I don't know — help me pick"

Push back on "ship it" as a success metric. Shipping is not success.

### Q5 — Current alternatives

*"What do people do today when they hit this problem?"*

Open text. Look for: manual workaround, competitor tool, internal tool, nothing. Missing alternatives are a flag — it might mean the problem is not real.

### Q6 — Assumptions and risks

Ask: *"What are the biggest assumptions we're making? Which would collapse the whole thing if wrong?"*

Then walk Cagan's four risks with the user:
- **Value risk** — will customers use / pay?
- **Usability risk** — can they figure it out?
- **Feasibility risk** — can we build it?
- **Business viability risk** — does it work for the business (legal, financial, brand)?

Record each as a bullet with a one-line hypothesis.

### Q7 — What we don't know yet

*"What would you need to learn before you'd bet engineering cycles on this?"*

Open text. Capture each unknown as a bullet. Do not let the user say "nothing" unless all prior answers were confident — if they hand-waved on Q2–Q5, name those as unknowns here.

### Q8 — Stop condition

After Q7, check: does the brief have any bullets in "what we don't know yet"?

- **If yes**: ask whether to (a) proceed to publish as-is (status: `research-pending`), or (b) accept a gap via decision-log and proceed.
- **If no**: the brief advances to `ready-for-prd` status.

## Step 4 — Handling "I don't know" / "skip"

Do not silently skip. See [references/interview-tactics.md](../../references/interview-tactics.md) for the full playbook. Summary:

1. Name the gap: *"OK — let's record this as a research next-step."*
2. Coach on who to ask: suggest 1-2 concrete sources (support, a named team, a data source).
3. Offer the decision-log path if the user wants to proceed without filling the gap: *"If you want to move forward on this before knowing, we'll record that as a decision with the risk you're accepting."* Use [references/decision-log.md](../../references/decision-log.md) to create the decision page (see Step 6).

## Step 5 — End-of-interview summary

Show the user the full draft as markdown. Ask if anything needs edit before publishing.

## Step 6 — Decision-log entries (if any gaps accepted)

For each research gap the user chose to accept instead of resolve:

1. Create a Confluence page under the *Decisions log* parent (see [references/decision-log.md](../../references/decision-log.md)). Title: `DEC-YYYY-MM-DD-<short-slug>`.
2. Populate Page Properties: `decision_id`, `date`, `author_hash`, `artifact_refs` (empty for now — filled after brief publish), `gap_category` (pick from enum based on which Cagan question was skipped), `risk_accepted` (the user's own words), `re_evaluate_by` (today + 30 days), `outcome` (empty).
3. The decision pages will be linked to the brief in Step 7, after the brief gets its page ID.

## Step 7 — Confluence publish

Look up the destination from settings (default: PE › *Product requirements* ID 51642542). Show the destination explicitly:

> *"I'll publish this to PE › Product requirements with labels `discovery` and `draft`. OK to proceed? (y / change destination / N)"*

On yes:

1. Render the scratch markdown to ADF using the jira plugin's helper. Resolve the helper path via the shared locator:
   ```bash
   HELPER="$(${CLAUDE_PLUGIN_ROOT}/scripts/locate-jira-helper.sh)" || exit 1
   ADF_BODY="$("$HELPER" markdown-to-adf < draft.md)"
   ```
   Never hardcode the helper path — the locator handles the expected sibling layout and non-standard install fallbacks. **If either step fails, STOP and report the error to the user verbatim. Do NOT fall back to sending markdown through `createConfluencePage` with `contentFormat: markdown` — that path cannot emit the Page Properties macro and will silently produce a broken page.** If the failure is a credentials error from the helper, point the user at `"$HELPER" setup` and wait for them to complete it before retrying.
2. Create the page: `mcp__plugin_atlassian_atlassian__createConfluencePage` with `contentFormat: "adf"` and the ADF JSON from step 1 as `body`. Capture the returned page ID.
3. Add the `discovery` and `draft` labels via the helper:
   ```bash
   "$HELPER" confluence-label-add <PAGE_ID> discovery draft
   ```
   The MCP `createConfluencePage` tool does not accept labels, so this step is mandatory — without it, the Page Properties Report macro's label-based filter cannot find the page.
4. For each decision page from Step 6: update its `artifact_refs` field with the new brief page ID and add a bidirectional link in the brief page's "Decisions accepted during discovery" section.

On "change destination": ask for the new parent page ID, save it in the settings file for next time.

On N: keep the scratch, print the scratch path, and exit.

## Step 8 — Finalize or leave as draft

Ask: *"Ready to finalize this brief (remove the `draft` label) or keep iterating?"*

On finalize: remove the `draft` label. Status → `research-pending` if unknowns exist, `ready-for-prd` otherwise. Clean up scratch directory.

On keep iterating: leave the `draft` label. Keep scratch (so session can resume).

## Step 9 — Sentiment + telemetry

Before fully exiting, ask once:

> *"Quick sentiment check — was this session helpful / mixed / not useful / painful? (skip ok)"*

Then: *"Anything specific you'd change? (Enter to skip)"*

Log the install event (if first run) and the session event via MCP `updateConfluencePage` per [references/telemetry.md](../../references/telemetry.md). Skill name = `opportunity-brief`; artifact type = `opportunity-brief`; populate the full field list there.

If `telemetry.enabled == false`, skip the sentiment prompt and all log writes. If `tracker_page_id` is missing from settings, print the one-line note from [references/telemetry.md](../../references/telemetry.md) and continue.

## Never

- Never bombard with questions. One per turn.
- Never write a cold Cagan question without first loading the persona and methodology references.
- Never impersonate Marty Cagan or use first-person framings that imply you authored his work. See [references/persona.md](../../references/persona.md).
- Never proceed silently past a gap. Either record it in "what we don't know yet" or create a decision page.
- Never publish without explicit user confirmation of the destination.
- Never fall back to sending markdown directly through the Atlassian MCP `createConfluencePage` when the helper's `markdown-to-adf` fails. The markdown path cannot emit the Page Properties macro and will produce a silently broken page. If the helper is unavailable, stop and tell the user.