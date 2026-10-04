---
name: speckit-version-guard-check
description: Verify tech stack versions against live registries and write version-correct
  constraints
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: version-guard:commands/speckit.version-guard.check.md
---

# Version Guard — Tech Stack Verification

Verify that locked library versions are current, fetch migration documentation for
flagged packages, and write a structured constraints file that subsequent plan, task,
and implement phases MUST reference. This command fires automatically before
`/speckit.plan` via hooks (`optional: false` — always runs; handles all error
conditions internally via graceful degradation). The lightweight
`speckit.version-guard.load` command re-loads the artifact before `/speckit.tasks`
and `/speckit.implement` without re-fetching.

**Note:** This command may pause for developer acknowledgment if critical or high
severity CVEs are found (see Step 7). In non-interactive contexts where pausing is
not possible, the command emits a prominent warning and continues.

## Execution Steps

### Step 1 — Resolve the feature directory

- Read `.specify/feature.json` to get the current feature directory path (referred to
  as `<feature_dir>` in subsequent steps)
- If `.specify/feature.json` does not exist or has no feature directory, fall back to
  `.specify/` as the output directory
- Create `<feature_dir>` if it does not already exist
- The constraints artifact will be written to `<feature_dir>/version-guard-report.md`

### Step 2 — Locate dependency versions

Resolve **actual locked versions** (not declared ranges) using this precedence order
(first match wins per location):

1. **`package-lock.json`** (npm lockfile — exact resolved versions)
2. **`pnpm-lock.yaml`** (pnpm lockfile)
3. **`yarn.lock`** (Yarn lockfile)
4. **`package.json`** (fallback — only if no lockfile exists at that location). If a
   version field contains a range (`^`, `~`, `>=`), use the minimum version the range
   satisfies as a conservative proxy. Note: this may not match the actual installed
   version.

Apply this precedence **independently** at each location in this order: repo root,
`frontend/`, `backend/`. Aggregate all discovered packages across locations. If the
same package appears at multiple locations with different versions, use the version
from the first location in that order (repo root wins over `frontend/`, which wins
over `backend/`).

Additionally, if `docs/reference/tech-stack-decision-record.md` exists, read it as
**supplemental context** when lockfiles or package.json are present (e.g., rationale
for version choices, planned upgrades). It does not override the versions found in
lockfiles or package.json. However, if the decision record lists a version that
differs from the lockfile version for the same package, note the discrepancy in the
status table (e.g., "locked 18.3.1, decision record says 19.0.0") so the developer
is aware.

**Last-resort fallback for greenfield projects**: If no lockfile or package.json
exists at any location, but `docs/reference/tech-stack-decision-record.md` exists,
look for a Stack Decisions table:

- If the file has **no Stack Decisions table**, treat it the same as no usable
  packages — write a skip artifact:
  ```
  # Version Guard Report — Skipped
  No npm packages with exact versions found in tech stack decision record.
  ```
  Then output: "ℹ️ Tech stack decision record found but no Stack Decisions table
  present — skipping version check" and stop.

- If the file **has a Stack Decisions table**, extract npm-relevant packages using
  these rules:

1. **Parse the table**: Read rows from the Stack Decisions table (columns: Scope,
   Layer, Chosen Value, Version).
2. **Skip non-npm rows**: Ignore rows where the Chosen Value is not an npm package
   (e.g., "PostgreSQL", "GitHub Actions", "Azure App Service"). Focus on rows where
   the Layer is a programming language runtime, framework, build tool, or test
   framework that maps to an npm package.
3. **Map product names to npm packages**: The Chosen Value column contains product
   names, not npm package names. Map them (e.g., "React" → `react`, "TypeScript" →
   `typescript`, "Vite" → `vite`, "Express" → `express`, "Tailwind CSS" →
   `tailwindcss`). If a mapping is uncertain, skip the row.
4. **Require exact versions**: Only use rows with a concrete version number (e.g.,
   `5.8.3`, `18.3.1`). Skip rows with blank, placeholder (`*e.g., 5.8.3*`), or
   range versions.
5. **Minimum threshold**: The fallback only proceeds if at least one concrete npm
   package with an exact version is extracted. If zero usable packages result after
   filtering, write a minimal skip artifact to `<feature_dir>/version-guard-report.md`:
   ```
   # Version Guard Report — Skipped
   No npm packages with exact versions found in tech stack decision record.
   ```
   Then output: "ℹ️ Tech stack decision record found but no npm packages with
   exact versions could be extracted — skipping version check" and stop.

