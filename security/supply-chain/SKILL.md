---
name: supply-chain
description: Detects supply-chain risks in dependency manifests, lockfiles, install
  commands, and CI pipelines — missing lockfiles, absent vulnerability scanners,
  unverified installs, install hooks that pipe remote content to a shell, and
  AI-hallucinated package names. Use when writing package install commands,
  dependency manifests, CI/CD configs, build scripts, or code that loads
  external packages.
---

# Supply Chain Security Check (A03:2025)

## What this checks

Most exploited supply-chain incidents come from *not updating fast enough* (sitting
on known-CVE versions) and from *unverified installs* (curl-to-shell, typosquats,
install hooks). Aggressive exact-pinning is no longer the right default — it traps
you on vulnerable releases. Lockfiles + scanners + auto-merge of patches is.

## Vulnerable patterns

- No lockfile committed alongside the manifest — builds aren't reproducible and you can't tell when a dependency moved
- CI install command silently re-resolves instead of failing on lockfile drift (`npm install` vs `npm ci`, `pip install` vs `pip install --require-hashes`, `bundle install` vs `bundle install --frozen`)
- No automated dependency-update bot, or one that doesn't auto-merge passing PRs — sitting on known-vulnerable versions
- No vulnerability scanner in CI, or a scanner whose findings do not fail the build
- Direct dependencies pinned to exact versions with no auto-update path — strands you on known-CVE releases
- Installs from arbitrary git refs, tarball URLs, or local paths with no integrity guarantee
- Install hooks, build scripts, or CI steps that pipe remote content into a shell — `curl | bash`, `wget | sh`, `iwr | iex`
- AI-generated manifests with hallucinated package names attackers can claim (slopsquatting)

## Fix immediately

Flag the issue, explain the risk, and suggest a fix. Translate to the package
manager and CI system of the audited file.

1. **Direct dependencies use a range that accepts patches and minors automatically** (npm caret, Python `~=`, Ruby `~>`, Cargo's default caret). Patches are nearly always security fixes; an exact pin means a CVE sits in your build until someone clicks "bump." Exact pins only for documented known-incompatibility cases.
2. **A lockfile is committed** that records resolved transitive versions with content hashes. Reproducibility lives here, not in the manifest.
3. **CI installs with a frozen-lockfile command** that fails on lockfile-manifest drift.
4. **A dependency-update bot runs on a schedule** (Renovate, Dependabot), opens PRs for patches and minors, and auto-merges after tests + scanner pass. This is how patches reach production fast enough to matter.
5. **A vulnerability scanner runs in CI and fails the build on high-severity findings.** Advisory-only scanners do not gate.
6. **No install hook, build script, or CI step pipes remote content into a shell.**
7. **AI-suggested or unrecognized package names are verified in the registry before install** — slopsquatted typosquats are a growing vector in AI-generated manifests.

## Verification

- [ ] Direct dependencies use a range that auto-accepts patches and minors; exact pins only for documented known-incompatibility cases
- [ ] A lockfile is committed with resolved transitive versions and content hashes
- [ ] CI installs with a frozen-lockfile command that fails on drift
- [ ] A dependency-update bot is configured and auto-merges patches and minors after tests and scanner pass
- [ ] A vulnerability scanner runs in CI and fails the build on high-severity findings
- [ ] No install hooks, build scripts, or CI steps pipe remote content into a shell
- [ ] Any AI-generated or unrecognized package names are flagged for registry verification before install

## References

- CWE-1395 ([Dependency on Vulnerable Third-Party Component](https://cwe.mitre.org/data/definitions/1395.html))
- CWE-506 ([Embedded Malicious Code](https://cwe.mitre.org/data/definitions/506.html))
- [OWASP A03:2025 Vulnerable and Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)
