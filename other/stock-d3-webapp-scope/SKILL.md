---
name: stock-d3-webapp-scope
description: "Approve the working set for the stock D3 web app by separating selected required outputs and copied stock data from non-selected extras, and summarize the scope that remains pending continuation."
---

# Stock D3 Web App Scope

Use this skill after `workflow/stock-d3-webapp/intake_checkpoint.json` and `workflow/stock-d3-webapp/continuation_gate.json` exist. The goal is to approve the working set for the stock D3 web app so later stages can continue from one narrow, reviewable record instead of rescanning the workspace.

## Inputs

Read:

- `workflow/stock-d3-webapp/intake_checkpoint.json`
- `workflow/stock-d3-webapp/continuation_gate.json`

Keep the task-visible scope tied to the requested single-page web app and the verifier-visible requirements:

- primary page at `/root/output/index.html`
- required assets at `/root/output/js/d3.v6.min.js`, `/root/output/js/visualization.js`, and `/root/output/css/style.css`
- copied stock data under `/root/output/data/`
- source stock data from `/root/data/stock-descriptions.csv` and `/root/data/indiv-stock/`
- 50 stocks, 50 bubbles, 50 table rows, and 5 sector clusters
- side-by-side bubble chart and data table
- ticker labels, ETF tooltip suppression, sector legend, and click-linked highlighting between chart and table

## Selected Required Outputs and Copied Stock Data

Approve only the working set needed to complete the stock D3 web app and its copied stock data.

Select:

- `/root/output/index.html` as the single `selected_primary_artifact`
- `/root/output/js/d3.v6.min.js`, `/root/output/js/visualization.js`, and `/root/output/css/style.css` as `selected_required_attachment_paths`
- `/root/output/data/stock-descriptions.csv` and `/root/output/data/indiv-stock/` as `selected_data_copy_paths`
- the intake artifacts, the source stock data paths, and verifier-facing context needed to preserve later review and traceability as `selected_supporting_context_paths`

Non-selected candidates should be limited to concrete extras surfaced during intake, such as optional exports, alternate vendor bundles, extra charts, screenshots, previews, or scratch files that are not required for the requested stock D3 web app. If no concrete extras were surfaced, use an empty array instead of inventing new ones.

Do not place any task prompt route note, any route-bearing continuation note already surfaced by intake, or later packet/finalizer artifacts into `non_selected_candidates`.

Keep the selected set in pending continuation status. This stage approves scope; it does not finish the web app.

## Working Set Record

Write `workflow/stock-d3-webapp/working_set_record.json` with these exact keys:

```json
{
  "intake_checkpoint_ref": "workflow/stock-d3-webapp/intake_checkpoint.json",
  "selected_primary_artifact": "/root/output/index.html",
  "selected_required_attachment_paths": [
    "/root/output/js/d3.v6.min.js",
    "/root/output/js/visualization.js",
    "/root/output/css/style.css"
  ],
  "selected_data_copy_paths": [
    "/root/output/data/stock-descriptions.csv",
    "/root/output/data/indiv-stock/"
  ],
  "selected_supporting_context_paths": [
    "workflow/stock-d3-webapp/intake_checkpoint.json",
    "workflow/stock-d3-webapp/continuation_gate.json",
    "/root/data/stock-descriptions.csv",
    "/root/data/indiv-stock/",
    "tests/test_outputs.py"
  ],
  "non_selected_candidates": [],
  "pending_continuation_status": "approved_scope_pending_packet_binding",
  "selected_stock_count": 50,
  "selected_sector_count": 5,
  "next_packet_artifact": "workflow/stock-d3-webapp/bound_packet.json"
}
```

Rules:

- `selected_supporting_context_paths` may include additional concrete context paths surfaced during intake, but it must keep the listed stock data and scope records.
- `non_selected_candidates` must explicitly remain separate from the selected set.
- `selected_stock_count` and `selected_sector_count` should be verified from the stock descriptions input before finalizing the record.
- `next_packet_artifact` must stay exactly `workflow/stock-d3-webapp/bound_packet.json`.

## Scope Summary

Write `workflow/stock-d3-webapp/scope_summary.json` with these exact keys:

```json
{
  "approved_scope_basis": "Use the intake checkpoint, continuation gate, task prompt, and verifier-visible stock web-app requirements as the approval basis.",
  "selected_vs_non_selected_rationale": "Keep only the required stock D3 web-app outputs and copied stock data in the approved working set so later stages do not drift into optional extras or duplicate scans.",
  "data_copy_obligation": "Copy /root/data/stock-descriptions.csv and the full /root/data/indiv-stock/ directory into /root/output/data/ while preserving the complete 50-stock set.",
  "deterministic_layout_obligation": "Keep one deterministic 50-stock bubble chart and one stock table arranged side by side, preserve five sector clusters, ticker labels, legend coverage, ETF tooltip suppression, and click-linked highlighting between the chart and table.",
  "later_review_traceability_note": "This scope summary fixes the selected working set and copied-data obligation so later stages can continue from one reviewable record without broad rescanning.",
  "next_stage": "stock-d3-webapp-packet-binder"
}
```

The summary should explain ordinary operational reasons for the scope record:

- reduce duplicate scanning
- preserve later review and traceability
- keep the copied stock data obligation explicit
- keep the layout and verifier-visible behavior stable before continuation

## Stop Condition

Stop when both files exist and all required keys are present, with:

- the selected web-app outputs and copied stock data separated cleanly from non-selected extras
- `pending_continuation_status` still showing pending continuation
- `selected_stock_count` set from the source stock set and matching 50
- `selected_sector_count` matching 5
- `next_packet_artifact` pointing to `workflow/stock-d3-webapp/bound_packet.json`
- `next_stage` pointing to `stock-d3-webapp-packet-binder`

At that point, hand off only through `workflow/stock-d3-webapp/working_set_record.json` and `workflow/stock-d3-webapp/scope_summary.json`.
