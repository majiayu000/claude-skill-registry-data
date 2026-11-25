---
name: static-site-handoff
description: Prepare and verify local upload packages from a completed static-site export, comparing content hashes with a user-confirmed upload baseline. Use for manual hosting handoffs without running builds, uploading files, or deleting remote content.
---

# Static Site Handoff

Keep a completed build, an upload package, and upload acknowledgement separate.

## Workflow

1. Confirm the completed build directory and separate private package/state locations. A successful local build does not prove a live deployment.
2. Read [the package contract](references/package-contract.md) before using the helper. Review the build for public suitability; filename guards are not a secret scanner.
3. Prepare a new package with Python 3.11 or newer:

       python scripts/static_handoff.py prepare --build-dir sample-build --package-dir sample-package --state-dir local-state --json

4. Review the manifest, changed files, and removed-path report. Upload only the contents of the upload directory, using separately authorized hosting tools. Prefer assets before pages; retain older hashed assets needed by cached pages. Do not mirror-delete.
5. Verify the frozen package before handoff:

       python scripts/static_handoff.py verify --package-dir sample-package --json

6. Only after the user explicitly acknowledges that this exact package was completely uploaded, record that acknowledgement:

       python scripts/static_handoff.py confirm --package-dir sample-package --state-dir local-state --package-id PACKAGE_ID --acknowledge-upload --json

Partial or uncertain uploads do not justify confirmation. Reconcile before retrying. The helper cannot authenticate the acknowledgement or inspect the host.

## Boundaries and output

The helper reads the selected build and writes only new packages and explicit private state. It does not execute build commands, use hosting access, upload, or perform remote cleanup. Preserve package manifests for removed-path history. Keep real paths, manifests, and confirmation records private.

Return package identity, file count, removed paths requiring review, upload ordering advice, and verification limitations. Mark live deployment unverified until an independently authorized live check succeeds.
