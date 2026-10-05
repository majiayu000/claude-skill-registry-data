---
name: sbom-generation
description: Generate Software Bill of Materials (SBOM) for compliance with NTIA, EU CRA, and other regulatory requirements. Use when preparing for audits, compliance.
---

# SBOM Generation

Generate complete, standards-compliant Software Bill of Materials documentation for security, compliance, and supply chain management.

## When to Use This Skill

Use this skill when you need to:

- Meet NTIA minimum element requirements
- Comply with EU Cyber Resilience Act
- Track software dependencies
- Identify vulnerable components
- Prepare for security audits
- Establish supply chain transparency

**Trigger phrases**: "generate SBOM", "software bill of materials", "dependency inventory", "NTIA compliance", "EU CRA", "CycloneDX", "SPDX"

## What This Skill Does

### SBOM Standards

| Standard | Format | Use Case |
|----------|--------|----------|
| SPDX | JSON, RDF, Tag-Value | Industry standard, Linux Foundation |
| CycloneDX | JSON, XML | Security-focused, OWASP |
| SWID | XML | Software identification |

### Compliance Frameworks

- **NTIA Minimum Elements** - US government requirements
- **EU Cyber Resilience Act (CRA)** - European compliance
- **Executive Order 14028** - US federal suppliers
- **FDA Requirements** - Medical device software

## Instructions

### NTIA Minimum Elements

The NTIA requires these seven elements:

1. **Supplier Name** - Who created the component
2. **Component Name** - Name of the software
3. **Version** - Component version string
4. **Unique Identifier** - PURL, CPE, or other ID
5. **Dependency Relationship** - How components relate
6. **Author** - Who created the SBOM
7. **Timestamp** - When SBOM was created

### Generate SBOM by Language

#### Python

```bash
# Using pip-licenses
pip install pip-licenses
pip-licenses --format=json --output-file=sbom-licenses.json

# Using cyclonedx-bom
pip install cyclonedx-bom
cyclonedx-py -r requirements.txt -o sbom.json --format json

# Using syft (multi-language)
syft . -o cyclonedx-json=sbom.json
```

#### JavaScript/Node.js

```bash
# Using cyclonedx-npm
npx @cyclonedx/cyclonedx-npm --output-file sbom.json

# Using npm audit for vulnerabilities
npm audit --json > audit.json

# Using syft
syft . -o spdx-json=sbom.json
```

#### Java

```bash
# Using cyclonedx-maven-plugin
mvn org.cyclonedx:cyclonedx-maven-plugin:makeBom

# Using gradle plugin
# Add to build.gradle:
# plugins { id 'org.cyclonedx.bom' version '1.7.4' }
gradle cyclonedxBom
```

#### C#/.NET

```bash
# Using dotnet-cyclonedx
dotnet tool install -g CycloneDX
dotnet CycloneDX project.csproj -o sbom.json -j

# Using nuget
nuget locals all -list
```

#### Go

```bash
# Using cyclonedx-gomod
go install github.com/CycloneDX/cyclonedx-gomod/cmd/cyclonedx-gomod@latest
cyclonedx-gomod mod -json=true > sbom.json

# Using syft
syft . -o cyclonedx-json=sbom.json
```