Extracted versions are marked "(from decision record)" in the status table to
distinguish them from lockfile-sourced versions. This ensures version guard provides
value during planning even before the project is scaffolded.

- If no lockfile, package.json, **or** tech stack decision record exists, write a
  minimal skip artifact to `<feature_dir>/version-guard-report.md`:
  ```
  # Version Guard Report — Skipped
  No dependency sources found (no lockfile, package.json, or tech stack decision record).
  ```
  Then output: "ℹ️ No dependency sources found (no lockfile, package.json, or tech stack decision record) — skipping version check" and stop

### Step 3 — Fetch and compare versions

For each locked dependency, fetch the latest stable version from the npm registry:

- Fetch `https://registry.npmjs.org/{package}/latest`
- Compare the locked version against the latest stable version
- Classify each package:
  - **✅ Current** — locked major version matches the latest stable major version (minor/patch differences are not flagged — they rarely cause API incompatibilities). **Exception:** for `0.x` packages, compare major *and* minor — `0.x` packages treat minor bumps as breaking per SemVer.
  - **⚠️ Behind** — locked major version is behind the latest stable major version, or for `0.x` packages, the locked minor version is behind.
  - **❓ Unverified** — registry fetch failed (network error, rate limiting, private package). Record the reason. No constraints can be generated for unverified packages.
- Build a status table:

  | Package | Locked | Latest Stable | Status |
  |---------|--------|---------------|--------|
  | react   | 18.3.1 | 19.x.x       | ⚠️ Behind |
  | vite    | 6.0.0  | 6.2.x        | ✅ Current |
  | axios   | 0.27.2 | 1.7.x        | ⚠️ Behind |
  | some-lib | 0.3.1 | 0.4.x        | ⚠️ Behind (0.x minor bump) |

  **Annotations**: Append source and discrepancy notes inline:
  - Decision record sources: append "(from decision record)" after the version in the **Locked** column, e.g., `18.3.1 (from decision record)`
  - Version mismatches between lockfile and decision record: append the note in the **Status** column, e.g., `⚠️ Behind (locked 18.3.1, decision record says 19.0.0)`
  | @internal/lib | 2.1.0 | — | ❓ Unverified (private registry) |

### Step 4 — Check for known issues

For **every** locked package (including ✅ Current):

- Check the GitHub repository's security advisories or the npm audit endpoint for
  known vulnerabilities (CVEs) affecting the locked version
- Check the package's GitHub issues for labels like `bug`, `critical`, `regression`,
  or `security` that mention the locked version
- If the package has a GitHub Security Advisory (GHSA) page, check:
  `https://github.com/{owner}/{repo}/security/advisories`

Record any findings. If a known issue is found:
- Note the severity (critical, high, moderate, low)
- Summarize the issue in one sentence
- Link to the advisory or issue
- Note whether a patched version exists

### Step 5 — Fetch documentation for flagged packages

For any package that is **⚠️ Behind** or has **known issues**:

- Fetch the official migration guide or changelog:
  - React: `https://react.dev/blog`
  - Vite: `https://vite.dev/blog`
  - Azure SDKs: use Microsoft docs MCP tools
  - Other packages: fetch the GitHub releases page or CHANGELOG.md from the repo
- Summarize key API changes, new patterns, and deprecated features in 3–5 bullets
- Fetch documentation for **both** the locked version and the latest version to
  support both constraint channels (see Step 6)

### Step 6 — Write the constraints artifact

Create or overwrite `<feature_dir>/version-guard-report.md` with the following sections:

