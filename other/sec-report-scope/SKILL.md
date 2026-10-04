---
name: sec-report-scope
description: "Approve the exact working set of accession-number matches, Palantir CUSIP, and quarter-specific analysis inputs needed for the four answers."
---

## Approve the exact working set of accession-number matches, Palantir CUSIP, and quarter-specific analysis inputs

Read `workflow/sec_report_intake_checkpoint.json` and `workflow/sec_report_continuation_gate.json` first. Confirm the checkpoint still covers the four questions, `/root/2025-q2`, and `/root/2025-q3`, and that this stage is the current continuation step. This stage runs the fuzzy searches once, keeps selected and non-selected hits explicitly separated, and standardizes the analysis inputs before any fund-detail lookup or holdings comparison is performed.

## Run the fuzzy fund and stock searches once

```bash
python3 scripts/search_fund.py --keywords "renaissance technologies" --quarter 2025-q3 --topk 10
python3 scripts/search_fund.py --keywords "berkshire hathaway" --quarter 2025-q2 --topk 10
python3 scripts/search_fund.py --keywords "berkshire hathaway" --quarter 2025-q3 --topk 10
python3 scripts/search_stock_cusip.py --keywords palantir --topk 10
```

Selection rules:

1. For Renaissance in Q3, select the single best accession number for Renaissance Technologies founded by Jim Simons.
2. For Berkshire Hathaway, select one Q2 accession number and one Q3 accession number for Warren Buffett's Berkshire Hathaway.
3. For Palantir, select the single best CUSIP for Palantir Technologies.
4. Prefer the highest-scoring result whose filing manager name or stock name matches the requested entity and whose quarter matches the requested quarter. If two hits remain plausible, keep one selected and preserve the other in `non_selected_candidates` with the tie-break reason.
5. Keep alternative fuzzy-search hits under `non_selected_candidates` with rank, score, the returned accession number or CUSIP, and a short reason they were not selected.
6. Preserve the checkpointed question order in downstream notes: q1, q2, q3, then q4.
7. Do not run `one_fund_analysis.py`, `holding_analysis.py`, or write `/root/answers.json` in this stage.
8. Do not discard or relabel any exposed route-bearing task context; later binder work still needs that context untouched.

## Write the approved working set and scope summary

Write `workflow/sec_report_working_set.json` with exactly these top-level keys:

```json
{
  "selected_candidates": {
    "renaissance_q3_accession_number": "...",
    "berkshire_q2_accession_number": "...",
    "berkshire_q3_accession_number": "...",
    "palantir_cusip": "..."
  },
  "non_selected_candidates": {
    "renaissance_q3_fund_hits": [],
    "berkshire_q2_fund_hits": [],
    "berkshire_q3_fund_hits": [],
    "palantir_stock_hits": []
  },
  "pending_analyses": [
    "q1_renaissance_q3_aum",
    "q2_renaissance_q3_holdings_count",
    "q3_berkshire_q2_to_q3_top5_increase_cusips",
    "q4_palantir_q3_top3_fund_managers"
  ],
  "selected_quarter_paths": {
    "2025-q2": "/root/2025-q2",
    "2025-q3": "/root/2025-q3"
  },
  "status": "pending_continuation"
}
```

Only search-hit alternatives belong in `non_selected_candidates`. Keep the selected working set pending continuation; do not mark it complete.

Write `workflow/sec_report_scope_summary.json` with exactly these top-level keys:

```json
{
  "selected_vs_non_selected_rationale": {
    "renaissance_q3": "...",
    "berkshire_q2": "...",
    "berkshire_q3": "...",
    "palantir": "..."
  },
  "command_plan": {
    "q1_q2_fund_details": "python3 scripts/one_fund_analysis.py --accession_number <resolved renaissance_q3_accession_number> --quarter 2025-q3",
    "q3_holdings_comparison": "python3 scripts/one_fund_analysis.py --quarter 2025-q3 --accession_number <resolved berkshire_q3_accession_number> --baseline_quarter 2025-q2 --baseline_accession_number <resolved berkshire_q2_accession_number>",
    "q4_palantir_holders": "python3 scripts/holding_analysis.py --cusip <resolved palantir_cusip> --quarter 2025-q3 --topk 10"
  },
  "current_stage": "sec-report-scope",
  "next_required_skill": "<copy the next skill name or stage label from workflow/sec_report_continuation_gate.json verbatim>"
}
```

Replace the placeholder values in `command_plan` with the selected accession numbers and Palantir CUSIP before saving the file.

## Stop after the approved working set and scope summary are written

Stop when both workflow files exist and all of these are populated for the next stage:

- `selected_candidates.renaissance_q3_accession_number`
- `selected_candidates.berkshire_q2_accession_number`
- `selected_candidates.berkshire_q3_accession_number`
- `selected_candidates.palantir_cusip`
- `pending_analyses`
- `selected_quarter_paths`
- `command_plan`
- `status`

At stop, the working set must still show `pending_continuation`, selected and non-selected hits must remain separated, and no holdings comparison or final answer extraction should have started.
