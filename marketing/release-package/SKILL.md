---
name: release-package
description: Assemble the verified film master, trailers, social masters, subtitles, artwork, audio master, copy, metadata, QC reports, and checksums into one traceable release manifest and optional collected package directory.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Release Package

## Workflow

1. Read `../../references/RELEASE_DELIVERY.md`, media registry, film master, trailer masters, campaign delivery, subtitles, artwork, and QC reports.
2. Write `06_release/release_manifest.json` with stable `DELIV-###` IDs.
3. Mark each deliverable required or optional.
4. Run `scripts/release_package.py PROJECT --validate`.
5. Run with `--collect` when a single collected package directory is requested.
6. Write `06_release/SHA256SUMS.txt` from actual final files.
7. Do not mark release complete if a required file is absent or has blocking QC failure.

## Done

A separate person can identify, verify, and distribute every required release file without consulting chat history.
