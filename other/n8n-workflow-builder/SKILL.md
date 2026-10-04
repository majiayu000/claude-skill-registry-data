---
name: n8n-workflow-builder
description: Build the proof-of-concept automation that backs a freelance bid — turns a drafted gig's solution shape into a real, validated n8n workflow via the n8n Cloud MCP (SDK flow), publishes it, and writes the live workflow URL back onto the gig's Notion row. The Prove phase of the Inbound Gig Engine.
allowed-tools: Read, Grep, Glob, Bash, mcp__claude_ai_n8n_Cloud__get_sdk_reference, mcp__claude_ai_n8n_Cloud__get_workflow_best_practices, mcp__claude_ai_n8n_Cloud__search_nodes, mcp__claude_ai_n8n_Cloud__get_node_types, mcp__claude_ai_n8n_Cloud__validate_node_config, mcp__claude_ai_n8n_Cloud__validate_workflow, mcp__claude_ai_n8n_Cloud__create_workflow_from_code, mcp__claude_ai_n8n_Cloud__publish_workflow, mcp__claude_ai_n8n_Cloud__get_workflow_details
area: Sales
use_for: "Build + publish a real n8n workflow that demonstrates the solution for a drafted gig, via the n8n Cloud MCP SDK flow, with the live URL written back onto the gig row"
deps:
  mcp: ["n8n Cloud", "Notion", "Slack"]
  gateway: ["FiveAgents (logging)"]
  files: ["product.md", "brand.md", "sales.md"]
  env: ["`${BRAND}_GIGS_DB` (created by `gig-prospector`)", "`${BRAND}_N8N_PROJECT` (opt — target n8n project/folder)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.17.0 | June 21, 2026 |

**Description:** Build the proof-of-concept n8n workflow that backs a freelance bid — from a drafted gig's solution shape to a real, validated, published workflow, with the live URL written back onto the gig's Notion row.

### Change Log

**v2.17.0** — June 21, 2026
- New skill (Sales). The **Prove** phase of the **Inbound Gig Engine** (`gig-prospector → gig-proposal-writer → n8n-workflow-builder → vsl-demo-producer`). Reads the solution shape `gig-proposal-writer` recorded on a `${BRAND}_GIGS_DB` row and builds a real, runnable n8n workflow through the **n8n Cloud MCP** — the official SDK flow (`get_sdk_reference → get_workflow_best_practices → search_nodes → get_node_types → validate_node_config → validate_workflow → create_workflow_from_code → publish_workflow`), **never** guessed JSON or the legacy REST script. Follows the brand's design rules (start with a trigger, 3–6 steps, one linear chain, label nodes in the client's language, end with a visible outcome). Writes the live workflow URL + ID back onto the gig row and advances `Status` to `Workflow Built`. Replaces the legacy `create_n8n_workflow.py` REST path from the ai-agency prototype.

---

# SKILL.md — n8n Workflow Builder

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

**You MUST use the n8n Cloud MCP SDK flow — never hand-write workflow JSON and never use the legacy REST script.** The n8n MCP server's own instructions are authoritative; follow them in order (SDK reference → best practices → node discovery → node types → per-node validation → full validation → create → publish). Guessing SDK syntax or node parameters produces invalid workflows.

## Role

