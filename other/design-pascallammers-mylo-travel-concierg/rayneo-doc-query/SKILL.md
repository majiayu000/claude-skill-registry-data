---
name: rayneo-doc-query
description: Query and navigate RayNeo X2/X3 Pro AR glasses documentation. Use this skill when answering questions about RayNeo XR hardware specifications, SDK usage, Android 12 development, binocular display APIs, device setup, ADB commands, design guidelines, troubleshooting, or any technical aspects of RayNeo X-series glasses development.
---

# RayNeo Doc Query

## Overview

This skill enables efficient querying and navigation of RayNeo X2 and X3 Pro AR glasses documentation. The documentation covers hardware specifications, development SDKs, design guidelines, API references, troubleshooting guides, and device setup procedures.

## When to Use This Skill

Use this skill when the user asks questions about:

- RayNeo X2 or X3 Pro hardware specifications (display, sensors, battery, connectivity)
- Development workflow and SDK setup (Unity ARDK, Android ARDK, IPCSDK)
- Design guidelines for AR glasses UI/UX (binocular display, interaction patterns, layout zones)
- API references and capabilities (focus management, touch handling, sensors, 3D effects)
- Device setup procedures (ADB configuration, Unity deployment, screen mirroring)
- Troubleshooting SDK issues (permissions, camera FOV, overheating, app lifecycle)
- ADB commands and device debugging

## Documentation Structure

The RayNeo documentation consists of seven core PDF files, each serving a specific purpose:

### Primary Documents

1. **Device Introduction.pdf** - Hardware specs, platform comparisons (XR2 vs AR1), sensors, battery, connectivity
2. **Developer manual.pdf** - Onboarding guide, SDK overview, publishing workflow, change logs
3. **Design specifications for AR glasses.pdf** - UX/UI standards, interaction patterns, FoV layout, typography
4. **Capabilities & API.pdf** - ARDK SDK reference with binocular display APIs, focus management, sensors
5. **Development Issue_SDK.pdf** - FAQ-style troubleshooting for common SDK problems
6. **USB debugging & Screen mirroring.pdf** - Step-by-step device connectivity and visualization setup
7. **ADB.pdf** - Quick command reference and ADB toggle instructions

### Documentation Index

The skill includes `references/memory-index.md` which provides:

- Quick reference table mapping files to content areas
- Detailed descriptions of each document with search keywords
- Cross-document task maps for common workflows
- Retrieval tips and search strategies

Read `references/memory-index.md` when first invoked to understand the complete documentation landscape.

## Query Strategies

### Initial Assessment

When receiving a RayNeo-related query:

1. Read `references/memory-index.md` to orient to the documentation structure
2. Identify which PDF(s) are most relevant based on the query topic
3. Note the suggested keywords and sections for the relevant documents

### Document Selection

Match query topics to documents using these guidelines:

- **Hardware/specs queries** → Device Introduction.pdf
- **Getting started/setup** → Developer manual.pdf, USB debugging & Screen mirroring.pdf
- **UI/UX design** → Design specifications for AR glasses.pdf
- **API/SDK implementation** → Capabilities & API.pdf
- **Troubleshooting** → Development Issue_SDK.pdf
- **ADB/device commands** → ADB.pdf, USB debugging & Screen mirroring.pdf

### Multi-Document Workflows

For complex queries spanning multiple concerns, consult the Cross-Doc Task Map in `references/memory-index.md`:

- **Device setup** → USB debugging + ADB + Developer manual
- **UI/UX implementation** → Design specifications + Capabilities & API
- **SDK integration** → Developer manual + Capabilities & API + Development Issue

### Search Techniques

Use the Grep tool to search within the rayneo-xr-docs directory:

```bash
# Search specific PDF (requires pdftotext)
pdftotext "rayneo-xr-docs/Capabilities & API.pdf" - | rg 'FocusHolder'

# Search all docs for a keyword
rg 'ShareCamera' rayneo-xr-docs
```

Combine document name prefixes with search terms for targeted results as suggested in the memory index.

## Answer Construction

When answering queries:

1. Reference specific PDF files by name in responses
2. Cite document sections when known (from memory-index.md section details)
3. For detailed technical answers, note that the actual PDF files can be read if available
4. Provide context about where information fits in the broader documentation ecosystem
5. Suggest related documents or sections for follow-up exploration

## Resources

### references/

**memory-index.md** - Comprehensive index of the RayNeo documentation structure with:
- Directory snapshot and quick reference table
- Detailed document descriptions and notable sections
- Suggested search keywords per document
- Cross-document task mappings
- Retrieval tips and search strategies

Read this file first when the skill is invoked to understand the complete documentation landscape and plan the query strategy.
