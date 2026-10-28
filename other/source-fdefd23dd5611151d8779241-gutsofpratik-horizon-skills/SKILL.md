---
name: carta-portfolio-valuations
description: >
  Portfolio valuations workflow — firm selection, dashboard, bulk-create valuations
  on one or many companies (refresh, manual EV), and dive-in on a single
  valuation. TRIGGER when the user mentions working on, reviewing, or running
  portfolio valuations, takes a closer look at a specific company's valuation, or
  updates the EV / company value (e.g. "work on my valuations today", "review our
  portfolio valuations", "run all my Q2 valuations", "which companies need new
  valuations", "look at MangoCart's valuations", "update the EV for Acme", "set the
  company value for MangoCart", "batch valuations", "auto-run valuations"). DO NOT TRIGGER for 409A
  valuations or cap table valuations, or to turn the valuation tool on for a firm
  (this skill runs valuations only once it is already enabled). Use instead:
  carta-valuations-excel when the user is working in Claude for Excel (a workbook
  is open) — this skill's dashboard and bulk-create UI don't run there.
user-invocable: true
model: inherit
allowed-tools:
  # Carta MCP.
  - mcp__carta__search_tools
  - mcp__claude_ai_Carta__search_tools
  - mcp__2827383e-1775-4df3-b6ff-04d5392f6d18__search_tools
  - mcp__carta__call_tool
  - mcp__carta__read_tool
  - mcp__claude_ai_Carta__call_tool
  - mcp__claude_ai_Carta__read_tool
  - mcp__2827383e-1775-4df3-b6ff-04d5392f6d18__call_tool
  - mcp__2827383e-1775-4df3-b6ff-04d5392f6d18__read_tool
  - mcp__carta__list_accounts
  - mcp__claude_ai_Carta__list_accounts
  - mcp__2827383e-1775-4df3-b6ff-04d5392f6d18__list_accounts
  - mcp__carta__list_contexts
  - mcp__claude_ai_Carta__list_contexts
  - mcp__2827383e-1775-4df3-b6ff-04d5392f6d18__list_contexts
  - mcp__carta__set_context
  - mcp__claude_ai_Carta__set_context
  - mcp__2827383e-1775-4df3-b6ff-04d5392f6d18__set_context
  # Supplies the `environment` that deep-link.md Step 1 maps to the app host.
  - mcp__carta__get_current_user
  - mcp__claude_ai_Carta__get_current_user
  - mcp__2827383e-1775-4df3-b6ff-04d5392f6d18__get_current_user
  - Artifact
  - mcp__visualize__read_me
  - mcp__visualize__show_widget
  - mcp__Claude_Preview__preview_start
  - mcp__Claude_Preview__preview_list
  - mcp__Claude_Preview__preview_eval
  - mcp__Claude_Browser__preview_start
  - mcp__Claude_Browser__preview_list
  - mcp__Claude_Browser__navigate
  - mcp__Claude_Browser__javascript_tool
  - ToolSearch
  - Skill(carta-investors:carta-valuations-excel)
  - Skill(carta-investors:carta-download-tearsheet)
  - Bash(uv run "${CLAUDE_PLUGIN_ROOT}/skills/carta-portfolio-valuations/scripts/build_artifact.py" *)
  - Bash(uv run "${CLAUDE_PLUGIN_ROOT}/skills/carta-portfolio-valuations/scripts/backsolve_calculator.py" *)
  - Bash(uv run "${CLAUDE_PLUGIN_ROOT}/skills/carta-portfolio-valuations/scripts/wait_for_run_request.py" *)
  - Bash(sleep *)
  - Bash(mkdir *)
  - Bash(cat *)
  - Bash(printf *)
  - Bash(mktemp *)
  - Bash(rm -f *)
  - Bash(echo *)
  - Read
  - Write
---

<!-- carta:plugin-version -->
<carta-plugin>carta-investors:6.71.0</carta-plugin>

<!-- Part of the official Carta AI Agent Plugin -->

# Portfolio Valuations Skill

**Plugin root in reference files.** Reference files write the plugin root as a `CLAUDE_PLUGIN_ROOT` variable in braces. Bash does not set that variable, so never run it as written: replace it with the literal plugin root `${CLAUDE_PLUGIN_ROOT}`, keep every quote, and keep the command on one line.

Entry point for the portfolio valuations workflow. The skill is focused
on the **bulk** experience:

- **Bulk mode** — the bulk runner creates draft valuations across **one
  company or many** in a single pass via `create:bulk` (new drafts, and
  copy-from-previous for GPC). Driven by Steps 3–7 in
  `references/bulk/bulk-runner.md`.
- **Dive into one** — open a single candidate, show a recap of where it
  stands, then route the user's free-text request directly to the
  relevant individual flow (cap table, financials, approaches, comps,
  GPC, allocation, finalize). No rigid wizard.

References live in `references/bulk/` (the bulk runner) and
`references/dive-in/` (the individual single-valuation ability flows,
reachable on dive-in). `references/deep-link.md` is shared.
See [README.md](README.md) for a full catalog of reference files, templates, and scripts.

## Gate 0: Redirect if the user is in Excel

Run this before anything else, even if the description-level trigger already
routed here — a skill already loaded earlier in the conversation can still
receive a fresh valuations request without re-reading the description.

```
ToolSearch({ query: "excel worksheet workbook", max_results: 3 })
```

- **If results include tools with "excel", "worksheet", or "workbook" in their
  name** (Claude for Excel is open) → `carta-valuations-excel` owns the
  in-workbook experience end to end, so hand off to it **when it is
  available**. Check your own available-skills listing for
  `carta-investors:carta-valuations-excel`:
  - **Listed** → invoke `Skill(carta-investors:carta-valuations-excel)` and
    stop. Do not run the dashboard, bulk runner, or any dive-in flow here.
  - **Not listed** → **continue with this skill** from Gate 1 below. Do not
    stop, do not tell the user to install anything, and do not go looking for
    the skill on disk — it is genuinely absent from this session, and a user
    in a workbook still needs their valuations work done. Render everything
    as plain markdown per **Step
    2.2c** — in a workbook there is no preview panel and no `Artifact` tool,
    so Step 2.2a will classify the session `env_mode: "inline"` on its own;
    never offer the runner widget or
    the preview panel here. The dive-in flows all work as written; the only
    thing lost is the visual dashboard and runner.
- **Otherwise** (chat / Cowork / Desktop, no workbook) → continue normally
  below.

This is a one-time check per invocation, not a per-step re-check. Once you're
past Gate 0 and continuing here, later dive-in flows (e.g.
`references/dive-in/backsolve/backsolve-excel.md`) still do their own
narrower in-sheet-vs-file detection for their own purposes — that's unrelated
to this top-level redirect.

## Gate 1: Access check — upsell when Portfolio Valuations isn't enabled

**Run this once, on first invocation of the skill, before anything else
except Gate 0.** One probe up front — never a check scattered through the
individual flows. Every step after this may assume access is settled.

A caller without Portfolio Valuations is stopped in one of **two** ways, and
which one they hit depends on how their access is configured:

- **The commands are hidden.** The MCP server filters them out of the tool
  surface, so calling one returns `Unknown tool:
  'portfolio_valuations__…'` — the same error a typo produces.
- **The commands are callable but the API refuses.** The call goes through
  and the API returns an access-denied error — no permissions, or the
  feature isn't enabled for the firm.

Both mean the same thing to the user: they can't use Portfolio Valuations.
Treat them identically. There is no entitlement field to read beforehand, so
the only way to know is to call something and read the response.

**Do not probe with `search_tools`.** Nearly every command in this domain is
registered unindexed, so it is absent from `search_tools` results whether or
not the caller has access. A missing command there means nothing and must
never be treated as an access or health signal.

### The probe

```
read_tool({"name": "portfolio_valuations__search__tickers",
           "arguments": {"query": "aapl"}})
```

Its only parameter is one you supply, so it needs no firm, project, or
candidate — which is why it can run before firm selection, and why it is
cheap. **The payload doesn't matter; only whether the call got through.**

Never show the probe or its output to the user, and never mention tickers —
this is a silent capability check, not a search the user asked for.

### Branching

Show the upsell on **either** of these:

1. **`Unknown tool`** for a `portfolio_valuations__*` name — the commands
   are hidden from this caller.
2. **Access-denied** — the response says the user or their firm has no
   permissions for Portfolio Valuations, or that the feature isn't enabled
   (an authorization failure, typically HTTP 403).

**Anything else** — results, an empty list, a validation error, a timeout, a
5xx, a network failure, a dropped connection → treat the caller as **having
access**. Continue to Step 1 and never mention this gate.

That last rule is deliberately the catch-all: only the two signals above
trigger the upsell. A transient outage or a malformed request must never
tell a paying customer to buy what they already own — when the signal is
ambiguous, assume access and let the real error surface where it occurs.

Cache the outcome for the session. Do not re-probe on re-entry, and do not
re-check before individual calls. If a later call hits either signal after
this gate passed, show the upsell then — but say nothing about the earlier
check.

### The upsell message

Show this instead of the dashboard, runner, or recap — never alongside a
partial render, and never after already showing portfolio data.

Output it as written — do not reword, expand, or add a feature list:

> This feature requires Portfolio Valuations, which isn't enabled for your
> firm yet. You're on the Investors plugin, so unlocking it is
> straightforward — reach out to your Carta account team or
> [request a demo →](https://carta.com/demo/portfolio-valuations/?&utm_medium=product&utm_source=claude&utm_campaign=valuations-plugin-inq-ww-q3-26).
>
> In the meantime, I can help with fund performance data, NAV, TVPI, LP
> documents, or anything else in your current plan.
>
> Request a demo:
> https://carta.com/demo/portfolio-valuations/?&utm_medium=product&utm_source=claude&utm_campaign=valuations-plugin-inq-ww-q3-26

**Always print the bare URL on its own line after the message**, exactly as
shown above. A markdown link is not clickable in a terminal, so the plain
URL is the only way a Claude Code user can reach it — keep it even though it
duplicates the inline link, which is what renders in chat and Cowork.

Keep both URLs exactly as written — the `utm_` parameters attribute the lead
to this plugin, so a trimmed or rebuilt URL loses the attribution. Do not
wrap, break, or shorten the bare URL; a line-wrapped URL won't copy cleanly.

Then stop. Do not present the dashboard-or-company fork, and do not attempt
any further `portfolio_valuations` call this session.

The closing line is an offer, so honour it if the user takes it up: fund
performance, NAV and TVPI go to `carta-explore-data`; LP documents to
`carta-lp-documents`. Those domains are gated separately and generally do
work for a caller without valuations. Route on request — don't
pre-emptively start one.

## End Goal

A valuation candidate is **complete** when all six items below hold.
This checklist is the orchestrator's goal — every routing decision on
dive-in and the entire bulk flow are organized around it.

1. **Cap table data is present** — **`CORPORATION` only.**
   `read_tool({"name": "portfolio_valuations__get__cap_table_summary", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})`
   returns share-class data (non-empty). A c-corp candidate stores its own
   cap-table snapshot, so "is it present?" is a real property of the
   candidate — an empty snapshot blocks allocation.
   - **`LLC_ISSUER` — not applicable.** An LLC's cap table is live issuer
     data that is **not part of the candidate**, so there is nothing here
     to be "present" or missing, and nothing for the user to populate.
     Treat item 1 as N/A on the LLC path — never mark it ⏳ missing, and
     never fetch the LLC cap table just to tick it off. What LLC
     completeness actually depends on is **access** to that cap table,
     which surfaces through item 5 (see below), not here.
2. **Financials are filled in** — **only when the selected methodology
   requires Financials** (see **Required inputs by methodology** below).
   Filled in means `read_tool({"name": "portfolio_valuations__get__financials", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})`
   returns at least one period with revenue/EBITDA populated, OR the user
   has populated financials via the DWH path / manual entry. When no
   selected methodology requires Financials, item 2 is N/A. Never mark it
   ⏳ missing then.
3. **Required approach inputs are in place.** Derive the selected
   methodology from
   `read_tool({"name": "portfolio_valuations__get__approaches", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})`:
   every approach with `isUsed: true`. Then:
   - **Comparables**, when the mapping below requires them: filled in
     means `read_tool({"name": "portfolio_valuations__get__comparables", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})`
     returns at least one comp with `isGpc: true`.
   - **GPC enabled** also needs
     `read_tool({"name": "portfolio_valuations__get__gpc_multiples", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})`
     to return a non-empty multiples set.
   - **Custom Value enabled** (`otherIndicationOfValue.isUsed: true`) also
     needs `get:custom_value.company_value` to be non-zero.
   - No other methodology has an approach-specific input to check here.
   - **Every selected approach has produced a positive value**:
     `get:approaches` → `approachValues.{key}.value` > 0. This is what the
     Step 2.5c checklist shows as each **Calculate {method}** / **Set … value**
     item.
4. **Company value is positive** — `read_tool({"name": "portfolio_valuations__get__valuation", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})`.`companyValue.amount` returns a
   positive number. Zero or negative (e.g. a GPC draft with no comps, left
   with only its debt adjustment) is not done.
5. **Holdings value is positive** — `read_tool({"name": "portfolio_valuations__get__valuation", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})`.`valueOfHoldings.amount`
   returns a positive number. The field is `valueOfHoldings`, not
   `holdingsValue`. The dashboard's `latestValuation.holdingsValue` is a
   different response.
   - **On the LLC path this is where cap-table access bites.** An LLC's
     holdings value comes from a **Niagara** allocation — run through
     `references/dive-in/allocation.md`, which offers it whenever the
     valuation's configuration reports it as supported — and that
     allocation reads the LLC cap table. If the user lacks access to it,
     the allocation fails, holdings value stays zero, and the candidate
     cannot be completed. There is no cheap access flag on the dashboard
     (`hasCorpCapTableAccess` is c-corp-only, with no LLC equivalent), so
     **do not preflight it with an extra call** — that flow's own
     eligibility check (`get:configuration`, before it prompts for
     anything) reports the access problem. When it comes back
     permission-denied, say so plainly rather than reporting a generic
     failure or a zero holdings value:
     > "You don't have access to **{company}**'s cap table, so the
     > allocation can't run. Contact the company to grant access, then we
     > can compute the holdings value."
6. **Status is FINAL** — the candidate's `status` field is `FINAL`.

### Required inputs by methodology

Items 2 and 3 above, the **Required inputs missing** column in
`references/bulk/bulk-results.md`, and the **Inputs:** section of the
valuation summary checklist (Step 2.5c) all read this one table. Keep them
in step: change it here, never in a copy. The checklist lists both inputs
every time and marks the ones this table requires `(Required)`. Its **Next
steps:** section carries a **Calculate {method}** item per selected method
and ends with **Run allocation** (Step 2.5c). Neither is a required input,
so neither is in this table or in the results column; that table has its
own Allocate column.

| Methodology (`get:approaches` key) | Required inputs |
|---|---|
| Custom Value (`otherIndicationOfValue`) | None |
| Post-money (`postMoney`) | None |
| GPC (`gpc`) | Financials, Comparables |
| DCF (`dcf`) | Comparables |
| Backsolve (`backsolve`) | Comparables |
| M&A (`ma`) | Financials |

- **More than one methodology selected** → combine their required inputs
  and list each once. `GPC 50% / M&A 50%` requires Financials and
  Comparables.
- A methodology not in the table requires no inputs here.
- **Filled in:**
  - **Financials**: `get:financials` returns at least one period with
    revenue/EBITDA populated.
  - **Comparables**: `get:comparables` returns at least one comp with
    `isGpc: true`.
- **Required inputs missing** = the required inputs that aren't filled in.

### How to use the goal

The agent does not track checklist state in its head. It re-derives the
state from the API on demand whenever it matters.

In **bulk mode**, the bulk runner creates a draft for every company in
one pass (`create:bulk`). Failures are isolated per-company.

On **dive into one**:
- **When entering a candidate**, silently call
  `read_tool({"name": "portfolio_valuations__get__valuation", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})` and
  `read_tool({"name": "portfolio_valuations__get__approaches", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})`
  to establish where the candidate is on the checklist.
- **While the user is working on the valuation**, end every response with
  the **valuation summary checklist** (Step 2.5c), re-fetched each time.
  That is the always-on view of items 4 and 5 and the required inputs.
- **In lateral-entry routing**, do not proactively suggest next steps.
  Answer what the user asked, then return control. The summary checklist
  is a status line, not a suggestion, so it still renders.
- **When the user explicitly asks** "what's left?", "am I done?",
  "what's next?", surface the checklist with simple status markers
  (✅ done / ⏳ missing). Show only the candidate name and the six items
  — do not surface command names or field names.
- **When the user tries to skip ahead** to a step that isn't ready
  (e.g. "finalize this" while EV is zero), refuse gracefully and point
  at the gap.
- **Never *offer* a step whose prerequisites aren't met.** When you
  compose a next-step menu (a plain-text option list — see UX Rules),
  only include options that are actually runnable right now. In
  particular:
  - **Do not offer "Finalize" until holdings value is positive** — i.e.
    until allocation has run (item 5). Finalize requires both a positive
    company value (item 4) AND a positive holdings value (item 5); if
    either is zero or negative, finalize is **not** a valid next step, so leave it
    off the menu entirely. Offer the missing prerequisite instead ("Run
    allocation", "Set an approach and value").
  - **Do not offer "Run allocation" while company value is zero** — set
    an approach and capture a value first.
  This is proactive gating: the reactive refusal above is the safety net
  for when the user asks directly; this rule stops the premature option
  from ever appearing in a menu you build.

### Trust the API, not the session

If the API state changes underneath you, trust the API. Re-derive the
checklist from a fresh
`read_tool({"name": "portfolio_valuations__get__valuation", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})` /
`read_tool({"name": "portfolio_valuations__get__approaches", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})`
call before deciding what's done.

## UX Rules

- **Never use the `AskUserQuestion` tool** — it is not granted to this
  skill (not in `allowed-tools`) and must not appear anywhere in these
  reference files either. Every follow-up question, anywhere in this
  skill, is asked **inline as plain text**: state the question, list
  numbered options where relevant, and wait for the user's free-text
  reply. This applies uniformly across every `env_mode` (`artifact`,
  `preview-server` and `inline`) — none of them use `AskUserQuestion`.
- When presenting the user with a **single question or choice set**, output
  the options as plain text in the chat message.
- When presenting the user with **multiple fields or a form** (more than
  one question at once), use `show_widget` to render an elicitation form.
- The prose examples below (shown as `> "..."`) are illustrative wording,
  not the delivery mechanism.
- Do not surface raw command names, API field names, HTTP status
  codes, or numeric IDs in chat. Speak in business terms ("revenue",
  "comps", "allocation", "company value", "holdings value").

## User-Facing Output Rules

**Never display any internal IDs** (org_pk, corporationId, firm_id,
project IDs, candidate IDs, etc.) to the user. These are backend
identifiers used only when making API calls.

**When a sub-flow reference exists for the user's intent, you MUST
read the reference and follow it.** Do not paraphrase the concept from
your own knowledge.

**When executing Step 6's bulk pipeline, you MUST run every step
in the path** — including for refreshes, which are not silent clones.
See "Execution discipline" in `references/bulk/bulk-runner.md` for
the full rule, the required mutate sequence, and the post-run
self-check.

**Creating more than one valuation at a time MUST go through
`create:bulk`, never a per-company loop of `create:project` /
`create:project_from_copy`.** This applies everywhere in this skill,
not just the bulk-runner widget path — including `references/md-table-runner.md`'s
text-based runner. Exactly **one** confirmed company is the only case
where the single-company create call (`references/dive-in/create-val.md`)
is correct. `create:bulk`'s `items` array already carries its own
`methodology`/`copyFromPrevious` and `valuationDate` per entry, so there
is no per-company configuration need that justifies looping individual
creates for N>1 companies.

## Table values — render what the command returned

**Every table in this skill**, in any reference file. A value the command
returned goes in the cell as that value — negatives, zeros, and outliers
included. Never substitute `NM`, `N/A`, a blank, or any other
not-meaningful marker, and never drop or bury the row. Comparable
multiples are where this slips most; finance convention prints `NM` there
and this skill does not.

`—` means the response carried nothing — null, absent, or a documented
unset sentinel. That is the only thing it may mean.

Flag an odd value in a line under the table, never by emptying its cell.

## Volatility disclosure — always label the source, show the full table

This skill surfaces **multiple, independent volatility datasets** on
the same candidate, and they are not interchangeable even though every
one of them is "a volatility percentage":

- **OPM volatility** (`get:volatility_comps` called without an
  `allocationId` — see `references/dive-in/allocation.md` Step 4C.2) —
  equity or asset, chosen by the candidate's debt treatment.
- **DLOM volatility** (`get:approaches`'s `dlomVolatilityQuartiles` /
  `dlomVolatilityRegression` / `dlomChaffe` / `dlomFinnerty` — see
  `references/dive-in/allocation.md` Step 5.2) — its own comp-derived
  distribution, computed independently of the OPM figure above. These
  two can and do differ materially on the same candidate.
- **Backsolve volatility** (`get:volatility_comps` called with and
  without the Backsolve allocation's `allocationId` — see
  `references/dive-in/backsolve/backsolve.md`'s "show volatility
  comps" entry point) — the Backsolve allocation's regression and the
  candidate's standard-scenario regression, which can also diverge on
  identical comps.

Users have reported getting "the wrong volatility" back — most often
someone asking for one of the above and being handed a different one,
usually because only a bare number was shown with nothing to indicate
which dataset, entity, or statistic it came from.

**The rule, wherever any of this skill's reference files displays a
volatility number:**

1. **Always name the source** alongside the number — which dataset
   (OPM / DLOM / Backsolve), which entity when more than one is in
   play (Backsolve allocation vs. standard scenario; subject company
   vs. comp set), which volatility type (equity vs. asset — and why,
   e.g. "asset, because debt is included"), and which statistic
   (regression result, mean, median, a specific percentile, or a
   manual entry).
2. **Show the full quartile/regression table, not just the single
   number**, whenever there's a table available for that dataset —
   even if the user only asked about one figure (e.g. "what's the
   equity volatility?"). The full table is what lets the user see
   where that number was picked from within the distribution, and
   catches a source mix-up before it reaches a filing. A one-line
   summary with no supporting table is only acceptable when the
   underlying command genuinely returns a single scalar with nothing
   else to show.
3. **Never default one dataset's value into another's without saying
   so.** If a manual override is missing and a reference file's
   guidance says to default to a value captured elsewhere in the
   session, state plainly which dataset that default is borrowed from
   before applying it — silent cross-dataset defaulting is exactly how
   the wrong number reaches a user.

## Tool surface

**Every** read-only command in this skill (`read_only: true` in `search_tools`) is called via
`read_tool({"name": "...", "arguments": {...}})`, and every command that changes data —
including the `compute:*` commands, which carta-mcp marks as changing data — via `call_tool` with the same
shape. There is no exception,
and the raw `mutate(command=..., params={...})` gateway is not needed
anywhere in this skill.

Some writes declare body fields as **required**, because the API rejects
them as null and an omitted argument reaches it as an explicit null. A
call that leaves one out is refused by argument validation before any
request is sent:

| Command | Required body fields |
|---|---|
| `mutate:approaches` | `usesCompanyLevelDlom`, `dlomConfigured`, `dlomMethod`, `dlomVolatilityManualEntry`, `dlomTimeToExitManualEntry` |
| `mutate:comparables` | `comparables` |
| `mutate:financials` | `financials` |
| `mutate:gpc_multiples_selection` | `multiples` |

So read the current state first — `get:approaches`, `get:comparables`,
`get:financials`, `get:gpc_multiples_selection` — and echo back the
fields you are not changing. The rejection names every missing field at
once, so recovering takes one retry, not one per field.

Per-approach objects on `mutate:approaches` (`gpc`, `dcf`, `ma`, …) are
the opposite: they are ignored when null, so naming only the approaches
you are changing leaves every other approach's `isUsed` and `weight`
untouched.

## Writes — save, then show what was saved

Applies to **every** write in this skill — every `mutate:*` and
`create:*` command, in **any** reference file (`set-approaches.md`,
`financials-review.md`, `comps.md`, `gpc-analysis.md`,
`allocation.md`, `backsolve.md`, `commentary.md`, etc.), not just one
flow.

**Do not ask the user to confirm a write before making it.** When the
user asks to save, set, update, or enter a value, make the call. A
question the skill genuinely needs answered — which period, which
share class, how to split the weights — is still asked; a "does this
look right? / apply these changes?" gate on a value the user already
gave is not.

**After every write, show the user what was saved** so they can check
it without being interrupted first. One row or line per changed field:
`{Field} — {full previous value, or "—" if new} → {full saved value}`.
Build it from the write's response (or a re-fetch), not from what you
sent. If the user spots a mistake, fix it with another write.

**Numbers in that saved-values summary must be the full,
non-abbreviated value — never write `$130.1M` when the underlying
number is `$130,107,041.24`; show `$130,107,041.24`.** Abbreviated
formatting (`$X.XM`, `$X.XB`) is fine everywhere else in this skill —
dashboards, recaps, read-only tables — it is specifically the
saved-values summary where the exact number must be spelled out,
because rounding hides exactly the kind of mistake (an extra zero, a
misplaced decimal) the user is checking for.

### Exceptions: finalize and delete always need an explicit yes

Two writes can't be undone, so they are the only ones that wait for
the user:

- **Finalizing a valuation** (status → FINAL) — `references/dive-in/ship.md`
  Step 3.
- **Deleting a valuation** — `references/dive-in/ship.md`
  **Delete a valuation**.

For these two, say what will happen, ask as plain text (no
`AskUserQuestion` — see **UX Rules** above), and call the write only on
an explicit yes. An earlier "finalize it" or "delete it" is the request,
not the confirmation.

---

## Routing: match the request to a capability

This skill does three things — **review the dashboard**, **bulk-create
valuations**, and **dive into one valuation**. There is **no fixed
sequence**: read the user's first message, match it against the table
below, and enter that capability directly. The only hard prerequisite is
**firm selection** (Step 1) — resolve `org_pk` first, then act on the
matched capability.

### Global interrupt: fund holdings request (any point in the flow)

**This check runs on every user message, at every step, regardless of
where the conversation currently is** — dashboard, bulk runner, dive-in
recap, mid-comps-selection, mid-financials-review, wherever. It is not
scoped to Step 2.4 or Step 2.5; those are just two common places the
request tends to come from, and both now point back here.

Trigger phrases: "show fund holdings", "fund breakdown", "fund holdings
value", "fund level breakdown", or equivalent. On match, jump to
**Fund Holdings (cross-flow capability)** below — do not keep processing
whatever step you were on. Do **not** use `get:allocation` to answer
this; it returns per-share-class allocation model output, not the
fund-level holdings split.

| The user's request… | Enter |
|---|---|
| **One** company named, or single-company drill-down ("show me MangoCart's valuations", "let's work on Acme today", "I want to pick comps myself", "review Acme's cap table", "let's go step by step on Acme", "update the EV for Acme") | **Dive into one** — after Step 1, go to **Step 2.5**: show the recap, then route the request. If the candidate isn't identified, ask which one. |
| **Multiple** companies named ("review MangoCart and Acme") | **Bulk-create** with that pre-selected set — see *Multi-company entry* below. |
| Generic / unscoped ("I want to work on my portfolio valuations", "let's work on valuations today", "work on portfolio valuations for {firm}") | **Ask which way in** — after Step 1, present the *dashboard-or-company fork* (below) and wait. Do **not** assume the dashboard. |
| Review / status phrasing, scoped to reviewing the portfolio ("review my Q2 valuations", "which companies need new valuations") | **Review the dashboard** — after Step 1, go to **Step 2.2** (environment detection + the **Step 2.2b** format choice run **before** any render). Act from the rendered dashboard via **Step 2.3**. Do **not** jump straight into `references/bulk/bulk-runner.md` — that skips the format choice. |
| Explicit bulk/multi-valuation **action** intent, no specific companies named ("run all my valuations", "batch valuations", "auto-run valuations", "let's do some bulk valuations", "I want to do a few bulk valuations", "do multiple valuations at once") | **Ask which way in** — after Step 1, present the *bulk-intent fork* (below) and wait. Do **not** jump straight to the dashboard or the runner. |
| Bare / help-ish (empty message, "help", "what can you do", "get started", "show me what you can do", bare `/carta-portfolio-valuations`) | **Welcome** (below) — resolve the firm, print the menu, wait for the choice. Do not fetch or render the dashboard until the user asks. |
| Ambiguous | Short & inscrutable → treat as bare entry (**Welcome**). Clear scope but unclear specifics → the *dashboard-or-company fork* (below), not a direct jump to the runner. |

Resolve company-name matches against
`read_tool({"name": "portfolio_valuations__list__portfolio_dashboard", "arguments": {"organizationId": "<org_pk>", "page_size": 100, "raw": false}})`
only after Step 1 (firm selection) — the `org_pk` is needed.

**Dashboard-or-company fork (generic entry).** When the request is
generic/unscoped — no company named and no "all" / time-period scope — do
**not** assume the dashboard. After Step 1, present a single plain-text
choice and wait (per **UX Rules** — no `AskUserQuestion`):

> You're working in **{firm_name}**. Would you like to:
> 1. **View your portfolio dashboard** — see every company, its latest valuation, status, and recent events.
> 2. **Work on a specific company** — tell me which one and we'll dive in.

Route the reply:
- **Dashboard** ("1", "dashboard", "view", "show me everything") → go to
  **Step 2.2**; the render preference gate runs there **before** any data
  is fetched (see Step 3.2's *Render preference gate*).
- **Specific company** ("2", a company name, "I have one in mind") → go to
  **Step 2.5 (dive into one)** for that company; if none was named, ask
  which one.

**Bulk-intent fork (explicit bulk/multi-valuation action entry, no
companies named).** After Step 1, ask inline as plain text (per **UX
Rules** — no `AskUserQuestion`):

> Would you like to:
> 1. **See the bulk runner table** — review every company eligible for a valuation, then pick which to run.
> 2. **Tell me which companies** — you already have specific ones in mind.

Route the reply:
- **Bulk runner table** ("1", "show me", "see the table") → using the
  `env_mode` already established in Step 1, go
  straight to the runner — **do not** render the full portfolio dashboard
  first, this fork already replaces that step:
  - **`env_mode: "artifact"` or `"preview-server"`**: ask the
    same "Runner format" question used in Step 2.4 (**1. Runner widget** —
    a quick plan you can bulk-create in one click, or open the full list
    to customize / **2. Inline view** — text-based plan you confirm
    before I run anything). Route **Runner widget** to the **Plan card**
    section of `references/cowork-artifact.md`; route **Inline view** to
    `references/md-table-runner.md`, Step 1.
  - **`env_mode: "inline"`**: no question — read
    `references/md-table-runner.md` inline and follow from Step 1
    directly.
- **Already have companies in mind** ("2", "I know which ones", a company
  name) → if none were named yet, ask "Which companies?" in prose; once
  named, treat as **Multi-company entry** below (pre-selected set).

**Multi-company entry.** Read `references/bulk/bulk-runner.md`
**immediately** (no `org_pk` dependency — in parallel with Step 1's API
calls); carry the named set in as the pre-selected company list and start
at **Step 4** once Step 1 completes (skip Step 3).
- **`env_mode: "artifact"`**: follow the **Plan card** section of
  `references/cowork-artifact.md` before loading the runner (it leads to
  the Runner widget section for the customize path).
- **`env_mode: "preview-server"`**: if `preview_server_render_pref`
  is not yet set, ask once ("How would you like to run valuations?
  **1. Widget** — a quick plan you can bulk-create in one click, or open
  the full list to customize / **2. Inline view** — text-based plan you
  confirm before I run anything") and store as `preview_server_render_pref`.
  If `"widget"`, follow the **Plan card** section of
  `references/cowork-artifact.md`; if `"markdown"`, read
  `references/md-table-runner.md` inline and follow from Step 1.
- **`env_mode: "inline"`**: no question — read
  `references/md-table-runner.md` inline and follow from Step 1 directly.

### Silent entry signals (apply before routing, never surfaced)

- **Display-format preference.** Scan the first message for an explicit
  format signal and set `dashboard_render_pref` if present — Step 3.2's
  render preference gate then skips its question:
  - "inline", "in chat", "as text", "markdown", "no artifact", "text only" → `"markdown"`
  - "artifact", "side panel", "as an artifact", "in the panel" → `"artifact"`
  - No signal → leave unset; the gate asks at render time.

  Silent — do not confirm the preference back, and do not let it change
  the routing above.
- **One-line intro (bulk-create paths only).** This line is specifically
  about bulk-create defaults (roll-forward, per-company overrides) — it
  must **only** fire on paths that actually lead toward creating drafts
  across companies: **multiple companies named**, **review/status
  phrasing** (dashboard entry, which can lead to bulk-create via Step
  2.3's Act bucket), and the **bulk-intent fork** (both of its branches
  lead to bulk-create — fire it once the fork is presented, no need to
  hold it like the dashboard-or-company fork below). Emit it **once per
  session**, gated on `intro_shown`, before the work:
  > ⚡ I can create these as **drafts** — each defaults to a roll-forward of last period (refreshed multiples + the latest financials), and you can override any company before I start or finalize later.

  **Do NOT emit it for a single company named** (dive-in, Step 2.5) —
  that path works on one existing/specific candidate, never bulk-creates
  anything, and "override any company" / "create these as drafts" makes
  no sense there. Do not emit it for bare/help-ish entry either — the
  Welcome block is shown instead (see below).

  If `intro_shown` is unset, print the line and set `intro_shown = true`;
  if already true, skip silently. On the generic *dashboard-or-company
  fork*, hold this line until the user picks a direction, then apply it
  only if they picked **dashboard** — skip it entirely if they picked a
  specific company.

---

## Fund Holdings (cross-flow capability)

Reached from the **global interrupt** above — from any step, any mode,
any point in the conversation. Fund holdings are only ever available for
a **finalized (`status: FINAL`)** valuation; drafts have no committed
allocation to report against.

**Never substitute `get:allocation` for this capability.** `get:allocation`
returns per-share-class allocation model inputs/outputs for a single
candidate — a different shape entirely from the fund-level holdings
split this capability answers. If you've reached for `get:allocation` in
response to a "fund holdings" request, stop and use the query below
instead.

### Step F1: Resolve target company + valuation date

- **A specific company/candidate is already in context** (e.g. mid
  dive-in, Step 2.5a's recap already ran) → use that company's name and
  the valuation date currently in view. Skip to **Step F2**.
- **On the rendered dashboard** (Step 2.3/2.4) with no company named →
  use every company in the **Final valuation** bucket (already derived
  in Step 3.2). Skip to **Step F2**.
- **No company/candidate in context at all** (e.g. the interrupt fired
  before any dashboard or dive-in has loaded) → ask in plain text:
  "Which company's fund holdings would you like to see?" Once named,
  resolve it against the dashboard/company list, then continue.

### Step F2: Check valuation status — gate on FINAL

For the resolved company(ies), check `latestValuation.status` (from the
dashboard data, or from `read_tool({"name": "portfolio_valuations__get__valuation", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})`
if you're mid dive-in and don't already have it in context):

- **Status is `FINAL`** → proceed to **Step F3** with that company +
  valuation date.
- **Status is `DRAFT`, or there is no valuation at all** → do **not**
  run the query. Tell the user plainly, e.g.:
  > Fund holdings can only be viewed for a **finalized** valuation — this one is still a draft.
  Then list that company's finalized valuations (via
  `read_tool({"name": "portfolio_valuations__list__projects", "arguments": {"ownerId": "<org_pk>", "ownerKind": "FIRM", "targetId": "<corporation_id>", "targetKind": "CORPORATION"}})`,
  filtering candidates where `status == "FINAL"`) and ask which one they'd
  like to see:
  > Here are the finalized valuations for **{company}** — which would you like to see fund holdings for?
  > 1. {date 1}
  > 2. {date 2}
  > ...
  Wait for the reply, then continue to **Step F3** with the chosen date.
  If there are **no** finalized valuations for that company at all, say
  so plainly and stop — do not offer a date list.
- **Multiple companies resolved in Step F1** (dashboard-wide request) →
  apply this gate per company; only companies with a `FINAL` valuation
  go into Step F3's query. If none are final, say: "No final valuations
  are in the dashboard yet."

### Step F3: Query and render

`FUND_ADMIN.FUND_HOLDINGS_VALUE` is a general-purpose fund-holdings table
— not a private implementation detail of this one flow. Treat this
capability as **discoverable from any angle**, not only "company +
finalized valuation date." A user may instead ask by fund ("show me
Owl Ventures Opportunity Fund II's holdings"), by firm-wide rollup
("show fund holdings across the portfolio"), by date range ("as of last
quarter"), or by some other column entirely. Build the `WHERE` clause
from whatever the user actually specified — do not force every request
through a `TARGET_NAME` + `VALUATION_DATE` shape just because Step F1/F2
resolved a specific company and date.

**Confirm the schema before hand-writing SQL** — don't assume the
column list below is exhaustive or unchanged. Call
`read_tool({"name": "dwh__get__table_schema", "arguments": {"table_name": "FUND_HOLDINGS_VALUE", "schema": "FUND_ADMIN"}})`
(or `dwh__list__tables` first if you're unsure the table still lives in
`FUND_ADMIN`) to confirm the live column set, especially if the user's
ask references a column not listed here.

Known columns as of this writing: `VALUATION_DATE`, `TARGET_NAME`,
`FUND_NAME`, `FUND_HOLDINGS_VALUE`, `FUND_INVESTED_CAPITAL`,
`FUND_LEGAL_OWNERSHIP_PCT`, `FUND_MOIC`, `TOTAL_HOLDINGS_VALUE`,
`SOURCE`, `ALLOCATION_METHODOLOGY`. `SELECT *` (or an explicit
superset) rather than hand-trimming columns when the user's question
implies fields beyond this list.

Baseline shape — company + valuation-date scoped (the common case coming
out of Step F1/F2), one clause per company joined with `OR` when there's
more than one:

```sql
SELECT
    VALUATION_DATE,
    TARGET_NAME,
    FUND_NAME,
    FUND_HOLDINGS_VALUE,
    FUND_INVESTED_CAPITAL,
    FUND_LEGAL_OWNERSHIP_PCT,
    FUND_MOIC,
    TOTAL_HOLDINGS_VALUE,
    SOURCE,
    ALLOCATION_METHODOLOGY
FROM FUND_ADMIN.FUND_HOLDINGS_VALUE
WHERE (<one clause per company: TARGET_NAME ILIKE '%{name}%' AND VALUATION_DATE = '{date}'>)
ORDER BY FUND_HOLDINGS_VALUE DESC
```

Adapt the `WHERE` (and `SELECT`/`ORDER BY`) to the actual ask — e.g.
`WHERE FUND_NAME ILIKE '%{fund}%'` for a fund-scoped request, no
`WHERE` at all (just `SOURCE = 'PORTFOLIO_VALUATION'`, still filtered to
`FINAL`-status valuations per Step F2) for a firm-wide rollup, or a
`VALUATION_DATE BETWEEN` range for a date-range ask. The company+date
shape above is a default, not a constraint.

Call via `read_tool({"name": "dwh__execute__query", "arguments": {"sql": "<query>", "limit": 200}})`.
For open-ended fund-holdings questions where you're unsure how to shape
the SQL, `dwh__execute__question` (plain-English) is an acceptable
fallback — it resolves schema and SQL itself.

Display results as a markdown table with columns: **Company**, **Fund**,
**Valuation Date**, **Holdings Value**, **Invested Capital**,
**Ownership %**, **MOIC**, **Method**. Format currency with $M/B/K
suffix; ownership % as `X.XX%`; MOIC as `X.Xx`; show `—` for any null
field. If the query returns no rows, say: "There are no fund holdings
for this valuation."

After answering, return control to wherever the user was before the
interrupt fired (re-present the dashboard menu, the dive-in recap, etc.)
— do not force a new menu.

---

## Welcome (bare entry only)

Reached only when routing classified the entry as **bare / help-ish**.
Skipped entirely on any direct-intent entry. This is a lean welcome — a
high-level menu of the three things the skill does. Do **not** front-load
any bulk-run detail, and do **not** fetch or render the dashboard; that
happens only if the user asks (reply routing below).

Resolve the firm first via **Step 1** — the MCP `welcome` / connection
banner appears here. **Do not fire the speculative dashboard fetch**; the
dashboard is loaded lazily only when the user picks it.

Then print the single message below — the **only** prompt shown. Do not
also emit a separate firm-confirmation line or a trailing "what would you
like to do?"; the message covers both. Set `intro_shown = true` when this
message is shown, so a later direct request in the same session does not
re-emit the one-line intro.

Substitute `{firm_name}`, and append ` (your only firm)` when the user
has just one firm. Output verbatim:

> 👋 Working in **{firm_name}**[ (your only firm)] — here's what I can help with:
>
> 1. **Review your valuation dashboard** — see every portfolio company, their latest valuation, status, and recent events.
> 2. **Bulk-create valuations** — run draft valuations across many companies in one pass.
> 3. **Dive into a valuation** — open one company and work through it step by step.
>
> Want to start by viewing your dashboard? Or tell me what you'd like to do.

Edge cases (resolved during Step 1):
- **Multiple firms, none active** — run Step 1's firm picker first, then
  return here with the chosen firm.
- **Zero firms** — output Step 2.1's zero-firms line and stop.

**Route the user's reply** — the dashboard has **not** been fetched; load
it only on the dashboard route:

| Reply | Action |
|---|---|
| "yes", "sure", "show me", "1", "dashboard", "view it" | Go to **Step 3.2** to fetch and render the dashboard now. (Skip Step 2.1's greeting — the firm was already confirmed above.) |
| "2", "bulk", "run all of them", "create valuations" | Enter bulk mode. Read `references/bulk/bulk-runner.md` inline and follow from Step 3. |
| "3", "dive in", "{single company name}", "let's work on Acme" | Go to **Step 2.5 (dive into one)** for the named company. |
| Anything else | Match on intent generously against the routes above. If still unclear, ask one short clarifying question. |

Do **not** repeat the menu or re-confirm the firm once the user has chosen.

---

## Step 1: Firm selection (prerequisite — resolve before any capability)

This is the one genuinely order-dependent gate: every capability needs
`org_pk`, so resolve the firm first. Everything after this is
intent-routed (see **Routing** above), not a linear sequence.

**Environment detection (runs on every entry, before anything else).**
Determine the runtime rendering capability — `env_mode` is one of
`preview-server`, `artifact` or `inline` — using the `ToolSearch` probes in
**Step 2.2a** below, and store the result as `env_mode`. The modes are named
after the rendering tool that is present, not the Claude product the user is
in: the Claude Code desktop app, the Claude Code CLI and Cowork are told
apart only by which tools they expose. `env_mode: "preview-server"` means
`mcp__Claude_Preview__preview_start` OR `mcp__Claude_Browser__preview_start`
is present (see `preview_tool_family` in Step 2.2a), which is what makes the
interactive preview panel available. Fire the ToolSearch probe
in **Step 2.2a** in parallel with the speculative fetch and
`list_contexts` below — it has no dependencies. This is silent and must
never be skipped, because the dashboard render-preference gate (Step
2.2b), the bulk-intent fork, and the runner widget-vs-inline choice all
branch on `env_mode` regardless of which capability
the user is entering. Every other reference in this skill that needs to
know the environment reuses this cached `env_mode` —
none of them re-detect it. (Deep-link rendering, `references/deep-link.md`
Step 5, does **not** branch on `env_mode` — it always spells out the raw
URL now; see that file.)

**Speculative dashboard fetch (cold-start acceleration):** If `org_pk`
is already cached from earlier in this session, fire
`read_tool({"name": "portfolio_valuations__list__portfolio_dashboard", "arguments": {"organizationId": "<org_pk>", "page_size": 100, "raw": false}})`
with the cached `organizationId` and `page_size: 100` **immediately, in parallel with `list_contexts`** —
do not wait for firm confirmation first. Hold the result as
`speculative_dashboard`. After `list_contexts` confirms the active firm
is unchanged, use `speculative_dashboard` in Step 3.2 instead of
fetching again. If `list_contexts` shows the firm changed (or the
speculative call errored), discard `speculative_dashboard` and fetch
fresh in Step 3.2 as normal. Also fire `search_tools` in this same
parallel fan-out — it has no dependencies either.

On a **first entry** (no cached `org_pk`), skip the speculative fetch
and proceed with the normal sequence below.

**Speculative preview schema pre-load — fires on every entry, cached
`org_pk` or not**, immediately once `env_mode` is known (no dependency on
`list_contexts` or `list_accounts`):
- **`env_mode: "artifact"`**: skip — `Artifact` is a loaded tool, not a deferred one, so it has no schema to pre-load.
- **`env_mode: "preview-server"`**: `ToolSearch(query: "select:mcp__Claude_Preview__preview_start,mcp__Claude_Browser__preview_start")`
  — this is how `env_mode` and `preview_tool_family` get set; if
  both come back empty (and neither is already loaded), there are no schemas to
  pre-load and `env_mode` is not `preview-server`.

This fires in parallel with everything else below so the schemas are
ready by the time the user answers the display format question in Step
2.2b — no extra round-trip at render time.

1. Call `list_contexts` to check for an active firm and get the firm name.
   (If `org_pk` is cached, `list_contexts` + `read_tool({"name": "portfolio_valuations__list__portfolio_dashboard", ...})` +
   `search_tools` all fire together — see above.)
2. If `org_pk` is **not** cached, fire **all of the following** **in parallel**
   once `list_contexts` returns:
   - `list_accounts` with `search: "<firm name>"` to resolve `org_pk`
     (integer ID from `organization_pk:<n>`). **Never call `list_accounts`
     without the search filter** — the unfiltered response returns 200+
     accounts.
     (No `search_tools` sentinel — it cannot report on this domain at all.
     Access was already settled by **Gate 1** before this step, and the
     schema pre-load above already fired separately — do not repeat it here.)
3. If active firm exists, confirm by asking in plain text. If multiple
   firms and no active one, list them and ask the user to pick. If one firm, auto-select silently.
4. Call `set_context` if the user picked a different firm.

**Important**: The `list_contexts` `firm_id` is a UUID used for
Snowflake — it is NOT the same as the integer org_pk needed by
valuation commands. Always resolve org_pk from the `list_accounts`
search result (`organization_pk:<n>`).

**Session cache**: Once `org_pk` is resolved, hold it in context for the
rest of the session. If this skill is re-entered (e.g. after a run
completes and the user asks to do more), skip `list_accounts` and reuse
the cached `org_pk` — `list_contexts` is still needed to confirm the
active firm hasn't changed, but `list_accounts` is not.

If the user has no firms, surface plainly and stop.

After firm selection, resolve any company-name matches captured during
routing:
- **One match (single company named)** → proceed to Step 2.5 (dive into
  one) for that company.
- **Multiple matches (named in the user's message)** → read
  `references/bulk/bulk-runner.md` inline; carry the matched list
  in as the pre-selected company set and start at Step 4. Skip Step 3.
- **No company named or no match** → read
  `references/bulk/bulk-runner.md` inline and follow from Step 3.

---

## Step 2: Dashboard entry

Reached by **two paths**, both of which render the portfolio dashboard
through the same gate so the experience is identical:

1. **Bare/welcome entry** — the user chose to view the dashboard from
   the Welcome reply routing. The firm was confirmed in the Welcome block.
2. **General/time-period phrasing** (e.g. "work on portfolio valuations
   for {firm}", "run all my valuations") — routed here from the routing
   table. The firm was resolved in Step 1 and the one-line intro already
   fired.

On **both** paths, **skip the Step 2.1 greeting** and go to **Step 2.2 →
Step 3.2** to fetch and render the portfolio. In interactive modes, Step
2.2b asks the "Dashboard view" format choice (interactive dashboard vs.
inline text table) **before** rendering. The dashboard was not
pre-fetched — Step 3.2 fetches it now. From the rendered dashboard,
Step 2.3's menu routes the user to the bulk runner (Act) or any other
next step.

Skipped entirely when the user named a specific company (→ dive-in) or
multiple companies (→ bulk runner with a pre-selected set).

### Step 2.1: Edge-case firm lines

The Welcome block shows the normal merged firm + menu message, so the
happy-path greeting is **not** used here. This block holds only the
edge-case lines referenced from the Welcome block:

- **Multiple firms, none active** (user must pick first):
  > 👋 **Portfolio Valuations**. Pick a firm to get started.

  Then run Step 1's firm picker. After selection, return to the Welcome
  block and print the merged firm + menu message with the chosen firm.

- **Zero firms**:
  > 👋 **Portfolio Valuations** — you don't have any firms set up in Carta yet. Add one and come back.

  Stop.

- **Firm has zero portfolio companies** (detected after Step 3.2's
  data load):
  > 👋 **Portfolio Valuations** — working in **{firm_name}**, but there are no portfolio companies yet. Add some in Carta and come back.

  Stop.

### Step 2.2: Render the dashboard

Use the `env_mode` already established in Step 1 (see **Step 2.2a** for
the detection rules themselves) to decide how to render the dashboard —
do not re-detect it here. (Step 3.1's search_tools call was already
fired in parallel during Step 1 — its result is in context.)

### Step 2.2a: Environment detection

**This runs once, in Step 1, on every entry — not here.** This section
is the reusable rule set every other part of this skill points back to
(deep-link rendering, the dashboard render-preference gate, the
bulk-intent fork, the runner widget-vs-inline choice); it is documented
here for reference, not as a step you re-run each time the dashboard is
rendered.

**Use `ToolSearch` as the primary probe — do not rely on passive context
scanning.** The deferred-tools list is hundreds of names long; scanning it
by eye is unreliable and is the root cause of false classifications.
Instead, fire the probe as an active, deterministic tool call:

```
ToolSearch(query: "select:mcp__Claude_Preview__preview_start,mcp__Claude_Browser__preview_start")
```

**Two tool families answer for the same capability — probe for both, never
just one.** The local-preview-panel tool has shipped under two different MCP
server names across hosts/versions: `Claude_Preview` (older) and
`Claude_Browser` (current, seen in Claude Code CLI sessions as of this
writing). A host exposes at most one of the two — never assume which one, and
never hardcode a single name in a probe or a downstream call. Whichever
family answers, record it as `preview_tool_family` (`"claude_preview"` or
`"claude_browser"`) and use *that* family's tool names for every subsequent
preview call in this session (Step 2.2b, `references/desktop-preview.md`).
Treating an absent `Claude_Preview` as "no preview panel" without also
checking `Claude_Browser` is exactly the bug that silently downgrades a real
Claude Code CLI session to the `artifact` path — the two paths produce
visibly different "Get started" behavior (a working local server vs. a
copy-to-chat panel that always fires), so misclassifying this is not cosmetic.

`Artifact` needs no probe — it arrives as a loaded tool when present, so read it
straight off the tool list.

A non-empty ToolSearch response (the tool schema appears in the output)
means the tool is present as a deferred tool in this session.

Additionally check whether either tool is already loaded — a tool that was
provided with its full JSON schema at conversation start (listed alongside
`Read`, `Bash`, etc.) will NOT appear in ToolSearch results because it is
not deferred. If it is already loaded it is equally present.

A tool is **present** if ToolSearch returns its schema OR it is in the
already-loaded list. A tool is **absent** only when ToolSearch returns empty
for it AND it is not in the already-loaded list.

There are exactly **three** mutually exclusive values for `env_mode`. They
name the rendering capability, so there is no Desktop-vs-Terminal split: the
Claude Code CLI (terminal) can now also expose the `Artifact` tool, so tool
presence alone can no longer tell the Claude Code desktop app, the CLI and
Cowork apart — don't try.

**`preview-server`** (`env_mode: "preview-server"`) — `mcp__Claude_Preview__preview_start`
OR `mcp__Claude_Browser__preview_start` is present (see `preview_tool_family`
above). This takes priority over `Artifact` — classify as `preview-server`
**regardless of whether `Artifact` is also present**; when both are
available, always render through the preview panel, not the `Artifact`
tool. This is what makes the interactive preview panel available.

**`artifact`** (`env_mode: "artifact"`) — the `Artifact` tool is present and
**neither** `mcp__Claude_Preview__preview_start` **nor**
`mcp__Claude_Browser__preview_start` is present. (Known gap: a Claude Code
CLI session with `Artifact` exposed and no preview panel at all is
indistinguishable from Cowork by tool presence, and takes this path too.)

**`inline`** (`env_mode: "inline"`) — none of the preview tools are present
and `Artifact` is absent. Only classify as `inline` after the ToolSearch
probe returns empty for **both** preview families AND neither appears in the
already-loaded list, AND `Artifact` is not in the tool list.

---

### Step 2.2b: Interactive mode (`artifact` or `preview-server`) — dashboard render preference

This question is asked whenever an interactive rendering surface exists:
`env_mode: "artifact"` or `env_mode: "preview-server"`.
Ask it inline, as plain text (no `AskUserQuestion` — see UX Rules), before
rendering. This question is asked **once per session** — once answered,
`dashboard_render_pref` applies to every subsequent dashboard render
without re-asking (unless the user explicitly requests a different
format). `env_mode: "inline"` skips this gate
entirely — go straight to **Step 2.2c**.

**While waiting for the user's answer**, speculatively read the relevant reference in parallel — user think-time covers the file read entirely:
- **`artifact`**: read `references/cowork-artifact.md`
- **`preview-server`**: read `references/desktop-preview.md`

Ask:

> **How would you like to see your portfolio?**
> 1. **Interactive dashboard** — a richer, clickable view that updates after each run. Takes a moment longer to load.
> 2. **Inline view** — a quick text table, right here in the chat.

Wait for the reply, then store it as `dashboard_render_pref` (`"artifact"`
for the interactive dashboard, `"markdown"` for the inline view).

**If "Interactive dashboard"**: Fire **both** of the following **in parallel**:
- `read_tool({"name": "portfolio_valuations__list__portfolio_dashboard", "arguments": {"organizationId": "<org_pk>", "page_size": 100, "raw": false}})` fetch (Step 3.2 data load)
- Pre-load the artifact tool schemas via `ToolSearch`:
  - **`artifact`**: nothing to pre-load — `Artifact` is a loaded tool.
  - **`preview-server`**: pre-load the tool names for
    whichever `preview_tool_family` Step 2.2a recorded —
    `ToolSearch(query: "select:mcp__Claude_Preview__preview_start,mcp__Claude_Preview__preview_list,mcp__Claude_Preview__preview_eval")`
    when `"claude_preview"`, or
    `ToolSearch(query: "select:mcp__Claude_Browser__preview_start,mcp__Claude_Browser__preview_list,mcp__Claude_Browser__navigate,mcp__Claude_Browser__javascript_tool")`
    when `"claude_browser"`.

The reference file is already in context — use it once both calls complete:
- **`artifact`**: follow `references/cowork-artifact.md`
- **`preview-server`**: follow `references/desktop-preview.md`

**If "Inline view"**: Follow **Step 3.2** to render the grouped markdown table inline (same as `env_mode: "inline"`).

When the user subsequently selects the bulk-create action (Step 2.4, or
any bulk entry path), ask inline as plain text (no `AskUserQuestion`):

> **How would you like to run valuations?**
> 1. **Runner widget** — a quick plan you can bulk-create in one click, or open the full list to customize
> 2. **Inline view** — text-based plan you confirm before I run anything

**If "Runner widget"**: show the **Plan card** first (the method rule set + a
valuation-date picker) — the user clicks **Create draft valuations** to
bulk-create in one click, or **Adjust by company** to open the full runner list.
The Plan card carries its own valuation-date picker, so **skip the Step 3 date
question** for this path (the card collects the date).
- **`artifact`**: follow `references/cowork-artifact.md` **Plan card** section
  (which links onward to the **Runner widget** section for the customize path).
- **`preview-server`**: follow `references/desktop-preview.md` — the `open_runner`
  branch shows the Plan card (which links onward to the Runner widget section of
  `references/cowork-artifact.md` for the customize path).

**If "Inline view"**: read `references/md-table-runner.md` inline and
follow from Step 1.

---

### Step 2.2c: `inline` mode — render markdown table

Reached when `env_mode: "inline"` —
`Artifact` is absent, and neither `mcp__Claude_Preview__preview_start` nor
`mcp__Claude_Browser__preview_start` is available.
**Do NOT call any preview or artifact tools** (`mcp__Claude_Preview__*`, `mcp__Claude_Browser__preview_*`, `Artifact`, `build_artifact.py`), write dashboard response files, or ask for a display format preference — those paths are unavailable. Fall through directly to **Step 3.2** (data load + grouped markdown table). Render the greeting from 2.1 first, then the table from Step 3.2 below it.

The table is the discovery surface — users see real company names and can type
"1, 3, 7" or "take a closer look at Acme" without
needing an example phrases list.

### Step 2.3: Prompt the user

After the table, present a three-bucket follow-up menu in plain text.
The **Act** bucket is always static. The **Analyze** and **Export**
buckets are data-aware — omit any option whose condition is not met,
and omit the bucket heading entirely if all its options are suppressed.

Render in plain text using this structure:

```
**⚡ Act**
- Bulk-create draft valuations — open the runner across all companies that need one

**📊 Analyze**
- _(if final or draft bucket non-empty)_ Dig into a specific holding — compare approaches, see comp multiples, check DLOM
- _(if final bucket non-empty)_ Which holdings are most overdue for a refresh?
- _(if new-events bucket non-empty)_ How does the new round for {first company in new-events bucket} affect our valuation?

**📤 Export**
- _(always)_ Download a tearsheet for any holding
- _(always)_ Export portfolio SOI
```

Company names in Analyze are pulled directly from the bucket lists —
use real names from the data, not placeholders.

Close with one line: "What would you like to do?" and wait for the
user's reply (free text or named action). Step 2.4 routes all replies.

After the "What would you like to do?" line, add one inline note (no section heading, no bullet):

> 💡 I can also show the individual fund-level holdings breakdown for any company with a final valuation — say "show fund holdings" to see it.

### Step 2.4: Route the reply

Route based on the user's free-text reply or named action from Step 2.3:

- **Act — run/refresh valuations** (e.g. "refresh", "continue drafts",
  "run first valuations", "re-value stale", "bulk", "run them all",
  "do the ones that need it", bucket-scoped phrases like "just the
  drafts", "the no-val ones", named companies, row numbers) → start
  the bulk runner immediately.
  - **`env_mode: "artifact"`** (per the `env_mode` resolved in Step 1 — not a
    fresh tool check; see Step 2.2a):
    follow `references/cowork-artifact.md` **Plan card** section (it leads to
    the **Runner widget** section for the customize path).
  - **`env_mode: "preview-server"`**:
    follow `references/desktop-preview.md` (the Plan card is shown first; it
    leads to the Runner widget section for the customize path).
  - **`env_mode: "inline"`**: read `references/md-table-runner.md`
    inline and follow from Step 1.
  Route via Step 3.3's intent routing table in
  `references/bulk/bulk-runner.md` (read it inline).

- **Act — dive into one** (e.g. "dig into", "take a closer look",
  "dive in", a single company name) → go to **Step 2.5 (dive into one)**
  for that company.

- **Analyze** (e.g. "which are most overdue", "how does the round affect
  valuation", "compare approaches", "what's the status", questions about
  specific holdings) → answer using data already in context from Step 3.2.
  Fetch additional detail as needed. After answering, re-present Step 2.3's
  menu.

- **Export — tearsheet** (e.g. "download tearsheet", "tearsheet for Acme")
  → invoke `Skill(carta-investors:carta-download-tearsheet)`.

- **Export — SOI** (e.g. "export SOI", "download SOI") → a schedule of
  investments isn't built here. Say so in one line and leave it there —
  don't assemble one by hand out of the dashboard data, and don't offer
  the valuation ledger as a substitute. Then re-present Step 2.3's menu.

- **Fund holdings** (e.g. "show fund holdings", "fund breakdown", "fund holdings value", "fund level breakdown") →
  Handled by the **global interrupt** (top of Routing) → **Fund Holdings (cross-flow capability)**.
  The Final valuation bucket (already in context from Step 3.2) is the candidate list when the
  user hasn't named a specific company.

The bucket lists are already in context from Step 3.2's silent derivation.

---

## Step 2.5: Dive into one (single-company entry)

Reached from:
- **Routing / firm selection** matched a single named company.
- **The Welcome reply routing** routed "dive in" / a single company.
- **Step 3.4** confirm resolved to exactly 1 company.
- **Bulk run results** — the user clicked a row's next-step button ("Dive
  into the {company} valuation and {step}") or typed "dive into {company}"
  after a bulk run. Take the candidate context from that company's
  `bulk_results` entry, skip Step 2.5a's `list:projects` lookup, and after
  the recap start on the step. See `references/bulk/bulk-results.md` Step 3.

There is **no mode picker** — do not ask "run autonomously vs. work on
it myself." Show the recap, then answer what the user asks.

### Step 2.5a: Recap (where the candidate stands)

Resolve the candidate context (`project_id`, `candidate_id`,
`valuation_id`; if the company has multiple projects, list them via
`read_tool({"name": "portfolio_valuations__list__projects", "arguments": {"ownerId": "<org_pk>", "ownerKind": "FIRM", "targetId": "<corporation_id>", "targetKind": "CORPORATION"}})`
and ask which one — match a row the user
already named without re-asking).

**Capture the target type.** The `list:projects` response carries a
`target` object with `id` and `kind` per project. Hold the resolved
project's `target.kind` (one of `CORPORATION`, `LLC_ISSUER`, `LLC_ENTITY`)
and `target.id` in context — the cap-table flow (Step 2.5b →
`references/dive-in/cap-table-review.md`) branches on `target.kind` to
pick which cap table to read, and the LLC path uses `target.id` as the
issuer id. **Allocation does not branch on it.** Which allocation
methodologies a candidate can run comes from its own configuration
(`references/dive-in/allocation.md` Gate 0), not from its target kind —
don't use `target.kind`, `isLlc`, or `llcIssuerId` to decide what to
offer or which allocation flow to enter.

**Stop here when `target.kind` is `LLC_ENTITY`.** That target kind is
deprecated and no flow in this skill supports it. Handle it once, here —
do not route the request onward and do not let it fall through to the
cap-table or allocation branches below. Surface one plain line and return
control:

> "**{company}** is an entity type we no longer support for valuations.
> Open it in Carta if you need to look at it there."

Everything after this point assumes `target.kind` is `CORPORATION` or
`LLC_ISSUER`.

**When `list:projects` returns zero projects**, the holding simply has
no valuation yet. Do not treat this as an error and do not dead-end the
user. The response carries a generic gateway warning ("EMPTY RESPONSE …
BEST EFFORT — flag this clearly to the user") that fires on every empty
result; it does **not** apply here — never surface it, and never let it
turn into a "this data may be incomplete" caveat on data that came from
a different, fully-populated call. Fall back to the dashboard's
`isLlc` / `llcIssuerId` for the
target signal, and skip the `get:valuation` / `get:approaches` /
`get:financials` calls
below (there is no candidate to describe) — recap what you do know, then
route the user's request as normal. Cap-table review in particular is
**fully available for an LLC in this state**: it is an issuer-scoped
live read that needs no candidate. Only genuinely candidate-scoped flows
(financials, approaches, comps, GPC, allocation, finalize) require
creating a valuation first — offer `create-val.md` for those.

Then silently call
`read_tool({"name": "portfolio_valuations__get__valuation", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})`,
`read_tool({"name": "portfolio_valuations__get__approaches", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})`, and
`read_tool({"name": "portfolio_valuations__get__financials", "arguments": {"ownerId": <ownerId>, "project_id": <project_id>, "candidate_id": <candidate_id>}})`
(needed for the **Financials** recap line below — `get:valuation`/`get:approaches`
alone don't carry period data), and render a short recap so the user sees
where the valuation stands before doing anything:

> Here's where **{company}**'s {valuation date} valuation stands:
> - **Approaches:** {approach list with weights} — {how they were set, e.g. "copied from the prior valuation"}
> - **Company value:** {companyValue} — {one-line note if an approach is contributing $0 / dragging the value}
> - **Financials:** {populated / all periods blank — note the DLOM impact if blank}
> - **Cap table:** {accessible / not accessible on this candidate}
> - **Status:** {Draft / Final}

Keep it to these lines. Speak in business terms — no command names, field
names, or IDs. Omit a line only if genuinely not applicable.

Follow the recap with the **valuation summary checklist** (Step 2.5c).

### Step 2.5b: Route the user's request (no wizard)

After the recap, wait for the user and route their free-text request to
the matching individual flow. Do **not** push a "where would you like to
start?" menu and do **not** prompt "ready for the next step?" — answer
what they asked, then return control.

| User intent (examples) | Flow to read inline |
|---|---|
| "review the cap table", "show holders", "ownership %" | `references/dive-in/cap-table-review.md` |
| "review financials", "show revenue", "what's the EBITDA", "refresh financials" | `references/dive-in/financials-review.md` |
| "set approaches", "change methodology", "use GPC / M&A / post-money / backsolve", "Custom Value", "manual EV", "set the company value to {N}" | `references/dive-in/set-approaches.md` |
| "find comps", "update comps", "add a peer", "drop {ticker}" | `references/dive-in/comps.md` |
| "run GPC analysis", "recommend multiples", "set the 75th percentile", "quartile stats" | `references/dive-in/gpc-analysis.md` (requires `gpc` enabled; if not, read `set-approaches.md` first) |
| "work on Backsolve", "run backsolve", "select a backsolve share class", "solve for equity value", "override the backsolve value", "make an equity adjustment", "adjust the equity value" | `references/dive-in/backsolve/backsolve.md` (requires `backsolve` enabled; if not, read `set-approaches.md` first — an override/adjustment request on an already-computed candidate enters directly at that file's Step 5) |
| "how is the backsolve calculated", "explain the backsolve math", "how do we arrive at this value", "walk me through the backsolve numbers", "how does backsolve work", "how is the equity value derived", "show me the formulas", "show me the math" | `references/dive-in/backsolve/backsolve-explained.md` (only enter on explicit "explain / how is it calculated / show me the formulas" phrasing — do NOT enter for requests to configure or run backsolve) |
| "create an Excel spreadsheet for the backsolve", "export backsolve to Excel", "give me the backsolve in a spreadsheet", "backsolve Excel file", "download as Excel" | `references/dive-in/backsolve/backsolve-excel.md` — the file handles environment detection: writes directly into the current sheet when Claude for Excel is active, generates a `.xlsx` file otherwise |
| "create a backsolve artifact", "interactive backsolve calculator", "backsolve HTML", "show me an interactive calculator for the backsolve" | `references/dive-in/backsolve/backsolve-html.md` — fetch `get:backsolve` and `get:equity_adjustment` in parallel, then follow the file |
| "run waterfall / OPM / CSE", "allocate to share classes", "compute holdings value" | `references/dive-in/allocation.md`, for every target kind — **do not branch on `target.kind` here.** That file's Gate 0 resolves which methodologies the candidate supports from `get:configuration` and offers only those, covering CSE/Waterfall/OPM and the Niagara Waterfall / Niagara OPM pair alike. **Route the request and let Gate 0 make that call — don't call `get:configuration` here, and don't call it for any other row in this table.** It fires on an allocation request and nowhere else. Requires a positive EV; if zero or negative, surface plainly and route to `set-approaches.md`. Pass `valuationId` along with the usual ids — Gate 0 and the Niagara commands key off it alone. (`LLC_ENTITY` never reaches here — Step 2.5a stops it.) |
| "add another scenario", "create a Version 2", "what if {X}" | `references/dive-in/add-candidate.md` |
| "create a new valuation", "start a Q2 valuation", "new valuation as of {date}" | `references/dive-in/create-val.md` |
| "draft audit notes", "produce the audit memo" | `references/dive-in/audit-notes.md` |
| "view / read the valuation commentary", "add / edit / update the commentary", "write a note explaining this valuation", "clear the commentary" | `references/dive-in/commentary.md` |
| "upload/attach a document", "add the DCF workbook", "list documents", "what's attached to this valuation", "download a document", "get me the backsolve file" | `references/dive-in/documents.md` |
| "goal seek", "tune the EV to {target}", "open the GPC dashboard" | Solving backwards from a target value isn't something this skill does. Say so plainly in one line, then offer what it can do: set the company value directly (`references/dive-in/set-approaches.md`, Custom Value) or work the GPC multiples by hand (`references/dive-in/gpc-analysis.md`). Don't invent a solver, and don't iterate multiples yourself trying to land on the number. |
| "show fund holdings", "fund breakdown", "fund holdings value", "fund level breakdown" | Handled by the **global interrupt** (top of Routing) → **Fund Holdings (cross-flow capability)** below. Do **not** use `get:allocation` for this. |
| "finalize", "mark as final", "ship it" | `references/dive-in/ship.md` (requires a positive EV and holdings value — verified inline) |
| "delete this valuation" | `references/dive-in/ship.md` → **Delete a valuation** (requires an explicit `YES` before the call). |
| "I'm done", "let's move on", "back to the list", "back to the results" | Leave this valuation: stop the Step 2.5c checklist. If the user came from a bulk run and asks for the list, re-show it refreshed (`references/bulk/bulk-results.md` Step 4). Otherwise ask what they'd like to do next. |
| Anything else | Answer from the recap / current state, or ask one short clarifying question. |

Dependency gates still apply: a candidate must be selected for every flow
except create-val; allocation and finalize require a positive EV. Surface
plain-language messages on dependency failures.

### Step 2.5c: Valuation summary checklist (every response)

Render this markdown checklist after the Step 2.5a recap, then again at the
**end of every response** while the user is working on this valuation. That
includes responses from inside a dive-in flow (comps, financials,
allocation…), so the user never loses track of what's left.

Always render it **inside a fenced code block** (plain ```` ``` ````, no
language tag), so it shows as a boxed, monospaced panel set apart from the
chat text, the same treatment as the bulk runner's Step 5 status table.
Markdown doesn't render inside the block, so use no bold or links there.
It has three parts: the values (no heading), **Inputs:** and **Next steps:**.
Pad the labels so the values line up in one column:

````
```
MangoCart, Inc. summary

• Company value    -
• Holdings value   -

Inputs:
[ ] Financials (Required)
[ ] Comparables (Required)

Next steps:
[ ] Calculate GPC
[ ] Run allocation
```
````

Once values and inputs are in place (a GPC 60% / M&A 40% blend in EUR, to
show one Calculate item per method and that the currency comes from the
valuation):

````
```
Acme GmbH summary

• Company value    €48,200,000
• Holdings value   €6,150,000

Inputs:
[x] Financials (Required)
[x] Comparables (Required)

Next steps:
[x] Calculate GPC
[x] Calculate M&A
[x] Run allocation
```
````

A Custom Value valuation requires neither input, so neither is marked
`(Required)` and its **Next steps:** are `[ ] Set custom value`, then
`[ ] Run allocation` (Post-money: `[ ] Set post-money value`):

````
```
IMIM summary

• Company value    €10,000
• Holdings value   -

Inputs:
[ ] Financials
[ ] Comparables

Next steps:
[x] Set custom value
[ ] Run allocation
```
````

- **Company value** is End Goal item 4 and **Holdings value** is item 5.
  They are plain bullets (`•`), never checkboxes. Show the current value
  next to the item, or `-` when it's zero or negative (same exception to
  the **Table values** rule as the bulk results table: on a draft, zero or
  a debt-only negative means the value isn't set up yet).
  Format it in the valuation's currency
  (`get:valuation` → `currencyCode`). Never assume USD or `$`. With no
  currency code, show the bare number.
- **Selected methodology** comes from `get:valuation` too: the approaches with
  `isUsed: true` on the standard scenario (the `scenarios[]` entry whose `id`
  equals `standardScenario.id`). The method items' values need
  `get:approaches` (`approachValues`), which `get:valuation` doesn't carry.
- **Inputs:** always lists **Financials** then **Comparables**, whatever the
  methodology. Add ` (Required)` after each one the selected methodology
  requires, from **Required inputs by methodology** (End Goal). `[x]` when
  it's filled in (the **filled-in** rules there), `[ ]` when not, required
  or not. The two are independent: `(Required)` comes from the table alone,
  never from whether the input is filled in. A Backsolve valuation with
  financials in place shows `[x] Financials`, with no `(Required)`.
- **Next steps:** lists, in this order:
  1. one **method item** per selected methodology, in the API's order (see
     below);
  2. **Run allocation**, last, for every methodology.

  `[x]` when done, `[ ]` when not. The section always shows, because every
  methodology has at least a method item and Run allocation.
- **Run allocation** is `[x]` when the standard scenario's
  `allocation.isCompleted` is `true`, `[ ]` otherwise. It carries no value
  text, with one exception: `[ ] Run allocation   Failed` when an
  allocation attempt on this valuation failed earlier in the session. Never
  infer it from the holdings value: a fixed-value holding such as a
  convertible note gives a holdings value before any allocation has run.
- **Method items.** One per approach with `isUsed: true`. `[x]` when that
  approach has produced a positive value: `get:approaches` →
  `approachValues.{key}.value` > 0 (`gpc`, `ma`, `dcf`, `backsolve`,
  `postMoney`, `otherIndicationOfValue`, …). Zero or negative, e.g. GPC
  with no comps left holding only its debt adjustment, is `[ ]`. Label them
  by what the user does:

  | Approach key | Item |
  |---|---|
  | `gpc` | Calculate GPC |
  | `dcf` | Calculate DCF |
  | `ma` | Calculate M&A |
  | `backsolve` | Calculate Backsolve |
  | `asset` | Calculate Asset |
  | `investedCapital` | Calculate Invested capital |
  | `otherIndicationOfValue` | Set custom value |
  | `postMoney` | Set post-money value |
- **Re-fetch before every render. Trust the API, not the session.** In one
  parallel batch, silently call `get:valuation`, `get:approaches`,
  `get:financials` and `get:comparables`. Both inputs always show, so both
  are always fetched. The
  checklist must show what the user just changed: Comparables flips to
  `[x]` in the same response that saves the comps. Never re-render it from
  values held over from an earlier turn. Reads already made in the same
  response count (e.g. the Step 2.5a recap's), as long as no write came
  after them.
- Put nothing else in it: no status, cap table, command names, or IDs. The
  six-item ✅/⏳ view is still what "what's left?" / "am I done?" gets (see
  **How to use the goal**). Show that view in place of this checklist in
  the same response, not in addition to it.
- **Stop rendering it** only when the user leaves the valuation: they say
  they're done ("I'm done", "back to the list", "let's move on"), switch to
  another company, or start a different flow (dashboard, bulk runner). A
  global interrupt such as Fund Holdings hands control back to this
  valuation afterwards, so the checklist picks back up.

### Step 2.5d: Allocation complete: offer the review download

When the checklist's **Run allocation** step is `[x]` on a **DRAFT** valuation,
tell the user they can download the valuation for review before
finalizing. Put it directly under the checklist:

> ✅ Allocation is complete. Before you finalize, you can download this valuation for review: open it in Carta and choose **Actions → Export PDF** (or **Export Excel**).
>
> [View in Carta]({Pattern B deep link, value-holdings tab})

- **Once per valuation per session.** Show it the first time the item is
  `[x]`: right after an allocation run (`references/dive-in/allocation.md`
  Step 9 / N6), or on entering a draft whose allocation is already complete.
  Don't repeat it on every later checklist render.
- **Skip it for a FINAL valuation.** Its report was already rendered when
  it was finalized.
- **The download happens in Carta.** This skill has no command that exports
  a draft (the report is only rendered on finalize). So never say "I'll
  download it" or offer to fetch the file. Point at the Actions menu.
- Build the link per `references/deep-link.md`: Pattern B, `value-holdings`
  tab, rendered as a markdown link per its Step 5. The Actions menu is on every tab of
  the valuation page, so the allocation results tab is the natural landing
  spot.
- Keep **Finalize** as a later, separate step. The notice doesn't replace
  the Step 9 handoff menu; it goes above it.

---

## Step 3.1: Access check (silent)

Used by Step 2.2 (bare entry) and Step 3 (bulk general entry).

Nothing to do here. Access was settled once by **Gate 1** on first
invocation — do not probe, re-check, or call `search_tools` to confirm
availability. Proceed straight to Step 3.2.

(This step used to run a `search_tools` sentinel on
`portfolio_valuations:create:project`. That was always broken: the command
is registered unindexed, so it never appears in `search_tools` results for
anyone, and the check reported failure for entitled and unentitled callers
alike.)

## Step 3.2: Load and render the portfolio dashboard

Used by Step 2.2 (bare entry) and Step 3 (bulk general entry).
Access is already settled by **Gate 1** — fetch without re-checking.

### Render preference gate (runs once per session, before fetching data)

**This gate must run on every entry path — not just bare entry.** Before
fetching any dashboard data, check whether `dashboard_render_pref` is
already set in this session:

- **If already set**: skip the gate and proceed to the data fetch below.
- **If not set**: use the `env_mode` already
  established in Step 1 and ask the user for their preferred display
  format, inline as plain text (no `AskUserQuestion` — same question as
  Step 2.2b):
  - **`env_mode: "artifact"`** (`Artifact` available and neither
    `mcp__Claude_Preview__preview_start` nor `mcp__Claude_Browser__preview_start`
    is present, see Step 2.2a): ask
    > **How would you like to see your portfolio?**
    > 1. **Interactive dashboard**
    > 2. **Inline view**

    Store as `dashboard_render_pref`. If "Interactive dashboard", follow
    `references/cowork-artifact.md`.
  - **`env_mode: "preview-server"`** (`mcp__Claude_Preview__preview_start` OR
    `mcp__Claude_Browser__preview_start` present (see `preview_tool_family`),
    taking priority over `Artifact` when both are present): ask
    the same question as `artifact` mode above.
    Store as `dashboard_render_pref`. If "Interactive dashboard", load preview
    tool schemas via `ToolSearch` (for the recorded `preview_tool_family`) and
    follow `references/desktop-preview.md`.
  - **`env_mode: "inline"`** (neither tool available):
    no question — set `dashboard_render_pref: "markdown"` silently and proceed.

#### Param naming — non-negotiable

Carta's MCP API uses different parameter names and casing across
endpoints. **Do not pattern-match or guess.** Specifically, when calling
`read_tool` or `call_tool`, the `name` value and `arguments` keys below are fixed:

| `name` | Required `arguments` |
|---|---|
| `portfolio_valuations__list__portfolio_dashboard` | `organizationId` (NOT `organizationPk`), `page_size: 100` (always — never omit), `raw: false` (always — never omit). The formatted response strips null fields and is what downstream scripts expect. Only switch to `raw: true` when the user explicitly asks for the raw API response. |
| `portfolio_valuations__list__projects` | `ownerId`, `ownerKind: "FIRM"`, `targetId`, `targetKind: "CORPORATION"` (camelCase) |
| `portfolio_valuations__get__llc_cap_table_summary` | `issuerId` (the LLC issuer id — the candidate's `target.id` from `list:projects`, == the dashboard `llcIssuerId`); optional `asOfDate` — a **full ISO-8601 timestamp** (`YYYY-MM-DDT00:00:00Z`), **never** a bare `YYYY-MM-DD`. Both camelCase — contrast the c-corp cap-table commands' snake_case `project_id` / `candidate_id`. |
| `portfolio_valuations__get__configuration`, and the four Niagara commands (`compute__niagara_waterfall`, `get__niagara_waterfall`, `compute__niagara_opm`, `get__niagara_opm`) | `valuation_id` (snake_case) — the valuation's **integer** id, the `valuationId` on a `list:projects` candidate. These take it **alone**: no `ownerId`, no `project_id`, no `candidate_id`. Both `get__niagara_*` polls additionally require `groupingMethod` (camelCase, `BY_INTEREST_HOLDER` or `BY_INTEREST_TYPE`) and 400 without it. |

Using a wrong name returns a validation error.

**If `speculative_dashboard` is in context** (set by Step 1's speculative
fetch), use it directly as page 1 — do not re-fetch. If the portfolio
spans multiple pages, fetch the remaining pages normally using the cursor
from `speculative_dashboard`. If `speculative_dashboard` is absent or was
discarded (firm changed or error), fetch all pages fresh:

1. Call `read_tool({"name": "portfolio_valuations__list__portfolio_dashboard", "arguments": {"organizationId": "<org_pk>", "page_size": 100, "raw": false}})`
   to get the first page. Use `page_size: 100` unless the user has explicitly
   requested a different value — never omit it.
2. While `companies.length < totalCompanies`, call again with a `cursor`
   (or `page`) param from the previous response until you have all companies.
3. Merge all `companies` arrays from every page response into one array.
   Do **not** run `build_artifact.py` or render the dashboard until the
   last page is received.

Each page response shape:
- `companies` — portfolio companies in this page. Each item has:
  `name`, `corporationId`, `isCartaCorporation`, `hasCorpCapTable`,
  `hasCorpCapTableAccess`, `isLlc`,
  `llcIssuerId` (present only for LLC targets — the issuer id used as
  the cap-table `issuerId`),
  `latestValuation` (nullable — fields: `date`, `status`, `approaches`,
  `companyValue`, `holdingsValue`),
  `newFinancingRound` (nullable — fields: `shareClassName`, `cashRaised`,
  `closingDate`, `initialClosingDate`, `postMoney`),
  `newTenderOffer` (nullable — fields: `date`, `endDate`, `price`,
  `currencyCode`),
  `newShareTransfer` (nullable — fields: `date`, `operationType`,
  `quantity`, `pricePerShare`).
- `totalCompanies` — total count of portfolio companies.

If all `companies` entries are non-Carta, surface and stop:
> "**{firm_name}** has no Carta-managed portfolio companies yet. Add
> companies in Carta and come back."

#### Classify each company

**Events sections are independent** — a company can appear in multiple events sections
simultaneously if it has more than one event type. Each events section includes every
company where the condition holds, regardless of what other events that company has.

**Valuation and status groups are mutually exclusive** — assign each company to exactly
one of these based on the first condition it meets (priority order):

| Label | Condition |
|---|---|
| Draft valuation | `latestValuation != null && latestValuation.status == "DRAFT"` |
| Final valuation | `latestValuation != null && latestValuation.status == "FINAL"` |
| No valuation | `(hasCorpCapTable == true && latestValuation == null && hasCorpCapTableAccess == true) \|\| (isLlc == true && latestValuation == null)` |
| No cap table access | `hasCorpCapTable == true && hasCorpCapTableAccess == false` |
| No cap table | `hasCorpCapTable == false AND isLlc == false` |

**Events sections** — rendered independently, each showing all companies matching its condition:

| Section | Condition |
|---|---|
| Recent financing rounds | `latestValuation != null && newFinancingRound != null` |
| Recent tender offers | `latestValuation != null && newTenderOffer != null` |
| Recent share transfers | `latestValuation != null && newShareTransfer != null` |

> **LLC companies (`isLlc == true`) are always eligible.**: ignore `hasCorpCapTable` and `hasCorpCapTableAccess` entirely — they use `llcIssuerId` instead of a corp cap table. If they have a `latestValuation`, they fall into the events groups or valuation groups as normal. If they have no valuation, they go directly to the No valuation group regardless of cap table fields.

The No cap table group is **never rendered in the table**.

#### Render the dashboard as a grouped markdown table

Render as a grouped, numbered table. **Assign row numbers only to
companies in the events groups and valuation groups** — these are actionable.
The No cap table access group is shown without row numbers. Row numbers run as
a single sequence across all actionable groups. Only render non-empty groups;
precede each with a bold section label using the label name only
(e.g. **Recent financing rounds**, **Draft valuation**) — do not include group numbers.

**Valuation groups** (Draft valuation, Final valuation) columns: `#`, `Portfolio Company`,
`Latest Val. Date`, `Status`, `Approach`, `Company Value`, `Holdings Value`.

**No valuation** group columns: `#` and `Portfolio Company` only. Do not include valuation columns.

In the `Portfolio Company` cell, suffix the name with `[C]` if
`isCartaCorporation == true` (e.g., `MangoCart, Inc. [C]`).

**Recent financing rounds** — render as its own table with columns:
`Portfolio Company`, `Round`, `Cash raised`, `Post-money`, `Closing date`, `Initial close`.
Format cash raised and post-money with B/M/K suffix. Use `shareClassName` for Round,
`cashRaised`, `postMoney`, `closingDate`, `initialClosingDate` from `newFinancingRound`.

**Recent tender offers** — render as its own table with columns:
`Portfolio Company`, `Date`, `End date`, `Price`, `Currency`.
Use `date`, `endDate`, `price`, `currencyCode` from `newTenderOffer`.
Format price with B/M/K suffix.

**Recent share transfers** — render as its own table with columns:
`Portfolio Company`, `Date`, `Type`, `Quantity`, `Price per share`.
Use `date`, `operationType`, `quantity`, `pricePerShare` from `newShareTransfer`.
Format quantity with locale comma separators; format price per share as a decimal number.
Show `—` for price per share when null (non-sale transfers).

Companies in events sections **also appear in their valuation group** (Draft or Final)
with normal row numbers — the events tables are separate sections, not a replacement.

**Approach signals** — after all events tables, if any company appears in one or more events
sections, print an approach signals block headed **Approach signals:**. One line per company,
listing **all events present** and the recommended approach based on the event with the
**latest date**. If dates tie, financing round takes precedence over secondary market events.

Event → approach mapping:

| Event | Date field | Recommended approach |
|---|---|---|
| `newFinancingRound` | `closingDate` (fall back to `initialClosingDate`) | Post-Money — note the postMoney EV |
| `newTenderOffer` | `date` | Backsolve |
| `newShareTransfer` | `date` | Backsolve |

**Backsolve caveat (accuracy):** the bulk runner **can** create a
Backsolve valuation project — it is a supported methodology. It simply
does **not** auto-populate the Backsolve transaction price from the
event; that price is entered in Carta afterward (see bulk-runner Step
6.3). When recommending or creating Backsolve, never say it "can't be
created in bulk" or "requires a value first" — only the transaction
price entry is deferred to Carta.

Format each line as:
*{Company} — {all events with dates} → **{Approach}** (latest event: {event type}, {date})*

Example:
> **Approach signals:**
> - IMIM [C] — new financing round ($62.5M, 2018-03-02) → **Post-Money** (latest event: financing round, 2018-03-02)
> - Meetly [C] — tender offer (2020-01-10) + share transfer (2020-02-15) → **Backsolve** (latest event: share transfer, 2020-02-15)
> - Acme Corp — new financing round ($50M, 2026-01-15) + tender offer (2026-04-01) → **Backsolve** (latest event: tender offer, 2026-04-01)

**No cap table access** group — render as a single comma-separated line of company names
(no table). After the list, add the note plus the request-access link
(see `references/deep-link.md`'s **Cap table access request page** section
for how to construct it — firm-level, needs only the resolved `org_pk`):
*"Cap table access required — request it from the company, or create a
pro-forma cap table."*
[Request cap table access]({BASE_URL}/investors/firm/{ownerId}/information-access/?has_active_holdings=true&inactive=false&ordering=captable_access&page=1&page_size=50)

This is also the link to give whenever the user directly asks how to
request cap table access, or asks for "the request access link" —
independent of whether the dashboard is currently being rendered.

Sort within each group:
- Events groups (Recent financing rounds, Recent tender offers, Recent share transfers): alphabetical by company name
- Valuation groups (Draft valuation, Final valuation): newest `latestValuation.date` first
- No valuation: alphabetical by company name
- No cap table access: alphabetical

Format currency with a B/M/K suffix ($12.5M, $8.0M, $1.2B). Show `—`
for any unavailable column.

After all group tables, print a legend line:
> *[C] = Carta company*

Then, if any companies have `hasCorpCapTable == false AND isLlc == false`, print:
> *{N} companies have no cap table and are not shown. To run
> valuations for these companies, a pro-forma cap table must be
> created first. Ask me to list them if you'd like to see them.*

#### Derive bucket lists for Step 3.3 (silent)

After rendering, silently capture four derived lists into context —
these power Step 3.3's prose suggestions:

- **New events** — companies appearing in any events section (Recent financing rounds, Recent tender offers, Recent share transfers). A company with multiple event types is counted once.
- **Draft** — companies in the Draft valuation group (draft valuation in progress, no new events).
- **No valuation** — companies in the No valuation group (no valuation yet, accessible cap table).
- **Final** — companies in the Final valuation group (final valuation, no new events).

The No cap table access and No cap table groups are never included in any bucket.


