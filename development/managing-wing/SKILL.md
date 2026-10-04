---
name: managing-wing
description: |
  Use when working with Wing — wing cloud-oriented programming language
  management. Covers compilation, testing, simulation, deployment to cloud
  targets, resource inspection, and console usage. Use when developing Wing
  applications, running local simulations, deploying to AWS/Azure/GCP, or
  debugging preflight and inflight code.
connection_type: wing
preload: false
---

# Wing Management Skill

Manage Wing applications, simulate locally, compile to cloud targets, and deploy infrastructure.

## MANDATORY: Discovery-First Pattern

**Always inspect Wing project structure and compile before deploying.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Wing Version ==="
wing --version 2>/dev/null

echo ""
echo "=== Project Structure ==="
ls *.w 2>/dev/null | head -10
cat package.json 2>/dev/null | jq '{name, wingCompiler: .wing}' 2>/dev/null

echo ""
echo "=== Main Entry ==="
if [ -f main.w ]; then
  head -30 main.w
fi

echo ""
echo "=== Wing Libraries ==="
cat package.json 2>/dev/null | jq '.dependencies // {}' | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
TARGET="${1:-sim}"

echo "=== Compile (target=$TARGET) ==="
wing compile --target "$TARGET" 2>&1 | tail -15

echo ""
echo "=== Test Results ==="
wing test 2>&1 | tail -20

echo ""
echo "=== Generated Resources ==="
if [ -d "target/$TARGET" ]; then
  find "target/$TARGET" -name "*.tf.json" -exec jq '.resource | keys' {} \; 2>/dev/null | head -15 || \
  ls "target/$TARGET/" | head -15
fi

echo ""
echo "=== Simulation ==="
if [ "$TARGET" = "sim" ]; then
  echo "Run 'wing it' to start the Wing Console simulator"
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show compiled resource summaries, not full generated templates
- Summarize test results with pass/fail counts
- Use simulation target for local validation

## Safety Rules
- **NEVER deploy without compiling and testing first**
- **Use `wing test`** to validate before deployment
- **Start with `--target sim`** for local testing
- **Review generated Terraform** before applying to cloud targets
- **Check cloud target permissions** before deployment

## Output Format

Present results as a structured report:
```
Managing Wing Report
════════════════════
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

