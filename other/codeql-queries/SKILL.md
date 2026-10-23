---
name: codeql-queries
description: "Configures and runs GitHub CodeQL - semantic-database SAST with queries written in the CodeQL declarative query language; supports `codeql database create` (per-language) + `codeql database analyze` with --format=sarif; ships query packs (`codeql/javascript-queries`, `codeql/python-queries`, `codeql/java-queries`, `codeql/go-queries`, etc.); integrates with GitHub Code Scanning via SARIF upload; suppression via inline comment + sarif-filter + Security-tab dismissal. Use when the team uses GitHub-hosted repos and needs deep semantic SAST beyond pattern matching (cross-file taint flows, dataflow analysis)."
---

# codeql-queries

## Overview

Per [docs.github.com/code-security/codeql-cli][cql-docs]:

[cql-docs]: https://docs.github.com/code-security/codeql-cli/getting-started-with-the-codeql-cli/

CodeQL is GitHub's semantic-analysis SAST: build a **database** of the
codebase (control flow, data flow, type info), run `.ql` **queries**
against it, emit **SARIF** for GitHub Code Scanning. This
database-then-query model catches cross-file taint flows (user input
reaching a SQL sink unsanitized) that pattern matchers cannot express.

## When to use

- The team uses GitHub-hosted repos (Code Scanning is GitHub-native).
- The codebase has cross-file taint flows that pattern-matchers
  miss (e.g., user input → service A → service B → SQL).
- A security audit requires CodeQL coverage (some compliance
  regimes prefer it).
- The team writes custom queries for org-specific patterns.

For multi-platform CI without GitHub, use `semgrep-rules`
or `sonarqube-rules`.

## Step 1 - Install

CodeQL CLI download from
[github.com/github/codeql-cli-binaries/releases](https://github.com/github/codeql-cli-binaries/releases).
Per [cql-docs][cql-docs] the CLI is bundled separately from the
queries - install both:

```bash
# Download CodeQL CLI (per platform)
curl -L https://github.com/github/codeql-cli-binaries/releases/latest/download/codeql-linux64.zip -o codeql.zip
unzip codeql.zip
export PATH="$PATH:$PWD/codeql"

# Verify
codeql --version
```

Query packs (the `.ql` files) are pulled per-scan via
`--download` flag or pre-installed via `codeql pack download`.

## Step 2 - Create a database

```bash
# For interpreted languages (JS, Python, Ruby): no build needed
codeql database create my-db --language=javascript --source-root=.

# For compiled languages (Java, C#, Go): wrap the build
codeql database create my-db --language=java --command="./gradlew build" --source-root=.

codeql database create my-db --language=cpp --command="make all"
```

The `--language` flag accepts: `cpp` / `csharp` / `go` / `java` /
`javascript` / `python` / `ruby` / `swift` / `kotlin` (verify
support against [cql-docs][cql-docs] for the current CodeQL release).

For JS/TS + Python, the `--build-mode none` extraction works
without a build step. For Java/C#/C++, you MUST wrap the project's
build via `--command` so CodeQL can observe compilation.

## Step 3 - Analyze with query packs

```bash
codeql database analyze my-db \
  --format=sarif-latest \
  --output=results.sarif \
  codeql/javascript-queries
```

The full per-language pack list, the query suites (`code-scanning`,
`security-and-quality`, `security-extended`), a custom `.ql` query
example, and the GitHub Actions CI integration are in
[references/codeql-reference.md](references/codeql-reference.md).

## Step 4 - False-positive triage (MANDATORY)

Three layers:

| Mechanism | Example | When to use |
|---|---|---|
| Inline `// codeql[<rule-id>]` | `// codeql[js/sql-injection] - Reason: input pre-sanitized via library X` | Single-line exception with documented rationale |
| SARIF post-processing filter | `cat results.sarif \| jq 'del(.runs[].results[] \| select(.ruleId == "js/path-injection" and .locations[].physicalLocation.artifactLocation.uri \| startswith("vendor/")))'` | Bulk exclusion of vendored / generated code |
| GitHub Security tab dismissal | UI: "Dismiss alert" → False positive / Won't fix / Used in tests | Persistent, auditable, requires reviewer comment |

**Justification template (mandatory in code):**

```javascript
// codeql[js/sql-injection]
// Reason: parameter pre-validated via Joi schema (line 42); literal interpolation safe
// Reviewer: alice@example.com (2026-05-15)
// Expires: 2026-12-15
const result = await db.query(`SELECT * FROM users WHERE id = ${userId}`);
```

GitHub Security tab dismissals are persistent + auditable + show in
the audit log; prefer them over inline comments for production
suppressions.

Cadence: every quarter, review GitHub Security → "Dismissed alerts"
filter; expired ones reopened for re-review.

## Step 5 - Database performance

CodeQL databases can be GBs for large codebases. Performance flags:

```bash
codeql database create my-db --language=java \
  --command="./gradlew build" \
  --threads=8 \
  --ram=8192   # MB
```

For incremental scanning (changed-files-only), GitHub's hosted
runner uses caching across runs. Self-hosted CI must implement
caching manually (the `codeql-action/init` action handles it on
GitHub).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Skip `--command` for compiled languages | Database empty; analysis returns no findings silently | Always wrap the build (Step 2) |
| Use `security-extended` without baseline | Flood of pre-existing findings overwhelms the team | Start with `code-scanning`; ratchet up |
| Inline comment without GitHub dismissal | No audit trail | Use Security-tab dismissal for persistent FPs (Step 4) |
| Run CodeQL on every PR for large codebase | Database creation is slow (10 - 30 min); PR cycle slow | Schedule full scan nightly; PR-only delta scanning via Code Scanning |
| Custom queries without test suite | Bugs in custom queries miss real findings | Use `codeql test` to validate against expected-results files |

## Limitations

- Database creation is slow for large codebases (10 - 30 min on
  monorepos); incremental scanning helps but requires caching.
- Custom-query authoring has a steep learning curve; the CodeQL
  University courses help.
- Some languages have less depth than others (Go, Ruby, Swift are
  newer than JS/Java/C++).
- Self-hosted (non-GitHub) integration requires manual SARIF
  routing.
- License: CodeQL CLI is free for open-source repos; commercial
  use requires GitHub Advanced Security license.

## References

- [cql-docs][cql-docs] - CodeQL CLI getting started
- codeql.github.com/docs - official documentation root
- codeql.github.com/codeql-standard-libraries/ - per-language stdlibs
- github.com/github/codeql - query packs source
- learningqltest.github.io/learningql/ - CodeQL University training
- `semgrep-rules`,
  `sonarqube-rules`,
  `language-native-sast` - sister scanners
