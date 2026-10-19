---
name: swap-file-scanner
description: Replace the upload virus scanner (ClamAV) with a scanning API or cloud malware scanning. Use when the user decides on a different scanner. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Swap the file scanner

- **Interface:** `FileScanner` (`scan(bytes): Promise<ScanResult>`) in
  `apps/worker/src/files/file-scanner.ts`.
- **Today:** `ClamdScanner` streams the bytes to clamd (INSTREAM); `NoScanner` accepts
  everything and is refused in production when uploads are on.
- **Selected in:** `createScanner()` in `apps/worker/src/files/files.module.ts`.
- **Env:** `FILE_SCANNER` (`clamav` | `none`), `CLAMAV_URL` (`apps/worker/src/env.ts`). In
  Kubernetes, clamd is the stack chart's `clamav` service (`services.clamav` in
  `deploy/charts/stack/values.yaml`, enabled per environment).

## Swap

1. A class implementing `FileScanner`: `{ clean: true }`, or `{ clean: false, signature }`
   for a detection. Throw on errors and timeouts so the job retries; never report
   clean when the scan didn't happen.
2. Add its name to the `FILE_SCANNER` enum and its settings to `apps/worker/src/env.ts`,
   `.env.example` and `docs/environment.md`; add a branch in `createScanner()`.
3. If ClamAV is no longer used, set `services.clamav.enabled: false` in the environments'
   `stack.yaml`.

## Tests

`apps/worker/src/files/file-scanner.test.ts` (unit, a fake clamd), and the `uploads`
tests in `apps/worker/test/worker.integration.test.ts`, which scan real files with
ClamAV (EICAR). Add the same cases for the new scanner.

## Finish

1. The verify skill.
2. Ask the `reviewer` agent to review the change, and the `security-reviewer` agent: a
   new implementation brings its own credentials and sends data somewhere new. If you
   wrote a migration, the `migration-reviewer` agent too.
3. Update the seam's row in the README's "Scaling path" table if what's "Now" changed.
