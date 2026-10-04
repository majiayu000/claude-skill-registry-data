---
name: code-audit
description: Perform a structured audit of a codebase covering security, code quality, performance, dependencies, architecture, and testing hygiene, then produce a prioritized findings report. Use this skill whenever the user asks for a code review, code audit, security review, codebase assessment, "look over this repo", "what's wrong with this codebase", legacy-code triage, pre-acquisition technical due diligence, or any request to systematically evaluate the health of a project. Trigger even when the user is casual ("can you eyeball my repo?") — this skill imposes the structure that ad-hoc review misses. This skill audits a whole repository at a point in time — for reviewing a diff or PR use the built-in code-review skill; for security checks on pending changes use security-review.
---

# Code Audit

A structured methodology for auditing a codebase end-to-end. The goal is not to read every line — it's to **find the issues that matter** in finite time and present them in a form the owner can act on.

## When to use this skill

- "Audit this codebase" / "review this repo" / "look over this project"
- "Is this code any good?" / "What's wrong with this?"
- Pre-acquisition / due diligence / vendor handoff review
- Inheriting a legacy codebase
- Pre-launch security/quality checks
- Periodic health checks on an active project

If the user just wants a single function reviewed, that's a code review, not an audit — answer directly without this skill. Likewise, if the target is a diff or pull request rather than the whole repository, use the built-in code-review skill (or security-review for security checks on pending changes) instead of this one.

## Operating principles

1. **Breadth before depth.** First pass establishes scope and shape. Don't dive into individual files until you understand the whole.
2. **Severity-weighted output.** A leaked API key matters more than inconsistent indentation. Always sort findings by impact.
3. **Evidence over opinion.** Every finding cites a file and line. "This is bad" without a pointer is noise.
4. **Actionable remediation.** Each finding ends with what to do about it.
5. **Respect the budget.** A 50k-file monorepo can't be read exhaustively. Sample intelligently, document what was sampled.
6. **No false alarms.** Verify findings before reporting. A "vulnerability" that's actually safe-by-context destroys credibility.

## The audit workflow

Work through these phases in order. Don't skip Phase 1 — without inventory, later phases are guesswork.

### Phase 1: Inventory & Orientation

Goal: understand what you're auditing before judging it.

1. **Locate the root.** Confirm the path the user wants audited. If they just dropped a repo URL, clone it. If they uploaded files, locate the root directory.
2. **Run inventory.** Execute `scripts/inventory.sh <path>` to get a one-page overview: file counts by language, total LOC, presence of key files (README, LICENSE, lockfiles, CI configs, tests, Dockerfile).
3. **Read the README and package manifest.** This tells you the project's stated purpose, stack, and entry points. Note any divergence between what the README claims and what's in the tree.
4. **Identify the stack.** Language(s), framework(s), runtime, datastore(s), deployment target. The audit lens depends on this.
5. **Identify entry points.** `main.*`, `index.*`, `app.*`, `server.*`, route definitions, CLI handlers, cron entries, webhook handlers, public API endpoints. Audit attention follows control flow from these.
6. **Note red flags up front.** A `node_modules/` checked into git, a `.env` in version control, a `dist/` directory committed alongside source — these are skill-test problems. Flag them, but don't stop the audit; finish the inventory pass first.

Write a short orientation summary before moving on. Three to six sentences: "This is an X-stack Y, ~Z kLOC, primary entry points are A and B, deployment appears to target C, notable absences are D."

### Phase 2: Security pass

This is usually the most important phase — a security bug ships and harms users. See `references/security.md` for the full checklist. The high-leverage moves:

1. **Run `scripts/scan_secrets.sh <path>`.** Catches the easy wins: hardcoded API keys, AWS credentials, JWT secrets, database URLs with passwords, private keys.
2. **Trace user input to dangerous sinks.** For each entry point, ask: where does untrusted data go? Database queries (SQLi), shell commands (RCE), HTML output (XSS), file paths (traversal), deserialization, redirects (open redirect), eval-likes.
3. **Auth & authorization.** Who can call this endpoint? How is the session validated? Are there per-resource checks (IDOR), or just "is logged in"? Are admin routes gated?
4. **Cryptography.** MD5/SHA1 for passwords, hardcoded IVs, ECB mode, custom crypto, missing TLS verification, secrets in URLs. Most "we wrote our own crypto" is a finding.
5. **Dependencies with known CVEs.** See Phase 5 — but flag obviously-unmaintained packages here too.
6. **Configuration.** `DEBUG=true` in production paths, permissive CORS (`*` with credentials), missing security headers, exposed admin panels, default credentials.

