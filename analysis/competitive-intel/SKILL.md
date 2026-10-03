---
name: competitive-intel
description: "Federal capture competitor, incumbent, and obligation intelligence backed by live USAspending.gov data via the vendored `usaspending` MCP. USE WHEN the user asks \"who's the incumbent on this contract?\", \"what was the last award value?\", \"give me a black-hat read on Bidder X\", \"who are the top three competitors for this NAICS?\", \"what's typical pricing for this work?\", \"pull award history for this agency / NAICS / PSC\", \"analyze burn rate\", \"obligation trend by year\", or \"start from this contract number\". Supports both black-hat competitor research and contract-number-first obligation analysis, including standalone awards, parent IDIQs, and orders under IDIQs with parent/child rollups. DO NOT USE FOR proposal drafting (use `proposal-generator`), clause / FAR compliance audit (use `compliance-auditor`), or generic web search about a company (no MCP tool covers that yet)."
license: MIT
metadata:
  title: Competitive Intel
  category: market-competitive
  status: active
  origin: theseus
  invoke: agent
  runtime: tools
  supports_llm: true
  max_turns: 20
  mcps:
    - usaspending-gov-mcp
    - sam-gov-mcp
  output: "pursuits/{slug}/02_intel/competitive_intel.json"
  upstream: govcon-capture-vibe/.github/skills/competitive-intel
---
# Competitive Intel — Black-Hat + Obligation Intel

## Capture-insights adapter (no KG / no VDB)

**Run** from **Agent Skills** or chat ("burn rate on contract X") — no CLI.

- **Workflow B/C (active):** Deterministic USAspending collector via `usaspending-gov-mcp`. Paginates IDV child orders per Settings caps. Full JSON at `02_intel/competitive_intel_obligation.json`; brief at `02_intel/competitive_intel.md`.
- **Context:** Pipeline row `award_key`, pursuit workspace, or PIID typed in chat.
- **Workflow A (black-hat):** Later slice — uses pursuit vault files + DuckDB + MCP, not a knowledge graph.

Every claim must trace to a **vault file path**, **DuckDB citation**, or a **USAspending award** from MCP — never invented entities.

You are a **federal capture analyst** working against the active **pursuit workspace** (Studio markdown + Pipeline row) PLUS live USASpending.gov award data (via the `usaspending` MCP). This skill has three modes:

- **Workflow A (Black-Hat)**: Convert pursuit/RFP context into a defensible black-hat brief on incumbent and likely competitors. *(PR3 — vault context bundle, not KG.)*
- **Workflow B (Vehicle Obligation Intel)**: Start from a contract number and build a parent-level obligation rollup, child-order accumulation, sibling-awardee context, and vehicle-wide insights.
- **Workflow C (Single Award / Order Burn Intel)**: Start from one contract or order number and produce a clean by-award burn read with grouped modifications, POP windows, and localized insights.

## When to Use

- "Who's the incumbent on this contract?"
- "Pull award history for similar work in the last 5 years"
- "Black-hat: what would Lockheed bid here?"
- "What's the typical price range for this NAICS at this magnitude?"
- "Top 3 competitors for a 541512 IT modernization recompete with HHS"
- "Here's a contract number - show burn rate / obligation trend"
- "Is this contract an IDIQ parent, an order, or standalone?"
- "Roll up obligations across all child orders"
- "If this is an order under a multiple-award IDIQ, who are all parent-level competitors?"

## Operating Discipline

