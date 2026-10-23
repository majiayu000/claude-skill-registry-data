---
name: vex-author
description: "Authors and validates OpenVEX documents - produces `not_affected`, `affected`, `fixed`, and `under_investigation` statements with justification codes using `vexctl create`; attaches VEX assertions to container images; outputs `.openvex.json` files consumed on a downstream VEX-filter / vulnerability-prioritization path. Use when a scanner flags a CVE that analysis confirms is not exploitable in your deployment, and a machine-readable `not_affected` assertion is needed to suppress false positives without discarding the finding from the audit trail."
metadata:
  keywords: "vex, openvex, vulnerability-exception, not-affected, sbom"
  version: "1.1.13"
---

# vex-author

## Overview

Per [github.com/openvex/spec][vex-spec], OpenVEX is a minimal implementation
of the Vulnerability Exploitability eXchange (VEX) standard. A VEX document
carries statements that assert the exploitability status of a CVE against a
specific product, allowing downstream consumers to suppress false positives
while preserving the audit trail.

[vex-spec]: https://github.com/openvex/spec
[vexctl]: https://github.com/openvex/vexctl

A downstream vulnerability-prioritization step reads a `.openvex.json` file
and moves findings with `vex_status: not_affected` to the `Filtered-VEX`
bucket: not blocking the build, but still surfaced in the report. A
`not_affected` assertion without a populated `justification` is rejected as
unverified.

## When to use

- A scanner reports a CVE against a package present in the image, but the
  vulnerable code path is not reachable in production (e.g. a CLI flag that
  is never passed, a library function that is never called).
- A CVE is fixed in a newer patch but your vendor ships an older version with
  the fix backported - the package version string still triggers scanner hits.
- You need to attach a machine-readable exploitability assertion to a container
  image for downstream consumers (SBOM attestation pipeline, compliance audit).
- You are accumulating VEX statements from multiple sub-teams into a single
  document to pass to a vulnerability-prioritization step.

Do not use VEX as a waiver mechanism for CVEs in CISA KEV; a conformant
prioritization step refuses `not_affected` on KEV entries regardless of
justification.

## Step 1 - Install vexctl

Per [github.com/openvex/vexctl][vexctl]:

```bash
# Go
go install github.com/openvex/vexctl@latest

# Homebrew
brew install vexctl
```

Verify:

```bash
vexctl version
```

## Step 2 - Understand the statement model

Per [github.com/openvex/spec/blob/main/OPENVEX-SPEC.md][vex-spec-md], an
OpenVEX document wraps an array of statements. Each statement has:

[vex-spec-md]: https://github.com/openvex/spec/blob/main/OPENVEX-SPEC.md

| Field | Required | Notes |
|---|---|---|
| `vulnerability.name` | yes | CVE-ID or GHSA-ID |
| `products[].@id` | yes | Package URL (purl) identifying the component |
| `status` | yes | `not_affected` / `affected` / `fixed` / `under_investigation` |
| `justification` | yes for `not_affected` | One of five codes (see Step 3) |
| `impact_statement` | alt for `not_affected` | Free-form prose if no justification code fits |
| `action_statement` | optional for `affected` | Remediation description |
| `status_notes` | optional | Supporting detail for any status |

Document-level required fields per [vex-spec-md][vex-spec-md]:
`@context` (`https://openvex.dev/ns/v0.2.0`), `@id`, `author`, `timestamp`,
`version` (integer, incremented on any content change), `statements`.

## Step 3 - Choose the right justification code

Per [vex-spec-md][vex-spec-md], the five justification codes for `not_affected`:

| Code | When to use |
|---|---|
| `component_not_present` | The component containing the vulnerable code is not included in the product at all |
| `vulnerable_code_not_present` | The component is present but the vulnerable code was excluded via configuration or build flags |
| `vulnerable_code_not_in_execute_path` | The vulnerable code exists but cannot be reached during normal execution |
| `vulnerable_code_cannot_be_controlled_by_adversary` | The vulnerable code can run but adversary input cannot reach it |
| `inline_mitigations_already_exist` | Built-in protections prevent exploitation (e.g. RELRO, stack canaries, vendor backport) |

