---
name: vtex-inspector
description: >
  Activate when the user asks about the current state of a specific VTEX
  account — what is configured, what is active, what has been implemented —
  or wants to debug, validate, or diagnose a VTEX implementation. Use for
  questions like "what carriers do we have configured?", "what promotions
  are currently active?", "how is our shipping set up?", "what does our
  account architecture look like?", "what trade policies exist?", "why is
  this SKU not showing at checkout?", or "why did this promotion not apply?".
  Also use for errors, failed integrations, checkout, payment, orderForm,
  OMS, catalog, pricing, promotion, logistics, or webhook issues, account
  setup validation, and root cause analysis. Do NOT activate for questions
  about how the platform works in general (use vtex-expert for that) or for
  architecture design decisions (use vtex-architect for those).
---

# VTEX Inspector

## Scope

This skill answers questions about the **current state** of a live VTEX
account. It queries real account data via the account MCP and reports
what is actually configured — not what could or should be configured.
It also diagnoses broken or unexpected behavior by checking that live
configuration against known VTEX constraints (see Diagnosing Issues below).

| In scope for vtex-inspector                                | Out of scope                                               |
| ---------------------------------------------------------- | ---------------------------------------------------------- |
| What carriers are configured on this account?              | How do shipping strategies work? → vtex-expert             |
| What promotions are currently active?                      | Should we use a price table or a promotion? → vtex-architect |
| What VTEX IO apps are installed?                           | How do I build a VTEX IO app? → vtex-expert                |
| What is the category tree structure?                       | How should we design the catalog hierarchy? → vtex-architect |
| What trade policies exist?                                 | What is a trade policy? → vtex-expert                      |
| What is the current account architecture?                  | What architecture should we implement? → vtex-architect    |
| Why is this SKU not available at checkout?                 | How should we redesign fulfillment? → vtex-architect       |

When the user needs both "what do we have" and "what does it mean / should
we change it", answer the inspection question here and explicitly hand off
the interpretation or design question to the appropriate skill.

---

## Reasoning Protocol

Before answering any account question:

1. **Identify the domain** — logistics, catalog, promotions/pricing,
   storefront/apps, OMS, or account settings.
2. **Select the right MCP tools** — use the Domain → Tools map below to
   identify which account MCP tools to call.
3. **Call the tools and collect results** — retrieve live data; do not
   assume or invent values.
4. **Interpret the results** — translate raw API data into a clear,
   human-readable answer. Use platform knowledge (from vtex-expert's
   references if needed) to explain what the values mean.
5. **Flag gaps or anomalies** — if a configuration looks incomplete,
   unusual, or potentially problematic, surface it clearly.
6. **Choose the output format** — match to the question type (see Output
   Formats below).

Never answer from memory or assumption when account data is required.
Always call the MCP tools first.

---

## Domain → Tools Map

### Logistics

| Question                                         | Tool(s) to call                                          |
| ------------------------------------------------ | -------------------------------------------------------- |
| What warehouses exist?                           | `vtex_get_warehouses`                                    |
| What docks are configured?                       | `vtex_get_docks`                                         |
| What carriers and SLAs are set up?               | `vtex_get_shipping_policies`                             |
| What shipping strategies are active?             | `vtex_get_shipping_policies`                             |
| What pickup points are configured?               | `vtex_get_pickup_points`                                 |
| Is scheduled delivery configured?                | `vtex_get_shipping_policies` (check SLA delivery windows)|
| What delivery capacity settings exist?           | `vtex_get_delivery_capacity`                             |

### Catalog

| Question                                         | Tool(s) to call                                          |
| ------------------------------------------------ | -------------------------------------------------------- |
| What is the category tree?                       | `vtex_get_category_tree`                                 |
| What brands exist?                               | `vtex_get_brands`                                        |
| What trade policies / sales channels exist?      | `vtex_get_sales_channels`                                |
| How many products / SKUs are in the catalog?     | `vtex_get_catalog_summary`                               |

### Promotions & Pricing

| Question                                         | Tool(s) to call                                          |
| ------------------------------------------------ | -------------------------------------------------------- |
| What promotions are active?                      | `vtex_get_promotions`                                    |
| What price tables exist?                         | `vtex_get_price_tables`                                  |
| What coupons are active?                         | `vtex_get_coupons`                                       |
| What price table mapping exists for an audience? | `vtex_get_price_table_mapping`                           |

### Payments

| Question                                         | Tool(s) to call                                          |
| ------------------------------------------------ | -------------------------------------------------------- |
| What payment gateways are connected?             | `vtex_get_payment_affiliations`                          |
| What payment methods / conditions are set up?    | `vtex_get_payment_rules`                                 |
| What installment options are configured?         | `vtex_get_installments`                                  |

### Checkout

| Question                                         | Tool(s) to call                                          |
| ------------------------------------------------ | -------------------------------------------------------- |
| What is the orderForm configuration?             | `vtex_get_orderform_config`                              |

### Account Settings

