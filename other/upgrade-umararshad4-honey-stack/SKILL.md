---
name: upgrade
description: "Safely upgrade dependencies, patch a CVE, or handle a breaking change or runtime EOL. Use for dependency bumps, audits (osv-scanner/npm audit), vulnerable transitive deps, framework codemods, or lockfile hygiene."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "honey-stack research 2026-10-18 (Renovate/Dependabot, osv-scanner v2, uv/pip-audit, React 19 codemods, Node EOL). Details in references/."
---

# upgrade

Move dependencies forward without breaking the build or shipping a regression. Upgrade debt compounds, so stay current — but one careful step at a time.

## Safe workflow
1. **Read first** — the changelog, release notes, and `UPGRADING.md`/migration guide before touching anything. Check `BREAKING CHANGES`.
2. **One major dependency per PR.** Never batch unrelated majors — you lose the ability to bisect a failure. Patch/minor can be grouped.
3. **Gate each step** with the full test suite + typecheck + lint + build. Green before the next bump.
4. **Small, revertible PRs.** Majors solo.
5. **Lockfile discipline** — commit it, regenerate deterministically, review its diff.

## Tools
- **Node:** `npm/pnpm outdated` and `npm/pnpm audit` (report); `npm-check-updates` (`ncu -u`, `--target minor`) to move ranges deliberately.
- **Automation:** **Renovate** (`renovate.json`, fine-grained `packageRules`, built-in `automerge`, multi-platform, dependency dashboard, stability-days) is the stronger choice; **Dependabot** (`.github/dependabot.yml`) is GitHub-native and zero-setup but needs an Actions workflow for automerge. Common policy: automerge patch/minor devDeps after tests + stability-days; majors always manual.
- **Python:** `uv` (`uv lock --upgrade`, `uv sync --frozen`); `pip-audit` (OSV, fails CI on findings). Dependabot supports `uv` but won't widen a pinned range.
- **Rust:** `cargo update`, `cargo upgrade` (cargo-edit), `cargo audit`. **Go:** `go get -u`, `go list -m -u all`, `govulncheck` (reachability-aware).

## CVE / vuln patching
Read the advisory (GHSA/OSV/NVD): affected range, fixed version, CVSS score + vector (network-reachable? privileges?). **Is it reachable** — does your code call the vulnerable path? Use reachability tools (`govulncheck`, `osv-scanner` v2 with call analysis) to prioritize, not to declare "safe forever". **Transitive dep** you can't wait on the parent to fix → force a patched version: npm `"overrides"`, pnpm `"pnpm.overrides"`, yarn `"resolutions"`, Cargo `[patch]`, Go `replace`, Python pinned constraint. Scan lockfiles with `osv-scanner scan -r .`; generate an SBOM (CycloneDX/SPDX via `syft`) for audit. `references/vulns.md`.

## Breaking changes, codemods, EOL
Semver is a promise authors sometimes break — pin-and-test critical deps, don't auto-trust ranges. Use the **framework's official codemod** (jscodeshift-based) for mechanical changes but expect it to miss peer-dep conflicts and library-level usage. React 19: bridge via 18.3.1 first (surfaces warnings), then `npx codemod react/19/migration-recipe` + `types-react-codemod preset-19`. Next.js: `npx @next/codemod upgrade latest`. **Runtime EOL gets no security patches** — Node 18 (EOL Apr 2025) and 20 (EOL Apr 2026) are past/near; target 22 or 24. Upgrade off EOL for the security feed alone. `references/breaking-changes.md`.

## Lockfile hygiene
Commit lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `uv.lock`, `Cargo.lock` for apps, `go.sum`). **CI uses frozen installs** — `npm ci`, `pnpm install --frozen-lockfile`, `uv sync --frozen`, `cargo build --locked` — so it fails on drift. Dedupe (`npm/pnpm dedupe`). Libraries publish permissive ranges (`^1.2.0`, never `*` or exact); applications pin via the committed lockfile.

## Decision rules
- **Upgrade now:** a reachable/high-CVSS CVE, a runtime/dep near EOL, a needed feature/fix, or a widening version gap.
- **Hold:** no security driver, a brand-new major still shaking out `.0` bugs (use stability-days), or a release freeze.
- **Roll back a bad upgrade:** revert the PR and restore the previous lockfile (`git revert`; `git checkout <prev> -- package-lock.json && npm ci`) — deps are reversible because the lockfile is versioned.

## Confirm before (never on your own)
A major framework/runtime bump; a change touching auth/crypto/payments; an `override`/`resolution` forcing a transitive version the parent doesn't sanction; automerging a non-patch into production code.

Done when: the chosen upgrades are applied one-major-per-PR, the full test/typecheck/build is green, the lockfile is committed, any forced transitive override is noted, and risky bumps were confirmed with the user.
