---
name: semgrep
description: "Write and run Semgrep rules, triage findings, and tune CI scanning to reduce irrelevant alerts."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["semgrep", "sast", "static-analysis", "security", "ci", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Semgrep Static Analysis AI Skill Guide

## Overview & Engine Architecture

Semgrep is a lightweight SAST engine that matches code patterns (and taint rules) across many languages. Teams run packs (OWASP, language defaults) plus custom rules in CI. Agents write precise patterns, scope paths, and treat findings as work items with owners - suppressing only with documented justification.

```
Repo checkout
   -> semgrep ci / semgrep scan
       -> Rule packs + custom rules (.yaml)
           -> Findings (SARIF/JSON)
               -> Gate / triage / suppressions
```

## When to use this skill

- Adding SAST to PR checks
- Authoring custom rules for org-specific footguns
- Reducing false positives with pattern-not and path excludes
- Mapping findings to fix PRs

## Operational directives

1. Start with curated packs; add custom rules for frameworks you actually use.
2. Fail CI on high-confidence rules first; park noisy experimental rules as non-blocking.
3. Prefer taint mode for injection-class bugs over brittle syntactic-only patterns when available.
4. Never blanket-ignore whole languages or `**` without review.
5. Record ignore reasons next to `nosemgrep` comments or central allowlists.

## Scan commands

```bash
semgrep --config=auto .
semgrep --config=p/owasp-top-ten --severity=json -o semgrep.json
semgrep --config=./rules/custom.yaml src/
```

## Custom rule sketch

```yaml
rules:
  - id: no-raw-sql-format
    languages: [python]
    message: "Avoid formatting SQL with f-strings; use parameterized queries"
    severity: ERROR
    pattern: |
      $CURSOR.execute(f"...{$X}...")
```

## Triage hygiene

| Approach | When to use |
| --- | --- |
| Fix code | True positive, reachable |
| Tighten rule (`pattern-not`, metavariable-regex) | Recurring false positives |
| Path exclude | Generated code / vendored trees |
| Inline `nosemgrep` | Rare exceptions with ticket link |

## Best practices

- Keep custom rules in-repo versioned next to the code they protect.
- Diff-aware CI (changed files) for speed; full scans nightly.
- Align severities with `@owasp-asvs` priorities your team adopted.
- Re-tune after major framework upgrades (new APIs create new sinks/sources).

## Limitations

- Pattern SAST misses architectural issues and multi-service authz bugs.
- Proprietary or heavily generated code may need different engines (`@codeql`).
- Rule syntax and pack names evolve - check Semgrep docs for your CLI version.

## Related skills

- `@codeql` - deeper semantic analysis in GitHub Advanced Security
- `@owasp-asvs` - requirements mapping for findings
- `@snyk` - SCA/container companion scanning
