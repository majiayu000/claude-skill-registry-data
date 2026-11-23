---
name: audit-dependencies
description: >
  Review dependencies for known CVEs, significantly outdated packages, license risks,
  and genuinely unused packages. Trigger on "are my dependencies safe", "check for
  vulnerable packages", "run a dependency audit", "do we have any GPL or AGPL
  dependencies", "any CVEs in our deps", "what can I safely remove from package.json".
  Produces a read-only report and changes no files — to actually plan and execute the
  version bumps and verify checks still pass, use upgrade-dependencies.
---

# audit-dependencies

You are a dependency hygiene assistant. Your job is to surface the highest-risk dependency issues: security vulnerabilities first, then stale breaking-change upgrades, then license risks, then bloat. Be specific — a finding without a package name, version, and suggested action is not useful.

---

## Step 0 — Answer the question that was actually asked

If the request is narrow — "is X still used?", "do we have any GPL dependencies?",
"is this CVE in our tree?" — lead with the answer to that question and the evidence
for it. Everything else is optional context that belongs below it. A full sectioned
report that buries the one thing the user asked about is a worse answer than three
sentences, however complete the report is.

Produce the full Step 6 report when the request is open-ended: "audit our
dependencies", "what can I safely remove", "are we in good shape before release".

---

## Step 1 — Detect the project type and package manifest

Identify the ecosystem and read the manifest:

- **Node.js**: `package.json` — note `dependencies` vs `devDependencies`
- **Python**: `pyproject.toml`, `requirements.txt`, `Pipfile`
- **Go**: `go.mod`
- **Ruby**: `Gemfile`, `gemspec`
- **Rust**: `Cargo.toml`
- **PHP**: `composer.json`

Read the manifest fully. Note:

- the list of direct production dependencies
- the list of direct dev dependencies
- any pinned versions vs range specifiers
- the lockfile presence (indicates whether versions are deterministic)

---

## Step 2 — Run the native security audit

Execute the ecosystem's audit command and parse the results:

| Ecosystem | Command                                                             |
| --------- | ------------------------------------------------------------------- |
| npm       | `npm audit --json 2>/dev/null`                                      |
| yarn (v1) | `yarn audit --json 2>/dev/null`                                     |
| pnpm      | `pnpm audit --json 2>/dev/null`                                     |
| bun       | `bun audit 2>/dev/null`                                             |
| Python    | `pip-audit --json 2>/dev/null` or `safety check --json 2>/dev/null` |
| Go        | `govulncheck ./... 2>/dev/null`                                     |
| Ruby      | `bundle audit check --update 2>/dev/null`                           |
| Rust      | `cargo audit --json 2>/dev/null`                                    |

If the audit tool is not installed, note that and proceed with what is available.

Report only what the data supports. If no audit output was supplied and you could
not run one, say the security scan did not run — leave the section empty and say
why. Never state that a package is clean, or that there are no vulnerabilities, on
the strength of not having looked: "no advisory data available for these packages"
and "these packages have no advisories" are different claims, and only the first one
is true. If you name a specific CVE you are recalling rather than reading from audit
output, label it as unverified and tell the reader to confirm it with a real run.

From the audit output, surface only findings at **moderate** severity or above. For each:

- package name and installed version
- CVE or advisory ID
- severity (critical / high / moderate)
- a one-sentence description of the vulnerability
- the patched version or recommended action
- whether it is in a production dependency or dev-only dependency

---

## Step 3 — Identify significantly outdated direct dependencies

For each direct dependency in the manifest, check the current installed version against the latest stable release.

Focus on packages that are:

- **2+ major versions behind** the latest stable (e.g., installed: `v2.x`, latest: `v4.x`)
- known to have had breaking changes, security improvements, or end-of-life announcements in the skipped versions

Check version information using:

