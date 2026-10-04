---
name: sbomr
description: Analyze a CycloneDX/SPDX SBOM file using sbomr. Use when asked to inspect, summarize, or query an SBOM file — e.g. list dependencies, check licenses, find vulnerabilities, or export data.
argument-hint: [path/to/bom.json]
allowed-tools: Bash, Read, Glob
---

Use the `sbomr` CLI to analyze SBOM files non-interactively.

## Check availability

```sh
sbomr --version 2>/dev/null || cargo install --path .
```

## Export to CSV (primary non-interactive operation)

```sh
sbomr --csv /tmp/sbom.csv [path/to/bom.json]
```

Defaults to `bom.json` in the current directory if no path given.

CSV columns: `name`, `version`, `registry`, `type`, `license`, `scope`, `dep_type`, `description`

After exporting, read the CSV to answer questions about the SBOM contents.

## Enrich with vulnerability data before exporting

```sh
sbomr --enrich --csv /tmp/sbom.csv path/to/bom.json
```

Fetches vulnerability info from OSV.dev via purl. Adds vulnerability counts to the output.

## Common analysis tasks

**List all direct dependencies:**
Filter CSV rows where `dep_type` column is `direct`.

**Find packages with no license:**
Filter CSV rows where `license` column is empty.

**Find vulnerable packages:**
Use `--enrich` and filter rows where vulnerability data is present. The TUI shows full CVSS scores; the CSV export captures component-level data.

**Check for copyleft licenses:**
Filter for licenses containing `GPL`, `LGPL`, `AGPL`, `MPL`, `EUPL`, `CDDL`.

## Supported SBOM formats

CycloneDX JSON (1.4+) and SPDX JSON. Not XML.

## Generating SBOM files

Before you can analyze an SBOM, you need one. Use the appropriate tool for the ecosystem:

### Rust (Cargo)
```sh
cargo install cargo-cyclonedx
cargo cyclonedx --format json --spec-version 1.4
# Output: bom.json in the current directory
```

### Node.js / npm / yarn / pnpm
```sh
npx @cyclonedx/cyclonedx-npm --output-file bom.json
# or
npx @cyclonedx/cyclonedx-yarn --output-file bom.json
```

### Python (pip / poetry / pipenv)
```sh
pip install cyclonedx-bom
cyclonedx-py environment --of JSON -o bom.json
# or from a requirements.txt:
cyclonedx-py requirements requirements.txt --of JSON -o bom.json
```

### Go
```sh
go install github.com/CycloneDX/cyclonedx-gomod/cmd/cyclonedx-gomod@latest
cyclonedx-gomod app -json -output bom.json
```

### Java (Maven / Gradle)
```sh
# Maven
mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom
# Output: target/bom.json

# Gradle
# Add plugin: id("org.cyclonedx.bom") version "1.8.2"
gradle cyclonedxBom
# Output: build/reports/bom.json
```

### Any project (via Trivy — most universal option)
```sh
brew install trivy   # or: https://aquasecurity.github.io/trivy/
trivy fs --format cyclonedx --output bom.json .
# Works for Rust, Go, Node, Python, Java, Ruby, PHP, .NET, etc.
```

### Container images (via Trivy or Syft)
```sh
trivy image --format cyclonedx --output bom.json myimage:latest
# or
syft myimage:latest -o cyclonedx-json=bom.json
```
