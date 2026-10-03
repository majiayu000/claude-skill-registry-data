---
name: igce-builder-ffp
description: "Firm-fixed-price cost buildup mirroring 1102 IGCE FFP wrap-rate math (BLS OEWS + GSA CALC+ + GSA Per Diem). USE WHEN the user asks to \"build an FFP IGCE\", \"wrap rate buildup\", \"FFP cost estimate\", \"layer fringe overhead G&A fee\", \"how should we price this FFP task order\", or \"IGCE parity for our bid\". Pulls labor categories from pursuit vault or defaults, stacks fringe/overhead/G&A/fee, exports JSON + XLSX to Studio. DO NOT USE FOR T&M/LH pricing (`igce-builder-lh-tm`), cost-reimbursement (`igce-builder-cr`), OT milestones (`ot-prototype-strategist`), or obligation intel (`competitive-intel`)."
license: MIT
metadata:
  title: IGCE Builder — FFP
  category: acquisition-deliverables
  status: active
  origin: 1102-federal-contracting-skills
  invoke: agent
  runtime: tools
  supports_llm: true
  max_turns: 10
  mcps:
    - bls-oews-mcp
    - gsa-calc-mcp
    - gsa-perdiem-mcp
  output: "pursuits/{slug}/03_capture/igce_ffp.json"
  upstream: 1102tools.com/tools
---
# IGCE Builder — FFP

## Capture-insights adapter (contractor seat)

**Run** from Agent Skills or chat — mirrors [1102tools IGCE Builder FFP](https://1102tools.com/tools) math for **your bid**, not an official government IGCE submission.

- **Deterministic:** labor categories from vault (or PM/SME/Analyst/Engineer defaults) → fringe → overhead → G&A → fee.
- **MCP:** BLS OEWS, GSA CALC+, GSA Per Diem when configured; graceful proxy when offline.
- **Outputs:** `03_capture/igce_ffp.json`, `.md`, `.xlsx` (via renderers toolchain).
- **Handoff:** `ptw-analysis`, `proposal-generator`.

You are a capture pricing analyst building a defendable **firm-fixed-price** cost stack. Use the same layered wrap-rate discipline a contracting specialist applies in an IGCE — inverted for the bidder who must hit a competitive FFP number.

## When to Use

- "Build an FFP IGCE for this pursuit."
- "Wrap rate buildup — fringe, OH, G&A, fee."
- "What's our FFP price ceiling from labor assumptions?"
- "IGCE parity check before we submit."

## When NOT to Use

- Labor-hour / T&M → `igce-builder-lh-tm`
- CPFF / CPAF / CPIF → `igce-builder-cr`
- OT prototype milestones → `ot-prototype-strategist`
- Incumbent burn rate → `competitive-intel` + `ptw-analysis`

## Operating Discipline

- **Cite wage sources.** BLS series, CALC+ keyword/N, or explicit "hourly proxy" when MCP offline.
- **No invented labor.** Pull categories from vault SOW/PWS; default mix only when vault is silent.
- **Wrap order:** direct labor → fringe (32%) → overhead on direct (75%) → G&A on subtotal (12%) → fee on pre-fee (8%). Document rates in JSON `buildup[]`.
- **Contractor stance.** This informs your bid — not advice to the government.

## Output Contract

JSON at `pursuits/{slug}/03_capture/igce_ffp.json` with `labor_categories[]`, `buildup[]`, `totals{base,total}`, `mcp_benchmarks[]`, `sheets_for_xlsx` for workbook export.