If none of the five codes accurately describes the determination, omit
`justification` and supply `impact_statement` with a precise technical
explanation instead. The prioritization step accepts either field as evidence
of analysis.

## Step 4 - Author a `not_affected` assertion

Per [vexctl][vexctl]:

```bash
vexctl create \
  --author="platform-team@example.com" \
  --product="pkg:oci/my-app@sha256:abc123" \
  --vuln="CVE-2024-9999" \
  --status="not_affected" \
  --justification="vulnerable_code_not_in_execute_path" \
  > sbom.openvex.json
```

The generated document looks like:

```json
{
  "@context": "https://openvex.dev/ns/v0.2.0",
  "@id": "https://openvex.dev/docs/public/vex-...",
  "author": "platform-team@example.com",
  "timestamp": "2026-06-04T10:00:00Z",
  "version": 1,
  "statements": [
    {
      "vulnerability": { "name": "CVE-2024-9999" },
      "products": [{ "@id": "pkg:oci/my-app@sha256:abc123" }],
      "status": "not_affected",
      "justification": "vulnerable_code_not_in_execute_path"
    }
  ]
}
```

Use a precise purl that matches the `package` value in the prioritization
step's `ContainerFinding` records; a mismatch on version or arch will cause the
`affect.ref.endsWith(f['package'])` check to miss.

## Step 5 - Add statements to an existing document

Per [vexctl][vexctl], merge multiple single-statement files into one document:

```bash
# Author each assertion separately
vexctl create --product="pkg:oci/my-app@sha256:abc123" \
              --vuln="CVE-2024-1111" \
              --status="not_affected" \
              --justification="component_not_present" \
              > vex-cve-1111.json

vexctl create --product="pkg:oci/my-app@sha256:abc123" \
              --vuln="CVE-2024-2222" \
              --status="under_investigation" \
              > vex-cve-2222.json

# Merge into a single document
vexctl merge --product="pkg:oci/my-app@sha256:abc123" \
             vex-cve-1111.json vex-cve-2222.json \
             > sbom.openvex.json
```

`vexctl merge` re-timestamps the merged document and increments `version`.

## Step 6 - Attach to a container image

Per [vexctl][vexctl], sign and attach the VEX document to the image manifest
(requires `cosign` credentials):

```bash
vexctl attest --attach --sign sbom.openvex.json \
  my-registry.io/my-app@sha256:abc123
```

Downstream consumers retrieve the attestation without a separate file transfer.
The prioritization step can also read the VEX file directly from disk; image
attachment is optional for local CI use.

## Step 7 - Validate the document before passing to prioritization

Validation checklist:

- [ ] `@context` is `https://openvex.dev/ns/v0.2.0` (per [vex-spec-md][vex-spec-md])
- [ ] Every `not_affected` statement has either `justification` or `impact_statement` populated
- [ ] `products[].@id` purl matches the scanner's package identifier exactly
- [ ] `vulnerability.name` is the canonical CVE-ID (not a GHSA alias) to match scanner output
- [ ] `version` integer has been incremented if the file was edited after initial generation
- [ ] No statement carries `not_affected` for a CVE in CISA KEV (will be rejected by the prioritization step)

Quick structural check with `jq`:

```bash
jq '.statements[] | select(.status == "not_affected") |
    select(.justification == null and .impact_statement == null) |
    .vulnerability.name' sbom.openvex.json
# Returns CVE IDs that are missing justification - must be empty before handing off
```

## Step 8 - Apply VEX to scanner output (filter workflow)

Per [vexctl][vexctl], apply a VEX document directly against a SARIF scan
output to preview which findings would be suppressed:

```bash
vexctl filter scan_results.sarif.json sbom.openvex.json
```

