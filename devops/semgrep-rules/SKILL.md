---
name: semgrep-rules
description: "Configures and runs Semgrep - pattern-based SAST across 30+ languages with the Semgrep Registry rulesets (`p/owasp-top-ten`, `p/default`, `auto`) plus custom YAML rules; integrates `semgrep ci` for PR-blocking gates with `--baseline-commit` diff-aware scanning, per-finding inline `nosemgrep` suppressions, `--exclude` / `--include` path filters, output formats (`--json` / `--sarif` / `--gitlab-sast` / `--junit-xml`), and severity filter (INFO/WARNING/ERROR). Use when the user runs Semgrep, asks about pattern rules, or needs a low-friction SAST gate without semantic-DB setup."
---

# semgrep-rules

## Overview

Per [semgrep.dev/docs/getting-started/quickstart][sg-quick]:

[sg-quick]: https://semgrep.dev/docs/getting-started/quickstart

Semgrep is a fast pattern-based static analyzer covering 30+
languages with a registry of community + paid rulesets and
straightforward YAML rule authoring. The `semgrep ci` subcommand
adds CI-aware features (baseline-diff, organization policies,
metrics).

Per [semgrep.dev/docs/cli-reference][sg-cli]:

[sg-cli]: https://semgrep.dev/docs/cli-reference

> "**`semgrep scan`:** Local scans without account requirement;
> doesn't return failing codes by default.
>
> **`semgrep ci`:** Pipeline execution with organization policies,
> diff-aware scanning, returns failing codes on findings."

## When to use

- The repo has a `.semgrep.yml` / `.semgrep/` directory or wants
  zero-config registry rulesets.
- The user needs PR-time SAST without standing up SonarQube or
  CodeQL infrastructure.
- A team prefers pattern-DSL rule authoring over semantic-database
  query languages.

## Step 1 - Install

Per [sg-quick][sg-quick]:

```bash
# macOS
brew install semgrep

# Linux/macOS
pipx install semgrep
# or
uv tool install semgrep

# Windows (PowerShell)
pipx install semgrep

# Docker (CI-friendly)
docker pull semgrep/semgrep
```

## Step 2 - First scan

```bash
semgrep scan --config auto
```

Per [sg-cli][sg-cli], `--config auto` "Auto-fetch rules from
registry based on project." Specific rulesets:

```bash
semgrep scan --config p/owasp-top-ten     # OWASP Top 10
semgrep scan --config p/default            # broad community ruleset
semgrep scan --config p/python p/javascript   # multiple
```

## Step 3 - Custom rule authoring

A minimal Semgrep rule in `.semgrep.yml`:

```yaml
rules:
  - id: hardcoded-jwt-secret
    pattern: jwt.sign($PAYLOAD, "...")
    message: Hardcoded JWT secret detected
    languages: [javascript, typescript]
    severity: ERROR
    metadata:
      cwe: "CWE-798: Use of Hard-coded Credentials"
```

Pattern operators: `pattern`, `pattern-either`, `pattern-not`,
`metavariable-pattern`, `pattern-inside`. Validate rule syntax:

```bash
semgrep validate --config .semgrep.yml
```

(Per [sg-cli][sg-cli] subcommand list.)

## Step 4 - CI integration with baseline diff

Per [sg-cli][sg-cli]: "`--baseline-commit=VAL` - Show only findings
not in specified commit". Diff-aware mode fails only NEW findings on
the PR; pre-existing findings are tracked but don't block - critical
for legacy adoption.

```yaml
jobs:
  semgrep:
    runs-on: ubuntu-latest
    container:
      image: semgrep/semgrep
    steps:
      - uses: actions/checkout@v5
      - run: semgrep ci --baseline-ref=main --sarif --output=semgrep.sarif
      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with: { sarif_file: semgrep.sarif }
```

## Step 5 - False-positive triage (MANDATORY)

Suppression mechanisms in priority order:

| Mechanism | Example | When to use |
|---|---|---|
| Per-line `nosemgrep` comment | `# nosemgrep: hardcoded-password` | Justified single-line exception |
| `nosemgrep` block | `# nosemgrep: rule-id` above a code block | Multi-line exception |
| `paths.exclude` in config | `exclude: ["**/*_pb.go"]` | Generated files / vendored code |
| Baseline ref | `--baseline-commit=main` (Step 4) | Legacy debt; ratchet |
| Organization-level rule disable | Semgrep AppSec Platform UI | Team-wide policy |

**Justification template (mandatory in code):**

```python
# nosemgrep: hardcoded-password
# Reason: Test fixture; password never reaches production runtime
# Reviewer: alice@example.com (2026-05-15)
# Expires: 2026-12-15
TEST_PASSWORD = "test-only-password-do-not-deploy"
```

Per [sg-cli][sg-cli] severity filter for triage workflow:

```bash
semgrep scan --severity ERROR --json   # only critical findings
```

Cadence: every quarter, audit `nosemgrep` suppressions for
staleness. Expired ones removed; persistent ones reviewed for
escalation.

## Step 6 - CLI reference (formats, flags, exit codes)

Gate on exit `0` = clean, `1` = findings, `2` = fatal error. The full
output-format flags, performance-tuning flags, and complete exit-code
table are in [references/cli-reference.md](references/cli-reference.md).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| `--config=auto` everywhere | Rulesets drift; no ownership | Pin specific rulesets (Step 2) |
| `nosemgrep` without justification | Becomes invisible debt | Required justification template (Step 5) |
| No baseline ref | Every legacy finding blocks; team disables | `--baseline-commit=main` (Step 4) |
| `semgrep scan` in CI | Doesn't return failing exit code by default | Use `semgrep ci` (Step 1 quote) |
| Mix `--severity ERROR` with `--baseline-commit` poorly | Can mask real new findings | Severity filter at output stage, not scan stage |

## Limitations

- Pattern matching can miss cross-file taint flows; for those,
  pair with `codeql-queries`.
- Registry rulesets evolve; pin specific versions for production.
- Semgrep AppSec Platform features (org policies, supply-chain
  scanning) are paid; the OSS engine covers the patterns above.

## References

- [sg-quick][sg-quick] - install, quickstart
- [sg-cli][sg-cli] - full CLI reference, exit codes, all flags
- semgrep.dev/docs/writing-rules/rule-syntax - custom rules
- semgrep.dev/docs/semgrep-ci/overview - CI integration
- `sonarqube-rules`,
  `codeql-queries`,
  `language-native-sast` - sister scanners
