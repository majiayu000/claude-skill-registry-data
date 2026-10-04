---
name: managing-sst
description: |
  Use when working with Sst — sST (Serverless Stack) application management.
  Covers stack deployment, live Lambda debugging, console access, resource
  binding, secret management, and multi-stage environments. Use when building
  full-stack serverless apps with SST, debugging Lambda functions live, managing
  secrets, or inspecting deployed infrastructure.
connection_type: sst
preload: false
---

# SST Management Skill

Manage SST applications, deploy stacks, debug live Lambdas, and inspect bound resources.

## MANDATORY: Discovery-First Pattern

**Always inspect SST project config and deployment status before operations.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== SST Version ==="
npx sst version 2>/dev/null || sst version 2>/dev/null

echo ""
echo "=== SST Config ==="
if [ -f sst.config.ts ]; then
  head -30 sst.config.ts
elif [ -f sst.config.js ]; then
  head -30 sst.config.js
fi

echo ""
echo "=== Stacks ==="
ls stacks/ 2>/dev/null || ls infra/ 2>/dev/null || echo "Check sst.config for stack definitions"

echo ""
echo "=== Secrets ==="
npx sst secrets list 2>/dev/null | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
STAGE="${1:-dev}"

echo "=== Stack Status (stage=$STAGE) ==="
npx sst diff --stage "$STAGE" 2>&1 | tail -25

echo ""
echo "=== Bound Resources ==="
npx sst bind -- printenv 2>/dev/null | grep SST_ | head -15

echo ""
echo "=== Deployed Outputs ==="
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --query "StackSummaries[?contains(StackName, '-${STAGE}-')].{Name:StackName,Status:StackStatus,Updated:LastUpdatedTime}" --output table 2>/dev/null | head -15

echo ""
echo "=== Functions ==="
aws lambda list-functions --query "Functions[?contains(FunctionName, '-${STAGE}-')].{Name:FunctionName,Runtime:Runtime,Memory:MemorySize}" --output table 2>/dev/null | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show bound resource names and outputs, not full stack details
- Summarize function configurations concisely
- Redact secret values in output

## Safety Rules
- **NEVER run `sst deploy` to production without explicit stage confirmation**
- **Use `sst diff`** before deploying to review changes
- **Never expose secrets** -- use `sst secrets` for secret management
- **Use `sst dev`** for local development with live debugging
- **Review IAM changes** in diff output before deploying

## Output Format

Present results as a structured report:
```
Managing Sst Report
═══════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

