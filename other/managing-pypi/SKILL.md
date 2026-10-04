---
name: managing-pypi
description: |
  Use when working with Pypi — pyPI package registry management. Covers package
  publishing, version management, distribution builds, dependency resolution,
  index configuration, and package metadata. Use when managing Python packages
  on PyPI, configuring private indexes, building distributions, or analyzing
  package health.
connection_type: pypi
preload: false
---

# PyPI Package Registry Management Skill

Manage and analyze Python packages, PyPI publishing, and distribution builds.

## MANDATORY: Discovery-First Pattern

**Always check current package configuration and index settings before publishing.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Package Configuration ==="
cat pyproject.toml 2>/dev/null | head -25
cat setup.py 2>/dev/null | head -20
cat setup.cfg 2>/dev/null | head -20

echo ""
echo "=== pip Configuration ==="
pip config list 2>/dev/null | head -10

echo ""
echo "=== Index Settings ==="
cat pip.conf 2>/dev/null || cat ~/.pip/pip.conf 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Installed Packages ==="
pip list --format=json 2>/dev/null | jq 'length' 2>/dev/null | xargs -I{} echo "Total installed: {}"

echo ""
echo "=== Outdated Packages ==="
pip list --outdated --format=json 2>/dev/null | jq '[.[:10][] | {
  name: .name,
  current: .version,
  latest: .latest_version,
  type: .latest_filetype
}]' 2>/dev/null

echo ""
echo "=== Package Info ==="
PACKAGE=$(cat pyproject.toml 2>/dev/null | grep '^name' | head -1 | sed 's/.*= *"//;s/"//')
curl -s "https://pypi.org/pypi/${PACKAGE}/json" 2>/dev/null | jq '{
  name: .info.name,
  version: .info.version,
  downloads: .info.downloads,
  requires_python: .info.requires_python
}' 2>/dev/null
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Summarize package metadata concisely
- List outdated dependencies with version gaps
- Never expose PyPI tokens in output

## Common Operations

### Build and Check Distribution

```bash
#!/bin/bash
echo "=== Build Distribution ==="
python -m build --sdist --wheel 2>&1 | tail -10

echo ""
echo "=== Check Distribution ==="
twine check dist/* 2>/dev/null | head -10
```

### Package Lookup

```bash
#!/bin/bash
PACKAGE="${1:?Package name required}"
echo "=== PyPI Package: $PACKAGE ==="
curl -s "https://pypi.org/pypi/${PACKAGE}/json" | jq '{
  name: .info.name,
  version: .info.version,
  summary: .info.summary,
  license: .info.license,
  requires_python: .info.requires_python,
  releases: (.releases | keys | length)
}' 2>/dev/null
```

## Safety Rules

- **Never expose PyPI API tokens** in configuration files or logs
- **Use `twine check`** before uploading to verify package metadata
- **Test on TestPyPI first** before publishing to production PyPI
- **Pin dependencies** in requirements.txt for reproducible builds

## Output Format

Present results as a structured report:
```
Managing Pypi Report
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

