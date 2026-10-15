---
name: env-doc
description: Document all environment variables in a project with purpose, type, default, sensitivity, and owning service
version: 0.1.0
execution-mode: advisory
argument-hint: "[PATH] [--format table|dotenv-template|markdown]"
category: backend-infra
status: candidate
---
# Environment Variable Documenter

Scan a codebase and produce a comprehensive inventory of every environment variable -- what it does, its type, default value, whether it contains secrets, and which service reads it. Generates output in table, dotenv template, or markdown format.

## When to Use
- Onboarding a new developer who needs to know what env vars to set
- Before deploying to a new environment and need a complete .env template
- Auditing which env vars hold secrets vs non-sensitive config
- Documenting the project for compliance or handoff purposes

## Execution
1. Parse `$ARGUMENTS` for optional `PATH` (default: repo root) and `--format` (default: `table`)
2. Scan all Python files for `os.environ`, `os.getenv`, `os.environ.get` patterns
3. Scan shell scripts for `$VAR` and `${VAR}` references
4. Scan .env files, .env.example, docker-compose.yml, and CI workflows for variable definitions
5. For each variable, determine: name, purpose (from context/comments), type (string/int/bool/path), default value, sensitivity level (PUBLIC/INTERNAL/SECRET), owning service or module
6. Flag variables that appear in code but have no .env.example entry (undocumented)
7. Flag variables in .env.example that are never referenced in code (stale)
8. Output in requested format

## Output Format
```
Env Doc | {format}
────────────────────────────────
Variables found: {N} | Undocumented: {N} | Stale: {N}

| Variable | Purpose | Type | Default | Sensitivity | Owner |
|----------|---------|------|---------|-------------|-------|
| ENABLE_IDP | IDP feature gate | bool | false | PUBLIC | delegation_token.py |

Undocumented (in code but not .env.example): {list}
Stale (in .env.example but unused): {list}
Action: {next steps or "No further action needed"}
```

## Skill Chains
| After this skill... | Consider... |
|--------------------|-------------|
| Documentation generated | `[env-audit]` to verify no secrets are leaked |
| Onboarding a developer | `[onboard-dev]` to include the env doc in setup guide |
| Preparing for deploy | `[deploy-checklist]` to verify all vars are set in target env |