- **Workspace first, web second.** The KG is the source of truth for the opportunity (program, agency, NAICS, PSC, place of performance). USAspending is the source of truth for who has actually won similar work.
- **Cite everything.** Workspace claims cite `chunk_id` (e.g., `[chunk-xxxxxxxx]`). Award claims cite the USAspending `generated_internal_id` (e.g., `[award:CONT_AWD_…]`).
- **Rank by obligated dollars, not transaction count.** A vendor with one $400M IDV beats a vendor with 200 $50K POs.
- **Linkage precedence for vehicle analysis.** For multiple-award IDIQs, resolve relationships in this order: parent IDV linkage, explicit child-order listing, PIID-family context, then solicitation identifier as a fallback signal.
- **Reject anti-patterns.** Inventing competitors not in award history. Pricing ranges with no underlying award sample. Generic SWOT bullets ("strong past performance"). Unsupported claims about CPARS or protests (no MCP source for those yet — say so).
- **Treat deterministic rosters as authoritative.** If `parent_vehicle_awardees` is present in the collector result or artifact, that is the complete parent-level prime roster for the answer. Do not add extra vehicle holders from memory, loose keyword matches, or workspace hints. The number you state in prose must equal `parent_vehicle_awardee_count` / `len(parent_vehicle_awardees)`.
- **Fail loudly.** If the workspace is missing NAICS / PSC / agency, halt with a `GAP` rather than guess.

## Workflow Selector

Pick exactly one workflow before running tools:

- **Workflow A: Black-Hat Competitor Intel (default)**
  Trigger: incumbent/competitor/theming/pricing benchmark questions anchored on NAICS/agency/program context.
- **Workflow B: Vehicle Obligation Intel**
  Trigger: user provides a contract number/PIID and asks for parent-level burn-rate, obligation trend, IDIQ hierarchy, child-order rollups, sibling awardees, vehicle competitors, or an overarching view of how the whole vehicle is burning.
- **Workflow C: Single Award / Order Burn Intel**
  Trigger: user provides one contract or order number and primarily wants that one award's mods, POP, burn-rate, option pattern, or a clean single-award read rather than a vehicle aggregation.

If both black-hat and obligation analysis are requested, run Workflow B or C first and feed its `competitor_discovery` result into Workflow A.

If the user wants both parent-level vehicle context and one-order detail, choose **Workflow B** and use the collector's grouped `award_rollups` / artifact `obligations.by_award` to write the order-specific portion. Do not narrate every order modification in the parent-level summary.

---

## Workflow A Checklist (Black-Hat)

Execute in order. Record entity counts, NAICS codes, and award IDs as you go so the final envelope can be audited.

### 1. Inventory the workspace context (KG slice)

Call `kg_entities` with:

```json
{
  "types": [
    "program",
    "organization",
    "contract_line_item",
    "regulatory_reference",
    "requirement",
    "deliverable"
  ],
  "limit": 60,
  "max_chunks": 2,
  "max_relationships": 3
}
```

Extract:

- **Agency / sub-agency** (look in `organization` entities; cross-check `program`)
- **NAICS code** (often a `regulatory_reference` like "NAICS 541512")
- **PSC code** (similar — `regulatory_reference` like "PSC R499")
- **Place of performance** (state / city if present)
- **Estimated magnitude** (search `contract_line_item` or chunks for "$", "ceiling", "estimated value")

If NAICS AND PSC are both missing, halt with `GAP: workspace lacks NAICS and PSC — cannot scope award history`. If only one is missing, proceed but flag it in `warnings`.

### 2. Resolve fuzzy codes via USAspending autocompletes

If the workspace mentions a NAICS by description but not by number (e.g., "custom computer programming"), call `mcp__usaspending__autocomplete_naics` with the keyword. If the agency is a friendly name ("Air Force") but you need the toptier code, call `mcp__usaspending__list_toptier_agencies` once and resolve. Same drill for PSC via `mcp__usaspending__autocomplete_psc` or `mcp__usaspending__get_psc_filter_tree`.

### 3. Pull award history (the spine)

Call `mcp__usaspending__search_awards` with a filters object scoped to the resolved NAICS, agency, and a 5-year window:

```json
{
  "filters": {
    "naics_codes": ["<resolved naics>"],
    "agencies": [
      { "type": "awarding", "tier": "toptier", "name": "<agency name>" }
    ],
    "time_period": [{ "start_date": "<5y ago>", "end_date": "<today>" }],
    "award_type_codes": ["A", "B", "C", "D"]
  },
  "fields": [
    "Award ID",
    "Recipient Name",
    "Award Amount",
    "Period of Performance Start Date",
    "Period of Performance Current End Date",
    "Awarding Agency",
    "Awarding Sub Agency",
    "Award Type"
  ],
  "page": 1,
  "limit": 100,
  "sort": "Award Amount",
  "order": "desc"
}
```