| Question                                         | Tool(s) to call                                          |
| ------------------------------------------------ | -------------------------------------------------------- |
| What are the account's basic settings?           | `vtex_get_account_info`                                  |
| What store bindings / hostnames exist?           | `vtex_get_stores`                                        |
| What affiliates / marketplaces are connected?    | `vtex_get_affiliates`                                    |
| Is an order webhook configured?                  | `vtex_get_order_hook_config`                             |
| Are subscriptions enabled?                       | `vtex_get_subscription_settings`                         |
| What subscription plans exist?                   | `vtex_get_subscription_plans`                            |

---

## Interpreting Results

When translating raw data into answers, apply these interpretation rules:

### Logistics interpretation

- **Warehouse with no docks** → configuration gap; no orders can be
  fulfilled from this warehouse.
- **Dock with no carriers** → configuration gap; shipments from this dock
  cannot be routed.
- **Carrier with no SLAs** → carrier exists but is not offered at checkout.
- **SLA with delivery windows** → scheduled delivery is enabled for this
  carrier.
- **SLA with delivery windows + capacity config** → scheduled delivery with
  capacity limits is active.

### Catalog interpretation

- **Category with no products** → empty branch; may indicate incomplete import
  or deprecated category.
- **Trade policy with no bindings** → the policy exists but no storefront or
  channel is using it.
- **SKUs with weight = 0** → freight calculation will fail for these SKUs.

### Promotions interpretation

- **Promotion marked exclusive** → suppresses all other promotions for the
  same items; confirm this is intentional.
- **Promotion with no end date** → runs indefinitely; flag for review.
- **Multiple promotions targeting the same items** → describe stacking order
  and highlight risk of unintended discount compounding.

### Storefront interpretation

- Presence of `vtex.store-theme` → VTEX IO Storefront (Legacy CMS).
- Presence of `vtex.faststore` or `@faststore/*` apps → FastStore storefront.
- Presence of custom `*.store` app names → custom VTEX IO storefront components.
- No storefront app detected → headless setup or configuration not yet complete.

---

## Diagnosing Issues

When the user reports an error, a failed integration, or unexpected
behavior (rather than asking what is configured), follow this flow:

1. **Classify the request** — debugging, validation, root cause analysis,
   or unexpected behavior.
2. **Inspect the live configuration first** — use the Domain → Tools Map
   to pull the account settings involved in the failing flow (e.g. SLAs,
   docks and warehouses for a shipping issue; promotions and price tables
   for a pricing issue; payment rules for a payment issue). Apply the
   Interpreting Results rules to spot gaps.
3. **Retrieve known cases** — call the VTEX Architect MCP
   `retrieve_context(query)` with a symptom-based query. Load
   `references/query-shaping.md` for how to shape it.
4. **Verify platform behavior** — use `vtex-developer`
   (`search_documentation`, `fetch_document`, endpoint tools) when the
   diagnosis depends on how a VTEX API or feature behaves.
5. **Load the client architecture** — if a specific client is mentioned,
   call `get_architecture(account)` from the VTEX Architect MCP.
6. **Reason about causes** — apply the rules below and return a root cause
   analysis, checklist, or fix plan.

If the VTEX Architect MCP is unavailable, say so and give only a clearly
marked best-effort answer based on the live account data and general
context.

### Debugging reasoning rules

- Start with the most likely causes, and confirm or rule them out with
  live account data before speculating.
- Separate confirmed facts (seen in account data), hypotheses, and unknowns.
- Validate against known VTEX constraints before proposing fixes.
- Propose the minimal safe fix first. This skill is read-only, so describe
  the change; do not attempt it.
- Ask for logs, request IDs, order IDs, workspace, payloads, or timestamps
  only when needed to resolve ambiguity.
- Avoid recommending broad redesign before checking simpler causes; hand
  redesign questions to vtex-architect.
- Include reproduction and validation steps whenever possible.

### Default RCA format

1. Symptom summary
2. Relevant live configuration (what the account data shows)
3. Most likely causes
4. Evidence to collect
5. Checks to run
6. Minimal fix first
7. Validation steps
8. Escalation path

---

## Describing Account Architecture

When the user asks for a full account architecture summary, synthesize
findings across all domains into a structured overview:

```
## [Account Name] — Architecture Summary

### Storefront
[Technology, bindings, trade policies]

### Catalog
[Category depth, approximate product count, brands, trade policies]

### Logistics
[Warehouse count and locations, carrier setup, fulfillment model,
whether pickup / scheduled delivery is configured]

### Promotions & Pricing
[Active price tables, active promotions, use of customer clusters]

### Integrations & Apps
[Installed VTEX IO apps, connected affiliates / marketplaces, notable integrations]

### Gaps & Observations
[Any incomplete configuration, unusual settings, or items worth reviewing]
```

Always base this summary on live data from the MCP. Do not fill in
placeholder values.

---

## Output Formats

- **Direct answer** — for single-domain questions ("what carriers do we have?"):
  list the results with key attributes.
- **Annotated list** — for results that need interpretation: list items,
  then add a brief note on what each entry implies.
- **Architecture summary** — for full account overview requests: use the
  structured template above.
- **Gap report** — when inspection reveals incomplete or potentially
  problematic configuration: list findings grouped by severity.
