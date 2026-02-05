---
name: llm-compact-logger-analysis
description: Analyze llm-compact-logger test output and configure enhancements. Use when user shares debug-compact.json or debug-report.json files.
version: 1.0.0
---

# LLM Compact Logger Analysis

## Quick Start

When analyzing llm-compact-logger output:

1. Read `debug-compact.json` first (~18 tokens vs ~88 for full report)
2. Check for `meta.rootCauses` - patterns found across failures (confidence >0.85 is actionable)
3. Review `topFails` - most common error types
4. Examine `code` field - failing line with context
5. Look for `history.flaky` - flakiness indicators

**Use jq for queries (not grep):** See [EXAMPLES.md](EXAMPLES.md) for jq query patterns.

For detailed format reference and error patterns, see [REFERENCE.md](REFERENCE.md).

## Analyzing Test Output

### Root Cause First

If `meta.rootCauses` exists, lead with the highest confidence pattern:

```json
{
  "meta": {
    "rootCauses": [{
      "pattern": "Accessing property 'name' on undefined",
      "confidence": 0.95,
      "suggestion": "Check if object exists before accessing"
    }]
  }
}
```

Confidence >0.85 means actionable insight found.

### Error Pattern Analysis

Group failures by `topFails`:

```json
{"topFails": [{"type": "TypeError", "count": 5}]}
```

**Common fixes:**
- TypeError undefined → Add null checks
- Type mismatch → API structure changed
- Array length → Data filtering issue

### Code Context

Display failing line from `code` field:

```json
{
  "code": {
    "fail": "expect(result).toBe(5)",
    "ctx": ["const result = calculate();", "expect(result).toBe(5);"]
  }
}
```

### Flakiness Detection

Flag tests with `history.flaky.isFlaky: true`.

## Configuring Enhancements

Ask user:
1. **Need history tracking?** → Enable `persistentIndex` (requires better-sqlite3)
2. **Using coverage?** → Enable Vitest coverage with `provider: 'v8', reporter: ['json']`
3. **Have flaky tests?** → Recommend `persistentIndex` for historical analysis

**Minimal setup:** `new VitestReporter({ outputDir: './debug' })`

See [REFERENCE.md](REFERENCE.md) for complete configuration options and examples.

## Response Format

Structure your analysis as:

```
📊 Summary: X tests (X passed, X failed) - X% pass rate

🎯 Root Cause: [Pattern] (X% confidence)
Suggestion: [Fix]

❌ Key Failures:
1. [Test] (file:line)
   Fix: [Solution]

💡 Next Steps: [Actions]
```

## When to Use This Skill

Activate when:
- User shares files ending in `debug-compact.json` or `debug-report.json`
- User asks to analyze test failures
- User mentions llm-compact-logger configuration
- User asks about test flakiness

## Troubleshooting

Common issues:
- "better-sqlite3 not installed" → Install or disable `persistentIndex`
- "Coverage file not found" → Enable Vitest coverage with `reporter: ['json']`
- Missing enhancements → Requires v0.2.0+

See [REFERENCE.md](REFERENCE.md) for complete troubleshooting guide.