`A`/`B`/`C`/`D` are contract award types (BPA, PO, definitive contract, IDV order). Capture the top ~50 by amount. If the result count is < 5, broaden: drop the agency filter, then drop the date window — and note the broadening in `warnings`.

### 4. Identify the incumbent

Within the result set scoped to the same agency and a recent active period of performance, the **incumbent** is typically the recipient with the largest obligated dollars on a contract whose period of performance covers today. If multiple candidates, pick the one whose award also matches the workspace's program name or PIID prefix (search chunks for the PIID, then call `mcp__usaspending__lookup_piid`). If no contract is currently active, fall back to "most recent prior award winner" and label as `incumbent_status: "prior"` instead of `"current"`.

### 5. Rank likely competitors

From the same award-history slice, take the top ~10 recipients by total obligated dollars. Drop the incumbent. The top 3–5 of the remainder are your "likely competitors". For each, call `mcp__usaspending__autocomplete_recipient` to get the recipient hash, then `mcp__usaspending__get_recipient_profile` for the full profile (parent recipient, business types, total federal contract dollars).

### 6. Pricing benchmark

Call `mcp__usaspending__spending_by_category` with category `awarding_agency` (or `naics`) over the same 5-year window:

```json
{
  "category": "naics",
  "filters": {
    "naics_codes": ["<resolved naics>"],
    "time_period": [{ "start_date": "<5y ago>", "end_date": "<today>" }]
  },
  "limit": 10
}
```

From the matching award sample (step 3), compute the median, p25, and p75 of award amount as your "typical award value range". Sample size MUST be ≥ 10 to publish a range — otherwise label as `pricing_band: "insufficient sample"` and report the raw min/max with a count.

### 7. (Optional) Recent transactions for the incumbent

For the incumbent's flagship award, call `mcp__usaspending__get_transactions` to surface modifications. A burst of recent option exercises with no scope expansion is a recompete signal worth noting.

### 8. Synthesize the black-hat one-pager(s)

For each competitor (incumbent + top 3 likely), populate the Black-Hat one-pager structure. `read_file references/black_hat_template.md` for the canonical layout. Each one-pager:

- Names the competitor + role (`incumbent | likely-1 | likely-2 | likely-3`)
- Lists their **last 3 wins** in this NAICS/agency with dollar amount + PoP + award_id
- Predicts 2–3 themes they will likely use (anchored to their public award history — e.g., "they've won 4 of the last 5 cyber recompetes at this agency, expect a continuity-of-operations theme")
- Flags **claim gaps** — things we cannot validate from MCP data (CPARS scores, protest history, news) and which the user must research manually before red-team
- Suggests **2 ghost-language hooks** for `proposal-generator` to weave in

### 9. Self-critique + anti-slop gate

Before writing the envelope: re-read your draft and confirm:

- Every "incumbent" / "competitor" name appears in the step-3 award results (no inventions)
- Every pricing claim has an underlying sample size ≥ 10
- No SWOT bullet uses generic adjectives ("strong", "robust", "leading") without an award_id citation
- Every `claim_gap` is honest about what MCP cannot verify (CPARS, protests, news)

If any check fails, iterate — do not ship.

### 10. Write the JSON envelope (MANDATORY — do this BEFORE any final summary)

**You MUST call `write_file` to save the envelope to `artifacts/competitive_intel.json` before producing your final assistant message.** This is the skill's primary deliverable — a run that ends without this artifact is a failed run, regardless of how good the prose summary looks.

If you are running low on turns and have not yet written the artifact, **stop gathering data and write what you have now**, with `warnings[]` honestly noting what is incomplete. A partial envelope with `claim_gap` entries is more useful than no envelope.