### Phase 3: Code quality & maintainability

Quality issues don't break things today but make tomorrow expensive. See `references/quality.md`.

1. **Run `scripts/find_smells.sh <path>`.** Surfaces oversized files, deeply nested directories, TODO/FIXME/HACK/XXX markers, long functions (heuristic by line count), commented-out code blocks.
2. **Sample the largest 5–10 files.** Big files are usually big for a bad reason. Read them. Note: god objects, mixed responsibilities, dead code, copy-paste duplication.
3. **Error handling.** Empty catches (`catch (e) {}`), swallowed promises, `unwrap()` everywhere, panics in library code, errors logged but not handled, errors returned but not checked.
4. **Naming & readability.** Single-letter vars in non-trivial scopes, abbreviations only the original author understood, misleading names (function called `getX` that mutates), inconsistent conventions.
5. **Dead code.** Unreferenced exports, commented-out blocks older than a few months, feature flags that never flipped, "v2" implementations alongside "v1".

### Phase 4: Performance & scalability

Don't speculate. Look for the patterns that bite under real load. See `references/performance.md`.

1. **Database access patterns.** N+1 queries (loops issuing one query per iteration), missing indexes (look at WHERE/JOIN columns vs. schema), `SELECT *` on wide tables, missing pagination on list endpoints, transactions held open across network calls.
2. **Synchronous I/O on hot paths.** Blocking file reads in request handlers, sync HTTP calls without timeouts, unbounded retries.
3. **Memory.** Loading entire datasets into memory for streaming-shaped problems, leaks from listeners never removed, caches with no eviction.
4. **Caching.** Where it exists: is it correct (cache key collisions)? Where it's missing: hot-path computations that are deterministic and recomputed every request.
5. **Frontend specifics** (if applicable): bundle size, unbatched re-renders, images served unoptimized, render-blocking scripts.

### Phase 5: Dependencies & supply chain

Run `scripts/deps_check.sh <path>`. It detects the package manager and runs the appropriate audit (`npm audit`, `pip-audit`, `bundle audit`, `cargo audit`, `composer audit`, `go list -m -u all`).

Look for:
- **Known CVEs** in direct or transitive dependencies, especially anything HIGH/CRITICAL.
- **Stale dependencies** more than 2 major versions behind.
- **Unmaintained packages** (last commit >2 years on a security-relevant package).
- **Lockfile hygiene.** Lockfile present and committed? Matches the manifest? CI installs from lockfile (`npm ci`, not `npm install`)?
- **Dependency sprawl.** 800 dependencies for a CRUD app is a finding.
- **License compatibility** if the user cares (commercial projects pulling AGPL etc.).

### Phase 6: Architecture & design

Read `references/architecture.md` for what to look for. The big questions:

1. **Layering.** Is there separation between transport (HTTP), domain logic, and persistence? Or are SQL queries inline in route handlers?
2. **Coupling.** Modules that import from too many other modules; circular imports; shared mutable state.
3. **Boundaries.** Where does trust end? Where is input validated? Are internal modules treating external input as already-validated?
4. **Configuration.** Hardcoded values that should be config; config sprawl (twelve places to change one thing); environment-specific code paths (`if (env === 'prod')` scattered around).
5. **Concurrency model.** If concurrent: what's protecting shared state? Are locks held across I/O? Are there obvious race windows?

### Phase 7: Testing & CI hygiene

1. **Tests exist?** Locate the test directory. Count test files vs. source files — a rough ratio.
2. **What's covered?** Sample a few tests. Are they testing the happy path only? Are critical paths (auth, payments, data mutation) tested?
3. **Are tests run in CI?** Look for `.github/workflows`, `.gitlab-ci.yml`, `circle.yml`, `Jenkinsfile`. Verify the pipeline actually runs the tests, not just lints.
4. **Test quality.** Tests that mock everything (testing the mock, not the code), tests with no assertions, tests that always pass, snapshot tests with stale snapshots.
5. **Other CI checks.** Lint, format, typecheck, secret-scanning, dependency audit. Each absence is a finding.

### Phase 8: Documentation & operational readiness

Brief check, often surfaces real issues:

