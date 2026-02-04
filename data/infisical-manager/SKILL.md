---
name: infisical-manager
description: Manages Infisical configuration. Use when user says "Infisical에 업데이트해줘", "환경변수 동기화해줘", "이 config Infisical에 저장해줘", "strategy config 업데이트", "YAML을 Infisical로", "JSON config 저장", or wants to sync environment variables to Infisical.
allowed-tools: Bash(.claude/scripts/infisical-update.sh:*), Bash(.claude/scripts/local-llm.sh:*), Bash(kubectl get:*), Read, Glob
---

# Infisical Secrets Management

Update Infisical secrets from various formats using local LLM for parsing sensitive data.

## Architecture

```
User Input (YAML/JSON/ENV)
        │
        ▼
   Local LLM (Parse & Validate)
        │
        ▼
   infisical-update.sh (safe-* commands)
        │
        ▼
   Infisical API (token never exposed)
        │
        ▼
   K8s Secret (via Operator)
        │
        ▼
   Pod (auto-reload)
```

## Safe Workflow (Recommended)

Token is **never exposed** to stdout or logs.

### Single Secret Update

```bash
# All-in-one: fetch token + update (token stays in memory only)
.claude/scripts/infisical-update.sh safe-update \
  infisical-strategy-010101-secrets deepfx \
  "/strategies/010101" "DEEPFX_STRATEGY_CONFIG" '{"foo":"bar"}'
```

### Bulk Update from File

```bash
# Parse JSON and update all keys
.claude/scripts/infisical-update.sh safe-parse \
  infisical-strategy-010101-secrets deepfx \
  json /tmp/config.json "/strategies/010101"

# Parse YAML
.claude/scripts/infisical-update.sh safe-parse \
  infisical-strategy-010101-secrets deepfx \
  yaml /tmp/config.yaml "/strategies/010101"

# Parse .env
.claude/scripts/infisical-update.sh safe-parse \
  infisical-strategy-010101-secrets deepfx \
  env /tmp/config.env "/strategies/010101"
```

### With Local LLM Parsing

For complex/sensitive config, parse with local LLM first:

```bash
# 1. Local LLM parses (data never leaves machine)
.claude/scripts/local-llm.sh qwen3-coder "Convert this YAML to JSON: <yaml>"

# 2. Save parsed output to temp file
cat > /tmp/parsed.json << 'EOF'
{"KEY1": "value1", "KEY2": "value2"}
EOF

# 3. Safe update (token never exposed)
.claude/scripts/infisical-update.sh safe-parse \
  infisical-strategy-010101-secrets deepfx \
  json /tmp/parsed.json "/strategies/010101"

# 4. Clean up
rm /tmp/parsed.json
```

## Path Convention

| Resource | Infisical Path |
|----------|----------------|
| Strategy 010101 | `/strategies/010101` |
| Strategy zrevert | `/strategies/zrevert` |
| Nightly Dream | `/workloads/nightly-dream` |
| RL Trainer | `/workloads/rl-trainer` |
| General deepfx | `/deepfx` |

## Finding the Secret Name

```bash
# List Infisical secrets in namespace
kubectl get secret -n deepfx | grep infisical
```

## Security Notes

1. **Use safe-* commands** - token never printed to stdout
2. **Use local LLM** for parsing sensitive data
3. **Delete temp files** after use
4. Token is scoped to specific workspace/path
5. Infisical Operator syncs to K8s within ~60s

## Verification

```bash
# Check K8s secret updated
kubectl get secret <secret-name> -n <namespace> -o yaml

# Restart pod if needed
kubectl rollout restart deployment/<deployment-name> -n <namespace>
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Token expired | Re-fetch (safe-* commands do this automatically) |
| 403 Forbidden | Check token scope matches path |
| Secret not syncing | Check Infisical Operator logs |
| Pod not reloading | Restart deployment |