Match the Output Contract below. After `write_file` succeeds, the final assistant message is a short cover note summarizing counts (incumbent identified yes/no, # competitors profiled, sample size for pricing, # warnings) and pointing at the artifact path. Do not write more prose before the artifact is on disk.

## Output Contract

```json
{
  "opportunity_context": {
    "program_name": "<from workspace>",
    "agency": "<resolved name>",
    "agency_toptier_code": "<resolved code>",
    "naics_code": "<resolved>",
    "naics_description": "<from autocomplete>",
    "psc_code": "<resolved or null>",
    "place_of_performance": "<state or null>",
    "estimated_magnitude_usd": <number or null>,
    "context_chunk_ids": ["chunk-xxxxxxxx"]
  },
  "incumbent": {
    "name": "<recipient name>",
    "recipient_hash": "<from get_recipient_profile>",
    "incumbent_status": "current | prior | unknown",
    "flagship_award_id": "<generated_internal_id>",
    "flagship_award_amount_usd": <number>,
    "period_of_performance": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
    "evidence_award_ids": ["<id1>", "<id2>"]
  },
  "competitors": [
    {
      "rank": 1,
      "name": "<recipient name>",
      "recipient_hash": "<hash>",
      "last_3_wins_in_naics": [
        {"award_id": "<id>", "amount_usd": <n>, "agency": "<name>", "pop_end": "YYYY-MM-DD"}
      ],
      "predicted_themes": ["<theme 1 grounded in award history>"],
      "claim_gaps": ["No CPARS data via MCP", "No protest history via MCP"],
      "ghost_language_hooks": ["<hook 1>", "<hook 2>"]
    }
  ],
  "pricing_benchmark": {
    "sample_size": <n>,
    "pricing_band": "valid | insufficient sample",
    "p25_usd": <n or null>,
    "median_usd": <n or null>,
    "p75_usd": <n or null>,
    "min_usd": <n>,
    "max_usd": <n>,
    "window": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
  },
  "recompete_signals": [
    "<observation, e.g. incumbent's flagship PoP ends in 7 months — recompete window>"
  ],
  "warnings": [
    "<e.g. 'PSC missing from workspace — search broadened to NAICS only'>"
  ],
  "data_provenance": {
    "kg_chunk_ids": ["chunk-xxxxxxxx"],
    "usaspending_award_ids": ["<generated_internal_id>"],
    "tools_invoked": ["mcp__usaspending__search_awards", "mcp__usaspending__get_recipient_profile", "..."]
  }
}
```

## Hand-off to `proposal-generator`

When the cover note is written, suggest the user run `proposal-generator` next so the `predicted_themes` and `ghost_language_hooks` from each competitor flow into the win-themes / FAB-chains step. Do not call `proposal-generator` yourself — that's a Phase 5 capability.

---

## Workflow B Checklist (Vehicle Obligation Intel)

Execute in order. The output is a **parent-level vehicle summary** backed by child-order accumulation, grouped award data, and competitor completeness findings.

### 1. Resolve the contract number

Input may be contract/order number only. **Do not hand-walk the USAspending hierarchy anymore.**

Call `collect_competitive_obligation_intel` once with the raw contract number and `scope="vehicle"`. That tool deterministically:

- resolves the PIID,
- classifies `standalone_contract | parent_idiq | idiq_order`,
- expands child orders / sibling orders without spending more model turns,
- pulls all transaction pages needed for the rollup,
- computes period-of-performance, fiscal-year, burn-rate, competitor-completeness, and PTW seed fields,
- computes `insights.headline` plus deterministic story blocks you should use in prose before free-writing,
- returns compact `award_rollups` so you can reason about one order without re-walking the hierarchy,
- writes `artifacts/competitive_intel_obligation.json` directly.

Only fall back to manual `mcp__usaspending__*` calls if the deterministic collector returns an explicit tool error or warns that linkage is incomplete.

Record:

- `input_contract_number`
- `resolved_award_id`
- `resolved_award_type`
- `resolved_piid`

If no match, return `GAP: contract number not found in USAspending lookup_piid`.

### 2. Classify scenario

The deterministic collector already classifies the resolved award into one of:

- `standalone_contract`
- `parent_idiq`
- `idiq_order`

Classification in the artifact must cite the detail fields used. Never infer vehicle class from PIID format alone.

### 3. Build hierarchy and obligation rollup

The deterministic collector already applies the scenario-specific logic below and persists the output contract for you. Treat this section as the behavior contract the collector must satisfy:

- **Standalone contract**:
  - Call `mcp__usaspending__get_transactions` on the resolved award.
  - Sum obligations by transaction, period of performance, and fiscal year.
  - Preserve transaction metadata that helps a human read the burn: `action_date`, modification identifier if present, `action_type`, `action_type_description`, and transaction-level narrative/description if present.

- **Parent IDIQ**:
  - Pull children via `mcp__usaspending__get_idv_children` and/or `mcp__usaspending__get_idv_activity`.
  - For each child order, pull transactions and compute per-order totals, period-of-performance view, and annual trend.
  - Report parent direct obligations separately from child obligations.

- **IDIQ order**:
  - Pull this order's transactions and totals.
  - Resolve parent IDIQ from award detail.
  - Pull sibling orders under the same parent and roll up full vehicle totals.
  - Use order and parent award detail plus sibling activity to capture the order's current period of performance window and any visible base/current/potential end dates.

For all scenarios:

- Include deobligation periods explicitly; net totals can decrease over time.
- Prefer **period-of-performance breakdowns over fiscal-year rollups** in the narrative and the artifact. Fiscal years are still required, but POP windows are the primary burn-rate lens.
- Build `obligations.by_period_of_performance` from award-detail and child-activity dates. Use the strongest available fields such as start date, current end date, and potential end date. If only a single current POP window is available, still emit it.
- For each item in `obligations.by_transaction`, include human-readable transaction metadata. If the transaction payload does not expose a narrative description, set `modification_description` to `null` and add a warning rather than inventing one.
- Keep `obligations.by_award` clean and grouped. This is the primary structure for single-award or per-order reading. `by_transaction` is the whole-vehicle flattened audit trail.

**Derived fields — compute from fetched data (no additional MCP calls required):**

- Sort `by_transaction` by `action_date` ascending.
- Compute `cumulative_obligated_usd` as the running total of `amount_usd` through each transaction row (preserving negatives for deobligations).
- Assign `inferred_pop_segment` using this rule:
  - Modification `0` (or first transaction) → `"base_year"`
  - Each action_type `G` ("EXERCISE AN OPTION") transaction → `"option_year_1"`, `"option_year_2"`, etc. in sequence
  - Action_type `B` ("SUPPLEMENTAL AGREEMENT") or `J` ("FAR 52.232-22 FUNDED") within a segment → `"supplemental"`
  - Action_type `M` ("OTHER ADMINISTRATIVE ACTION"), `X` (termination), or `R` (rescind/cancel) → `"admin"`
  - Unknown or null action_type → `"unknown"`
- Compute `rate_analysis` using `obligations.by_period_of_performance.current_order_pop` (or the strongest available POP window):
  - `total_pop_days` = `pop_end_current` − `pop_start` in calendar days
  - `total_pop_months` = round to nearest 0.5
  - `monthly_burn_usd` = `net_obligated_usd` / `total_pop_months`
  - `daily_burn_usd` = `net_obligated_usd` / `total_pop_days`
  - `by_option_year`: group transactions by `inferred_pop_segment`, sum `amount_usd` per segment, estimate the segment's date window as the span between consecutive G-type action dates (use award end date as the final segment's close), and compute `monthly_rate_usd` = segment `obligated_usd` / segment `months`.
  - Include `derivation_notes` listing assumptions made (e.g., "Option year boundaries estimated from G-type action dates; per-modification POP dates not available in USAspending transaction payload").

