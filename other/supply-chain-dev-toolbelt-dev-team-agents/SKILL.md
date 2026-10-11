---
name: supply-chain
description: Supply chain security — dependency audit, CI pinning, typosquatting.
---

# Supply Chain Attack Prevention

Supply chain attacks compromise software by injecting malicious code into dependencies, build tools, or CI/CD pipelines — not the application itself.

---

## Attack Vectors

| Vector | Example | Risk |
|--------|---------|------|
| Malicious npm/PyPI/Composer package | `lodash` vs `lodahs` (typosquatting) | Code execution at install time |
| Compromised dependency account | Maintainer takeover → malicious version | All consumers affected |
| Unpinned CI/CD action | `uses: actions/checkout@main` | Attacker pushes to `main` → runs in your CI |
| Dependency confusion | Private package name leaked; public registry serves malicious version | Pulled over private package |
| Build script injection | `postinstall` script in `package.json` | Runs arbitrary code on developer machines |

---

## CI/CD Action Pinning

**Never reference actions by branch or tag — always pin to a full commit SHA.**

```yaml
# BAD — tag can be moved or deleted
- uses: actions/checkout@v4

# GOOD — SHA is immutable
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

Audit rule: any `uses:` line not ending in a 40-character SHA is a `[HIGH]` finding.

**Allowed exceptions**: actions owned and controlled by your own organization (internal actions).

### Pinning tools
```bash
# pin-github-action (CLI)
pin-github-action .github/workflows/*.yml

# Renovate / Dependabot: configure to auto-update pinned SHAs
```

---

## Dependency Auditing

Run on every PR and in CI:

```bash
# Node.js
npm audit --audit-level=high
npx better-npm-audit audit

# Python
pip-audit
safety check

# PHP
composer audit

# Ruby
bundle audit

# Go
govulncheck ./...

# All-language scanner
trivy fs .
snyk test
```

**Rules:**
- CRITICAL or HIGH CVEs in direct dependencies: block merge
- CRITICAL CVEs in transitive dependencies: flag and track; block if exploitable via this app's code path
- No dependency should have `postinstall`/`prepare` scripts from an unknown/unreviewed maintainer

---

## Lock File Verification

| Check | Why |
|-------|-----|
| `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` committed and up to date | Guarantees reproducible installs |
| `composer.lock`, `Pipfile.lock`, `Gemfile.lock`, `go.sum` committed | Same guarantee |
| CI installs with `--frozen-lockfile` / `ci` / `--no-update` flag | Prevents silent dependency upgrades in CI |
| Lock file diff reviewed in PRs touching `package.json` | Catches unexpected transitive upgrades |

```bash
# Node — fail if lock file is out of sync
npm ci                         # equivalent to --frozen-lockfile
yarn install --frozen-lockfile
pnpm install --frozen-lockfile

# Python
pip install --require-hashes -r requirements.txt
```

---

## Typosquatting Detection

Before adding any new dependency, verify:

1. Check exact spelling against the official registry page
2. Confirm maintainer identity and publish history
3. Check download count anomalies (newly published package with suspiciously high installs)
4. Run `npm pack <package>` locally and inspect contents before installing in CI

```bash
# Node: inspect what a package actually contains
npm pack lodash --dry-run

# Check package metadata
npm info lodash | grep -E "(maintainers|dist-tags|time)"
```

**Red flags:** package published < 30 days ago, < 100 weekly downloads but claims popularity, no source repo link, `postinstall` script present.

---

## Dependency Confusion

Occurs when an attacker publishes a public package with the same name as your internal/private package.

**Mitigations:**
- Use scoped packages for all internal deps: `@yourorg/package-name`
- Configure your package manager to always resolve `@yourorg/*` from your private registry only
- Never publish internal package names to public registries, even as empty placeholders

```bash
# npm .npmrc — always fetch org packages from private registry
@yourorg:registry=https://your-private-registry.com
```

---

## SBOM (Software Bill of Materials)

Generate and store an SBOM for every production release:

```bash
# CycloneDX format (standard)
npx @cyclonedx/cyclonedx-npm --output-file sbom.json
syft . -o cyclonedx-json > sbom.json

# Attach to GitHub Release or store in artifact registry
```

---

## Review Checklist

| Item | Severity if missing |
|------|---------------------|
| All CI actions pinned to SHA | HIGH |
| Lock files committed and used in CI with frozen flag | HIGH |
| No unreviewed `postinstall` scripts | HIGH |
| Dependency audit runs in CI | HIGH |
| Scoped packages for all internal deps | MEDIUM |
| SBOM generated on release | LOW |
| Renovate/Dependabot configured for SHA updates | LOW |
