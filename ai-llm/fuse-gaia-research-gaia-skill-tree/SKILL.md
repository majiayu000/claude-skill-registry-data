---
name: fuse
description: 'Combine two AI agent skills into one. Trigger phrases: /fuse, "fuse these skills", "combine skills", "merge these two skills", "create a fusion skill"'
---

A sequential routing pipeline to compose two installed skills into a single integrated agent capability.

## Setup

1. Check for the existence of `.agents/skills/`, `.claude/skills/`, or `.cursor/rules/` to locate the target skills directory.
2. Note if a `.gaia/` directory is present in the workspace root.

## Routing Table

Execute these steps in order to perform a skill fusion:

| Step | Action | Reference |
|---|---|---|
| 1 | **Detect** -- find and confirm the two source skills | [reference/detect.md](reference/detect.md) |
| 2 | **Compose** -- read sources and apply the fusion prompt | [reference/compose.md](reference/compose.md) |
| 3 | **Name** -- propose, validate, and select a target name | [reference/name.md](reference/name.md) |
| 4 | **Register** -- write the files and log the fusion event | [reference/register.md](reference/register.md) |

## Package

Standalone-package docs and metadata: [README.md](README.md), [LICENSE](LICENSE), [CITATION.cff](CITATION.cff). Install helper: [install.sh](install.sh). Attribution mark: [powered-by-gaia.svg](powered-by-gaia.svg).
