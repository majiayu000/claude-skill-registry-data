---
name: kakaotalk-db-key-recovery
description: Recover and validate a local KakaoTalk SQLCipher database key on Windows with kakaocli-win, storing it under the current user's DPAPI protection. Use only for data owned by or explicitly authorized to the current Windows user.
---

# KakaoTalk DB Key Recovery

Use this only on the current user's own signed-in KakaoTalk process and database, or where the data owner has explicitly authorized access. Do not weaken process checks, export raw keys, copy databases, or upload recovered material.

Run `scripts/recover-db-key.ps1` for deterministic invocation. Prefer the default database discovery unless the user supplies a specific `.edb` path. The helper never prints the raw key; successful keys are stored by `kakaocli-win` in a local DPAPI-protected store.

When a stored key exists, prefer `kakaocli friends` or `kakaocli db-schema` over exporting a plaintext database. These commands decrypt to a temporary local file, open it read-only, and remove it after the query.

Start with the default stride and timeout. If no validated key is found, ask the user to open the KakaoTalk screen that uses the target database and retry. Use stride `1` only for an explicitly requested deeper local scan because it is slower.

Report only success state, key fingerprint, timing, and aggregate scan statistics. Treat full database paths, process IDs, stored-key files, and fingerprints as local diagnostic data; redact them before publication.
