---
name: swap-storage
description: Point file storage somewhere other than the in-cluster RustFS (another S3-compatible server or service) or add one without an S3 API. Use when the user decides to change where uploads live. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Swap object storage

- **Interface:** `Storage` (presigned upload and download URLs, `head`, `read`, `write`,
  `move`, `delete`) in `packages/nest-common/src/storage.ts`.
- **Today:** `S3Storage`, built by `createStorage(env)` in the same file (null when
  `S3_BUCKET` is unset: uploads are off). It covers RustFS (locally and in every cluster,
  from the data chart) and any other S3 API: AWS S3, R2, GCS (XML API with HMAC keys),
  Azure behind an S3 gateway.
- **Provided as** `STORAGE` in `apps/api/src/modules/files/files.module.ts` (signs
  uploads) and `apps/worker/src/files/files.module.ts` (checks and moves them).
- **Env:** `S3_BUCKET`, `S3_REGION`, `S3_ENDPOINT`, `S3_ACCESS_KEY_ID`,
  `S3_SECRET_ACCESS_KEY`, `S3_FORCE_PATH_STYLE` (`storageEnv` in
  `packages/nest-common/src/env.ts`), and `STORAGE_ORIGIN` for the web app's CSP.

## Another S3-compatible provider

No code: set the `S3_*` variables for api and worker (their SOPS Secrets, in place of the
data chart's `storage` Secret), `STORAGE_ORIGIN` for web, and give the bucket a CORS rule
allowing `PUT` and `GET` from the site's origin (browsers upload directly; see `s3-init`
in `docker-compose.yml` and the data chart's bucket Job). Everything is self-hosted on
purpose: check with the user before moving uploads to a managed service.

## A provider without an S3 API

1. A class implementing `Storage`. Presigned uploads must bind content type and length
   so a client can't upload something else; `read` must refuse objects over `maxBytes`
   without buffering them.
2. Choose it in `createStorage` from a new variable in `storageEnv`, documented in
   `.env.example` and `docs/environment.md`. Callers don't change.

## Tests

`packages/nest-common/test/storage.integration.test.ts` runs against RustFS
(`bun run test:integration` starts it); the upload flow is covered in
`apps/api/test/api.integration.test.ts`, the worker's `uploads` tests in
`apps/worker/test/worker.integration.test.ts`, and `apps/web/e2e/avatar.spec.ts`.

## Finish

1. The verify skill.
2. Ask the `reviewer` agent to review the change, and the `security-reviewer` agent: a
   new implementation brings its own credentials and sends data somewhere new. If you
   wrote a migration, the `migration-reviewer` agent too.
3. Update the seam's row in the README's "Scaling path" table if what's "Now" changed.
