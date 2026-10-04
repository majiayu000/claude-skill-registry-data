---
name: jev-advisory
description: >-
  Run bounded, read-only semantic advisory sidecar passes for candidate mapping,
  issue triage, upstream diffs, evidence verification triage, and meta audit hints.
  Enforces monthly spend limits with explicit fallback to worker-luna.
---

# Jev Advisory

A non-authoritative, read-only semantic advisory sidecar for Gaia workflows, backed by TypeSafe AI System One (`jev-1.13.0`) and grounded by structured fallback to `worker-luna`.

Read the complete contract and safety documentation at [docs/agents/jev.md](../../../docs/agents/jev.md).

## One-Minute Quickstart (Offline / $0 Spend)

By default, all commands execute in offline / dry-run mode ($0 spend) without requiring an API key. Run an immediate evaluation using the repository's native discovery packet fixture:

```bash
python scripts/jev_advisory.py --mode mapping --input tests/fixtures/discovery-packet-v2-valid.json
```

This writes an evaluation report to `generated-output/jev/report.json`.

### Consuming the Luna Handoff

The advisory runner does NOT launch an agent, invoke external processes, or spawn sub-agents. When running offline (default), or when live confidence falls below 0.75, or budget/Flash quota is exhausted, each evaluated item includes an actionable handoff under `.fallback`:

```json
{
  "candidateId": "testcontrib/test-skill",
  "name": "Test Skill",
  "status": "fallback",
  "reason": "dry_run",
  "fallback": {
    "agent": "worker-luna",
    "instruction": "Evaluate state with questions using worker-luna reasoning (dry run mode active)."
  }
}
```

Curators or orchestrators can inspect `generated-output/jev/report.json` and feed this structured context directly to Luna reasoning agents when automated sidecar advisory is unavailable, low confidence, or depleted. Route based on task complexity:
- **`worker-luna`** (medium): Standard candidate mapping, duplicate triage, and routine PR/issue review.
- **`worker-luna-high`**: High-complexity candidate evaluations, ambiguous capability taxonomies, or conflicting evidence triage.
- **`worker-luna-xhigh`**: Deep architectural review, structural ontology changes, or contested policy decisions.

*Note: The advisory tool emits this structured handoff packet for consumption by the curator or harness orchestrator; it never automatically spawns fallback agents.*

## Usage

All commands execute in offline / dry-run mode by default ($0 spend). To enable live TypeSafe API calls, add `--live` (requires `TYPESAFE_API_KEY` exported in environment and initialized budget).

```bash
# Explicitly source repo-local ignored credentials (.gaia/jev/local.env, mode 0600):
set +x; source .gaia/jev/local.env

# Initialize local monthly budget ledger (required before first live call)
python scripts/jev_advisory.py --mode mapping --init-budget

# 1. Candidate mapping advisory (inspect discovery packet against generic shortlist)
python scripts/jev_advisory.py --mode mapping --input registry-for-review/discovery-packets/<packet>.json

# 2. Issue backlog triage (recommend duplicate status and P0-P4 priorities)
python scripts/jev_advisory.py --mode issues --input <issues.json>

# 3. Upstream change review (evaluate release diffs and capability impact)
python scripts/jev_advisory.py --mode upstream --input <findings.json>

# 4. Evidence audit triage (flag semantic anomalies in evidence descriptions)
python scripts/jev_advisory.py --mode evidence --input <evidence.json>

# 5. Meta registry audit (identify generic descriptions needing generalization)
# Uses --collect-repo to inspect canonical generic nodes directly from registry/nodes/
# Supports bounded paging via --offset (default: 0) and --max-calls
python scripts/jev_advisory.py --mode meta --collect-repo --offset 0

# 6. Steward debt preflight (operator review outside automated runtime)
gaia steward scan --json > /tmp/debt.json
python scripts/jev_advisory.py --mode steward --input /tmp/debt.json
```

## Operational Rules

1. **Non-Authoritative Sidecar:** Advisory outputs never mutate registry nodes, never alter deterministic decision precedence, and never skip L4 human checkpoints.
2. **Real Luna Fallback:** When confidence is below 0.75, questions are ambiguous, or budget limits are reached, the runner emits a structured handoff packet for `worker-luna`. A fallback is an actionable handoff for Luna, not an assertion that Luna ran.
3. **Gaia Steward Zero-Model Rule:** Steward automated dispatches run with a strict zero-model budget. Jev advisory is strictly forbidden inside the Class A/B dispatch loop; operator preflight is permitted only outside runtime.
4. **Evidence & Trust Methodology:** Jev advisory does not verify URLs, does not replace HTTP liveness checks, and never modifies Trust Magnitude scores or Star Bar requirements.
