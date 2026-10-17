---
name: sync
description: "Sync program scope, policy, and hacktivity from a bug bounty platform. Usage: /sync hackerone tesla or /sync bugcrowd uber"
disable-model-invocation: false
---
Sync bug bounty program data: $ARGUMENTS

Parse the arguments as: <platform> <program_handle>

1. Use the `bounty-platforms` MCP server tool `sync_program` with the platform and program handle. This fetches scope, policy, and hacktivity and writes them to the current directory.
2. After sync completes, run `uv run python3 $CLAUDE_PROJECT_DIR/tools/brain.py init` if brain isn't initialized yet.
3. Read the generated `scope.yaml` and `hacktivity.md` files.
4. Update the brain with key intelligence from hacktivity:
   - Run `uv run python3 $CLAUDE_PROJECT_DIR/tools/brain.py log "Synced program data from <platform>/<program>"`
   - If hacktivity shows common vulnerability types, note them as priority areas
   - If hacktivity shows many duplicates of a type, note them as areas to avoid
5. Summarize: scope overview, policy highlights (restrictions, safe harbor), and hacktivity patterns (most common vuln types, average bounties).

## Top-Tier Sync Standard

Policy is hunting input, not paperwork.

Extract and persist:
- exact in-scope assets, wildcard rules, mobile/API/cloud qualifiers, and third-party exclusions
- required headers, user-agent, testing accounts, sandbox rules, rate limits, and forbidden actions
- severity exclusions and never-pay classes
- payout hints from hacktivity: accepted classes, duplicate-heavy classes, bounty tiers, triage language
- newly added or removed assets since last sync

End with a hunt bias: where the program appears to pay, where it appears saturated, and what proof standard the policy implies.