You are an automation engineer for the active brand. Your job is to take **one** drafted gig — a freelance job the brand intends to bid on, already written up by `gig-proposal-writer` — and build the small, real, **visually legible** n8n workflow that proves the brand can deliver it. The workflow is a demo asset: it must look right on screen (clean left-to-right chain, labels in the client's words) and validate cleanly, but it does not need live credentials wired — it's the proof, not the production deployment. You build through the n8n Cloud MCP, validate before publishing, and write the live URL back so `vsl-demo-producer` can screenshot it.

---

## When to use

Use this skill when:
- A gig in `${BRAND}_GIGS_DB` is `Status="Drafted"` and needs its proof workflow
- Rebuilding a workflow after the founder changes the solution shape or step count
- Producing a standalone demo workflow for a category (pass the shape directly)

Do NOT use this skill for:
- Writing the bid copy → use `gig-proposal-writer` (this skill follows it)
- Screenshotting the workflow + recording instructions → use `vsl-demo-producer` (the next phase)
- Production automations with live credentials and real data → that's a paid delivery engagement, out of scope for a demo
- Discovering gigs → use `gig-prospector`

---

## Inputs required

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| Gig | Yes | A Notion page URL/ID in `${BRAND}_GIGS_DB`, typically `Status="Drafted"`. Must carry a `Category` (solution shape) from `gig-proposal-writer` |
| Solution shape | From gig | The `Category` on the gig row; if absent, infer from the job description + `product.md` and note it |
| Step count | Optional | Default 3–6 nodes incl. the trigger |
| n8n project/folder | Optional | `${BRAND}_N8N_PROJECT`; else the default project |

---

## Step-by-step workflow

### Step 1 — Read brand context + the gig

Read `product.md` (the services/tools the brand actually delivers — the workflow must reflect a service the brand sells), `brand.md` (locale/voice for naming), and `sales.md` (any standard delivery shape). Then fetch the gig — it **must** live in `${BRAND}_GIGS_DB`:

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: <gig page URL or page ID>
```

Extract `title`, `Category` (solution shape), the job description, and the plain-language plan steps from the `## Cover Letter` block `gig-proposal-writer` wrote. If `Category` is missing, infer the shape from the description + `product.md` and record it back on the row. If the gig is not yet `Drafted`, tell the founder to run `gig-proposal-writer` first (the plan steps come from the bid).

### Step 2 — Load the n8n SDK reference + best practices (mandatory, in order)

Per the n8n Cloud MCP instructions:

1. `mcp__claude_ai_n8n_Cloud__get_sdk_reference` — **required before writing any workflow code.** Also pull the `guidelines` and `design` sections. Do not guess SDK syntax.
2. `mcp__claude_ai_n8n_Cloud__get_workflow_best_practices` — call once per relevant technique for this gig's shape (e.g. `"scheduling"`, `"chatbot"`, `"triage"`, `"lead generation"`). If unsure which apply, call with `technique="list"` first.

### Step 3 — Discover nodes + get their exact types

Map the gig's plain-language plan (Step 1) to concrete nodes:

1. `mcp__claude_ai_n8n_Cloud__search_nodes` — one query per service/utility you need (e.g. `["schedule trigger", "http request", "gmail", "set", "if"]`). Note the discriminators (resource/operation/mode) in results.
2. `mcp__claude_ai_n8n_Cloud__get_node_types` — pass **all** node IDs you plan to use, including discriminators, to get exact TypeScript parameter definitions. Do not guess parameter names.

Prefer nodes that match tools named in `product.md` so the demo reflects the brand's real stack.

### Step 4 — Design the workflow (brand demo rules)

Honor the ai-agency design rules for a legible demo (from the legacy `directives/generate_n8n_workflow.md`):

- **Start with a trigger** (manual / webhook / schedule), matched to the gig (recurring job → schedule; inbound request → webhook; on-demand demo → manual).
- **3–6 nodes total**, one **linear** left-to-right chain — no sprawl, no parallel branches unless the gig truly needs an `if`/`switch`.
- **End with a visible outcome** (send email, post to Slack, write a row, respond to webhook) so the demo has a payoff on screen.
- **Label every node in the client's language**, not node-type jargon ("Find New Leads", not "HTTP Request"). This is what makes the screenshot sell.
- Map each plan step from the cover letter to exactly one node so the workflow mirrors the pitch.

### Step 5 — Validate per-node, then write the code

- As you settle each node's config, call `mcp__claude_ai_n8n_Cloud__validate_node_config` (it can check several candidate configs in one call) so param/discriminator errors surface before they're buried in a full-graph run.
- Write the workflow using the SDK patterns from the reference and the exact param names from Step 3. Lay nodes out left-to-right and wire them sequentially.

### Step 6 — Validate the full workflow, then create + publish

1. `mcp__claude_ai_n8n_Cloud__validate_workflow` — must pass clean. Fix and re-validate; do not create a workflow that fails validation.
2. `mcp__claude_ai_n8n_Cloud__create_workflow_from_code` — create it (target `${BRAND}_N8N_PROJECT` if set). Name it for the gig: `"{Brand} — {client solution} demo"`.
3. `mcp__claude_ai_n8n_Cloud__publish_workflow` — publish so it has a stable, shareable URL.
4. `mcp__claude_ai_n8n_Cloud__get_workflow_details` — capture the workflow `id` and live URL for the gig row + the screenshot phase.

Do **not** execute the workflow against live services — it's a demo. If a node needs credentials to validate, leave a clearly-labeled placeholder credential; never wire the client's real accounts.

### Step 7 — Write the workflow back onto the gig row

**Ensure properties exist** on `${BRAND}_GIGS_DB` (idempotent — add only if missing):

```
Use mcp__claude_ai_Notion__notion-update-data-source (only for properties not already present):
- Workflow URL  : url
- Workflow ID   : rich_text
- Node Count    : number
```

Then update the page and append a `## Demo Workflow` body block listing the node chain (client-language labels, in order):

```
Use mcp__claude_ai_Notion__notion-update-page:
- page_id: <gig page id>
- properties: {
    "Status":       "Workflow Built",   // adds the option if new
    "Workflow URL": "<live n8n url>",
    "Workflow ID":  "<id>",
    "Node Count":   <n>
  }
```

### Step 8 — Save local backup + Slack the founder

Save a record to `outputs/{brand}/sales/gigs/workflows/Workflow_{gig-slug}_{DDMonYYYY}.md` (node chain, URL, validation result).

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"select:mcp__claude_ai_Slack__slack_send_message"` to load the deferred tool schema.**

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "$SLACK_NOTIFY_USER"
- text: "🛠️ [{brand}] Demo workflow built — {gig title}
         {node count} nodes · {trigger} → … → {final visible step}
         Live workflow: {workflow_url}
         Next: /link-skills:vsl-demo-producer to capture the screenshot + recording script.
         Gig row: {notion_url}"
```

---

## Output format

**Save location:** `outputs/{brand}/sales/gigs/workflows/`
**Naming:** `Workflow_{gig-slug}_{DDMonYYYY}.md`

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: n8n-workflow-builder
Brand: {brand}
Gig: {gig title}
Category: {solution shape}
Workflow URL: {live n8n url}
Workflow ID: {id}
Node Count: {n}
Validation: passed
Notion Gig Row: {url}
Status: Workflow Built
---
```

**Output sections:**
1. **Node chain** — table: order, client-language label, n8n node type, role in the demo
2. **Build notes** — techniques pulled from best-practices, any node substitutions, placeholder credentials used
3. **Links** — live workflow URL, gig row URL

---

## Quality checklist

- [ ] Active brand resolved; `agents/link.md` + `product.md` read first
- [ ] Gig confirmed in `${BRAND}_GIGS_DB`; `Category` present (or inferred + recorded)
- [ ] SDK reference + relevant best-practices pulled **before** writing any workflow code
- [ ] Node types fetched via `get_node_types` — no guessed parameter names
- [ ] Workflow starts with a trigger, is a 3–6 node linear chain, ends with a visible outcome
- [ ] Every node labeled in the client's language, one node per plan step from the bid
- [ ] Nodes reflect tools the brand actually sells (`product.md`) — no fabricated capabilities
- [ ] Each node config passed `validate_node_config`; full workflow passed `validate_workflow`
- [ ] Workflow created **and published**; live URL + ID captured via `get_workflow_details`
- [ ] No live client credentials wired — placeholders only (it's a demo, not a deployment)
- [ ] Workflow URL + ID + node count written to the gig row; `Status="Workflow Built"`
- [ ] Local backup saved; Slack digest sent to `$SLACK_NOTIFY_USER`
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "n8n-workflow-builder"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "gig_title": "<title>",
    "category": "<solution shape>",
    "node_count": 0,
    "trigger_type": "<manual|webhook|schedule>",
    "validation": "passed",
    "published": true,
    "workflow_url": "<live n8n url>",
    "workflow_id": "<id>",
    "status_after": "Workflow Built",
    "notion_gig_url": "<url>",
    "output_path": "outputs/{brand}/sales/gigs/workflows/",
    "deliverable": "Workflow_{gig-slug}_{DDMonYYYY}.md"
  }
```

---

## Part of the pipeline

The **Prove** phase of the **Inbound Gig Engine**:

```
gig-prospector (Discover) → gig-proposal-writer (Write, Status="Drafted")
  → n8n-workflow-builder (this skill — real workflow + URL, Status="Workflow Built")
  → vsl-demo-producer (Demo — screenshot + recording instructions, Status="Demo Ready")
```

On-demand, one gig at a time. Uses the n8n Cloud MCP SDK flow exclusively.
