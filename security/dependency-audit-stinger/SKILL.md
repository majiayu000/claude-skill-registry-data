---
name: "dependency-audit-stinger"
description: "Audit dependencies for the target repository's ecosystem: lockfiles, vulnerability triage, SBOM and provenance. Use for supply-chain or publish safety; Hivemind is a worked npm example."
license: AGPL-3.0-or-later
---

# dependency-audit Stinger

Procedural arsenal for `dependency-audit-wasp-drone`. Start with the target repository's real ecosystem, package manager, lockfiles, dependency graph and publish boundary. The retained `@deeplake/hivemind` material is a worked npm case; its tree-sitter scripts, npm lockfile and OpenClaw publish guards are not requirements for other repositories.

**First action when this stinger is loaded:** Read [Target repository audit](guides/05-target-repository-audit.md). Inventory current source and authorized scope before selecting ecosystem-specific methods. Then consult the retained guides only where their case facts match the target and verify any vendor/version claim against current primary documentation.

## Preserved Hivemind case facts (not target ground truth)

`@deeplake/hivemind` is an ESM, TypeScript ^6, Node `>=22` npm package. The supply-chain facts that matter:

- **Lockfile:** `package-lock.json` (npm - NOT pnpm or yarn). CI installs with `npm ci`.
- **Runtime deps:** `deeplake`, `@modelcontextprotocol/sdk`, `@anthropic-ai/sdk`, `zod`, `js-yaml`, `just-bash`, `yargs-parser`.
- **optionalDependencies + native ABI risk:** `@huggingface/transformers` plus the full tree-sitter grammar set (c/cpp/go/java/javascript/python/ruby/rust/typescript). Three grammars are version-pinned in `overrides` (`tree-sitter-c`, `tree-sitter-python`, `tree-sitter-rust`). The `postinstall` hook runs `scripts/ensure-tree-sitter.mjs`, which heals native ABI / arm64 build failures. This native-dependency surface is the single biggest supply-chain risk on this package - a compromised or broken grammar build runs install-time code on every consumer's machine.
- **Publish guards:** `prepack` builds; the `files` allowlist controls what ships; `scripts/pack-check.mjs` (`npm run pack:check`) blocks publishing secrets; `scripts/audit-openclaw-bundle.mjs` (`npm run audit:openclaw`) replicates ClawHub's static scan of the OpenClaw bundle.
- **CI:** `.github/workflows/` - `ci.yaml` runs a cross-node install; `codeql.yaml` scans `javascript-typescript`. CodeRabbit profile is `chill`.

---

## When this stinger applies

Load this stinger when `dependency-audit-wasp-drone` is invoked. Typical triggers:

- "Set up Renovate for Hivemind / Renovate vs Dependabot for this repo"
- "Our dependency-update PRs are noisy"
- "npm audit returns findings - help me triage"
- "npm audit shows clean but I don't trust it"
- "The tree-sitter postinstall is failing / is it safe?"
- "We need an SBOM for the published package"
- "Generate an SBOM and attest it in CI"
- "Set up socket.dev to catch malicious packages"
- "Should we publish with --provenance?"
- "Is our npm publish safe? / what guards the published bundle?"
- "package-lock.json keeps changing unexpectedly"
- "Explain package.json and lockfiles to me"
- "Which dependencies are direct or indirect?"
- "Tie our SBOM to the exact release artifact"
- "Upgrade this major dependency without hiding breaking changes"

Do NOT load it for:

- Application-code CVEs requiring code changes -> `security-wasp-drone`
- Container image scanning -> `ci-release-wasp-drone`
- License compatibility legal opinions -> legal counsel
- CI/CD pipeline architecture beyond the dependency scanning step -> `ci-release-wasp-drone`

---

## Critical directives

These are the non-negotiables. The full rationale lives in each guide.

- **Never recommend ignoring a CVE without requiring an expiry date and a tracking issue link.** See `guides/01-vulnerability-triage.md`.
- **Always differentiate direct vs transitive exposure before recommending an upgrade.** Most `npm audit` findings on this package are transitive and unreachable. See `guides/01-vulnerability-triage.md`.
- **Identify the target's actual install-time execution risks.** In the Hivemind case, tree-sitter/optionalDependencies and `scripts/ensure-tree-sitter.mjs` were relevant; preserve those controls only if the inspected target actually has them. See `guides/01-vulnerability-triage.md` and `guides/03-lockfile-discipline.md`.
- **Choose an update tool from the target's requirements.** The retained Hivemind case preferred Renovate; grouping alone does not rule out Dependabot, which also supports grouped updates. See `guides/00-scanner-decision-matrix.md`.
- **Validate the target's actual lockfile and frozen-install procedure after a dependency change.** Use `package-lock.json`/`npm ci` only for an npm target; do not replace pnpm, Yarn, uv, Cargo or Go tooling with this example. See `guides/03-lockfile-discipline.md`.
- **Do not gate CI on `low`/`moderate` `npm audit` findings.** Gate only on `high` and `critical`. See `guides/01-vulnerability-triage.md`.
- **Preserve and check the target's existing publish guards.** The `files` allowlist, `pack-check.mjs`, and `audit:openclaw` belong to the retained Hivemind case; do not invent those scripts in another target. See `guides/04-provenance-verification.md`.
- **Defer to `security-wasp-drone` for any CVE that requires patching application code, not just upgrading a package.**

---

## Retained npm case toolchain (recheck current vendor behavior)

