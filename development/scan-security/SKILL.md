---
name: scan-security
description: "Run a Snyk SAST + SCA security audit on the repository, remediate findings that pass the project's verification gates, and write a prioritized report to .audit/. Optional scope argument: all (default), code, deps, or changed."
disable-model-invocation: true
metadata:
  author: Serghei Iakovlev
  version: "1.0"
  category: security
---

# Security Audit

Conduct a Snyk security audit of the current repository: static analysis (SAST) of code, software composition analysis (SCA) of dependencies, remediation of findings the project's verification gates accept, and a prioritized evidence-backed findings report.

This skill carries the audit workflow. The project supplies the rest: build / lint / test / install commands, source file conventions, dependency-manager invocations, false-positive patterns, and any hard remediation prohibitions live in the project's context files (AGENTS.md, CONTRIBUTING.md, README.md) and architecture documentation. This skill tells you *how to scan, remediate, and report*; the project tells you *what counts as valid* for fixes.

## Inputs

The user invokes this skill with an optional scope argument. Resolve the scope before any tool call.

| Scope | SAST target | SCA target |
|---|---|---|
| `all` (default when unset) | Entire repository | Full dependency manifest set |
| `code` | Entire repository | (skipped) |
| `deps` | (skipped) | Full dependency manifest set |
| `changed` | Source files modified vs. `HEAD` | Manifest / lock files modified vs. `HEAD` |

For `changed`, derive the file set from the union of `git diff --name-only HEAD` and `git diff --cached --name-only`, deduplicated. Within that set:

- **Source files**: pass the diff list to the SAST tool. Snyk Code skips files in unsupported languages. Filter out obvious non-source (lock files, binary assets, generated artifacts) only when their presence in the diff is incidental.
- **Manifest / lock files**: the files the project's package manager owns (`package.json` + lock, `go.mod` + `go.sum`, `pyproject.toml` + lock, `Gemfile` + `Gemfile.lock`, `composer.json` + lock, `Cargo.toml` + `Cargo.lock`, etc.). Include only manifests that appear in the diff.

## Workflow

Copy this checklist into your response and tick items as you complete them.

- [ ] Step 1 - Pre-flight (capability, auth, build gate, baseline SHA)
- [ ] Step 2 - Static analysis (SAST)
- [ ] Step 3 - Dependency scan (SCA)
- [ ] Step 4 - Triage findings
- [ ] Step 5 - Remediate Fix-Now findings
- [ ] Step 6 - Re-verification scan
- [ ] Step 7 - Report

### Step 1 - Pre-flight

Run these checks in order. Abort if any fails. Scanning incomplete or broken code produces unreliable results.

**1a. Snyk capability.** Determine how Snyk is reachable in this session, in preference order:

1. **MCP tools.** The Snyk MCP server registers tools with canonical names `snyk_auth_status`, `snyk_auth`, `snyk_code_scan`, `snyk_sca_scan`, `snyk_trust`, `snyk_iac_scan`, `snyk_container_scan`. Hosts namespace them differently (Claude Code exposes them as `mcp__<server>__snyk_code_scan`; other clients use other prefixes). Match by suffix and by tool description, not by exact name.
2. **`snyk` CLI on PATH.** Confirm with `command -v snyk`. The CLI subcommands are `snyk code test` (SAST), `snyk test` (SCA), `snyk auth`, and `snyk config get api` (auth status).
3. **Neither.** Halt. Inform the user that Snyk is not available in this session and link them to the Snyk MCP setup or `npm install -g snyk` as remediation. Do not proceed.

Record which path is in use; reuse it throughout the workflow.

**1b. Authentication.** Call the auth-status tool (`snyk_auth_status` via MCP) or run `snyk config get api`. If the result is empty or reports unauthenticated, halt. Tell the user to authenticate (`snyk auth` or the `snyk_auth` MCP tool) and re-invoke this skill.

**1c. Build gate.** Read the project's context files (AGENTS.md, CONTRIBUTING.md, README.md) and identify the canonical command that compiles or type-checks the codebase. Run it. The project must build cleanly before a scan is meaningful. If the gate fails, halt and surface the errors.

If the project context does not document a build command, infer the default from the project manifest (e.g., `tsc --noEmit` for TypeScript, `go build ./...` for Go, `cargo check` for Rust) and note the inference in the report's Next Steps.

**1d. Baseline SHA.** Capture `git rev-parse HEAD`. This SHA anchors the report.

### Step 2 - Static analysis (SAST)

Skip when scope is `deps`.

Call the SAST tool (`snyk_code_scan` via MCP, or `snyk code test --json` via CLI) against the SAST target from Inputs.

For every finding, record:

| Field | Content |
|---|---|
| ID | `SAST-{seq}` starting at `SAST-01` |
| Severity | `critical` / `high` / `medium` / `low` |
| CWE | Identifier and category (e.g., `CWE-89 SQL Injection`) |
| Location | `path:start-end` |
| Summary | One sentence describing the vulnerability |
| Snyk suggestion | Snyk's fix recommendation, if any |
| Confidence | `high` / `medium` / `low` |

Capture every finding Snyk reports. Do not filter or suppress at this stage. Triage happens in Step 4.

### Step 3 - Dependency scan (SCA)

Skip when scope is `code`.

Call the SCA tool (`snyk_sca_scan` via MCP, or `snyk test --json` via CLI) against the SCA target from Inputs.

