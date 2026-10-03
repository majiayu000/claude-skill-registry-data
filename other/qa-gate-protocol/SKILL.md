---
name: qa-gate-protocol
last_updated: 2026-05-17
description: "Beamix's 4-tier QA gate: Trivial/Lite/Full/Irreversible classification, reviewer assignment, evaluator-optimizer pattern, multi-judge setup, Codex CLI graceful degradation, and bypass rules. Use when QA-Lead is classifying a PR or CTO is routing a task to the correct tier."
tags: [quality, beamix-specific, testing, security]
source: beamix-authored 2026-05-16
risk: low
---

# QA Gate Protocol

## Quick reference

> Trivial / Lite / Full / Irreversible. `qa-tier-floor.yml` sets minimum tier deterministically. `<verdict>PASS|BLOCK</verdict>` XML tag mandatory.

## When to use

- QA-Lead assigning a risk tier to an incoming PR
- CTO pre-classifying a task before spawning workers
- Authoring or refining `.claude/qa-tier-floor.yml`
- Debugging why a merge was blocked or a bypass was rejected

## When NOT to use

- For product unit/integration test authoring (that's test-engineer's job)
- For performance testing (that's performance-engineer)

## The 4-tier matrix

| Tier | LOC threshold | Risk examples | Reviewers | Human sign-off |
|------|--------------|--------------|-----------|---------------|
| **Trivial** | < 50 LOC | Typo fix, copy change, log line | Auto-approve (post-tool-use hook passes) | None |
| **Lite** | < 300 LOC | Single-domain feature, non-auth API route | code-reviewer (Sonnet) | None |
| **Full** | 300+ LOC OR touches auth/billing/migrations/RLS | Auth flow, Paddle webhook, DB migration | code-reviewer + security-engineer (Opus) + Codex CLI | CEO can bypass with reason |
| **Irreversible** | Any LOC | Schema deletion, pricing change, vendor lock | Full reviewers + multi-judge + Adam sign-off | Required — cannot be bypassed |

Note: 300 LOC threshold is active during pre-revenue MVP sprint. Reverts to 100 LOC after first paying customer (per locked decision D8, 2026-05-16).

## Deterministic tier floor (file-path map)

The `.claude/qa-tier-floor.yml` file assigns minimum tiers by file path. The Cloudflare bridge reads it — no LLM involved.

```yaml
# .claude/qa-tier-floor.yml
floors:
  # Billing — always Full minimum
  - pattern: "apps/web/src/app/api/billing/**"
    min_tier: full
  - pattern: "apps/web/src/lib/paddle/**"
    min_tier: full

  # Auth — always Full minimum
  - pattern: "apps/web/src/middleware.ts"
    min_tier: full
  - pattern: "apps/web/src/app/api/auth/**"
    min_tier: full

  # Migrations — always Full minimum
  - pattern: "apps/web/supabase/migrations/**"
    min_tier: full

  # RLS policies — Full minimum
  - pattern: "**/*.sql"
    min_tier: full

  # War-room agent files — Lite minimum
  - pattern: ".claude/agents/**"
    min_tier: lite
  - pattern: ".claude/skills/**"
    min_tier: lite
```

A PR touching `apps/web/src/lib/paddle/webhook.ts` is always Full, regardless of LOC count.

## Evaluator-optimizer pattern

QA-Lead does not just flag issues — it also verifies the goal was achieved (intent, not just tests).

```
Goal inference: "Did this PR achieve the intent stated in the Linear ticket?"
State change check: "Does the diff produce the expected state change in the product?"
Test verification: "Do existing tests still pass? Are new tests present?"
```

QA-Lead never evaluates its own writes. If QA-Lead authored a file being reviewed, it spawns a second reviewer or flags conflict-of-interest to CEO.

## Multi-judge (Full and Irreversible tiers)

Full-tier PRs get two independent reviewers:
1. `code-reviewer` (Sonnet) — correctness, patterns, edge cases
2. `security-engineer` (Opus) — auth, RLS, injection, secrets exposure

Each reviewer returns structured findings independently (no cross-contamination before final report).

Irreversible-tier additionally gets:
3. Codex CLI `codex review --diff <pr-diff>` — external perspective

## Codex CLI graceful degradation (locked decision D6, 2026-05-16)

If `codex review --diff` fails (auth expired, binary not found, CLI breaking change):

```bash
# Graceful degradation pattern
if ! command -v codex &> /dev/null; then
  echo "codex_unavailable" >> audit_log_local
  CODEX_STATUS="unavailable"
fi

if [ "$CODEX_STATUS" = "unavailable" ]; then
  # Proceed with Claude-only multi-judge
  # Spawn a second Claude instance (different temperature/framing) as alternative judge
  # Write audit_log row: codex_status=unavailable
  echo "Proceeding with Claude-only multi-judge. Codex unavailable."
fi
```

Never hard-block a merge because Codex is unavailable. Log it. Continue with Claude-only review.

## QA-Lead return contract

Every QA-Lead response MUST include the XML tag for hook parsing:

```xml
<verdict>PASS</verdict>
```
or
```xml
<verdict>BLOCK</verdict>
```

Full return JSON:

```json
{
  "verdict": "PASS",
  "tier_assigned": "lite",
  "reviewers_spawned": ["code-reviewer"],
  "codex_status": "pass | fail | unavailable",
  "findings": [
    {
      "severity": "suggestion",
      "file": "apps/web/src/app/api/scan/start/route.ts",
      "line": 42,
      "description": "Consider adding explicit error boundary for Inngest event failure",
      "fix": "Wrap in try/catch and return 202 regardless of Inngest queue state"
    }
  ],
  "evidence_log": "session file: docs/08-agents_work/sessions/2026-05-16-qa-lead-bmx101.md"
}
```

Finding severity levels:
- `critical` — blocks merge (security hole, data loss risk, spec violation)
- `important` — blocks merge unless CEO bypasses
- `suggestion` — informational, does not block

## Bypass rules

Only CEO can bypass, and only for Trivial and Lite tiers.

```
# Required in PR comment to bypass:
BYPASS REASON: <specific, non-generic reason>

# Invalid bypass reasons (will be rejected by qa-lead-pass.yml hook):
"moving fast"
"low risk"
"urgent"
```

Full and Irreversible tiers: **cannot be bypassed under any circumstances.** The GitHub branch protection rule `qa-lead-pass.yml` enforces this structurally.

Every bypass writes an `audit_log` row with `status: bypass_invoked` and the stated reason.

## See also

- `code-review-excellence` — [[code-review-excellence]]
- `security-audit` — [[security-audit]]
- `worktree-isolation-pattern` — [[worktree-isolation-pattern]]
- `find-bugs` — [[find-bugs]]

## Anti-patterns

- Downgrading a tier without documented evidence (e.g., "this migration is trivial")
- Accepting a CTO return without re-checking files in the tier-floor YAML
- Verbose verdicts with prose explanations — binary verdict + structured findings only
- Self-evaluation: QA-Lead reviewing files it wrote
- Marking a PR PASS without checking that `apps/web/supabase/migrations/` is not in the diff when tier < full
- Skipping the `<verdict>PASS</verdict>` XML tag (hook parsing fails silently without it)
