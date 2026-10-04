---
name: orbit-sec-supply-chain
description: Supply-chain security audit — Composer + npm dependency CVE check, license compatibility (GPL-compatible only), abandoned package detection, typosquatting risk, lockfile integrity, post-install / preinstall scripts that smell like supply-chain attacks. Use when the user says "supply chain audit", "dependency CVE", "composer audit", "npm audit", "vendor security".
---

# 🪐 orbit-sec-supply-chain — Dependency supply-chain audit

A plugin is only as secure as its weakest dependency. This skill audits everything in `vendor/` and `node_modules/`.

---

## Quick start

```bash
# Composer side
cd ~/plugins/my-plugin && composer audit

# npm side
cd ~/plugins/my-plugin && npm audit

# Plus Orbit's deeper analysis
bash ~/Claude/orbit/scripts/supply-chain-audit.sh ~/plugins/my-plugin
```

---

## What this skill checks

### 1. Known CVEs in dependencies
```bash
composer audit --format=json | jq '.advisories'
npm audit --json | jq '.vulnerabilities'
```

Cross-referenced with:
- [GitHub Security Advisory DB](https://github.com/advisories)
- [Snyk DB](https://snyk.io/vuln)
- [PHP Security Advisories](https://github.com/FriendsOfPHP/security-advisories)

### 2. License compatibility (GPL-only for WP plugins)
**Whitepaper intent:** WP.org requires GPL-compatible. AGPL, BUSL, proprietary licenses break that. Auditor flags any non-compatible.

Compatible: GPL-2.0+, MIT, Apache-2.0 (permissive), BSD, LGPL.
Incompatible: AGPL, BUSL, proprietary, CC-NC, "must contact author."

### 3. Abandoned packages
```
A package is "abandoned" if:
- last commit > 2 years ago
- repository archived / 404
- composer.json has "abandoned: true"
- npm registry shows "deprecated"
```

Abandoned = no security patches → ticking time bomb.

### 4. Typosquatting risk
A dependency named `lodaash` (with double-a) is suspicious. Auditor checks Levenshtein distance from popular packages.

### 5. Post-install / preinstall scripts (npm)
```json
{
  "scripts": {
    "postinstall": "node ./postinstall.js"  ← red flag — review the script
  }
}
```

A malicious `postinstall.js` can exfiltrate secrets. Audit forces review.

### 6. Lockfile integrity
- `composer.lock` matches `composer.json`?
- `package-lock.json` matches `package.json`?
- All hashes verified?

```bash
composer install --dry-run
npm ci  # fails if lockfile-package mismatch
```

### 7. Direct GitHub dependencies (no version pinning)
```json
"dependencies": {
  "some-pkg": "github:user/repo"  ← no version, no integrity hash
}
```

→ Pin to a specific commit hash + verify hash on every install.

---

## Output

```markdown
# Supply Chain Audit — my-plugin

## Composer (15 packages)
- ✓ All GPL-compatible
- ❌ guzzlehttp/guzzle 6.5.5 — CVE-2024-XXXX (HIGH) — upgrade to 7.x
- ⚠ symfony/polyfill-iconv — abandoned (last release 18 months ago)

## npm (1,247 packages incl. transitive)
- ⚠ 14 vulnerabilities (3 HIGH, 11 LOW)
   `npm audit fix` resolves 9
- ❌ Package "lodahs" (note typo) found — looks like lodash typosquat. Investigate.
- ⚠ postinstall script in `node-pre-gyp` — common but read it
- ❌ Package `xyz-utils` — repo 404 (deleted from GitHub)

## Lockfile
- ✓ composer.lock matches composer.json
- ❌ package-lock.json out of sync with package.json — npm ci will fail

## Recommendation
1. `composer require guzzlehttp/guzzle:^7.0` — fixes critical
2. Investigate "lodahs" typo (likely safe but verify)
3. Remove `xyz-utils` (its repo is deleted)
4. `npm install` to refresh lockfile
```

---

## Pair with

- `/orbit-zip-hygiene` — vendor/ in release zip
- `/orbit-sec-secrets-leak` — secrets in lockfiles
- `/orbit-cve-check` — Orbit's own CVE feed

---

## Sources & Evergreen References

### Canonical docs
- [GitHub Advisory Database](https://github.com/advisories) — root vuln DB
- [composer audit](https://getcomposer.org/doc/03-cli.md#audit) — built-in
- [npm audit](https://docs.npmjs.com/cli/v10/commands/npm-audit) — built-in
- [Snyk Vulnerability DB](https://snyk.io/vuln) — alt source
- [Socket.dev](https://socket.dev/) — supply-chain risk scoring
- [PHP FIG Security Advisories](https://github.com/FriendsOfPHP/security-advisories)

### Rule lineage
- composer audit (built-in) — Composer 2.4+ (2022)
- Supply-chain attacks (xz-utils, event-stream) — broad awareness since 2021

### Last reviewed
- 2026-04-29 — supply-chain landscape evolves daily