### 4. Competitor completeness for multiple-award vehicles

For `parent_idiq` and `idiq_order` scenarios, derive competitor sets in two views:

- **Order-holder view**: distinct recipients with child orders under the parent IDIQ.
- **Parent-holder view**: parent recipients (normalize subsidiaries where possible).

Use parent/child vehicle linkage as primary. Use solicitation identifier only as a fallback clustering signal when direct linkage is incomplete.

Emit `competitor_discovery.completeness_status` as:

- `high` when parent-child traversal succeeded and sibling coverage is strong,
- `medium` when partial child coverage exists,
- `low` when only fallback solicitation clustering was possible.

Also surface `competitor_discovery.parent_vehicle_awardees` when available. This is the parent-level prime roster for the vehicle and is different from active order holders.

### 5. Produce PTW seed outputs

Compute and include:

- recent annual run-rate,
- trailing 3-year weighted run-rate,
- highest-obligation years,
- optional-year pattern signal,
- recommended PTW baseline input.

### 6. Write the obligation envelope (MANDATORY)

`collect_competitive_obligation_intel` already writes `artifacts/competitive_intel_obligation.json` before it returns. Do not rebuild the JSON envelope by hand unless you are intentionally creating a smaller derivative artifact.

```json
{
  "input_contract_number": "<raw user input>",
  "resolved": {
    "award_id": "<generated_internal_id>",
    "piid": "<resolved piid>",
    "scenario": "standalone_contract|parent_idiq|idiq_order"
  },
  "hierarchy": {
    "parent_award_id": "<id or null>",
    "child_award_ids": ["<id>"]
  },
  "obligations": {
    "total_obligated_usd": 0,
    "net_obligated_usd": 0,
    "by_period_of_performance": [
      {
        "label": "current_order_pop",
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD",
        "obligated_usd": 0,
        "source": "award_detail|idv_activity|derived"
      }
    ],
    "by_fiscal_year": [{ "fy": "2025", "amount_usd": 0 }],
    "rate_analysis": {
      "pop_start": "YYYY-MM-DD",
      "pop_end_current": "YYYY-MM-DD",
      "total_pop_months": 0,
      "total_pop_days": 0,
      "monthly_burn_usd": 0,
      "daily_burn_usd": 0,
      "by_option_year": [
        {
          "label": "base_year|option_year_1|option_year_2|...",
          "estimated_start": "YYYY-MM-DD",
          "estimated_end": "YYYY-MM-DD",
          "months": 0,
          "obligated_usd": 0,
          "monthly_rate_usd": 0
        }
      ],
      "derivation_notes": [
        "<e.g. 'Option year boundaries estimated from action dates of G-type mods; actual POP dates not in USAspending transaction payload'>"
      ]
    },
    "by_transaction": [
      {
        "transaction_id": "<id>",
        "action_date": "YYYY-MM-DD",
        "modification_number": "0|P00001|null",
        "action_type": "G|B|M|null",
        "action_type_description": "EXERCISE AN OPTION|SUPPLEMENTAL AGREEMENT FOR WORK WITHIN SCOPE|null",
        "modification_description": "<transaction narrative if present>|null",
        "amount_usd": 0,
        "cumulative_obligated_usd": 0,
        "inferred_pop_segment": "base_year|option_year_1|option_year_2|supplemental|admin|unknown"
      }
    ],
    "by_child_order": [
      {
        "award_id": "<id>",
        "description": "<child order description if present>|null",
        "pop_start_date": "YYYY-MM-DD|null",
        "pop_end_date": "YYYY-MM-DD|null",
        "amount_usd": 0
      }
    ]
  },
  "competitor_discovery": {
    "order_holder_recipients": [{ "name": "<recipient>", "obligated_usd": 0 }],
    "parent_holder_recipients": [{ "name": "<parent>", "obligated_usd": 0 }],
    "linkage_method_used": "parent_child|piid_family|solicitation_fallback",
    "completeness_status": "high|medium|low"
  },
  "ptw_seed": {
    "recent_annual_run_rate_usd": 0,
    "three_year_weighted_run_rate_usd": 0,
    "recommended_baseline_usd": 0
  },
  "warnings": ["<data caveat or linkage caveat>"],
  "data_provenance": {
    "usaspending_award_ids": ["<generated_internal_id>"],
    "tools_invoked": [
      "mcp__usaspending__lookup_piid",
      "mcp__usaspending__get_award_detail",
      "mcp__usaspending__get_transactions",
      "mcp__usaspending__get_idv_children"
    ]
  }
}
```

