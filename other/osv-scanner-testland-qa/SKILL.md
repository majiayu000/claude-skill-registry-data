---
name: osv-scanner
description: "Configures and runs Google OSV-Scanner - open-source SCA against the OSV.dev vulnerability database; supports `osv-scanner scan -r ./` recursive scan + per-lockfile scan via `-L package-lock.json`; SBOM input (CycloneDX / SPDX) for non-standard package managers; `--format json|sarif|markdown|vertical|html` output; suppressions via `osv-scanner.toml` config. Use when the team needs OSS-native SCA without commercial-license overhead, or wants a second-opinion DB pair with Snyk's commercial DB."
---

# osv-scanner

[osv-usage]: https://google.github.io/osv-scanner/usage/

## When to use

- Team prefers OSS tooling over commercial Snyk.
- Layered SCA strategy - pair with `snyk-test`
  for cross-DB consensus signal.
- Custom package manager produces SBOMs not natively supported;
  feed SBOM directly to OSV-Scanner.
- Lightweight CI gate without commercial-license setup.

## Step 1 - Install

Per [osv-usage][osv-usage]:

```bash
docker pull ghcr.io/google/osv-scanner:latest
```

Other install paths (consult google.github.io/osv-scanner for
current options per platform):

```bash
# Go install
go install github.com/google/osv-scanner/cmd/osv-scanner@v1

# Homebrew
brew install osv-scanner

# Direct binary download from github.com/google/osv-scanner/releases
```

## Step 2 - Basic recursive scan

Per [osv-usage][osv-usage]:

```bash
osv-scanner scan -r ./my-project-dir/
```

Auto-detects manifest files (package-lock.json, Pipfile.lock,
go.mod, Cargo.lock, etc.) and queries OSV.dev for each.

Per-lockfile scan (`-L` targets one lockfile without recursing, useful in
monorepos):

```bash
osv-scanner scan -L package-lock.json --output-file scan-results.txt
```

## Step 3 - Output formats

Per [osv-usage][osv-usage]: `--format json` and `--format=vertical`
and `--format=html` are referenced. Full format list per the
osv-scanner documentation:

| Format | Use |
|---|---|
| `--format json` | For downstream aggregation |
| `--format sarif` | GitHub Code Scanning upload |
| `--format markdown` | PR comments |
| `--format vertical` | Default human-readable |
| `--format html` | Standalone report |

## Step 4 - SBOM-driven scanning

For projects with custom build systems that emit SBOMs but lack
natively-parsed lockfiles:

```bash
osv-scanner scan --sbom my-app.cyclonedx.json
osv-scanner scan --sbom my-app.spdx.json
```

This composes with `syft-generation` - Syft generates the SBOM,
OSV-Scanner queries OSV.dev against it.

## Step 5 - `osv-scanner.toml` config

Suppress a vuln with an expiring, reasoned entry (auditable in git):

```toml
# osv-scanner.toml
[[IgnoredVulns]]
id = "CVE-2024-1234"
ignoreUntil = 2026-12-15T00:00:00Z
reason = "Reachability confirms unreachable; tracked in JIRA-1234"
```

The full schema (`[[PackageOverrides]]`, multi-entry config, `--config` flag,
the mandatory justification template) is in
[references/osv-scanner-config-and-ci.md](references/osv-scanner-config-and-ci.md).

## Step 6 - False-positive triage (MANDATORY)

Suppress via `[[IgnoredVulns]]` (per-CVE, with `ignoreUntil`) or
`[[PackageOverrides]]` (per pinned package + ecosystem) in `osv-scanner.toml`;
`--severity-threshold` is a scan-time filter, not a suppression. Every entry
carries a mandatory reason + approver + re-review date. `ignoreUntil` is
enforced - past-due ignores re-surface in the scan results. The
suppression-layer table and justification template are in
[references/osv-scanner-config-and-ci.md](references/osv-scanner-config-and-ci.md).

## Step 7 - Exit codes + CI gating

OSV-Scanner exit codes (verify against current docs):

- 0 - no vulnerabilities found
- 1 - vulnerabilities found
- 127 - config error

The `google/osv-scanner-action` GHA (Docker invocation + SARIF upload) is in
[references/osv-scanner-config-and-ci.md](references/osv-scanner-config-and-ci.md).

## Step 8 - License-checking (adjacent feature)

OSV-Scanner has experimental license-summary support:

```bash
osv-scanner --experimental-licenses-summary scan -r .
```

For full license-compliance + scanning, pair with `sbom-formats`
or use a dedicated tool like ScanCode / FOSSology.

## Anti-patterns

- `[[IgnoredVulns]]` without `ignoreUntil` -> debt persists; always set `ignoreUntil` (Step 5).
- Skipping `--format=sarif` upload -> findings invisible in the GitHub Security tab; always emit SARIF (Step 7).
- Running only OSV-Scanner -> OSV.dev has its own coverage profile; layer with `snyk-test`.
- Scanning without a committed lockfile -> manifest fallback resolves versions less accurately; commit the lockfile and scan via `-L`.
- `--config` pointing outside the repo -> suppressions not auditable; commit `osv-scanner.toml` at the repo root.

## Limitations

- OSV.dev coverage varies by ecosystem (Python / npm / Go strong; less common ones thinner).
- No reachability analysis: every CVE on a declared dep counts even if the vulnerable function isn't called.
- Container image scanning is limited; prefer `trivy-image` or the Grype workflow in `syft-generation`.
- Some CLI surface evolves; verify against current `osv-scanner` help output.

## References

- [osv-usage][osv-usage] - usage page (lockfile, SBOM, config)
- Full `osv-scanner.toml` schema, triage template, and CI workflow:
  [references/osv-scanner-config-and-ci.md](references/osv-scanner-config-and-ci.md)
- google.github.io/osv-scanner - full docs
- github.com/google/osv-scanner - repository
- osv.dev - OSV vulnerability database
- ossf.github.io/osv-schema/ - OSV schema
- `snyk-test`,
  `dependabot-config`,
  `renovate-config`,
  `npm-pip-maven-audit` - 
  sister tools
- `syft-generation` - 
  cross-plugin SBOM source