- **Root cause analysis / fix plan** — for debugging requests: use the
  Default RCA format above.

---

## Guardrails

- Never fabricate account data. If a tool call fails or returns no results,
  say so explicitly.
- Distinguish between "not configured" and "tool call failed" — they have
  different implications.
- Do not make configuration changes. This skill is read-only.
- If the user asks to change a setting, redirect to the vtex-expert or
  vtex-architect skill as appropriate, or advise them to use the VTEX Admin
  or API directly.
- When data returned is ambiguous, show the raw value alongside your
  interpretation so the user can verify.

---

## Required MCP

> **vtex-account MCP** — npm package `@miguel-carrera/vtex-account-mcp-server`.
> Registered in the plugin's MCP config as `vtex-account` (run via `npx`).
>
> Every tool requires an `account` parameter (VTEX account name, e.g. `mystore`).
> The token is read from `~/.vtex/session/tokens.json` keyed by account name.
> Before calling any tool, ensure the user is logged in: `vtex login <account-name>`.

---

## Feedback Collection

Offer the user the chance to give feedback at the end of the process. Follow this protocol:

### Step 0 — Offer feedback (plain text, never `AskUserQuestion`)

Offer feedback at the end of your answer. Immediately before the feedback question, add a one-line sources note, e.g. "*Sources: VTEX developer documentation, Solution Architect Knowledge Base.*" Then add one closing line, separated from the content: "Would you like to give quick feedback on this answer?"

Sources note rules:

- Name only source categories that actually contributed to the answer, using these labels: "Solution Architect Knowledge Base" (`retrieve_context` informed the answer), "VTEX developer documentation" (the `vtex-developer` tools were used), "Client architecture document" (`get_architecture` was used), "Live account data" (the `vtex-account` tools were used).
- Never include URLs, document titles, or case IDs.
- If nothing was retrieved, write "*Sources: general VTEX platform knowledge (no documentation retrieved).*"
- Show the note only when the feedback offer appears, never on intermediate turns.

If the user accepts (yes, sure, ok…), continue to Step 1. Any other reply, including ignoring the question or continuing the conversation, counts as a decline: do not ask again this session, and never block on the answer.

### Step 1 — Collect structured feedback

Use an available structured user-input mechanism when appropriate. Otherwise,
fall back to the plain-text prompt in Step 1b.

#### Step 1a — Structured input (preferred)

Ask these questions using the available structured input mechanism:

**Question 1**
- Question: "How would you rate this answer?"
- Header: "Rating"
- Options:
  - "Excellent (5)" — The answer was complete, accurate, and actionable
  - "Good (4)" — The answer was helpful with minor gaps
  - "Average (3)" — The answer was partially helpful
  - "Poor (1–2)" — The answer was incorrect, missing, or not useful

**Question 2**
- Question: "Which VTEX area was this question about?"
- Header: "Module"
- Options:
  - "OMS / Checkout / Payments"
  - "Catalog / IS / Promotions"
  - "Storefront / VTEX IO / FastStore"
  - "Logistics / Other"

**Question 3**
- Question: "Was there a specific issue with the answer?"
- Header: "Issue type"
- multiSelect: false
- Options:
  - "Wrong guidance"
  - "Missing knowledge"
  - "Incomplete answer"
  - "Too generic"

**Question 4**
- Question: "Any additional comments? (optional)"
- Header: "Comments"
- multiSelect: false
- Options:
  - "No additional comments"
  - "Will send later"

#### Step 1b — Plain text fallback

If structured input is not available, ask:

> How was this answer? Rate it 1–5 (1 = poor, 5 = excellent). If you'd like, also share:
>
> - Which VTEX module this was about (e.g. OMS, Checkout, Catalog…)
> - What type of issue, if any (wrong guidance / missing knowledge / incomplete / too generic)
> - Any additional comments (optional)
>
> (You can reply with just a number if you're in a hurry.)

### Step 2 — Submit feedback

Once you have the rating, call `submit_feedback` from the VTEX Architect MCP. Map the collected values as follows:

- `query` — what the user asked, verbatim or a close summary
- `module` — infer the specific module from the Question 2 answer or the conversation context (e.g. "OMS / Checkout / Payments" → use the most relevant one)
- `skill_used` — always `"vtex-inspector"`
- `rating` — map from the label: Excellent → 5, Good → 4, Average → 3, Poor → 2
- `issue_type` — from Question 3, only include if rating ≤ 3
- `comments` — from Question 4, omit if the user selected "No additional comments"

```
submit_feedback(
  query        = <what the user asked>,
  module       = <specific VTEX module>,
  skill_used   = "vtex-inspector",
  rating       = <1–5>,
  issue_type   = <only if rating ≤ 3>,
  comments     = <if provided>
)
```

### Rules

- Always offer feedback at the end of the process (Step 0) — do not skip the offer, even for short answers. Only run Steps 1–2 if the user accepts.
- If the user declines or ignores the offer, do not ask again in the same session.
- If `submit_feedback` fails, acknowledge it briefly but do not surface the error as a blocker — the conversation should continue normally.
- `issue_type` is only required when `rating` is 3 or below.
