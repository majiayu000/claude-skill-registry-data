---
name: cargo-billing
description: "Understand what Cargo is costing — remaining credits, usage broken down by workflow, connector, or agent, subscription state, and invoice history. Triggers: \"how many credits do I have left\", \"what did that cost\", \"why is my bill so high\", \"am I about to run out\", \"will this fit in our budget\", \"show me my invoices\", \"how much have I spent this month\", \"what plan am I on\", \"what do I get for free\", \"how many free credits\", \"can I afford this run\", \"add a card\", \"update my payment method\", \"why was my card declined\". Needs a token with admin access. Skip when: attributing spend to specific nodes or cutting a play cost — use cargo-diagnostics."
version: "2.0.1"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/cargo-skills
metadata:
  author: getcargo
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/cargo-skills
---

# Cargo CLI — Billing

Billing and credit management: pulling usage metrics, checking subscription status, viewing invoices, and managing credits.

> See `references/response-shapes.md` for full JSON response structures.
> See `references/troubleshooting.md` for common errors and how to fix them.
> See `references/examples/usage-metrics.md` for usage metric and subscription examples.

## Bootstrap

Already signed in (`cargo-ai whoami` returns a workspace)? Skip to the next section.

```bash
npm install -g @cargo-ai/cli            # no global install? prefix every command with `npx @cargo-ai/cli`
cargo-ai login --email you@company.com  # emailed code, no browser; creates the account on first use
                                        # alternatives: --oauth (browser) · --token <api-token> (CI)
cargo-ai whoami                         # confirm the active workspace before any write
```

Every command prints JSON to stdout; failures exit non-zero with `{"errorMessage": "..."}`. Anything that creates a run or a batch is async — pass `--wait-until-finished` or poll the matching `get`. **Admin-only:** every command in this skill requires a token with admin access on the workspace. Non-admin tokens return `{"errorMessage":"forbidden"}`. When the full skill bundle is installed, [`../cargo/references/prerequisites.md`](../cargo/references/prerequisites.md) adds the CLI version pin, token scopes, and the admin-only surface.

## Discover resources first

Usage metrics can be filtered and grouped by resource UUID. Discover them before querying.

```bash
cargo-ai orchestration play list            # all plays (name, workflowUuid)
cargo-ai orchestration tool list            # all tools (name, workflowUuid)
cargo-ai ai agent list                     # all agents (uuid, name)
cargo-ai connection connector list          # all connectors (uuid, name, integrationSlug)
cargo-ai storage model list                # all models (uuid, name, slug)
```

## Quick reference

```bash
cargo-ai billing usage get-metrics --from <YYYY-MM-DD> --to <YYYY-MM-DD>
cargo-ai billing usage get-metrics --from <YYYY-MM-DD> --to <YYYY-MM-DD> --group-by workflow_uuid
cargo-ai billing subscription get
cargo-ai billing subscription get-invoices
cargo-ai billing subscription update-payment-method --card-number <number> --card-exp <MM/YYYY> --card-cvc <cvc>
cargo-ai billing subscription create-portal-session
```

## Estimating cost before running a batch

Before triggering a large batch, estimate credit consumption to avoid unexpected charges.

**Step 1 — Check current credit balance:**

```bash
cargo-ai billing subscription get
# → subscriptionAvailableCreditsCount - subscriptionCreditsUsedCount = remaining credits
```

**Step 2 — Estimate cost from a sample run:**

Run the workflow on a single record first and measure credits consumed:

```bash
# Run on one record
cargo-ai orchestration run create --workflow-uuid <uuid> --data '{...}'
# → poll to completion

# Check credits used for that run
cargo-ai billing usage get-metrics \
  --from <today> --to <today> \
  --workflow-uuid <uuid>
# → metrics[].items[] for that workflow (the response has one key, `metrics` — there is no `totalUsage`)
```

**Step 3 — Project batch cost:**

```
estimated_cost = (credits_per_record × number_of_records)      # provider actions
               + (nodes_per_record × number_of_records / 100)  # execution charge
```

The second term is the 0.01-credit-per-execution platform charge ("The execution charge" below). A sample run measures it for free — the record's execution count is `length(run.executions)`, or one row of `--unit orchestration.executions` for the sample window. Leave it out and every step-heavy graph is under-quoted.

Compare against `subscriptionAvailableCreditsCount - subscriptionCreditsUsedCount` before proceeding.

**Step 4 — Monitor during the batch:**

```bash
# Check running costs mid-batch
cargo-ai billing usage get-metrics \
  --from <start-date> --to <today> \
  --workflow-uuid <uuid>
```

**Cost levers:**

