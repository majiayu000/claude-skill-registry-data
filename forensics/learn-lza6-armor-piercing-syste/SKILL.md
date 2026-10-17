---
name: learn
description: "Record a platform response and update learning. Usage: /learn <report_id> <status> [--bounty 500] [--vuln-type XSS]"
disable-model-invocation: false
---
Record platform response: $ARGUMENTS

1. Parse arguments and run: `uv run python3 $CLAUDE_PROJECT_DIR/tools/response_tracker.py log $ARGUMENTS`
2. Also update brain: `uv run python3 $CLAUDE_PROJECT_DIR/tools/brain.py log "Report response: $ARGUMENTS"`
3. Sync to global brain: `uv run python3 $CLAUDE_PROJECT_DIR/tools/global_brain.py sync-from-local`
4. Show updated insights: `uv run python3 $CLAUDE_PROJECT_DIR/tools/response_tracker.py insights`

## Top-Tier Learning Loop

Convert every platform response into a future hunting rule.

- If accepted: record the decisive proof artifact, impact framing, asset type, vuln variant, bounty tier, and why triage agreed.
- If duplicate: record the duplicated primitive and which uniqueness signal was missing.
- If N/A: record the exact sentence or policy clause that killed it.
- If informative: record the missing chain or business impact required to make it payable.
- If severity changed: record the evidence that moved it up or down.

End with one concrete update: a brain pattern, a never-submit rule, a report wording change, or a target ranking adjustment.
