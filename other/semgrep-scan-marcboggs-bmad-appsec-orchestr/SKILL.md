---
name: semgrep-scan
description: "Static analysis with Semgrep: detects languages in the current working directory, selects appropriate rulesets (OWASP, security-audit, language-specific), and runs semgrep scan. Prompts to install semgrep if not present. Use when source code is available and you want to find injection sinks, hardcoded secrets, insecure patterns, or taint-flow vulnerabilities via static analysis. Pairs with all hunt-* skills for white-box validation."
sources: original
---

# SEMGREP SCAN — Static Analysis for Source Code

> Use this skill when source code is available in the current directory or a specified path. It detects languages, selects the best Semgrep rulesets, runs the scan, and surfaces findings ranked by severity for further investigation.

---

## Prerequisites Check

**Before running any scan, verify Semgrep is installed:**

```bash
semgrep --version
```

**If not installed, prompt the user:**

> ⚠️ Semgrep is not installed. Install it with:
>
> ```bash
> pip install semgrep
> ```
>
> Or via Homebrew (macOS/Linux):
> ```bash
> brew install semgrep
> ```
>
> Then re-run this skill.

Do NOT proceed with scanning until `semgrep --version` succeeds.

---

## Language Detection

Before selecting rulesets, detect what's in the scan target directory. Check for these indicators:

| Signal | Language / Framework |
|---|---|
| `*.py`, `requirements.txt`, `setup.py`, `pyproject.toml` | Python |
| `*.js`, `*.ts`, `package.json` | JavaScript / TypeScript |
| `*.java`, `pom.xml`, `build.gradle` | Java |
| `*.go`, `go.mod` | Go |
| `*.rb`, `Gemfile` | Ruby |
| `*.php`, `composer.json` | PHP |
| `*.cs`, `*.csproj` | C# / .NET |
| `*.rs`, `Cargo.toml` | Rust |
| `*.swift` | Swift |
| `*.kt`, `*.kts` | Kotlin |
| `Dockerfile`, `docker-compose.yml` | Docker |
| `*.tf` | Terraform |
| `*.yaml`, `*.yml` (with k8s schemas) | Kubernetes |

---

## Ruleset Selection

Based on detected languages and engagement context, select rulesets in this priority order:

### Always include (broad coverage)
```
--config auto
```
This pulls Semgrep's recommended rules for detected languages. It is the best default.

### Security-focused rulesets (add when hunting vulnerabilities)

| Ruleset | When to use |
|---|---|
| `p/security-audit` | General security review — broad coverage |
| `p/owasp-top-ten` | Web app assessment — maps to OWASP classes |
| `p/secrets` | Hardcoded secrets, API keys, tokens |
| `p/default` | Semgrep's curated high-confidence rules |

### Language-specific security rulesets (add based on detection)

| Language | Ruleset |
|---|---|
| Python | `p/python`, `p/django`, `p/flask` |
| JavaScript/TypeScript | `p/javascript`, `p/typescript`, `p/nodejs`, `p/react`, `p/nextjs` |
| Java | `p/java`, `p/spring` |
| Go | `p/golang` |
| Ruby | `p/ruby`, `p/rails` |
| PHP | `p/php`, `p/laravel`, `p/symfony` |
| C# | `p/csharp` |
| Kotlin | `p/kotlin` |

### Infrastructure-as-code (when Dockerfile/Terraform/K8s detected)

| Type | Ruleset |
|---|---|
| Docker | `p/dockerfile` |
| Terraform | `p/terraform` |
| Kubernetes | `p/kubernetes` |

---

## Scan Execution

### Standard security scan (recommended default)

```bash
semgrep scan --config auto --config p/security-audit --config p/secrets .
```

### When hunting a specific bug class

Map the current hunt-* skill to a targeted scan:

| Active hunt skill | Additional Semgrep flags |
|---|---|
| `hunt-sqli` | `--config p/owasp-top-ten` — focus on injection rules |
| `hunt-xss` | `--config p/owasp-top-ten` — focus on output encoding |
| `hunt-rce` | `--config auto` — look for command injection, deserialization |
| `hunt-ssrf` | `--config auto` — look for URL construction from user input |
| `hunt-auth-bypass` | `--config p/security-audit` — auth/session patterns |
| `hunt-idor` | `--config p/security-audit` — authorization check patterns |
| `hunt-ssti` | `--config auto` — template rendering with user input |
| `hunt-file-upload` | `--config auto` — file operation patterns |

### Output options

```bash
# Default: human-readable terminal output
semgrep scan --config auto .

# JSON (for programmatic processing)
semgrep scan --config auto --json .

# SARIF (for CI/CD or tool integration)
semgrep scan --config auto --sarif .

# Only high/critical severity
semgrep scan --config auto --severity ERROR .

# Exclude test files
semgrep scan --config auto --exclude='*_test.*' --exclude='*test_*' --exclude='*/tests/*' --exclude='*/spec/*' .
```

---

## Interpreting Results

### Severity mapping to hunt priority

| Semgrep severity | Hunt priority | Action |
|---|---|---|
| `ERROR` | **High** — investigate immediately | Likely exploitable; trace the data flow manually, build PoC |
| `WARNING` | **Medium** — worth investigating | May be exploitable with specific conditions; check reachability |
| `INFO` | **Low** — note for later | Code smell or defense-in-depth issue; chain potential only |

### What to do with findings

1. **Read the rule message** — Semgrep rules explain the vulnerability pattern and often link to documentation.
2. **Trace the data flow** — Confirm user-controlled input actually reaches the flagged sink. False positives often occur when input is sanitized between source and sink.
3. **Cross-reference with hunt-* skills** — A Semgrep finding of SQL injection → load `hunt-sqli` for exploitation methodology. SSTI finding → load `hunt-ssti` for payload selection.
4. **Build dynamic PoC** — Static analysis confirms the pattern exists; dynamic testing confirms it's exploitable. Use Burp/curl to hit the endpoint with a crafted payload.
5. **Check for duplicates** — Multiple Semgrep rules may flag the same underlying issue. Deduplicate before reporting.

### Common false positive patterns

- Input is sanitized/escaped between source and sink (parameterized queries, template auto-escaping)
- Flagged code is in test files or dead code paths
- Framework-level middleware handles the concern globally (CSRF middleware, auth decorators)
- The "secret" is a placeholder/example value in documentation

---

## Integration with Engagement Workflow

### Phase 2 (Recon) — Run broad scan to map attack surface
```bash
semgrep scan --config auto --config p/secrets --severity ERROR .
```
Feed ERROR-level findings into the attack surface ranking.

### Phase 3 (Hunt) — Run targeted scans per hypothesis
```bash
# Hunting SQLi? Find all raw query construction
semgrep scan --config auto --include='*.py' --include='*.js' .
```
Use findings as starting points for dynamic testing.

### Phase 4 (Validate) — Confirm static findings are exploitable
Static finding alone ≠ submittable bug. Must prove with real HTTP request (7-Question Gate Q1).

---

## Quick Reference Commands

```bash
# Full security scan of current directory
semgrep scan --config auto --config p/security-audit .

# Secrets only (fast, high-signal)
semgrep scan --config p/secrets .

# High severity only
semgrep scan --config auto --severity ERROR .

# Specific language focus
semgrep scan --config p/python --config p/flask .

# Scan specific subdirectory
semgrep scan --config auto src/

# List available rules for a config
semgrep --config auto --dry-run .
```
