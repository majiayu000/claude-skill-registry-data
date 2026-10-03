---
name: igce-builder-cr
description: "Cost-reimbursement IGCE scaffold for CPFF, CPAF, and CPIF with fee caps and estimated-cost structure (BLS + CALC+ + per diem MCPs). USE WHEN the user asks to \"build a CPFF IGCE\", \"cost reimbursement estimate\", \"CPAF fee cap\", \"CPIF incentive structure\", \"CR IGCE\", or \"estimated cost plus fee\". DO NOT USE FOR FFP (`igce-builder-ffp`) or T&M (`igce-builder-lh-tm`)."
license: MIT
metadata:
  title: IGCE Builder — Cost-Reimbursement
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
  output: "pursuits/{slug}/03_capture/igce_cr.json"
  upstream: 1102tools.com/tools
---
# IGCE Builder — Cost-Reimbursement

## Capture-insights adapter (contractor seat)

**Run** from Agent Skills or chat — mirrors [1102tools IGCE Builder CR](https://1102tools.com/tools) for **bidder** estimated-cost + fee planning.

- **Detects** CPFF / CPAF / CPIF signals from vault clause text.
- **Fee caps:** CPFF 10%, CPAF ~6% base, CPIF incentive envelope (documented in JSON).
- **Outputs:** `03_capture/igce_cr.json`, `.md`, `.xlsx`.

## When to Use

- "CPFF estimated cost + fee buildup."
- "Cost-reimbursement IGCE scaffold."
- "What fee headroom under FAR 16.306?"

## Operating Discipline

- Separate **estimated cost** (direct + ODC proxy) from **fee** line.
- Cite inferred CR type and cap in `totals.fee_cap_note`.
- Contractor uses this to sanity-check proposal cost volume — not to file a government IGCE.