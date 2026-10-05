---
name: supply-chain
description: Use when assessing dependency and build-pipeline risk. Covers dependency vetting, lockfiles, SBOMs, provenance and signing, pinning CI actions, and responding to a compromised package.
metadata:
  category: security
  version: 1.0.0
  tags: [supply-chain, dependencies, sbom, provenance, ci]
---

# Supply Chain Security

## Purpose

Reduce the risk that arrives through your dependencies and your build pipeline — which is now a more common attack path than a vulnerability in your own code.

## When to Use

- Adding a dependency.
- Auditing an existing dependency tree.
- Hardening a CI/CD pipeline against compromise.
- Responding to a compromised or malicious package.

## Capabilities

- Dependency vetting and risk assessment.
- Lockfile discipline and reproducible builds.
- SBOM generation and vulnerability scanning.
- Artifact signing and provenance attestation.
- CI pipeline hardening.

## Inputs

- The dependency tree, direct and transitive.
- The build pipeline and its permissions.
- The advisory feeds relevant to your ecosystem.

## Outputs

- A vetted dependency tree with a committed lockfile.
- An SBOM per build, and a scan that fails on critical findings.
- A pipeline where a compromised dependency cannot exfiltrate credentials.

## Workflow

1. **Vet before adding** — Who maintains it? When was it last released? How many transitive dependencies does it drag in? A left-pad-sized utility with forty dependencies is a liability, not a convenience.
2. **Commit the lockfile and install from it** — `npm ci`, `pip install -r requirements.lock`, `cargo --locked`. An install that resolves versions at build time is an install that can pull a compromised patch release.
3. **Pin CI actions by SHA** — A tag is mutable. A compromised action with `pull_request` write access can exfiltrate every secret in the pipeline.
4. **Restrict pipeline permissions** — The build job does not need write access to the repository or production credentials. Scope tokens per job.
5. **Generate an SBOM and scan it** — On every build. Fail on critical vulnerabilities in what you actually ship, not in your dev dependencies.
6. **Sign and attest** — Sigstore/cosign for the artifact, with a provenance attestation linking it to the commit and the build.

## Best Practices

- The most dangerous dependency is the one you did not choose: a transitive dependency four levels deep, maintained by nobody, that runs an install script.
- Install scripts (`postinstall` in npm, `setup.py` in pip) execute arbitrary code at install time, on developer machines and in CI. Disable them where you can (`npm ci --ignore-scripts`) and audit them where you cannot.
- Every dependency is code you ship and are responsible for. A 200-line utility is usually cheaper to write than to depend on.
- Typosquatting is real and effective. Check the package name character by character before adding it, especially in a hurry.
- A CI job that can both read a secret and reach the internet can exfiltrate that secret. Minimize the jobs that hold production credentials.
- Automated dependency-update PRs are good, but merging them without review is how a compromised patch release reaches production automatically.

## Examples

**Pipeline hardening — pinned, scoped, and scanned:**

```yaml
permissions:
  contents: read              # the default is often write-all. It should not be.

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write         # for keyless signing only
      attestations: write
    steps:
      # Pinned by SHA. A tag can be moved by an attacker who compromises the action.
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

      - run: npm ci --ignore-scripts        # lockfile, no arbitrary install-time code

      - name: Generate SBOM
        run: npx @cyclonedx/cyclonedx-npm --output-file sbom.json

      - name: Fail on critical vulnerabilities in shipped dependencies
        run: npx osv-scanner --lockfile=package-lock.json --fail-on-severity=critical

      - name: Sign the artifact and attest its provenance
        uses: actions/attest-build-provenance@v1
        with:
          subject-path: dist/app.tar.gz
```

**Vetting a dependency before it enters the tree:**

```bash
npm view left-pad-ish --json | jq '{
  maintainers: .maintainers,
  last_publish: .time.modified,
  dependencies: (.dependencies // {} | keys | length)
}'

# Transitive weight: what does one `npm install` actually bring in?
npm install --dry-run left-pad-ish 2>&1 | grep "added"
# added 47 packages   <- for a function you could write in six lines
```

**Responding to a compromised package:**

```text
1. Determine exposure: is the compromised version in any lockfile, in any
   environment, including CI? `npm ls <pkg>` across every repository.

2. If it ran in CI: every secret that job could reach is compromised. Rotate
   all of them. This is the step people skip and it is the one that matters.

3. Pin to a known-good version, rebuild, redeploy.

4. Check for persistence: a malicious postinstall may have written to
   ~/.npmrc, added a git hook, or modified a lockfile.
```

## Notes

- The critical, frequently-missed step in a package compromise is rotating the CI secrets. If the malicious code executed in a job that had access to a deployment key, that key is compromised — and the package is the least of the problem.
- `--ignore-scripts` breaks packages that legitimately need to compile native code. The correct response is to allow-list those specific packages, not to re-enable scripts globally.
- An SBOM is only useful if something consumes it. Generating one to satisfy a compliance checkbox, and never scanning it, buys nothing.
