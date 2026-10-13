---
name: web-dependency-confusion
description: >
  Dependency confusion / substitution — publish a malicious public package matching an internal
  name so build systems pull yours. Load on leaked internal package names (npm/PyPI/RubyGems/Maven),
  package.json/requirements with unknown deps, or private-registry setups. Signals: @scope/internal
  packages, non-public dep names in manifests, .npmrc/registry config leaks.
domain: web
type: technique
stability: learning
modes: [bugbounty, pentest]
severity: critical
owasp: [A08:2021-Software-and-Data-Integrity-Failures]
cwe: [CWE-427, CWE-1357]
mitre: [T1195.001]
tools: [npm, pip]
schema_version: 1
---

# Dependency confusion

## When it applies
The target builds software using **internal package names** that aren't published publicly, on an
ecosystem (npm, PyPI, RubyGems, Maven, NuGet) where a public registry is also consulted. If you can
learn an internal name and publish it publicly, their resolver may fetch **your** package → RCE in their build/CI.

## Why it works
Many package managers, misconfigured, prefer the *highest version* across all configured registries
— public included. Publishing `internal-lib@99.0.0` to the public registry can outrank the private
`internal-lib@1.2.3`, so builds pull and execute your code (install scripts run automatically).

## Method
1. **Harvest internal names**: leaked `package.json`/`requirements.txt`/`pom.xml`, source maps and
   JS bundles (→ `recon-js-analysis`), error messages, public repos, `.npmrc`/registry config.
2. **Confirm the name is unclaimed** on the public registry (npm/PyPI/etc.).
3. **Publish a benign PoC package** under that exact name with a high version, whose install/postinstall
   step makes an **OOB callback** (DNS/HTTP to your collaborator) including hostname/user — *no
   destructive payload*. This proves execution if their build pulls it.
4. **Wait for the callback** from their build/CI environment → confirms confusion.
5. **Scoped packages**: `@company/pkg` on npm needs the scope unclaimed; note the config that would prevent it.

## Gotchas
- Keep the payload benign and identifiable (your marker only) — you're proving exec, not attacking. Mind program RoE (many bug-bounty programs have specific rules for this).
- Proper configs (scoped registries, `--registry` pinning, namespace ownership) prevent it — the finding is the *missing* control.
- Take down the package after reporting.

## Verify success
An OOB callback from the target's build/CI proving your public package was resolved and its code executed.

## References
Alex Birsan "Dependency Confusion"; npm/PyPI scoping & registry-pinning docs.