| Action | Effect |
|---|---|
| Use a cheaper model (e.g. `gpt-4o-mini` vs `gpt-4o`) | Significant reduction for AI nodes |
| Add `filter` nodes early in the graph | Skip ineligible records before expensive connector calls |
| Set `fallbackOnFailure: false` | Stop the run early on failures instead of continuing to downstream nodes |
| Reduce `maxSteps` on agent nodes | Limit how many tool calls an agent can make per record |
| Cut node count — collapse chained `variables`, fold branch pairs into one `switch` | 0.01/execution × records; the only lever for a graph whose spend is steps, not providers |

> To find out **which** node or provider dominates a play's spend before picking a lever, follow the attribution runbook in [`../cargo-diagnostics/references/play-optimize-credits.md`](../cargo-diagnostics/references/play-optimize-credits.md).

## Usage metrics

Pull credit and usage data for any time range, optionally filtered and grouped.

```bash
# Basic usage for a period
cargo-ai billing usage get-metrics --from <start-date> --to <end-date>

# Group by dimension
cargo-ai billing usage get-metrics --from <start-date> --to <end-date> --group-by workflow_uuid
cargo-ai billing usage get-metrics --from <start-date> --to <end-date> --group-by connector_uuid
cargo-ai billing usage get-metrics --from <start-date> --to <end-date> --group-by integration_slug
cargo-ai billing usage get-metrics --from <start-date> --to <end-date> --group-by model_uuid
cargo-ai billing usage get-metrics --from <start-date> --to <end-date> --group-by agent_uuid

# Filter by specific resource
cargo-ai billing usage get-metrics --from <start-date> --to <end-date> --workflow-uuid <uuid>
cargo-ai billing usage get-metrics --from <start-date> --to <end-date> --agent-uuid <uuid>
cargo-ai billing usage get-metrics --from <start-date> --to <end-date> --connector-uuid <uuid>
cargo-ai billing usage get-metrics --from <start-date> --to <end-date> --integration-slug <slug>

# One unit at a time — the three below are the only accepted values
cargo-ai billing usage get-metrics --from <start-date> --to <end-date> --unit billing.credits
cargo-ai billing usage get-metrics --from <start-date> --to <end-date> --unit orchestration.executions
cargo-ai billing usage get-metrics --from <start-date> --to <end-date> --unit storage.records
```

`--group-by` values: `workflow_uuid`, `connector_uuid`, `model_uuid`, `integration_slug`, `agent_uuid`.

Available filters: `--workflow-uuid`, `--model-uuid`, `--connector-uuid`, `--integration-slug`, `--slug`, `--agent-uuid`. Combine with `--group-by` and `--unit`.

### The three usage units

`--unit` takes exactly `billing.credits`, `orchestration.executions`, or `storage.records` — anything else is a `400` that lists them. **With no `--unit`, all three come back interleaved in the same `items[]` array**, and their `count` fields are not the same quantity. Read the unit off the slug:

| Unit | Slugs in `items[]` | What `count` is |
|---|---|---|
| `billing.credits` | `integration.<slug>.action.<action>`, `native.<action>`, `integration.<slug>.chat`, `integration.<slug>.extractor.<name>` | Credits (fractional) |
| `orchestration.executions` | `success`, `error` | **Node executions**, counted one-for-one — not credits |
| `storage.records` | `insert` | Records written |

An unqualified call that shows `{"slug":"success","count":1043}` next to `{"slug":"integration.peopleDataLabs.action.queryPeople","count":174}` is reporting 1,043 *executions* beside 174 *credits*. Pass `--unit` whenever the number is going into an estimate.

### The execution charge

**Every node execution bills 0.01 credits — 1 credit per 100 executions.** It applies to every node kind and every node, including the structural natives that carry no provider price: `branch`, `filter`, `switch`, `split`, `group`, `variables`, `start`, `end`. There is no free step in a workflow.

This charge is **not attributed per node**. `run get` → `executions[].creditsUsedCount` and the `spans.execution_credits_used_count` column both carry the *provider* cost alone, and read `0` on a native node that nonetheless billed. Node-by-node attribution therefore under-counts every graph, and the shortfall grows with step count, not with spend.

The only surface that shows it:

```bash
cargo-ai billing usage get-metrics --from <YYYY-MM-DD> --to <YYYY-MM-DD> --unit orchestration.executions
# → items[] = [{"slug":"success","count":<executions>}, {"slug":"error","count":<executions>}]
# credits = (success + error) / 100
```

Cross-check against the runtime tables, which agree row-for-row:

```bash
cargo-ai orchestration query execute \
  "SELECT execution_status, count() AS executions, count() / 100 AS credits
   FROM spans WHERE execution_started_at >= '<YYYY-MM-DD>' GROUP BY execution_status"
```

**Why it matters for estimates.** A graph's cost has two terms:

```
credits = (provider cost per record × records) + (nodes per record × records ÷ 100)
```

