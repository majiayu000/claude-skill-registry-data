---
name: local-sensitive
description: Routes to local LLM for sensitive operations. Use when user says "로컬에서 처리해줘", "외부로 보내지 마", "민감한 데이터야", "보안 감사해줘", "credential 분석", "시크릿 확인", or handles sensitive data that should not leave the machine.
allowed-tools: Bash(.claude/scripts/local-llm.sh:*), Bash(.claude/scripts/infisical-update.sh:*), Bash(kubectl get:*), Read, Grep, Glob
---

# Local LLM for Sensitive Operations

Route security-sensitive tasks to local LLM to prevent data exfiltration.

## When to Use

- Analyzing secrets or credentials
- Security audit of sensitive code
- Private code review
- Compliance checking with sensitive data
- Any task where data should not leave the machine

## Available Models

| Model | Endpoint | Best For |
|-------|----------|----------|
| `qwen3-coder` | localhost:8003 | Code analysis, generation |
| `gpt-oss` | localhost:8004 | General tasks, tool use |

## How to Use

```bash
.claude/scripts/local-llm.sh qwen3-coder "Review this code for secrets: <code>"
.claude/scripts/local-llm.sh gpt-oss "Analyze security of this config"
```

## Security Guidelines

1. **Never** send sensitive data to external APIs
2. Use this skill when file paths contain: `secret`, `credential`, `.env`, `key`
3. Prefer `qwen3-coder` for code-related tasks
4. Prefer `gpt-oss` for general analysis

## Example Workflow

1. User asks: "Check if there are any hardcoded secrets in this file"
2. Read the file locally
3. Send to local LLM for analysis
4. Report findings without exposing actual secret values

## Infisical Secret Updates

For updating Infisical secrets with sensitive config data (token never exposed):

```bash
# 1. Parse sensitive YAML/JSON with local LLM
.claude/scripts/local-llm.sh qwen3-coder "Parse this config and output JSON: <config>"

# 2. Save to temp file
cat > /tmp/parsed.json << 'EOF'
{"KEY": "value"}
EOF

# 3. Safe update (token fetched internally, never printed)
.claude/scripts/infisical-update.sh safe-parse \
  infisical-app-secrets namespace \
  json /tmp/parsed.json "/path"

# 4. Clean up
rm /tmp/parsed.json
```

See `infisical-manager` skill for detailed workflow.
