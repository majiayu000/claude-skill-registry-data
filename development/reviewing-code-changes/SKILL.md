---
name: reviewing-code-changes
description: Performs comprehensive reviews of git diffs, commits, branches, and pull requests. Use when the user asks to review code, a commit hash, a branch, or a PR, especially for security, best practices, performance issues, or dependency vulnerabilities.
allowed-tools: Read, Glob, Grep, Bash
---

# Code Review Skill

Follow this process for comprehensive code reviews.

## Step 1: Scope Selection

Ask the user what to review:

```
What would you like me to review?
1. Staged changes
2. Unstaged changes (working directory)
3. All uncommitted (staged + unstaged)
4. Specific commit (enter hash)
5. Branch as PR (compare to base branch)
6. Custom diff range
```

Wait for user selection before proceeding.

## Step 2: Gather Changes

Based on selection, run appropriate git command:
- **Staged**: `git diff --cached`
- **Unstaged**: `git diff`
- **All uncommitted**: `git diff HEAD`
- **Commit**: `git show <hash>`
- **Branch as PR**: `git diff <base>...<branch>` (ask for base branch if needed)
- **Custom**: `git diff <range>` (ask for range)

Also run `git diff --cached --name-only` or equivalent to get list of changed files.

## Step 3: Auto-Detect Tech Stack

Check for presence of:
- `package.json` / `package-lock.json` / `yarn.lock` → Node.js/JavaScript
- `requirements.txt` / `Pipfile` / `pyproject.toml` → Python
- `go.mod` → Go
- `Cargo.toml` → Rust
- `Gemfile` → Ruby
- `Dockerfile` / `docker-compose.yml` → Docker
- `*.tf` / `*.tfvars` → Terraform
- `*.yaml` / `*.yml` in k8s patterns → Kubernetes
- `ansible/` / `playbook.yml` → Ansible
- `.github/workflows/` → GitHub Actions

Note detected stack for context-aware analysis.

## Step 4: Run Available Scanners

Execute scanners if tools exist (skip silently if not installed):

| Stack | Scanner Commands |
|-------|------------------|
| Node.js | `npm audit --json`, `yarn audit --json` |
| Python | `pip-audit`, `safety check` |
| Docker | `trivy image`, `trivy fs .`, `hadolint Dockerfile` |
| Terraform | `tfsec .`, `checkov -d .` |
| General | `gitleaks detect --source .`, `trufflehog filesystem .` |

Summarize scanner findings (if any) in the output.

## Step 5: Claude Analysis

Analyze the diff for ALL categories below. Be pragmatic—flag likely issues, skip obvious false positives.

**Assume code will be published to a public repository unless stated otherwise.**

### 5.1 Errors & Deprecations
- Syntax errors, typos in code
- Deprecated APIs, functions, or patterns
- Breaking changes in dependencies
- Incompatible version usage

### 5.2 Best Practices (Stack-Specific)
- Code style and conventions for detected stack
- Idiomatic patterns
- Proper error propagation
- Resource cleanup (file handles, connections)
- Async/await correctness
- Type safety issues

### 5.3 Security Analysis
- **Secrets & Credentials**:
  - Hardcoded API keys, tokens, passwords
  - Connection strings with credentials
  - Private keys, certificates
  - `.env` files or secrets in code

- **Container Security**:
  - Running as root (`USER` directive missing)
  - Privileged mode
  - Exposed sensitive mounts
  - Unverified base images
  - Missing health checks

- **Sensitive Data Exposure**:
  - PII in logs or comments
  - Debug endpoints enabled
  - Verbose error messages exposing internals
  - Sensitive data in URLs/query params

- **Input Handling** (where obvious):
  - Command injection vectors
  - Path traversal risks
  - SQL injection (obvious patterns)
  - XSS in templates

### 5.4 Dependency Vulnerabilities
- Known vulnerable package versions
- Outdated dependencies with security patches
- Unpinned versions allowing vulnerable upgrades
- Suspicious or typosquatted package names

### 5.5 Performance Anti-Patterns
- N+1 query patterns
- Synchronous operations in async contexts
- Unbounded loops or recursion
- Memory leaks (unclosed resources, growing caches)
- Missing pagination on large datasets
- Blocking I/O in hot paths

### 5.6 Infrastructure Drift Risks
- Hardcoded values that should be variables
- Environment-specific configs in shared code
- Missing or inconsistent resource tags
- State management concerns (Terraform)
- Configuration that diverges from IaC patterns

## Step 6: Output Format

Present findings grouped by severity, with file and line references:

```
## Scanner Results
[Summary of any automated scanner findings, or "No issues detected" / "Scanners not available"]

## Code Review Findings

### CRITICAL
- `path/to/file.py:42` - Hardcoded AWS secret key detected
- `docker-compose.yml:15` - Database password in plain text

### HIGH
- `Dockerfile:1` - Container runs as root (no USER directive)
- `src/db.js:88` - SQL query built with string concatenation

### MEDIUM
- `utils.js:23` - Deprecated `Buffer()` constructor, use `Buffer.from()`
- `main.tf:45` - AWS provider version unpinned

### LOW
- `config.py:12` - Consider using environment variable for timeout value
- `k8s/deployment.yaml:8` - Missing resource limits

## Summary
- Critical: X
- High: X
- Medium: X
- Low: X

[Brief recommendation on whether changes are safe to merge]

## Review Score: X/20
[Brief justification based on code quality, security, and merge readiness]
```

## Guidelines

- **Be pragmatic**: Don't flag theoretical issues. Focus on likely problems.
- **Context matters**: Consider the file's purpose before flagging.
- **Actionable feedback**: Every finding should have a clear fix.
- **No false praise**: Skip "looks good" comments. Only report issues.
- **Public repo assumption**: Treat all secrets/sensitive data as critical.
