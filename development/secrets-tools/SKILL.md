---
name: secrets-tools
description: "Publish gate secrets scanning. Use for: safe_to_publish, scan for secrets, redact in-place. Determines publish gate status. Scan files for secrets (locations only - NEVER prints secret content). GitHub tokens, AWS keys, private keys, bearer tokens. Use ONLY in secrets-sanitizer. Invoke via bash .claude/scripts/demoswarm.sh secrets scan|redact."
allowed-tools: Bash, Read, Write
---

# Secrets Tools Skill

Secrets scanning and redaction for publish gates. High-risk surface with strict output contract.

## Invocation

**Always invoke via the shim:**

```bash
bash .claude/scripts/demoswarm.sh secrets <command> [options]
```

**Do not set PATH or call helpers directly.** The shim handles resolution.

---

## CRITICAL: Never Print Secret Content

This skill has a strict output contract:

1. **NEVER print matched secret values** to stdout, stderr, or any file
2. **NEVER store raw secret values** in JSON or any artifact
3. **Only output**: file path, line number, secret type, redacted snippet (first/last 4 chars)
4. **Redacted format**: `<prefix>...<suffix>` (e.g., `ghp_...abcd`)

Violations of this contract are security incidents.

---

## Operating Invariants

### Repo root only

- Assume working directory is repo root.
- All paths are repo-root-relative.

### Scan scope

- Only scan the publish surface (current flow directory + staged files)
- Never scan the entire repository

### No git / no GitHub

This skill does not run `git` or `gh`. File lists are passed as arguments.

---

## Allowed Users

**Primary:**

- `secrets-sanitizer` (the publish gate agent)

**Secondary (read-only scan):**

- `repo-operator` (for hygiene checks)

**Not allowed:**

- Cleanup agents (they read receipts, not scan for secrets)
- Author agents
- Critic agents

---

## Command Reference

| Command          | Purpose                                 |
| ---------------- | --------------------------------------- |
| `secrets scan`   | Scan files for secrets (locations only) |
| `secrets redact` | Redact specific secret type in file     |

---

## Quick Examples

### Scan for secrets

```bash
# Scan a file or directory
bash .claude/scripts/demoswarm.sh secrets scan \
  --path ".runs/feat-auth/signal" \
  --output ".runs/feat-auth/signal/secrets_scan.json"
# stdout: CLEAN | SECRETS_FOUND | SCAN_PATH_MISSING | PATTERN_ERROR
# JSON findings written to --output file
```

Output JSON format:

```json
{
  "status": "SECRETS_FOUND",
  "findings": [
    {
      "file": ".runs/feat-auth/signal/github_research.md",
      "type": "github-token",
      "lines": "42,87"
    }
  ],
  "skipped_count": 0
}
```

The `skipped_count` field indicates how many files/directories were skipped due to I/O errors (permission denied, etc.).

### Scan with verbose output

```bash
# Scan with verbose mode to see skipped paths
bash .claude/scripts/demoswarm.sh secrets scan \
  --path ".runs/feat-auth/signal" \
  --output ".runs/feat-auth/signal/secrets_scan.json" \
  --verbose
# stderr: Warning: skipped /path/to/file: failed to read file: Permission denied
# stdout: CLEAN
```

When `--verbose` (or `-v`) is enabled, skipped paths and reasons are logged to stderr.

### Scan with custom patterns

```bash
# Scan using additional patterns from a config file
bash .claude/scripts/demoswarm.sh secrets scan \
  --path ".runs/feat-auth/signal" \
  --output ".runs/feat-auth/signal/secrets_scan.json" \
  --patterns-file "secret-patterns.json"
```

### Scan a single file

```bash
bash .claude/scripts/demoswarm.sh secrets scan \
  --path ".runs/feat-auth/signal/github_research.md" \
  --output ".runs/feat-auth/signal/secrets_scan.json"
# stdout: CLEAN (if no secrets found)
```

### Redact a specific type

```bash
# Redact GitHub tokens in a file
bash .claude/scripts/demoswarm.sh secrets redact \
  --file ".runs/feat-auth/signal/github_research.md" \
  --type "github-token"
# stdout: ok | FILE_NOT_FOUND | null
# File is modified in-place
```

### Redact a custom type

```bash
# Redact a custom secret type defined in patterns file
bash .claude/scripts/demoswarm.sh secrets redact \
  --file ".runs/feat-auth/signal/config.md" \
  --type "custom-api-key" \
  --patterns-file "secret-patterns.json"
```

---

## Custom Patterns File

You can extend the built-in patterns by providing a JSON or YAML configuration file.

### JSON Format

```json
{
  "patterns": [
    {
      "pattern": "xoxb-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24}",
      "type": "slack-bot-token"
    },
    {
      "pattern": "sq0atp-[0-9A-Za-z\\-_]{22}",
      "type": "square-access-token"
    }
  ]
}
```

### YAML Format