```markdown
# Version Guard Report

Generated: {current ISO 8601 timestamp}

## Version Status

| Package | Locked | Latest Stable | Status |
|---------|--------|---------------|--------|
| {package} | {locked} | {latest} | {status emoji + label} |
...

## Known Issues

List any known vulnerabilities or critical bugs affecting locked versions.
If none are found, write "No known issues found for locked versions."
If lookups failed for any packages, write "⚠️ Known issue lookups failed for:
{package list} — results may be incomplete." This ensures downstream commands
(load, validate) do not treat a lookup failure as a clean bill of health.

⚠️ **Security vulnerabilities should be addressed promptly.** If a patched version
exists, consider upgrading. If upgrading is not possible, review the advisory for
available workarounds.

| Package | Version | Severity | Type | Issue | Patched In |
|---------|---------|----------|------|-------|------------|
| {package} | {locked} | {critical/high/moderate/low} | {CVE or Bug} | {one-sentence summary + link} | {version or "N/A"} |
...

## Compatibility Rules (mandatory)

These rules ensure generated code works correctly with the **locked version**.
The `speckit.version-guard.validate` command checks these rules after implementation.

Each constraint is an explicit pair: a pattern to avoid and what to use instead.

**How to derive rules for any package:** When reviewing migration docs between the
locked version and the latest version, look for:
- APIs added in newer versions that do not exist in the locked version
- APIs renamed or moved between versions
- Changed default behaviors (e.g., config options, return types)
- Removed or restructured internal import paths
- New syntax or patterns that require a minimum version
- Build/runtime behavior changes that affect generated code

Only include rules where the DON'T pattern would **fail or behave incorrectly** on
the locked version. Do not include stylistic preferences or deprecation warnings
for APIs that still work on the locked version.

### react (locked 18.3.1 — latest is 19.x)

| # | ❌ DON'T | ✅ DO instead |
|---|----------|--------------|
| 1 | Use `useActionState` (React 19 only) | Use `useReducer` or `useState` for form/action state management |
| 2 | Pass `ref` as a regular prop (not supported until React 19) | Use `forwardRef` to forward refs to child components |
| 3 | Use `use(Context)` hook (React 19 only) | Use `useContext(MyContext)` |

### axios (locked 0.27.2 — latest is 1.7.x)

| # | ❌ DON'T | ✅ DO instead |
|---|----------|--------------|
| 1 | Use `axios.formToJSON()` (v1.x only) | Parse FormData manually or use a third-party library |
| 2 | Use `AxiosHeaders` class for header manipulation (v1.x only) | Pass plain objects for headers — `{ headers: { 'Content-Type': 'application/json' } }` |

### {next package}
...

## Upgrade Guidance (informational)

For each ⚠️ Behind package, summarize what the latest version offers. This section
is informational — it helps the developer decide whether and when to upgrade.
It is NOT checked by the validate command.

### react (18.3.1 → 19.x)

Key changes in the latest version:
- `useActionState` replaces `useReducer` for form actions
- `ref` can be passed as a regular prop — `forwardRef` is no longer needed
- New `use()` hook for reading context, promises, and other resources
- `<form action={fn}>` for progressive enhancement

### axios (0.27.2 → 1.7.x)

Key changes in the latest version:
- Complete TypeScript rewrite with improved type safety
- New `AxiosHeaders` class for header manipulation
- Internal paths like `axios/lib/adapters/http` restructured — use public APIs
- `transformResponse` default behavior changed
- New `axios.formToJSON()` utility for parsing FormData

### {next package}
...

## Migration References

For each flagged package, list the URLs fetched for both the locked version and the
latest version:

- **react** (locked 18.x): https://react.dev/blog/2024/04/25/react-19-upgrade-guide
- **react** (latest 19.x): https://react.dev/blog
- **axios** (locked 0.27.x): https://github.com/axios/axios/blob/v0.27.2/CHANGELOG.md
- **axios** (latest 1.7.x): https://github.com/axios/axios/blob/v1.x/CHANGELOG.md
...

### Current-Version References

If any packages are ✅ Current, include documentation URLs for them here — consult
these before relying on training data:

- **{package}** ({version}): {doc_url}
- ...one entry per ✅ Current package (omit this subsection if no packages are current)
```

If the output directory does not exist, create it.

If **all packages are current** and no known issues are found, write a minimal report:

```markdown
# Version Guard Report

Generated: {current ISO 8601 timestamp}

## Version Status

| Package | Locked | Latest Stable | Status |
|---------|--------|---------------|--------|
| ... | ... | ... | ✅ Current |

## Known Issues

No known issues found for locked versions.

## Compatibility Rules (mandatory)

No compatibility rules — all locked versions are current.
(See Migration References for documentation URLs on locked versions.)

## Upgrade Guidance (informational)

No major-version upgrades available.

## Migration References

### Current-Version References

Documentation for locked versions — consult these before relying on training data for
any package that may be newer than your model training cutoff:

- **{package}** ({version}): {doc_url}
- ...one entry per ✅ Current package
```

