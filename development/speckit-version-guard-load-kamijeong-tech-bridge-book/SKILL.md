---
name: speckit-version-guard-load
description: Load existing version guard constraints into agent context before task
  generation or implementation
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: version-guard:commands/speckit.version-guard.load.md
---

# Version Guard — Load Constraints

Load the constraints artifact written by `speckit.version-guard.check` into the
agent's context so that task generation and implementation follow the Compatibility
Rules. This command fires automatically before `/speckit.tasks` and
`/speckit.implement` via hooks (`optional: false` — always runs, always completes;
it handles all error conditions internally via graceful degradation).

This is a lightweight command — when the artifact exists, it does NOT fetch from
registries or check for CVEs. If the artifact does not exist (e.g., the developer ran
`/speckit.implement` without running `/speckit.plan` first), it falls back to running
the full check command, which does fetch and may pause for critical/high CVEs in
interactive contexts.

## Execution Steps

### Step 1 — Resolve the feature directory

- Read `.specify/feature.json` to get the current feature directory path (referred to
  as `<feature_dir>` in subsequent steps)
- If `.specify/feature.json` does not exist or has no feature directory, fall back to
  `.specify/` as the output directory

### Step 2 — Check for the constraints artifact

- Look for `<feature_dir>/version-guard-report.md`
- If the file exists and starts with `# Version Guard Report — Skipped`, the check
  previously skipped. Read the reason line (the line after the heading) to determine
  what to re-check:
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
  command instead, then stop (check handles constraint loading, self-instruction,
  and CVE warnings from there — including write-failure fallback to in-memory
  content). If none exist, output "ℹ️ Version guard previously skipped — [reason
  from artifact]" and stop without re-running check.
- If the file exists with normal content, proceed to Step 3
- If the file does not exist, output: "ℹ️ No version guard report found — running
  full version check" and execute the `speckit.version-guard.check` command instead,
  then stop (the check command handles everything from there)

### Step 3 — Load and instruct

1. **Read `<feature_dir>/version-guard-report.md`** into context.
2. Print a brief summary:

   ```
   📋 Version guard constraints loaded from <feature_dir>/version-guard-report.md
   ```

   If the report contains a `### Current-Version References` subsection with one or
   more entries, also print:

   ```
   📚 Migration references: {N} packages have Current-Version References available — consult these before generating code.
   ```

   (Where N = count of entries under `### Current-Version References`. Omit this line
   when no Current-Version References are present.)

3. Instruct yourself:

   > The Compatibility Rules section above is mandatory guidance for all subsequent
   > steps in this session — including task generation and implementation. When
   > generating tasks or code for any listed package, follow every DO rule and avoid
   > every DON'T rule.
   >
   > The Upgrade Guidance section is informational — do not apply it to generated code
   > unless the developer explicitly requests an upgrade.
   >
   > If uncertain about an API, consult the Migration References URLs before falling
   > back to training data.
   >
   > Treat Current-Version References as primary sources for current-version packages —
   > your training data may predate their APIs even when they are at latest.

4. If the **Known Issues** section contains any critical or high severity CVEs,
   print a reminder:

   ```
   🚨 Reminder: Critical/high CVE(s) affect locked versions.
   Review the Known Issues section in <feature_dir>/version-guard-report.md.
   ```

   If the Known Issues section indicates lookup failures ("Known issue lookups
   failed"), print:

   ```
   ⚠️ Known issue data may be incomplete — some lookups failed during the check.
   ```

5. Continue the workflow — do NOT block.

## Graceful Degradation

- If `<feature_dir>/version-guard-report.md` does not exist: fall back to the full `speckit.version-guard.check` command
- If the file exists but cannot be read: use in-memory report content if available from an earlier check in this session (applying the stale-skip recheck logic from Step 2 if it is a skip report); otherwise re-run `speckit.version-guard.check` (which will attempt to regenerate and use in-memory content if the write still fails)