| Tool | Role for this package | Limit |
|---|---|---|
| **npm audit** | CVE compliance baseline, zero-config, built into the `npm ci` toolchain | Does not catch supply-chain attacks without a CVE (axios-style account hijack, tree-sitter build tampering) |
| **Renovate** | Grouped update PRs + `minimumReleaseAge` delay; right fit for this single-package npm repo | More config than Dependabot; needs a `renovate.json` |
| **Dependabot** | GitHub-native update PRs with configurable groups | Compare the target's ecosystem, update-delay and grouping requirements against current documentation |
| **socket.dev** | Behavioral threat intel for npm: typosquatting, malicious install scripts, account takeover - the control for the tree-sitter postinstall risk | Not a CVE scanner; complements npm audit, does not replace it |
| **Snyk (optional)** | Richer CVE DB + reachability + IDE integration for npm | Paid tiers for some features; npm audit + socket.dev cover the baseline |
| **Syft + CycloneDX** | SBOM for the published npm package in CycloneDX 1.6 JSON; CI-ready with Sigstore attestation | Does not scan vulnerabilities; pairs with Grype for that |
| **npm `--provenance`** | Sigstore-backed provenance on publish; verifiable with `npm audit signatures` | Transport guarantee only - does not vouch for source-code trust |

> **Key 2026 insight:** `npm audit` is a CVE compliance tool, not a supply-chain security tool. The March 2026 axios maintainer account hijack published a backdoor in 40 minutes with no CVE at time of attack - `npm audit` showed clean throughout. For this package the equivalent nightmare is a tampered tree-sitter grammar running install-time code via `postinstall`. socket.dev behavioral analysis and Renovate `minimumReleaseAge` are the controls that address this class. See `research/external/04-npm-provenance-sigstore-2026.md` (source-repository research, not shipped with the plugin).

---

## Guide map

Read the guide matching your task:

| Task | Guide |
|---|---|
| Identify target ecosystem, lockfiles, checks and permission boundaries | `guides/05-target-repository-audit.md` |
| Explain actual manifests and lockfiles to a beginner | `guides/06-explain-manifest-and-lockfile.md` |
| Pick tooling for a target that matches the retained npm case | `guides/00-scanner-decision-matrix.md` |
| Triage an `npm audit` finding (noise vs real, native-dep risk) | `guides/01-vulnerability-triage.md` |
| Qualify exact release artifact inventory and SBOM binding | `guides/07-bind-sbom-to-release-artifact.md` |
| Prepare a bounded major upgrade with baseline/candidate contracts | `guides/08-upgrade-major-dependency-safely.md` |
| Retained published-package SBOM case | `guides/02-sbom-workflow.md` |
| Harden `package-lock.json` + tree-sitter discipline | `guides/03-lockfile-discipline.md` |
| Verify npm provenance + the publish-time guards | `guides/04-provenance-verification.md` |

---

## Template map

| Template | Use case |
|---|---|
| `templates/renovate-base-config.json` | Drop-in Renovate config for this npm repo: grouping, `minimumReleaseAge`, automerge for devDependencies, and a guarded rule for the pinned tree-sitter grammars |
| `templates/github-actions-sbom-workflow.yml` | SBOM generation + Sigstore attestation for the published `@deeplake/hivemind` tarball on tag push |
| `templates/release-artifact-evidence.md` | Artifact/graph coverage, schema, subject, signature and identity evidence |
| `templates/major-upgrade-evidence.md` | Exact versions, consumer contracts, canary and rollback proof |
| `templates/manifest-reading-ledger.md` | Preserve declarations, recorded graph edges and unproved runtime/security facts; see [worked fixture](examples/read-manifest-fixture.md) |
| `templates/dependency-triage-report.md` | Markdown template for recording an `npm audit` triage pass on this package |

---

## Folder layout

```text
dependency-audit-stinger/
+- SKILL.md                                   (this file)
+- README.md                                  (one-page human overview)
+- guides/
|  +- 00-scanner-decision-matrix.md           (Renovate vs Dependabot + npm audit + socket.dev for this package)
|  +- 01-vulnerability-triage.md              (npm audit noise vs real, direct vs transitive, tree-sitter native-dep risk)
|  +- 02-sbom-workflow.md                     (Syft + CycloneDX 1.6 + Sigstore for the published tarball)
|  +- 03-lockfile-discipline.md               (npm ci + package-lock.json + minimumReleaseAge + optionalDependencies pins)
|  +- 04-provenance-verification.md           (npm --provenance + audit signatures + files allowlist / pack-check / audit-openclaw / CodeQL)
+- examples/
|  +- happy-path-node-scanner-setup.md        (Renovate + npm audit + socket.dev for @deeplake/hivemind)
|  +- edge-case-critical-cve-triage.md        (triaging a transitive CVE pulled through a Hivemind dependency)
+- templates/
|  +- renovate-base-config.json               (ready-to-use Renovate config for this repo)
|  +- github-actions-sbom-workflow.yml        (SBOM + attestation workflow)
|  +- dependency-triage-report.md             (npm audit triage report template)
+- reports/
|  +- README.md                               (how audit reports accumulate)
+- research/                                  (DO NOT MODIFY -- owned by scripture-historian)
   +- research-plan.md
   +- research-summary.md
   +- index.md
   +- internal/01-command-brief.md
   +- external/ (5 source files)
```

---

## Pairing

| Role | Artifact |
|---|---|
| This stinger | `.` |
| Paired Drone | `../../agents/dependency-audit-wasp-drone.md` |

---

*Forged by `stinger-forge`, retargeted to the `@deeplake/hivemind` npm package. Part of The Wasp Nest, curated by [Mario Aldayuz a.k.a @thenotoriousllama](https://github.com/thenotoriousllama).*
