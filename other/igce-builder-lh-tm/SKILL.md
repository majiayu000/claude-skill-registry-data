---
name: igce-builder-lh-tm
description: "Labor-hour and time-and-materials cost buildup with fully burdened hourly rates (BLS OEWS + GSA CALC+ + per diem MCPs). USE WHEN the user asks to \"build a T&M IGCE\", \"labor hour estimate\", \"fully burdened hourly rate\", \"LH IGCE\", \"time and materials pricing\", or \"burden multiplier stack\". Exports JSON + XLSX to Studio. DO NOT USE FOR FFP wrap rates (`igce-builder-ffp`), cost-reimbursement fee caps (`igce-builder-cr`), or OT bids (`ot-prototype-strategist`)."
license: MIT
metadata:
  title: IGCE Builder — LH / T&M
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
  output: "pursuits/{slug}/03_capture/igce_lh_tm.json"
  upstream: 1102tools.com/tools
---
# IGCE Builder — LH / T&M

## Capture-insights adapter (contractor seat)

**Run** from Agent Skills or chat — mirrors [1102tools IGCE Builder LH/T&M](https://1102tools.com/tools) burden math for **your** loaded rate card.

- **Deterministic:** base wage → fringe+OH burden → G&A wrap → fully burdened hourly per category.
- **MCP:** BLS + CALC+ + Per Diem when keys configured.
- **Outputs:** `03_capture/igce_lh_tm.json`, `.md`, `.xlsx`.

## When to Use

- "Build T&M / labor-hour IGCE."
- "Fully burdened rates for our rate card."
- "Burden multiplier stack for LH contract."

## When NOT to Use

- FFP total price → `igce-builder-ffp`
- CPFF/CPAF/CPIF → `igce-builder-cr`

## Operating Discipline

- Report **fully burdened hourly** and line totals (rate × hours) per labor category.
- Hours from vault FTE lines or default staffing mix.
- Government IGCE typically excludes profit on LH; contractor may layer fee in proposal — document separately in chat if needed.