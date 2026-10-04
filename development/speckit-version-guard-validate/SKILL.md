---
name: speckit-version-guard-validate
description: Scan generated code for version-incompatible API patterns flagged by
  version guard
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: version-guard:commands/speckit.version-guard.validate.md
---

# Version Guard — Post-Implementation Validation

Scan files changed during implementation for API patterns that are incompatible with
the project's locked dependency versions. Uses the **Compatibility Rules** from the
report written by `speckit.version-guard.check`. This command fires automatically
after `/speckit.implement` via hooks (`optional: false` — always runs, always
completes; it handles all error conditions internally via graceful degradation).

## Execution Steps

### Step 1 — Resolve the feature directory and load the constraints artifact

- Read `.specify/feature.json` to get the current feature directory path (referred to
  as `<feature_dir>` in subsequent steps)
- If `.specify/feature.json` does not exist or has no feature directory, fall back to
  `.specify/` as the directory
- Read `<feature_dir>/version-guard-report.md`
- If the file does not exist and version guard report content is available in the
  current agent context (from a check that ran earlier in this session but could not
  write to disk), use that in-memory content. If the in-memory content is a skip
  report (starts with `# Version Guard Report — Skipped`), apply the same
  stale-skip recheck logic described below before stopping or proceeding. If no
  in-memory content is available either, output "ℹ️ No version guard report found —
  skipping validation" and stop.
- If the file starts with `# Version Guard Report — Skipped`, read the reason line
  (the line after the heading) to determine what to re-check:
  - If the reason mentions "no dependency sources found" (nothing existed at all):
    check for `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, or `package.json`
    at the repo root, `frontend/`, and `backend/`, and also check for
    `docs/reference/tech-stack-decision-record.md`.
  - If the reason mentions "no npm packages with exact versions" (decision record
    existed but had no usable packages): check for `package-lock.json`,
    `pnpm-lock.yaml`, `yarn.lock`, or `package.json` at the repo root, `frontend/`,
    and `backend/`. Also re-scan the Stack Decisions table in
    `docs/reference/tech-stack-decision-record.md` using the same extraction rules as
    check (Layer is a runtime, framework, build tool, or test framework; Chosen Value
    maps to an npm package; Version is an exact semver like `19.0.0`) — if at least
    one such row now exists, treat as a new source.
  If any relevant new source exists, output "ℹ️ Dependency sources found since last
  check — re-running version check" and execute the `speckit.version-guard.check`
  command. After re-running, re-read the updated artifact from disk. If the file was
  not updated (write failure in check), use the report content that check output to
  the agent context instead. If the result is still a skipped artifact, output
  "ℹ️ Version guard was skipped — no validation needed" and stop. Otherwise continue
  to parsing below. If no relevant new sources exist, output
  "ℹ️ Version guard was skipped — no validation needed" and stop.
- Parse the **Compatibility Rules (mandatory)** section. Each package has a numbered
  constraint table with columns: **❌ DON'T** and **✅ DO instead**.
  Extract each row as a constraint pair: the incompatible pattern to search for and
  its version-correct replacement.
- **Ignore the Upgrade Guidance section** — it is informational and must not be used
  for validation.
- Also load the **Known Issues** section. If any CVEs with severity **critical** or
  **high** were found, note them for inclusion in the validation output.

### Step 2 — Identify files to scan

- Determine which files were created or modified during the implement phase
- If you cannot determine the changed files, fall back to scanning all source files
  (`*.ts`, `*.tsx`, `*.js`, `*.jsx`, `*.py`, `*.cs`, `*.java`) in the project,
  excluding `node_modules/`, `dist/`, `build/`, `.specify/`, and other common
  output directories
- If no source files are found, output "ℹ️ No source files to validate" and stop

### Step 3 — Scan for incompatible patterns

For each constraint pair (DON'T → DO) in the Compatibility Rules:

- Search the identified files for usage of the incompatible API or pattern from the
  DON'T column
- Match on function/method names, import paths, and common usage patterns
- Ignore matches inside comments and documentation strings
- Record each finding with: file path, line number (if available), the matched
  DON'T pattern, and the paired DO replacement from the same constraint row

### Step 4 — Output the validation report

If **no violations found** and **no critical/high CVEs**, output:

```
✅ Version Guard Validation: No incompatible API patterns detected.
```

If **no violations found** but **critical/high CVEs exist**, output:

```
✅ Version Guard Validation: No incompatible API patterns detected.

🚨 Security reminder: {count} critical/high CVE(s) affect locked versions.
Review the Known Issues section in <feature_dir>/version-guard-report.md (or in the in-memory report if the file was not written).
```

If **violations are found**, output an advisory report:

```
⚠️ Version Guard Validation: {count} potential incompatible pattern(s) found.

| File | Line | Incompatible Pattern | Version-Correct Replacement |
|------|------|----------------------|-----------------------------|
| src/App.tsx | 12 | useActionState | useReducer or useState (React 19 only — project is on 18.x) |
| src/Form.tsx | 45 | use(ThemeContext) | useContext(ThemeContext) (use() hook is React 19 only) |
...

These are advisory warnings — review each match and update if appropriate.
Some matches may be false positives (e.g., references in string literals or unrelated identifiers).
```

If **violations are found** and **critical/high CVEs also exist**, append the
security reminder after the violations table:

```
🚨 Security reminder: {count} critical/high CVE(s) affect locked versions.
Review the Known Issues section in <feature_dir>/version-guard-report.md (or in the in-memory report if the file was not written).
```

If the **Known Issues** section contains a lookup-failure marker("Known issue
lookups failed"), append an incomplete-data warning in any output path:

```
⚠️ Known issue data may be incomplete — some lookups failed during the check.
```

### Step 5 — Continue the workflow

- Do NOT block or fail the workflow regardless of findings
- The validation report is advisory — the developer decides whether to act on it
- If the developer asks to fix the violations, use the DO replacement from the
  constraint pair as the mandatory guidance for corrections

## Graceful Degradation

- If `<feature_dir>/version-guard-report.md` does not exist and no in-memory report content is available from an earlier check in this session: output "ℹ️ No version guard report found — skipping validation" and stop
- If `<feature_dir>/version-guard-report.md` exists but cannot be read (permissions, etc.): fall back to in-memory report content if available from an earlier check in this session (applying the stale-skip recheck logic from Step 1 if it is a skip report); otherwise re-run `speckit.version-guard.check` and validate against the regenerated or in-memory report
- If the Compatibility Rules section is empty or says "No compatibility rules": output "✅ No compatibility rules to check", then still check for critical/high CVEs in the Known Issues section and append the security reminder if any exist, then proceed
- If file scanning fails for any file: warn for that file and continue with others