The filtered output excludes findings whose CVE + product pair has a
`not_affected` statement. Use this to confirm suppression before committing
the file to the repository.

## Step 9 - CI integration

```yaml
jobs:
  vex-author:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: go install github.com/openvex/vexctl@latest
      - name: Validate existing VEX document
        run: |
          jq '.statements[] |
            select(.status == "not_affected") |
            select(.justification == null and .impact_statement == null) |
            .vulnerability.name' sbom.openvex.json \
          | grep -q . && echo "FAIL: not_affected without justification" && exit 1 || true
      - name: Attach to image
        run: |
          vexctl attest --attach --sign sbom.openvex.json \
            ${{ env.IMAGE_REF }}
```

Pass `sbom.openvex.json` to the prioritization step via its `vex_file` input;
its VEX-filter path reads `statements[].analysis.state` mapped
from `status`.

## Example

**Scenario:** Grype reports `CVE-2024-9999` against `bash@5.1.16` in the image.
Analysis confirms the vulnerable `SHELLOPTS=debug` parser is never invoked -
`SHELLOPTS` is locked to `privileged` by the entrypoint script.

```bash
vexctl create \
  --author="alice@example.com" \
  --product="pkg:apk/alpine/bash@5.1.16-r2" \
  --vuln="CVE-2024-9999" \
  --status="not_affected" \
  --justification="vulnerable_code_not_in_execute_path" \
  > sbom.openvex.json
```

Prioritization-step report section after ingestion:

```
### VEX-Filtered (surface for audit, not for action)

| CVE          | Package        | VEX status   | Justification                        |
|---|---|---|---|
| CVE-2024-9999 | bash@5.1.16   | not_affected | vulnerable_code_not_in_execute_path  |
```

The finding is not in the `Fix-Now` or `Fix-This-Sprint` buckets and does not
block the build. It remains visible in the report for the audit trail.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| `not_affected` without `justification` or `impact_statement` | The prioritization step rejects unverified claims (Trust unverified VEX claims anti-pattern) | Add one of the five justification codes or write a precise `impact_statement` |
| Asserting `not_affected` on a CISA KEV entry | The prioritization step hard-refuses; active exploitation cannot be hand-waved | Fix the vulnerability or apply a waiver per the step's waiver rules |
| Using a mismatched purl version | The `affect.ref.endsWith()` check will not match; finding stays in the fail bucket | Copy the exact `package` string from the scanner's `ContainerFinding` output |
| Authoring VEX in a text editor without `vexctl` | Field names, timestamp format, and `@context` URL are easy to get wrong | Always generate with `vexctl create` and validate with `jq` (Step 7) |
| One monolithic VEX file maintained by one person | Merge conflicts; no ownership | Author per-team files, merge with `vexctl merge` before passing to CI |

## Limitations

- VEX assertions are only as accurate as the analysis behind them. A wrong
  `not_affected` claim is harder to detect than a false positive. Require
  evidence (code path trace, test proof) before asserting, per the
  prioritization step's own warning.
- `vexctl create` does not validate that the purl resolves to a real package;
  typos in the `--product` flag produce silent mismatches. Cross-check against
  Syft SBOM output.
- OpenVEX spec is at v0.2.0 (per [vex-spec-md][vex-spec-md]); the schema may
  evolve. Pin `vexctl` to a specific release in CI to avoid breaking changes.
- `vexctl filter` accepts SARIF and CSAF inputs; raw Grype JSON or Trivy JSON
  require conversion before `vexctl filter` can process them. Use
  the prioritization step's non-SARIF Python path for those formats.

## References

- [vex-spec][vex-spec] - OpenVEX specification repository
- [vex-spec-md][vex-spec-md] - OpenVEX spec: document schema, statement model,
  status values, justification codes
- [vexctl][vexctl] - vexctl CLI: install, create, merge, attest, filter commands
- `syft-generation` - upstream SBOM generation
  (produces the purl identifiers used in `--product` flags)
- openvex.dev - OpenVEX landing page
