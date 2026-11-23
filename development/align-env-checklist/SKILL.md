---
name: align-env-checklist
description: >
  Verify that every runtime environment variable the code actually reads is documented
  in .env.example, that config validation covers the full required set, and that no real
  .env file is tracked. Trigger on "is my .env.example up to date", "are all our env
  vars documented", "did we miss a config variable", "check our environment variables
  before deploy", "why is this env var undefined in staging". Audits the documentation
  and config coverage of the whole codebase; to generate a fillable stub of the values
  missing from your own local environment, use setup-env. Delegates its secret scanning
  to audit-secrets rather than duplicating it.
---

# align-env-checklist

You are an environment configuration assistant. Your job is to verify that the project's runtime configuration requirements are completely documented, that no secrets are accidentally exposed, and that all required environment variables are accounted for after code changes.

Run this after adding new environment variables, onboarding a new developer, deploying to a new environment, or reviewing a PR that touches configuration.

---

## Step 1 — Discover configuration sources

Find all places where environment variables are declared or consumed:

```bash
# find all env access patterns
grep -rn "process\.env\." src/ --include="*.ts" --include="*.js"
grep -rn "os\.environ\|os\.getenv\|dotenv" . --include="*.py"
grep -rn "os\.Getenv\|viper\." . --include="*.go"
grep -rn "ENV\[" . --include="*.rb"

# find env documentation files
ls .env .env.* .env.example .env.sample .env.template
cat .env.example 2>/dev/null || cat .env.sample 2>/dev/null

# find config validation files
grep -rn "zod\|joi\|yup\|envalid\|t3-env\|pydantic\|BaseSettings" src/ --include="*.ts" --include="*.js" --include="*.py"
```

Build a complete list of environment variables the application reads.

---

## Step 2 — Check for secrets that must not be committed

**Delegate this to the `audit-secrets` skill.** Do not re-implement the scan here — that
skill owns the credential pattern set and, unlike a working-tree check, also scans git
history, where a secret survives after the file is deleted.

Run `audit-secrets` and use its result as a gate:

- **Secrets found** — stop. Report them and follow that skill's remediation, which
  includes rotating the credential, not merely removing it. Do not continue to Step 3.
- **Clean** — continue with the env-documentation audit below.

The env-specific concern this skill still owns is `.env` files with real values being
tracked at all, which `audit-secrets` reports but does not treat as a config problem:

```bash
git ls-files | grep -E '(^|/)\.env($|\.)' | grep -v '\.example$'
```

Any output here means a real `.env` is tracked — flag it alongside the `.gitignore`
gap in Step 4 even when it contains no recognisable credential pattern.

Rules:

- `.env.example` is safe to commit if it contains placeholder values only
- `.env`, `.env.local`, `.env.production` should be in `.gitignore`

---

## Step 3 — Diff the codebase against the documented example

Compare what the code uses against what `.env.example` documents:

Build two sets:

- **required by code**: all variables found by the grep in Step 1
- **documented in `.env.example`**: all keys present in the example file

Then identify:

- **missing from `.env.example`**: variables consumed by code but not documented
- **stale in `.env.example`**: variables documented but no longer consumed
- **undocumented defaults**: variables that have hardcoded fallbacks that may not be obvious

---

## Step 4 — Check for config schema validation

If the project uses a config validation library (Zod, `envalid`, Pydantic `BaseSettings`, `t3-env`, etc.):

- verify the schema covers all variables the code uses
- verify the schema is validated at startup, not lazily
- verify required variables do not have accidental default values of `undefined` or `""` that would silently allow misconfiguration

If there is no config validation, recommend adding it and suggest the appropriate library for the stack.

---

## Step 5 — Check environment-specific variables

Look for variables that differ between environments:

```bash
ls .env.* 2>/dev/null
cat .env.development .env.test .env.production 2>/dev/null
```

Verify:

- that environment-specific files do not contain production secrets
- that all environments have the same set of keys (values can differ, keys should not)
- that feature flags or environment-conditional behavior is clear in documentation

---

## Step 6 — Check deployment and CI environment config

```bash
cat .github/workflows/*.yml | grep -E 'env:|secrets\.'
```

Verify:

- all secrets used in CI are documented as needing to be configured
- no secret values are hardcoded in workflow files
- CI environment uses the same variable names as the local `.env.example`

---

## Step 7 — Update documentation

If there are gaps found in Steps 3–6:

- add missing variables to `.env.example` with clear placeholder values and inline comments explaining each variable's purpose
- remove stale variables from `.env.example` after confirming they are no longer used
- update the README or `docs/dev.md` if onboarding instructions reference env variables

Template for new `.env.example` entries:

```bash
# <What this variable does>
# Required: yes | no
# Example values: <example1>, <example2>
VARIABLE_NAME=
```

---

## Step 8 — Report

```text
Environment configuration audit

Secrets check
  No exposed secrets found | ISSUE: <describe finding>

Coverage
  Variables consumed by code:   <N>
  Variables in .env.example:    <N>

Gaps
  Missing from .env.example:    <list or "none">
  Stale in .env.example:        <list or "none">

Config validation
  Schema present: yes | no
  Startup validation: yes | no | unknown

CI environment
  Secrets properly referenced: yes | no | partially

Actions taken
  - <what was updated>
```

If secrets were found exposed, report only that finding and stop. Do not proceed with other steps until the exposure is resolved.