Do not omit these fields just because they are sparse. A partially populated POP or transaction record is still useful if it clearly shows which values were unavailable from the source.

### 7. Final cover note

Summarize:

- scenario detected,
- total/net obligations,
- number of child orders,
- competitor completeness status,
- PTW seed recommendation,
- warnings.

Start from `insights.headline` and `insights.blocks` from the collector result or artifact. Treat them as the deterministic spine of the cover note, not optional garnish.

For **Workflow B**, keep the cover note parent-level and insight-driven:

- open with `insights.headline` verbatim or nearly verbatim,
- use `burn_posture` as the quantitative lead,
- use `vehicle_concentration` to decide which 1-3 child orders matter most,
- use `competitive_context` for the exact parent-awardee roster / completeness sentence,
- surface `caveats` directly instead of paraphrasing warnings into mush,
- lead with vehicle-wide burn and what it implies,
- mention the sibling parent-awardee roster when relevant, using `parent_vehicle_awardees` as the exact roster,
- if you state a parent-awardee count in prose, copy the exact deterministic count from `parent_vehicle_awardee_count` and make the listed roster match it,
- call out the 1-3 most important child orders or burn inflection points,
- avoid itemizing every order unless the user explicitly asks for that level of detail.

Reference the saved artifact path from the deterministic tool result.