For every vulnerability, record:

| Field | Content |
|---|---|
| ID | `SCA-{seq}` starting at `SCA-01` |
| Severity | `critical` / `high` / `medium` / `low` |
| CVE | CVE identifier(s) |
| Package | Name plus installed version (e.g., `lodash@4.17.20`) |
| Fixed version | Earliest version resolving the issue |
| Dep type | `direct` or `transitive` |
| Upgrade path | What to change to reach the fixed version |

### Step 4 - Triage

Classify every finding from Steps 2-3 before touching any file.

| Verdict | Criteria | Next action |
|---|---|---|
| Fix Now | Safe fix exists; surgical change; no public API break; no major version bump | Remediate in Step 5 |
| Manual Review | Correct but risky: major version bump, API shape change, or expected test failures | Document; do not touch |
| False Positive | Matches a project-documented safe pattern | Suppress with inline justification |
| Track | Low severity with no safe upgrade path at this time | Document for backlog |

**Project-approved safe patterns.** Snyk's generic rules can fire on patterns that are intentionally safe in the host project. Search the project's context files and architecture documentation for documented safe patterns (search terms like "intentional", "false positive", "approved", "by design" alongside any term that appears in a finding). When a finding matches a documented pattern, classify as **False Positive** and cite the project documentation in the report. Never classify as False Positive without a citation; an undocumented suspicion is **Manual Review**.

**Project prohibitions.** The project context may document hard prohibitions: "never modify the database schema", "never downgrade dependency X below version Y", "never touch directory Z", "never modify lint / format config". Read these alongside the rest of project context at Step 1. Any Fix-Now candidate that would violate a documented prohibition becomes **Manual Review** with the prohibition cited as the reason.

### Step 5 - Remediation

Process Fix-Now findings ordered by severity, most severe first. After each individual fix, run the verification gate.

**Verification gate.** The set of commands the project considers proof that a change is acceptable. Read the project's context files at Step 1 (refresh now if needed) and run only the subset relevant to what you changed.

- A change to source code runs the formatter, linter, type checker (if any), and the tests covering the affected area.
- A change to a dependency manifest additionally runs the project's lock-file resolution command (e.g., `npm ci`, `yarn install --frozen-lockfile`, `pnpm install --frozen-lockfile`, `bundle install`, `poetry install`, `go mod tidy`, `cargo check`) and the full test suite.

Follow the project's declared commands verbatim. Do not substitute equivalents (e.g., do not invoke a binary directly when conventions specify a task runner). If the project context is silent on a category you touched, infer the default from the manifest and note the inference under the affected finding in the report.

On verification failure: revert the change with `git checkout -- <files>` and reclassify the finding as **Manual Review**. Move on.

**SAST fix procedure.**

1. Read the affected file in full to understand context.
2. Apply the minimal change that resolves the CWE. Prefer Snyk's suggestion when it aligns with project conventions; implement the architecturally correct equivalent when it does not.
3. Run the verification gate.
4. On gate failure: revert and reclassify as **Manual Review**.

**SCA fix procedure.**

1. Apply the upgrade using the project's package manager. Read the project context to determine the exact command (the package manager and its install / add / update verb). For transitive dependencies, prefer upgrading the direct parent that pulls the fixed version over forced overrides; record the choice in the report.
2. Run the project's lock-file resolution command and the verification gate.
3. On gate failure: restore the manifest and lock file with `git checkout` and reclassify as **Manual Review**.

**Suppressions and inline disables.** Never add a tool-specific disable comment (`// snyk:disable`, `/* eslint-disable */`, `# noqa`, `#nosec`, etc.) without an inline justification in the same comment that names the False Positive pattern the project context documents.

**Staging.** Never `git add -A`, `git add .`, or any equivalent blanket-staging command. Stage only files this skill intentionally modified, if asked to stage at all (the default is to leave changes unstaged for the user to review).

### Step 6 - Re-verification scan

After all Step 5 work is complete:

1. Re-run the SAST tool if SAST was in scope.
2. Re-run the SCA tool if SCA was in scope.

For each previously remediated finding, confirm it no longer appears in the new output. If it still appears, append to the **Manual Review** section and update the report counts.

If a finding appears that was absent in Steps 2-3, treat it as a regression introduced by remediation: revert the responsible change, reclassify the finding as **Manual Review**, and document the regression in the report.

### Step 7 - Report

Write the report to `.audit/security-{YYYYMMDD}-{short-sha}.md`, where `{short-sha}` is the first 8 characters of the baseline SHA from Step 1d. Create `.audit/` if absent. If a file with this name already exists, append `-2`, `-3`, etc. before the `.md` extension.

Use [assets/report-template.md](assets/report-template.md) as the structural template. Fill every section; write "None" when a section is empty.

After writing the file, print to chat: the report's absolute path, the Summary table, and the verdict. Do not paste the full report into chat.

## Constraints

- Do not commit, push, or stage changes. Leave modifications unstaged for the user to review.
- Do not invent findings. Work exclusively from Snyk output.
- Do not apply fixes that violate documented project prohibitions; reclassify as **Manual Review** and cite the prohibition in the report.
- Coding standards for any fix come from the project's coding rules and instructions; this skill does not override them.
- If the project context names a follow-up skill or command for staging and PR creation (e.g., a `create-pr` skill), recommend it in **Next Steps**; do not invoke it from this skill.