1. **README.** Can a new dev set up the project from the README alone? If not, what's missing?
2. **Setup/contribution docs.** Local dev setup, env vars list, how to run tests, how to deploy.
3. **API docs** (if it's an API).
4. **Runbooks/ops docs.** What happens when it breaks at 3am? Are there logs? Metrics? Health checks?
5. **License.** Present and appropriate?

### Phase 9: Compose the report

Use `assets/report-template.md` as the skeleton. The structure:

1. **Executive summary** (5–8 lines). Stack, scope audited, top 3 findings, overall health verdict.
2. **Findings table.** Every finding gets: ID, severity (Critical/High/Medium/Low/Info), category, title, file:line, one-line description.
3. **Detailed findings.** Each finding expanded with: what it is, why it matters, evidence (code excerpt + file:line), recommended fix, effort estimate (S/M/L).
4. **What's good.** Genuine strengths. Audits that only criticize get tuned out — the positive section calibrates and earns trust on the negatives.
5. **Recommended next steps.** A prioritized 30-60-90 day plan. The owner shouldn't have to re-prioritize your findings; you do that for them.

Severity guide:
- **Critical**: Active exploitation possible, data loss imminent, or production currently broken in a way the owner doesn't know about. Examples: hardcoded production credentials, SQLi in a public endpoint, RCE via deserialization.
- **High**: Real risk to security/availability/correctness, but requires conditions to trigger. Examples: missing auth on internal endpoint, N+1 on a hot path, dependency with known RCE CVE.
- **Medium**: Will cause incidents or pain at some point. Examples: no error handling on a critical path, no tests for payment logic, missing rate limits.
- **Low**: Quality issue, smell, or eventual-cost item. Examples: dead code, inconsistent style, missing types.
- **Info**: Observation, suggestion, or context. Not a defect.

Don't inflate severity. A linting issue is not Critical. Inflation makes the real Criticals invisible.

## Sampling for large codebases

If the repo is too big to audit exhaustively (rough threshold: >100k LOC or >2,000 source files), shift to sampling:

1. **Always-read.** README, package manifest, lockfile, CI config, all entry points, all auth/security-related modules, any file with "secret"/"key"/"password"/"auth"/"admin" in the path.
2. **Stratified sample.** From each top-level source directory, pick the 2–3 largest files plus 2–3 random files. Read those.
3. **Hotspot scan.** Use `git log --pretty=format:%n --name-only | sort | uniq -c | sort -rn | head -30` to find churned-most files. Read the top 10 — that's where bugs concentrate.
4. **State the sample explicitly** in the report so the owner knows what was and wasn't covered.

**Large repositories — parallelize.** Phases 2, 3, and 5 are independent of each other once Phase 1's inventory exists. On repos over ~100k LOC, delegate them to parallel subagents (one per phase) and merge their findings in Phase 9.

## Working with what's available

The skill works in any environment Claude can run, but tooling varies:

- **Claude Code / code execution available**: run the bundled scripts directly, run language-native tools (`npm audit`, `eslint`, `bandit`, `semgrep` if installed), produce a real LOC count, etc.
- **Read-only / no shell**: walk the file tree by reading directories, do the security/quality passes by reading files, skip the script-driven inventory and produce a qualitative orientation summary instead. The methodology still works; the mechanical scripts just become manual.

If a script fails (missing tool, permission denied, timeout), proceed without it and note in the report that automated checks were limited. Don't abort the audit because one tool isn't available.

## Reference files

Load these as needed; they go deeper than this overview:

- `references/security.md` — full security checklist organized by attack class, with language-specific examples
- `references/quality.md` — quality smells, complexity heuristics, maintainability checks
- `references/performance.md` — performance anti-patterns by layer (DB, network, memory, frontend)
- `references/dependencies.md` — supply-chain checks, lockfile hygiene, package-manager-specific commands
- `references/architecture.md` — layering, coupling, boundary, and design-pattern observations
- `references/language-notes.md` — language-specific gotchas (JS/TS, Python, PHP, Go, Ruby, Java)

## Scripts

Located in `scripts/`. All are bash, expect a single argument (path to the codebase root):

- `inventory.sh` — one-page overview of size, languages, key files
- `scan_secrets.sh` — regex-based search for common credential patterns
- `find_smells.sh` — TODO/FIXME markers, oversized files, suspicious patterns
- `deps_check.sh` — auto-detects the package manager and runs its audit command

## Final reminders

- An audit is a service to the owner. Be honest, be specific, be useful.
- Findings with no remediation aren't findings, they're complaints.
- If something looks bad but you can't be sure without runtime context, say so. "This *looks like* an N+1; needs verification with a query log" is more honest than asserting it.
- Earn the negatives by acknowledging the positives. No codebase is all bad; saying so signals you actually read it.