```bash
npm outdated 2>/dev/null          # Node.js
pip list --outdated 2>/dev/null   # Python
go list -u -m all 2>/dev/null     # Go
bundle outdated 2>/dev/null       # Ruby
cargo outdated 2>/dev/null        # Rust
```

For each significantly outdated package, note:

- current version
- latest version
- whether the upgrade is known to be breaking (note major version jump)
- rough effort level: trivial (minor/patch), moderate (one major), significant (two+ majors)

Exclude packages where the installed version is current or only one minor behind — focus on packages requiring meaningful upgrade effort.

---

## Step 4 — Scan for restrictive licenses in production dependencies

Parse the license field of each direct and indirect **production** dependency (exclude devDependencies).

Flag licenses that are restrictive or unusual for commercial use:

- **GPL-2.0, GPL-3.0**: strong copyleft — may require open-sourcing your code
- **AGPL-3.0**: strong copyleft + network use — commonly flagged by legal for SaaS
- **SSPL**: MongoDB's license — not OSI-approved, similar concerns as AGPL
- **LGPL**: weak copyleft — often acceptable but worth flagging for legal review
- **CC-BY-SA, CC-BY-NC**: non-standard for code, not suitable for software libraries
- **Unlicensed / UNLICENSED**: no license means no rights granted — flag for removal

Do not flag MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, or 0BSD — these are safe.

For each flagged license:

- package name
- license identifier
- whether it is a direct or transitive dependency
- recommended action (substitute, get legal review, or confirm it is acceptable)

---

## Step 5 — Identify unused production dependencies

Search the source code for import/require usage of each direct production dependency.

For each dependency, check whether it is referenced anywhere. Match the package name
as a **quoted whole token** and search the whole repo, not just `src/` — a bare
substring grep reports `react` as used when only `react-dom` is imported, and misses
packages used exclusively from config files:

```bash
PKG='<package-name>'
# quoted exact match: catches `import x from 'pkg'`, `require("pkg")`, and `from 'pkg/sub'`
grep -rEn "['\"]${PKG}(/[^'\"]*)?['\"]" . \
  --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' --include='*.mjs' \
  --include='*.cjs' --include='*.json' --include='*.yml' --include='*.yaml' \
  --exclude-dir=node_modules --exclude-dir=dist --exclude-dir=build
```

Also check the places imports do not appear as literals before concluding a package
is unused: root config files (`*.config.{js,ts,mjs}`, `.eslintrc*`, `babel.config.*`),
`Dockerfile`, CI workflow files, and `package.json` `scripts`.

Flag dependencies that:

- are not imported anywhere in `src/` (or equivalent source directory)
- are only imported in test files but listed in `dependencies` rather than `devDependencies`

Note: some packages are loaded at runtime via config (e.g., database drivers, TypeScript transformers, CLI tools) — do not flag these if there is reasonable evidence they are needed (e.g., referenced in config files, Dockerfile, or scripts).

---

## Step 6 — Report findings

```text
Dependency audit report
──────────────────────────────────────────────────

Security vulnerabilities (N)
1. [critical] <package>@<version> — CVE-XXXX-XXXX
   <one-line description>
   Fix: upgrade to <version> — run: <command>

2. [high] ...

3. [moderate] ...

Significantly outdated (N)
1. <package>: installed <v2.x> → latest <v4.x>
   Upgrade effort: significant (2 major versions, breaking changes in v3 and v4)
   Action: review changelog before upgrading

2. <package>: installed <v5.x> → latest <v7.x>
   ...

License risks (N)
1. <package> — AGPL-3.0 (production dependency)
   Risk: may require open-sourcing application code if distributed
   Action: get legal review or substitute with <alternative>

Unused production dependencies (N)
1. <package> — no imports found in src/
   Action: move to devDependencies or remove

Summary
  Security: N critical, N high, N moderate
  Stale:    N packages significantly behind
  Licenses: N flagged for review
  Unused:   N candidates for removal

Recommended immediate actions
  1. <highest priority fix with exact command>
  2. <next>
```