**URL resolution for Current-Version References** (applies to both all-current and
mixed reports): Use the well-known documentation URL for each package. Common mappings:

- `react` → `https://react.dev/reference/react`
- `vite` → `https://vite.dev/guide/`
- `typescript` → `https://www.typescriptlang.org/docs/handbook/`
- `vitest` → `https://vitest.dev/guide/`
- `@playwright/test` → `https://playwright.dev/docs/intro`
- `react-router` → `https://reactrouter.com/start/framework/installation`
- `react-i18next` → `https://react.i18next.com/`
- `i18next` → `https://www.i18next.com/overview/getting-started`

For unlisted packages, use the GitHub releases page
(`https://github.com/{org}/{package}/releases`) or the npm package page
(`https://www.npmjs.com/package/{package}`) as static fallbacks. No HTTP fetch is
required — these URLs are statically derived from the package name.

### Step 7 — Output summary and load constraints

1. Print the version status table to the conversation.
2. If any known issues were found, print them prominently with severity levels.
3. **If any critical or high severity CVEs were found**, pause and require explicit
   developer acknowledgment before continuing. Output:

   ```
   🚨 CRITICAL/HIGH CVE(s) found in locked dependencies:

   | Package | Version | Severity | CVE | Summary | Patched In |
   |---------|---------|----------|-----|---------|------------|
   | {package} | {locked} | {severity} | {CVE ID} | {one-sentence summary} | {version or "N/A"} |
   ...

   ⚠️ Proceeding will generate code using these versions. Acknowledge to continue.
   ```

   In interactive contexts (conversational sessions): wait for the developer to
   acknowledge before proceeding to the remaining Step 7 actions.

   In non-interactive contexts (automated pipelines, CI): emit the warning
   prominently, record it in the artifact, and continue — do not hang indefinitely.

4. If the write succeeded, print: `Constraints written to <feature_dir>/version-guard-report.md`
5. **Load the report into context:**
   - If the file was written successfully, read `<feature_dir>/version-guard-report.md` back into context.
   - If the write failed (permissions, etc.), use the in-memory report content generated in Step 6 directly — do not attempt to read a file that was not written.
6. Instruct yourself:

   > The Compatibility Rules section above is mandatory guidance for all subsequent
   > steps in this session (plan, tasks, and implement). When generating code for any listed
   > package, follow every DO rule and avoid every DON'T rule.
   >
   > The Upgrade Guidance section is informational — do not apply it to generated code
   > unless the developer explicitly requests an upgrade.
   >
   > If uncertain about an API, consult the Migration References URLs before falling
   > back to training data.
   >
   > For packages at current versions, your training data may predate these releases —
   > especially across multiple major versions. Use the Current-Version References URLs
   > to verify API patterns before relying on training-data defaults.

7. For ⚠️ Behind packages with no critical/high CVEs, and for moderate/low CVEs,
   do NOT block the workflow — continue to plan/implement. The Compatibility Rules
   are mandatory guidance regardless.

## Graceful Degradation

- If `web_fetch` or registry calls fail (network issues, rate limiting): classify the package as ❓ Unverified with the reason, skip it for constraint generation, and note the failure in the report
- If no lockfile or `package.json` exists but `docs/reference/tech-stack-decision-record.md` has versioned packages: use decision record as last-resort version source (marked "(from decision record)" in status table)
- If no lockfile, `package.json`, or tech stack decision record exists: output "ℹ️ No dependency sources found (no lockfile, package.json, or tech stack decision record) — skipping version check" and stop
- If all packages are current and no known issues found: write the minimal report and output "✅ All locked versions are current"
- If known-issue lookups fail (GitHub API rate limiting, etc.): record the failure in the Known Issues section ("⚠️ Known issue lookups failed for: {packages}"), warn, and continue — do not fail the entire check
- If `<feature_dir>/version-guard-report.md` cannot be written (permissions, etc.): warn and continue with in-memory report content — the Compatibility Rules remain mandatory guidance for the current session, but later hooks (load, validate) will not find the artifact on disk and will re-run check
- Critical/high CVEs: pause for developer acknowledgment in interactive contexts; emit prominent warning and continue in non-interactive contexts (see Step 7)