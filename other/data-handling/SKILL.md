---
name: data-handling
description: Read before changing capture, indexing, redaction, learning, skill publication, engine execution, Actions bot setup, or any path that stores or sends user data.
---

# Data handling

Follow the code conventions in `CONTRIBUTING.md`. Preserve the boundaries documented in `docs/data-handling.md`.

## Consent and scope

Every capture source has a named flag, off by default, and an entry in `docs/data-handling.md`. Widening locations or content counts as a source change. Transcript access does not enable Git metadata, and reading skills does not authorize editing them.

Before consent, source discovery may return one ephemeral boolean for whether a configured root exists and is non-empty. Do not open entries or retain their names, paths, counts, timestamps, or provider identifiers.

Preserve repository and remote-owner boundaries. Unknown origins stay isolated. Global guidance requires explicit global evidence or a user decision. Managed policy limits cannot be widened by user configuration.

## Learning input

Events carry pointers. `resolveRedacted` is the learning-text boundary: eligible excerpts pass through `redactSecrets` when materialized. Do not add competing downstream redaction gates. Derive fingerprints, metadata, and model-facing text from the same bounded source snapshot.

Exclude tool results, tool-returned file contents, thinking blocks, and data-access results from learning. Redaction reduces exposure without guaranteeing anonymity. Removing a redaction pattern needs a documented reason.

New sources need integration tests proving the adapter-to-redaction path, including excluded fields and synthetic secrets. Demonstrate that bypassing the gate makes the regression test fail.

## Storage and publication

Keep derived learning, revisions, backups, and private evaluation evidence in user-owned storage outside this public checkout. Use independently authored synthetic fixtures. Do not copy private material into ignored repository files.

The index stores locators and metadata, without captured text. No raw transcript archive exists, and shadowclone does not upload or synchronize private learning state by default.

Preserve manual edits, ownership fingerprints, permissions, and supporting resources when publishing skills. Keep third-party packages and native memory read-only. Record reversible revisions and block overwrites when intervening edits conflict.

## Model requests, diagnostics, and actions

Learning uses bounded redacted excerpts. Authorized coding runs can expose a repository to the selected provider, and evaluation judges receive unredacted generated code. Keep those distinct boundaries explicit; code evidence is not safe for logs or publication.

Log counts, sizes, hashes, source names, and opaque locators. Samples require an explicit debug flag and redaction. Never put raw capture or identifying transcript paths in errors or reports. Review any new network destination against the consent and purpose authorizing it.

Source, model, and publication permissions govern unattended learning. External actions require explicit approval for the particular action. The product does not commit, push, or act on GitHub itself; the `shadowclone-work` skill acts through the host agent's permissions.

## Removal and verification

Keep removal bounded to recorded ownership. Preserve original transcripts and report edited artifacts that block cleanup. Document retention limits in the data-handling guide.

Exercise changed consent, scope, storage, redaction, and process boundaries with synthetic tests. Inspect new logging, file, process, and network sinks before handoff. Report material boundary changes and verification without copying sensitive evidence into the report.