### CycloneDX SBOM Example

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "serialNumber": "urn:uuid:550e8400-e29b-41d4-a716-446655440000",
  "version": 1,
  "metadata": {
    "timestamp": "2025-01-15T10:30:00Z",
    "tools": [
      {
        "vendor": "CycloneDX",
        "name": "cyclonedx-python",
        "version": "3.0.0"
      }
    ],
    "authors": [
      {
        "name": "Security Team",
        "email": "security@example.com"
      }
    ],
    "component": {
      "type": "application",
      "name": "my-application",
      "version": "1.0.0",
      "description": "My Application Description",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "purl": "pkg:pypi/my-application@1.0.0"
    },
    "manufacture": {
      "name": "Example Corp",
      "url": [
        "https://example.com"
      ]
    },
    "supplier": {
      "name": "Example Corp",
      "url": [
        "https://example.com"
      ],
      "contact": [
        {
          "name": "Support",
          "email": "support@example.com"
        }
      ]
    }
  },
  "components": [
    {
      "type": "library",
      "bom-ref": "pkg:pypi/requests@2.31.0",
      "name": "requests",
      "version": "2.31.0",
      "description": "Python HTTP for Humans.",
      "licenses": [
        {
          "license": {
            "id": "Apache-2.0"
          }
        }
      ],
      "purl": "pkg:pypi/requests@2.31.0",
      "externalReferences": [
        {
          "type": "website",
          "url": "https://requests.readthedocs.io"
        },
        {
          "type": "vcs",
          "url": "https://github.com/psf/requests"
        }
      ],
      "hashes": [
        {
          "alg": "SHA-256",
          "content": "942c5a758f98d790eaed1a29cb6eefc7ffb0d1cf7af05c3d2791656dbd6ad1e1"
        }
      ]
    },
    {
      "type": "library",
      "bom-ref": "pkg:pypi/urllib3@2.0.7",
      "name": "urllib3",
      "version": "2.0.7",
      "description": "HTTP library with thread-safe connection pooling",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "purl": "pkg:pypi/urllib3@2.0.7"
    }
  ],
  "dependencies": [
    {
      "ref": "pkg:pypi/my-application@1.0.0",
      "dependsOn": [
        "pkg:pypi/requests@2.31.0"
      ]
    },
    {
      "ref": "pkg:pypi/requests@2.31.0",
      "dependsOn": [
        "pkg:pypi/urllib3@2.0.7",
        "pkg:pypi/charset-normalizer@3.3.2",
        "pkg:pypi/idna@3.6",
        "pkg:pypi/certifi@2024.2.2"
      ]
    }
  ],
  "vulnerabilities": [
    {
      "id": "CVE-2023-32681",
      "source": {
        "name": "NVD",
        "url": "https://nvd.nist.gov/"
      },
      "ratings": [
        {
          "source": {
            "name": "NVD"
          },
          "score": 6.1,
          "severity": "medium",
          "method": "CVSSv3"
        }
      ],
      "description": "Requests Session object does not verify requests after making first request with verify=False",
      "recommendation": "Upgrade to requests>=2.31.0",
      "affects": [
        {
          "ref": "pkg:pypi/requests@2.28.0"
        }
      ]
    }
  ]
}
```

### SPDX SBOM Example

```json
{
  "spdxVersion": "SPDX-2.3",
  "dataLicense": "CC0-1.0",
  "SPDXID": "SPDXRef-DOCUMENT",
  "name": "my-application-sbom",
  "documentNamespace": "https://example.com/sbom/my-application-1.0.0",
  "creationInfo": {
    "created": "2025-01-15T10:30:00Z",
    "creators": [
      "Tool: cyclonedx-python-3.0.0",
      "Organization: Example Corp"
    ],
    "licenseListVersion": "3.22"
  },
  "packages": [
    {
      "SPDXID": "SPDXRef-Package-my-application",
      "name": "my-application",
      "versionInfo": "1.0.0",
      "supplier": "Organization: Example Corp",
      "downloadLocation": "https://github.com/example/my-application",
      "filesAnalyzed": false,
      "licenseConcluded": "MIT",
      "licenseDeclared": "MIT",
      "copyrightText": "Copyright 2025 Example Corp",
      "externalRefs": [
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:pypi/my-application@1.0.0"
        }
      ]
    },
    {
      "SPDXID": "SPDXRef-Package-requests",
      "name": "requests",
      "versionInfo": "2.31.0",
      "supplier": "Organization: Python Software Foundation",
      "downloadLocation": "https://pypi.org/project/requests/",
      "filesAnalyzed": false,
      "licenseConcluded": "Apache-2.0",
      "licenseDeclared": "Apache-2.0",
      "copyrightText": "Copyright Kenneth Reitz",
      "checksums": [
        {
          "algorithm": "SHA256",
          "checksumValue": "942c5a758f98d790eaed1a29cb6eefc7ffb0d1cf7af05c3d2791656dbd6ad1e1"
        }
      ],
      "externalRefs": [
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:pypi/requests@2.31.0"
        },
        {
          "referenceCategory": "SECURITY",
          "referenceType": "cpe23Type",
          "referenceLocator": "cpe:2.3:a:python:requests:2.31.0:*:*:*:*:*:*:*"
        }
      ]
    }
  ],
  "relationships": [
    {
      "spdxElementId": "SPDXRef-DOCUMENT",
      "relatedSpdxElement": "SPDXRef-Package-my-application",
      "relationshipType": "DESCRIBES"
    },
    {
      "spdxElementId": "SPDXRef-Package-my-application",
      "relatedSpdxElement": "SPDXRef-Package-requests",
      "relationshipType": "DEPENDS_ON"
    }
  ]
}
```

### CI/CD Integration

```yaml
# GitHub Actions
name: Generate SBOM

on:
  release:
    types: [published]
  workflow_dispatch:

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Generate SBOM with Syft
        uses: anchore/sbom-action@v0
        with:
          artifact-name: sbom.spdx.json
          output-file: sbom.spdx.json
          format: spdx-json

      - name: Scan SBOM for vulnerabilities
        uses: anchore/scan-action@v3
        with:
          sbom: sbom.spdx.json
          fail-build: true
          severity-cutoff: high

      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.spdx.json

      - name: Attach SBOM to Release
        if: github.event_name == 'release'
        uses: softprops/action-gh-release@v1
        with:
          files: sbom.spdx.json
```

### Vulnerability Scanning

```bash
# Using Grype with SBOM
grype sbom:sbom.json

# Using Trivy
trivy sbom sbom.json

# Using OSV-Scanner
osv-scanner --sbom=sbom.json
```

## Tools

### SBOM Generation
- **Syft** - Multi-language, container support
- **CycloneDX tools** - Language-specific generators
- **SPDX tools** - Official SPDX tooling

### Vulnerability Scanning
- **Grype** - SBOM vulnerability scanner
- **Trivy** - Comprehensive scanner
- **OSV-Scanner** - Google's OSV database

### SBOM Management
- **Dependency-Track** - SBOM analysis platform
- **GUAC** - Graph for Understanding Artifact Composition

## Quality Checklist

- [ ] All NTIA minimum elements present
- [ ] Supplier information complete
- [ ] Component versions accurate
- [ ] PURLs/CPEs included for identification
- [ ] Dependencies mapped correctly
- [ ] Licenses identified
- [ ] Checksums/hashes included
- [ ] Known vulnerabilities documented
- [ ] SBOM format validated
- [ ] Automated generation in CI/CD

## Common Issues and Solutions

### Issue: Missing transitive dependencies
**Solution**: Use tools that resolve full dependency tree:
```bash
syft . -o cyclonedx-json=sbom.json --scope all-layers
```

### Issue: Incomplete license information
**Solution**: Combine multiple sources:
```bash
pip-licenses --format=json > licenses.json
# Merge with SBOM
```

### Issue: No vulnerability data
**Solution**: Add vulnerability scanning step:
```bash
grype sbom:sbom.json -o json > vulnerabilities.json
```

## Related Skills

- `dependency-security-audit` - Security scanning
- `licensing-compliance` - License checking
- `security-review` - Security analysis

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates documentation_generation/sbom/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
