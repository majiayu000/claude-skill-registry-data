---
name: pii-detect
description: Detect and flag personally identifiable information (PII) in text, code, and configurations
argument-hint: "<input-text>"
allowed-tools: mcp__claude-flow__aidefence_has_pii mcp__claude-flow__aidefence_scan mcp__claude-flow__aidefence_analyze mcp__claude-flow__transfer_detect-pii Bash
---

# PII Detection

Detect personally identifiable information before it enters logs, commits, or responses.

## When to use

Before committing code, storing data, or sending responses that might contain PII (emails, phone numbers, SSNs, API keys, passwords).

## Steps

1. **Quick PII check** — call `mcp__claude-flow__aidefence_has_pii` with the text for a boolean result
2. **Detailed scan** — call `mcp__claude-flow__transfer_detect-pii` for categorized PII findings
3. **Full analysis** — call `mcp__claude-flow__aidefence_analyze` for context-aware PII detection
4. If PII found, flag the specific locations and suggest redaction

## PII categories detected

- Email addresses, phone numbers
- Social security numbers, tax IDs
- Credit card numbers
- API keys, tokens, passwords
- Physical addresses
- Names linked to sensitive data
