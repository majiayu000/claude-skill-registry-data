---
name: runs-derive
description: "Grep/wc replacement for .runs artifacts. Use for: count, extract, Machine Summary, receipt reading, marker counts. Null-safe counting (REQ/NFR/QID/RSK markers), YAML block parsing, BDD scenario counting. Deterministic read-only - no judgment. Use when cleanup agents need mechanical counts/extraction. Invoke via bash .claude/scripts/demoswarm.sh."
allowed-tools: Bash, Read
---

# Runs Derive Skill

Read-only, deterministic helpers for `.runs/` derivation. Use when cleanup agents need mechanical counts/extraction without interpretation.

## Invocation

**Always invoke via the shim:**

```bash
bash .claude/scripts/demoswarm.sh <command> [options]
```

The shim resolves implementation in order:
1. `.demoswarm/bin/demoswarm` (Rust binary, preferred)
2. `demoswarm` on PATH (global install)
3. `cargo run` fallback (dev environments)
4. Python fallback (legacy)

**Do not set PATH or call helpers directly.** The shim handles resolution.

---

## Operating Invariants

### Repo root only

- Assume working directory is repo root.
- All paths are repo-root-relative.

### Null over guess (counts)

- **File/dir missing** → `null` (NOT `0`)
- **Present but no matches** → `0`
- **Present but unparseable / tool error** → `null`

### No writes

This skill only reads. Index updates use `runs-index`. Secrets use `secrets-tools`.

---

## Command Reference

| Command | Purpose |
|---------|---------|
| `count pattern` | Count lines matching regex in a file |
| `count bdd` | Count BDD scenarios in feature files |
| `ms get` | Extract field from Machine Summary block |
| `yaml get` | Extract field from fenced YAML block |
| `yaml count-items` | Count items in YAML block |
| `inv get` | Extract inventory marker value |
| `line get` | Extract value from line with prefix |
| `receipts count` | Count prior flow receipts in run dir |
| `receipt get` | Read field from receipt JSON |
| `openapi count-paths` | Count paths in OpenAPI YAML |
| `time now` | Get current UTC timestamp |

---

## Quick Examples

### Counting patterns (stable markers)

```bash
# Count functional requirements
bash .claude/scripts/demoswarm.sh count pattern \
  --file ".runs/feat-auth/signal/requirements.md" \
  --regex '^### REQ-' \
  --null-if-missing
# stdout: 5 (or null if missing)

# Count NFRs
bash .claude/scripts/demoswarm.sh count pattern \
  --file ".runs/feat-auth/signal/requirements.md" \
  --regex '^### NFR-' \
  --null-if-missing

# Count BDD scenarios
bash .claude/scripts/demoswarm.sh count bdd \
  --dir ".runs/feat-auth/signal/features" \
  --null-if-missing

# Count open questions (QID marker)
bash .claude/scripts/demoswarm.sh count pattern \
  --file ".runs/feat-auth/signal/open_questions.md" \
  --regex '^- QID: OQ-SIG-[0-9]{3}' \
  --null-if-missing

# Count risks by severity
bash .claude/scripts/demoswarm.sh count pattern \
  --file ".runs/feat-auth/signal/early_risks.md" \
  --regex '^- RSK-[0-9]+ \[CRITICAL\]' \
  --null-if-missing
```

### Extracting Machine Summary fields

```bash
# Get status from critic
bash .claude/scripts/demoswarm.sh ms get \
  --file ".runs/feat-auth/signal/requirements_critique.md" \
  --section "## Machine Summary" \
  --key "status" \
  --null-if-missing
# stdout: VERIFIED (or null)

# Get recommended_action
bash .claude/scripts/demoswarm.sh ms get \
  --file ".runs/feat-auth/build/code_critique.md" \
  --section "## Machine Summary" \
  --key "recommended_action" \
  --null-if-missing
```

### Reading receipt fields

```bash
# Read merge verdict from gate receipt
bash .claude/scripts/demoswarm.sh receipt get \
  --file ".runs/feat-auth/gate/gate_receipt.json" \
  --key "merge_verdict" \
  --null-if-missing
# stdout: MERGE (or null)

# Read prior flow status
bash .claude/scripts/demoswarm.sh receipt get \
  --file ".runs/feat-auth/plan/plan_receipt.json" \
  --key "status" \
  --null-if-missing
```

### Extracting YAML block fields

```bash
# Get deployment verdict
bash .claude/scripts/demoswarm.sh yaml get \
  --file ".runs/feat-auth/deploy/deployment_decision.md" \
  --key "deployment_verdict" \
  --null-if-missing
# stdout: STABLE (or null)

# Get Gate Result status from merge decision
bash .claude/scripts/demoswarm.sh yaml get \
  --file ".runs/feat-auth/gate/merge_decision.md" \
  --key "status" \
  --null-if-missing
```

### Counting items in YAML blocks

```bash
# Count blockers array length
bash .claude/scripts/demoswarm.sh yaml count-items \
  --file ".runs/feat-auth/gate/merge_decision.md" \
  --item-regex '^[[:space:]]*- check:' \
  --null-if-missing
```

### Timestamp generation

```bash
bash .claude/scripts/demoswarm.sh time now
# stdout: 2025-12-12T10:30:00Z
```

---

## Contract Rules

1. **stdout**: Always a single scalar (`null`, integer, or string)
2. **exit code**: Always `0` (errors expressed via `null` stdout)
3. **stderr**: Optional diagnostics (never required for parsing)
4. **null semantics**: Missing file → `null`, no matches → `0`
5. **template leak guard**: Values containing `|` or `<` → `null`

---

## For Agent Authors

When writing cleanup agents:

1. **Use `runs-derive`** — `bash .claude/scripts/demoswarm.sh ...`
2. **Do not embed `grep|sed|awk|jq` pipelines** — use shim commands
3. **Trust the contract** — helpers handle edge cases consistently
4. **Add blockers for nulls** — when a count is null, explain why

Example pattern:

```bash
REQ_COUNT=$(bash .claude/scripts/demoswarm.sh count pattern \
  --file ".runs/${RUN_ID}/signal/requirements.md" \
  --regex '^### REQ-' \
  --null-if-missing)

if [[ "$REQ_COUNT" == "null" ]]; then
  BLOCKERS+=("requirements.md missing or unparseable")
fi
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
