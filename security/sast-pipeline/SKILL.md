---
name: sast-pipeline
description: SAST — tool selection, CI integration, severity thresholds.
---

## SAST Tools by Language

| Language / Ecosystem | Recommended Tool | Notes |
|---|---|---|
| Any (polyglot) | **Semgrep** | Rule-based; custom rules; OWASP ruleset available |
| Python | **Bandit** | Focused on common Python security issues |
| Java / Kotlin | **SpotBugs + FindSecBugs** | Bytecode analysis; integrates with Maven/Gradle |
| Ruby on Rails | **Brakeman** | Rails-specific; fast; actionable output |
| JavaScript / TypeScript | **npm audit** + **ESLint security plugin** | Dependency CVEs + code patterns |
| Go | **gosec** | Go-idiomatic; checks crypto, SQL, file perms |
| PHP | **PHPCS Security Audit** | PSR-compatible; detects SQLi, XSS, CSRF patterns |
| .NET / C# | **Security Code Scan** | Roslyn analyzer; integrates with VS/Rider |
| iOS / Swift | **MobSF** | Mobile-specific; covers Swift and Obj-C |
| Android / Kotlin | **MobSF** | APK and source scanning |

**Baseline recommendation:** always run Semgrep with the OWASP ruleset as a first pass, then add the language-specific tool.

---

## CI Integration

### Trigger rules
- Run on every PR targeting `main` / `develop`
- Run on pushes to `main` and release branches
- Do NOT gate feature branches — developers need fast iteration

### Severity thresholds

| Severity | CI Behavior |
|---|---|
| CRITICAL | Block merge; require immediate fix or explicit security-team sign-off |
| HIGH | Block merge; must be resolved or triaged before merge |
| MEDIUM | Warning only; logged in PR comment; does not block |
| LOW / INFO | Informational; aggregated in weekly report |

### GitHub Actions example (Semgrep)

```yaml
name: SAST
on: [pull_request]

jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/owasp-top-ten
            p/secrets
            .semgrep/custom-rules.yml
        env:
          SEMGREP_APP_TOKEN: ${{ secrets.SEMGREP_APP_TOKEN }}
```

### GitLab CI example

```yaml
semgrep:
  image: returntocorp/semgrep
  script:
    - semgrep --config p/owasp-top-ten --config .semgrep/custom-rules.yml
      --error --severity ERROR --severity WARNING
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

---

## False Positive Management

**Never suppress a finding without written justification.**

### Semgrep inline suppression
```python
user_data = request.get_json()  # nosemgrep: direct-use-of-jinja2
```

### `.semgrepignore` file (file/path-level suppression)
```
# Auto-generated migration files — SQL is template-controlled, not user input
db/migrate/
database/migrations/

# Third-party vendored code — not our responsibility to fix
vendor/
node_modules/
```

**Rule:** every suppression must include a comment explaining:
1. Why the finding is a false positive
2. What compensating control exists (if relevant)
3. Who approved the suppression

### Triage workflow
1. Finding appears in PR
2. Developer assesses: true positive or false positive?
3. True positive → fix before merge
4. False positive → add to `.semgrepignore` with comment; request security review for HIGH/CRITICAL suppressions

---

## Custom Semgrep Rules

Store project-specific rules in `.semgrep/custom-rules.yml`.

```yaml
rules:
  - id: no-raw-sql-format
    patterns:
      - pattern: cursor.execute("..." % ...)
      - pattern: cursor.execute("..." .format(...))
    message: "Possible SQL injection via string formatting. Use parameterized queries."
    languages: [python]
    severity: ERROR
```

**When to write custom rules:**
- Project-specific dangerous patterns not covered by OWASP ruleset
- Internal SDK misuse (e.g., calling an internal auth helper incorrectly)
- Enforcing architecture constraints (e.g., no direct DB access from controller layer)

---

## Checklist

- [ ] SAST tool configured and running on every PR
- [ ] CRITICAL and HIGH findings block merge
- [ ] All suppressions have written justification
- [ ] Custom rules cover project-specific patterns
- [ ] OWASP ruleset is the baseline config
