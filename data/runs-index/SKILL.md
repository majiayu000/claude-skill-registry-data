---
name: runs-index
description: "Update index.json status. Use for: upsert index.json, update status/last_flow/updated_at. Deterministic writes - stable diffs, no creation. Use only in run-prep and *-cleanup agents. Invoke via bash .claude/scripts/demoswarm.sh index upsert-status."
allowed-tools: Bash, Read, Write
---

# Runs Index Skill

Deterministic updates to `.runs/index.json`. Write-bearing but with minimal surface.

## Invocation

**Always invoke via the shim:**

```bash
bash .claude/scripts/demoswarm.sh index upsert-status [options]
```

**Do not set PATH or call helpers directly.** The shim handles resolution.

---

## Operating Invariants

### Repo root only

- Assume working directory is repo root.
- All paths are repo-root-relative.

### Minimal ownership

This skill only updates:

- `status`
- `last_flow`
- `updated_at`

Other fields (`canonical_key`, `issue_number`, `pr_number`, etc.) are owned by `run-prep`, `signal-run-prep`, and `gh-issue-manager`.

### Stable diffs

- Upsert by `run_id` (update in place, not append)
- Preserve existing ordering
- Output is sorted for stable git diffs

---

## Allowed Users

Only these agents may use this skill:

- `run-prep`
- `signal-run-prep`
- `signal-cleanup`
- `plan-cleanup`
- `build-cleanup`
- `gate-cleanup`
- `deploy-cleanup`
- `wisdom-cleanup`

---

## Command Reference

| Command               | Purpose                         |
| --------------------- | ------------------------------- |
| `index upsert-status` | Update run status in index.json |

---

## Quick Example

```bash
# Update index after signal cleanup
bash .claude/scripts/demoswarm.sh index upsert-status \
  --index ".runs/index.json" \
  --run-id "feat-auth" \
  --status "VERIFIED" \
  --last-flow "signal" \
  --updated-at "$(bash .claude/scripts/demoswarm.sh time now)"
# stdout: ok
```

---

## Contract Rules

1. **stdout**: `ok` on success, error message on failure
2. **exit code**: `0` on success, non-zero on failure
3. **Idempotent**: Running twice with same args produces same result
4. **No creation**: If `.runs/index.json` doesn't exist, fail (run-prep owns creation)

---

## Index Schema Reference

```json
{
  "version": 1,
  "runs": [
    {
      "run_id": "feat-auth",
      "canonical_key": "gh-456",
      "task_key": "feat-auth",
      "task_title": "Add OAuth2 login",
      "issue_number": 456,
      "pr_number": null,
      "updated_at": "2025-12-11T22:15:00Z",
      "status": "VERIFIED",
      "last_flow": "signal"
    }
  ]
}
```

This skill only updates: `status`, `last_flow`, `updated_at`.

---

## For Agent Authors

In cleanup agents:

1. **Use `runs-index`** for index updates (no inline jq)
2. **Handle missing index** — if `.runs/index.json` is missing, add a blocker and do not create it
3. **Use `runs-derive` for reading** — this skill is write-only

Example pattern in cleanup agent:

```bash
# Get current timestamp
TIMESTAMP=$(bash .claude/scripts/demoswarm.sh time now)

# Update index
bash .claude/scripts/demoswarm.sh index upsert-status \
  --index ".runs/index.json" \
  --run-id "$RUN_ID" \
  --status "$STATUS" \
  --last-flow "signal" \
  --updated-at "$TIMESTAMP"
```

---

## Installation

The Rust implementation is preferred. Install to repo-local directory:

```bash
cargo install --path tools/demoswarm-runs-tools --root .demoswarm
```

The shim will automatically resolve in order:

1. `.demoswarm/bin/demoswarm` (repo-local install, preferred)
2. `demoswarm` on PATH (global install)
3. `cargo run` fallback (dev environments)
4. Python fallback (legacy)