---

## Workflow C Checklist (Single Award / Order Burn Intel)

Execute in order. The output is a **single-award read**, not a vehicle-wide narrative.

### 1. Resolve the contract or order number

Call `collect_competitive_obligation_intel` once with the raw contract number and `scope="single_award"`.

Use the tool result first. It already gives you:

- `resolved` scenario,
- `award_rollups` for clean grouped per-award analysis,
- `insights` with a deterministic headline plus burn/award-story blocks,
- aggregate competitor context if the award sits inside a larger vehicle,
- `vehicle_context` when the resolved award sits inside a larger vehicle.

Do not re-walk `get_transactions` manually unless the collector fails. Do not call `read_file` on `artifacts/competitive_intel_obligation.json`; the runtime `read_file` tool cannot open run artifacts. Use the collector result fields directly.

### 2. Select the focus award

Pick one focus award and stay on it:

- `standalone_contract` -> the resolved award
- `idiq_order` -> the resolved order
- `parent_idiq` -> only stay in Workflow C if the user explicitly wants one child order or one award's burn; otherwise switch to Workflow B

Use `award_rollups` / `obligations.by_award` as the canonical grouped structure. Do not reconstruct a single-award view from the flattened `by_transaction` list unless a grouped row is missing.

### 3. Write the single-award burn read

For the selected award, summarize:

- award id / PIID / role,
- POP start/end,
- gross + net obligations,
- fiscal-year pattern,
- important modifications and option events,
- current burn-rate,
- warnings or data quality limits.

This prose should read like one clean contract story. Keep mods grouped under that award. Do not drift into sibling or whole-vehicle narrative except a short context sentence when useful.

### 4. Optional parent-vehicle context

If the focus award belongs to a multiple-award vehicle, add a short context block only:

- parent IDIQ identity,
- sibling parent-awardee count,
- whether competitor completeness is high / medium / low.

Keep this to orientation, not the main answer.

### 5. Final cover note

Summarize the one award:

- scenario,
- selected award id / PIID,
- POP,
- total/net obligations,
- monthly / daily burn,
- biggest one or two modification inflection points,
- warnings.

Open with `insights.headline`. Then use `award_story` as the contract-story paragraph, `burn_posture` as the rate paragraph, optional `competitive_context` for brief parent-vehicle orientation, and `caveats` for blunt warnings. Do not ignore these blocks and rebuild the story from raw `by_transaction` unless an insight block is missing.

Reference the saved artifact path. If deeper detail exists for adjacent awards, mention that grouped `by_award` data is available in the artifact.

## References

- [`references/black_hat_template.md`](./references/black_hat_template.md) — Canonical one-pager structure
- [`references/data_sources.md`](./references/data_sources.md) — USAspending MCP tool reference + what each field means + known gaps (no CPARS / no protest data via MCP yet)