The second term is invisible in the credits cost table, which prices *actions*, not *steps*. It is small next to an action-heavy play (a LinkedIn enrich on every record dwarfs its 8 steps) and dominant on step-heavy, action-light ones — a 12-node routing sweep over 20,000 records is 2,400 credits with no provider call at all. Errored executions bill too, so a graph that fails late bills its whole prefix.

**Tools fan out.** A tool node is one execution *plus* every node inside the tool's own graph, each billed separately. Extracting a subgraph into a tool is a debuggability win, not a cost saving — it adds one execution per record on top of what the internals already cost. When a graph's execution count exceeds its visible node count, tool nodes are the first place to look: group by `node_slug` in `spans` to find them.

## Subscription and credits

```bash
cargo-ai billing subscription get                    # current plan, credits used/available, period dates
cargo-ai billing subscription get-invoices            # invoice history (amounts in cents)
cargo-ai billing subscription get-credit-card         # card on file
cargo-ai billing subscription update-payment-method   # add or replace the card (see below)
cargo-ai billing subscription create-portal-session   # Stripe portal URL for self-service billing
```

Remaining credits = `subscriptionAvailableCreditsCount - subscriptionCreditsUsedCount` from `subscription get`.

**Note:** Invoice amounts are returned in cents. Divide by 100 for the dollar value.

### The free tier

A new account starts with **100 free credits and no card on file**. When `subscription get` shows a fresh or near-fresh balance, answer cost questions against that budget rather than as an abstract number — "you've used 12 of your 100 free credits" is the useful answer to "how am I doing?", and it is also the honest one when the user is deciding whether to keep going.

What 100 credits buys, as ballpark anchors (per-action costs in [`../cargo-gtm/references/credits-cost-table.md`](../cargo-gtm/references/credits-cost-table.md)):

| Work | Cost | 100 credits ≈ |
|---|---|---|
| Source leads — `salesNavigator.searchLeads` | 0.2/record | ~500 leads |
| Enrich from a LinkedIn URL + verified email — `aiArk.enrichPerson` | 0.1 | ~1,000 people |
| Verify an email — `waterfall.verifyEmail` | 0.1 | ~1,000 checks |
| Full contact enrichment — `waterfall.enrichContact` | 2 | ~50 contacts |
| Find a phone — `FullEnrich.findPhone` | 6 | ~16 numbers |

The [quickstart demo](../cargo-quickstart/SKILL.md) spends about **5**. Phone lookups are the fastest way to burn a free tier, so phone is the **guarded lever**: the escalation tier runs 3–7 credits/record, ~10× email, and never belongs in a default chain — it enters a plan only on explicit user request, on qualified leads only. Full spend rules in [`../cargo-gtm/references/cost-discipline.md`](../cargo-gtm/references/cost-discipline.md).

### Adding a card

A workspace holds exactly one card. `update-payment-method` sets it, whether or not one is already on file, and takes the details three ways.

```bash
# Card details — no browser, nothing to hand off
cargo-ai billing subscription update-payment-method \
  --card-number 4242424242424242 --card-exp 12/2030 --card-cvc 123

# Same, but keeps the number out of shell history and the process list
echo '{"number":"4242424242424242","expMonth":12,"expYear":2030,"cvc":"123"}' \
  | cargo-ai billing subscription update-payment-method --card-stdin

# No card details — prints a Stripe-hosted form URL and waits for the card to land
cargo-ai billing subscription update-payment-method
```

**Prefer `--card-stdin`.** Anything passed as a flag is visible in shell history and to any process that can read the process list. Card details go from your machine straight to Stripe in exchange for a token; they never reach the Cargo API, and no output prints them.

**Never invent card details, and never reuse a number from elsewhere in the conversation.** Ask the user for them, or use the no-argument form and hand them the URL.

The no-argument form is the fallback when you have no details to submit: it prints a URL that opens directly on the card form, then polls until the card changes (`--timeout`, `--poll-interval`, `--no-open`). Relay that URL to the user — it works over SSH and in sandboxes.

Either way the card is verified against the issuer before it becomes the default, so a card that cannot be charged fails here rather than silently at the next renewal.

| Failure | What it means | What to do |
|---|---|---|
| `cardDeclined` + `declineCode` | The issuer refused the verification | Read `declineCode`. On a spend-limited virtual card, `insufficient_funds` or a limit code means the budget or merchant restrictions rule us out — ask the cardholder to raise it |
| `authenticationRequired` | The card wants 3-D Secure, which needs the cardholder present | Re-run with no arguments and hand the user the hosted-form URL |
| `paymentMethodNotFound` | The details did not resolve to a usable card | Re-check the number and expiry with the user |

Card updates are rate-limited to **10 per hour per workspace** (shared with setup intents). Retrying a declined card burns that budget — fix the cause rather than looping.

## Help

Every command supports `--help`:

```bash
cargo-ai billing usage get-metrics --help
cargo-ai billing subscription get --help
cargo-ai billing subscription get-invoices --help
```
