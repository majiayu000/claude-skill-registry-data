---
name: promotion-gate
description: "Enforce evidence-backed promotion criteria for candidate learnings. Use when the user runs /evolution promote <id>. Wraps bin/evolve-promote.sh and explains why each gate passed or failed. Never promotes on its own judgment — always runs the script."
---

# promotion-gate

## When to use
- `/evolution promote <candidate-id>` — user explicitly requests promotion.
- Before manual editing of `stable/global.md` — to confirm a proposed edit would have passed the gate.

## Protocol
1. Identify the candidate file: `~/.claude/evolution/candidates/<id>.yaml`.
2. Run gate check: `bash ~/.claude/evolution/bin/evolve-promote.sh --check <id>`.
3. Show the user each gate result (pass/fail with the specific reason).
4. If all gates pass AND the user confirms, run: `bash ~/.claude/evolution/bin/evolve-promote.sh <id>`.
5. Show the resulting diff of `stable/global.md` (or `stable/by-project/<slug>.md`).
6. Record the promotion as an evidence event (type: adaptation).

## Hard rules from `config.yaml`
- `evidence_count ≥ min_evidence` (default 3).
- Distinct `session_ids.length ≥ min_distinct_sessions` (default 2).
- Distinct `project_slugs.length ≥ min_distinct_projects` (default 2) — unless `scope: project-specific`.
- `last_confirmed > last_failed`.
- Post-promotion stable-file size ≤ `startup_budget_chars` (default 4000).
- No contradictions with existing stable rules.

## What to do on gate failure
- Explain each failed gate in plain English.
- Suggest what would unblock it (more evidence, wait for cross-project confirmation, condense text).
- Do NOT bypass the gate. Do NOT write to stable/ manually. If the user insists, document the bypass in `reports/` with reason.

## Output
Plain-text verdict per gate, followed by either (a) the diff of the promoted file or (b) the blocking reasons.
