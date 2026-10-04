---
name: codeql
description: "Configure GitHub CodeQL analysis, run or write queries, interpret SARIF findings, and verify fixes for reported vulnerabilities."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["codeql", "sast", "github", "security", "sarif", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# CodeQL Analysis AI Skill Guide

## Overview & Engine Architecture

CodeQL models source code as a queryable database. GitHub Actions (or CLI) builds a CodeQL DB per language, runs query suites, and uploads SARIF to code scanning. Agents enable default suites first, fix real issues with root-cause patches, and add path/query exclusions only with documented rationale - not to hide debt permanently.

```
Source checkout
   -> CodeQL init + autobuild/build
       -> CodeQL analyze (query suite)
           -> SARIF upload -> GitHub code scanning alerts
```

## When to use this skill

- Turning on GitHub code scanning for a repo
- Triaging CodeQL alerts on PRs
- Adding custom queries for org-specific bugs
- Comparing deep semantic findings vs pattern SAST (`@semgrep`)

## Operational directives

1. Start with `security-extended` or default suites; custom queries later.
2. Ensure the build step compiles/interprets the code CodeQL needs (compiled languages especially).
3. Fix alerts at the source (validation, authz, safe APIs); avoid "ack" without mitigation.
4. Use `paths-ignore` sparingly for generated/vendor trees only.
5. Treat PR scanning failures as merge blockers for high severity once baselines are clean.

## Actions sketch

```yaml
name: codeql
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }
  schedule: [{ cron: "0 6 * * 1" }]
jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: javascript, python
      - uses: github/codeql-action/autobuild@v3
      - uses: github/codeql-action/analyze@v3
```

## Triage guidance

| Alert class | Typical fix direction |
| --- | --- |
| SQL/NoSQL injection | Parameterize; remove string concat |
| XSS | Encode/sanitize by context |
| Path traversal | Canonicalize + allowlist roots |
| Insecure randomness (security-sensitive) | Use crypto RNG APIs |

## Best practices

- Run weekly scheduled full analysis in addition to PR diffs.
- Keep a baseline: clear or dismiss old alerts with reasons before enforcing gates.
- For polyglot monorepos, split jobs per language when builds conflict.
- Complement with `@semgrep` for fast custom patterns and `@snyk` for dependencies.

## Limitations

- Autobuild may fail for unusual build systems - supply explicit build commands.
- CodeQL/GitHub Advanced Security availability depends on plan/public-repo rules.
- Query packs and language support change over time - pin action major versions thoughtfully.

## Related skills

- `@semgrep` - lighter pattern SAST and custom rules
- `@owasp-asvs` - map alerts to verification requirements
- `@dependabot-config` - dependency upgrades adjacent to code scanning
