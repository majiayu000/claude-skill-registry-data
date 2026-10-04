---
name: HTTPLint
version: 1.0.0
description: "HTTP client & server misconfiguration detector -- detects insecure connections, missing timeouts, cookie security issues, caching misconfigurations, and request handling vulnerabilities"
homepage: https://httplint.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83c\udf10",
      "primaryEnv": "HTTPLINT_LICENSE_KEY",
      "requires": {
        "bins": ["git", "bash", "python3", "jq"]
      },
      "configPaths": ["~/.openclaw/openclaw.json"],
      "install": [
        {
          "id": "lefthook",
          "kind": "brew",
          "formula": "lefthook",
          "bins": ["lefthook"],
          "label": "Install lefthook (git hooks manager)"
        }
      ],
      "os": ["darwin", "linux", "win32"]
    }
  }
user-invocable: true
disable-model-invocation: false
---

# HTTPLint -- HTTP Client & Server Misconfiguration Detector

HTTPLint scans codebases for HTTP client/server misconfigurations, insecure connections, missing timeouts, cookie security issues, caching misconfigurations, header problems, and request handling vulnerabilities. It uses regex-based pattern matching against 90 HTTP-specific patterns across 6 categories, lefthook for git hook integration, and produces markdown reports with actionable remediation guidance. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `httplint scan [file|directory]`
One-shot HTTP configuration scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 30 HTTP configuration patterns against each file (free tier limit)
4. Calculates an HTTP configuration quality score (0-100) per file and overall
5. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if score >= 70, exit code 1 if HTTP configuration quality is poor
8. Free tier limited to first 30 patterns (HC + HS categories)

**Example usage scenarios:**
- "Scan my code for HTTP issues" -> runs `httplint scan .`
- "Check this file for HTTP misconfigurations" -> runs `httplint scan src/server.ts`
- "Find insecure HTTP connections" -> runs `httplint scan src/`
- "Audit HTTP configuration quality in my project" -> runs `httplint scan .`
- "Check for cookie security issues" -> runs `httplint scan .`

### Pro Tier ($19/user/month -- requires HTTPLINT_LICENSE_KEY)

#### `httplint scan --tier pro [file|directory]`
Extended scan with 60 patterns covering HTTP client, server, cookie security, and caching headers.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro
```

**What it does:**
1. Validates Pro+ license
2. Runs 60 HTTP patterns (HC, HS, CK, CH categories)
3. Detects cookie security issues (missing Secure flag, SameSite, session fixation)
4. Identifies caching and header misconfigurations
5. Full category breakdown reporting

#### `httplint scan --format json [directory]`
Generate JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format json
```

#### `httplint scan --format html [directory]`
Generate HTML report for browser viewing.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format html
```

#### `httplint scan --category CK [directory]`
Filter scan to a specific check category (HC, HS, CK, CH, RH, ER).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --category CK
```

### Team Tier ($39/user/month -- requires HTTPLINT_LICENSE_KEY with team tier)

#### `httplint scan --tier team [directory]`
Full scan with all 90 patterns across all 6 categories including request handling and error response.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --tier team
```

**What it does:**
1. Validates Team+ license
2. Runs all 90 patterns across 6 categories
3. Includes request handling checks (input validation, content-length, redirects, smuggling)
4. Includes error and response checks (stack traces, status codes, error handling, response format)
5. Full category breakdown with per-file results

#### `httplint scan --verbose [directory]`
Verbose output showing every matched line and pattern details.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --verbose
```

#### `httplint status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

## Check Categories

HTTPLint detects 90 HTTP misconfiguration patterns across 6 categories:

| Category | Code | Patterns | Description | Severity Range |
|----------|------|----------|-------------|----------------|
| **HTTP Client** | HC | 15 | Missing timeouts, no retries, insecure connections, hardcoded URLs, missing User-Agent | medium -- critical |
| **HTTP Server** | HS | 15 | Missing CORS configuration, no rate limiting, improper status codes, missing middleware | medium -- critical |
| **Cookie & Session** | CK | 15 | Missing Secure flag, no SameSite attribute, session fixation, insecure token storage | high -- critical |
| **Caching & Headers** | CH | 15 | Missing cache control, no ETags, missing security headers, improper content type | medium -- high |
| **Request Handling** | RH | 15 | Missing input validation, content-length issues, open redirects, request smuggling | high -- critical |
| **Error & Response** | ER | 15 | Stack trace exposure, improper status codes, missing error handling, response format issues | medium -- high |

## Tier-Based Pattern Access

| Tier | Patterns | Categories |
|------|----------|------------|
| **Free** | 30 | HC, HS |
| **Pro** | 60 | HC, HS, CK, CH |
| **Team** | 90 | HC, HS, CK, CH, RH, ER |
| **Enterprise** | 90 | HC, HS, CK, CH, RH, ER + priority support |

## Scoring

HTTPLint uses a deductive scoring system starting at 100 (perfect):

| Severity | Point Deduction | Description |
|----------|-----------------|-------------|
| **Critical** | -25 per finding | Severe security issue (insecure connections, missing authentication) |
| **High** | -15 per finding | Significant quality problem (missing timeouts, no CORS) |
| **Medium** | -8 per finding | Moderate concern (missing headers, caching issues) |
| **Low** | -3 per finding | Informational / best practice suggestion |

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| **A** | 90-100 | Excellent HTTP configuration quality |
| **B** | 80-89 | Good configuration with minor issues |
| **C** | 70-79 | Acceptable but needs improvement |
| **D** | 60-69 | Poor HTTP configuration quality |
| **F** | Below 60 | Critical HTTP configuration problems |

- **Pass threshold:** 70 (Grade C or better)
- Exit code 0 = pass (score >= 70)
- Exit code 1 = fail (score < 70)

## Configuration

Users can configure HTTPLint in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "httplint": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "medium",
          "ignorePatterns": ["**/test/**", "**/fixtures/**", "**/*.test.*"],
          "ignoreChecks": [],
          "reportFormat": "text"
        }
      }
    }
  }
}
```

## Important Notes

- **Free tier** works immediately with no configuration
- **All scanning happens locally** -- no code is sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Pattern matching only -- no AST parsing, no external dependencies beyond bash
- Supports scanning all file types in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = pass (score >= 70), 1 = fail (for CI/CD integration)
- Output formats: text (default), json, html

## Error Handling

- If lefthook is not installed and user tries hooks, prompt to install it
- If license key is invalid or expired, show clear message with link to https://httplint.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If an invalid category is specified with --category, show available categories

## When to Use HTTPLint

The user might say things like:
- "Scan my code for HTTP issues"
- "Check my HTTP configuration"
- "Find insecure HTTP connections"
- "Detect missing timeouts in my HTTP clients"
- "Are there any hardcoded URLs in my code?"
- "Check for missing CORS configuration"
- "Audit my cookie security"
- "Find missing security headers"
- "Check for request smuggling vulnerabilities"
- "Scan for HTTP anti-patterns"
- "Run an HTTP configuration audit"
- "Generate an HTTP quality report"
- "Check if cookies have the Secure flag"
- "Find missing rate limiting in my API"
- "Check my code for HTTP security issues"