```yaml
patterns:
  - pattern: "xoxb-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24}"
    type: slack-bot-token
  - pattern: "sq0atp-[0-9A-Za-z\\-_]{22}"
    type: square-access-token
```

### Pattern Merging

When `--patterns-file` is provided:

1. Built-in patterns are applied first
2. Custom patterns from the config file are applied second
3. If a file matches multiple patterns, all matches are reported

### Regex Validation

All custom patterns are validated at load time. If any pattern has invalid regex syntax, the scan will fail with `PATTERN_ERROR` status and an error message in the output JSON.

---

## Built-in Secret Types

| Type             | Pattern                                             | Replacement                 |
| ---------------- | --------------------------------------------------- | --------------------------- |
| `github-token`   | `gh[pousr]_[A-Za-z0-9_]{36,}`                       | `[REDACTED:github-token]`   |
| `aws-access-key` | `AKIA[0-9A-Z]{16}`                                  | `[REDACTED:aws-access-key]` |
| `stripe-key`     | `sk_live_[0-9a-zA-Z]{24,}`                          | `[REDACTED:stripe-key]`     |
| `private-key`    | `-----BEGIN .*PRIVATE KEY-----`                     | `[REDACTED:private-key]`    |
| `jwt-token`      | `eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*` | `[REDACTED:jwt-token]`      |

---

## Contract Rules

1. **stdout scan**: Status string (`CLEAN` | `SECRETS_FOUND` | `SCAN_PATH_MISSING` | `PATTERN_ERROR`)
2. **stdout redact**: Status string (`ok` | `FILE_NOT_FOUND` | `null`)
3. **JSON output**: Written to `--output` file path, not stdout
4. **exit code**: `0` always (errors expressed in output, not exit code). In CI or human scripts, fail-fast via exit code is appropriate; agents should record `PATTERN_ERROR` in the JSON and hand off to the orchestrator rather than exiting abruptly.
5. **No secrets in output**: Any output containing secret values is a bug

---

## Error Handling

### Missing scan path

```bash
# stdout: SCAN_PATH_MISSING
```

```json
{
  "status": "SCAN_PATH_MISSING",
  "findings": [],
  "skipped_count": 0
}
```

### Invalid patterns file

```bash
# stdout: PATTERN_ERROR
```

```json
{
  "status": "PATTERN_ERROR",
  "error": "Invalid regex in patterns file at index 0: pattern='[invalid', type='bad-pattern'",
  "findings": [],
  "skipped_count": 0
}
```

### File not found (redact)

```bash
# stdout: FILE_NOT_FOUND
```

### Read error (redact)

```bash
# stdout: null
```

### Unknown secret type (redact)

```bash
# stdout: null
# stderr: Unknown secret type: <type>
```

---

## For Agent Authors

In `secrets-sanitizer`:

1. **Use `secrets-tools`** -- `bash .claude/scripts/demoswarm.sh secrets ...`
2. **Never grep for secrets manually** -- the patterns are standardized here
3. **Check stdout status** -- `CLEAN`, `SECRETS_FOUND`, `SCAN_PATH_MISSING`, or `PATTERN_ERROR`
4. **Read JSON from file** -- findings are in the `--output` file, not stdout
5. **Redact in-place** -- use `secrets redact` for allowlist artifacts

Example pattern:

```bash
# Scan the publish surface
SCAN_OUTPUT=".runs/${RUN_ID}/${FLOW}/secrets_scan.json"
STATUS=$(bash .claude/scripts/demoswarm.sh secrets scan \
  --path ".runs/${RUN_ID}/${FLOW}" \
  --output "$SCAN_OUTPUT")

if [[ "$STATUS" == "SECRETS_FOUND" ]]; then
  # Read findings from JSON file
  FINDINGS=$(cat "$SCAN_OUTPUT" | jq -r '.findings[] | "\(.file) \(.type)"')

  # Redact each finding type
  bash .claude/scripts/demoswarm.sh secrets redact \
    --file ".runs/${RUN_ID}/${FLOW}/github_research.md" \
    --type "github-token"
fi
```

### Using Custom Patterns

```bash
# Scan with organization-specific patterns
SCAN_OUTPUT=".runs/${RUN_ID}/${FLOW}/secrets_scan.json"
STATUS=$(bash .claude/scripts/demoswarm.sh secrets scan \
  --path ".runs/${RUN_ID}/${FLOW}" \
  --output "$SCAN_OUTPUT" \
  --patterns-file ".config/secret-patterns.yaml")

# Handle PATTERN_ERROR status
if [[ "$STATUS" == "PATTERN_ERROR" ]]; then
  ERROR=$(cat "$SCAN_OUTPUT" | jq -r '.error')
  echo "Pattern configuration error: $ERROR"
  exit 1
fi
```

---

## Installation

The Rust implementation is preferred:

```bash
cargo install --path tools/demoswarm-runs-tools --root .demoswarm
```

The shim will automatically use the installed binary.
