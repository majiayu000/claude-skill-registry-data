---
name: swap-storage
description: Point file storage somewhere other than the in-cluster RustFS or production's GCS (another S3-compatible server or service) or add one without an S3 API. Use when the user decides to change where uploads live. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Swap object storage

- **Interface:** `Storage` (presigned upload and download URLs, `head`, `read`, `write`,
  `move`, `delete`, `directUri`) in `packages/nest-common/src/storage.ts`.
- **Today:** `STORAGE_PROVIDER` chooses between `S3Storage` (RustFS locally and in kind,
  from the data chart, or any other S3 API: AWS S3, R2, GCS's XML API with HMAC keys,
  Azure behind an S3 gateway) and `GcsStorage` (production's bucket, GCS's own JSON API,
  Application Default Credentials, no key file), both built by `createStorage(env)` in
  the same file (null when the chosen provider's bucket is unset: uploads are off).
  `storageBucket`/`filesEnabled` beside it are the one answer to "are files on", for
  `createStorage`, the api's features and the worker's boot checks; they throw on a
  half-configured provider.
- **Provided as** `STORAGE` in `apps/api/src/modules/files/files.module.ts` (signs
  uploads) and `apps/worker/src/files/files.module.ts` (checks and moves them).
- **Env:** `STORAGE_PROVIDER`; `S3_BUCKET`, `S3_REGION`, `S3_ENDPOINT`,
  `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`, `S3_FORCE_PATH_STYLE`; `GCS_BUCKET`
  (`storageEnv` in `packages/nest-common/src/env.ts`); `STORAGE_ORIGIN` for the web
  app's CSP (`https://storage.googleapis.com` for `gcs`).

## Another S3-compatible provider

No code: set the `S3_*` variables for api and worker (their SOPS Secrets, in place of the
data chart's `storage` Secret), `STORAGE_ORIGIN` for web, and give the bucket a CORS rule
allowing `PUT` and `GET` from the site's origin (browsers upload directly; see `s3-init`
in `docker-compose.yml` and the data chart's bucket Job). Everything is self-hosted on
purpose: check with the user before moving uploads to a managed service.

## Another GCS bucket, or GCS in another environment

Set `STORAGE_PROVIDER=gcs` and `GCS_BUCKET` for api and worker with `storage: none` (no
`S3_BUCKET`: it's refused beside `gcs`), `STORAGE_ORIGIN=https://storage.googleapis.com`
for web (also `storage: none`), give the stack chart's `allowMetadataServer: true` to
every service that calls `createStorage` (egress to the metadata server, otherwise
unreachable like the rest of `networkPolicy.privateRanges`),
and give the bucket `roles/storage.objectAdmin` and, on itself,
`roles/iam.serviceAccountTokenCreator` for the running identity (a GCE VM's service
account, a GKE pod's workload identity): `getSignedUrl` needs the IAM Credentials API's
`signBlob` when Application Default Credentials have no private key to sign with, which
is every identity but a downloaded key file. CORS on the bucket itself, same as above.

## A provider with neither API

1. A class implementing `Storage`. Presigned uploads must bind content type and length
   so a client can't upload something else; `read` must refuse objects over `maxBytes`
   without buffering them, and read the very version whose size it checked; `directUri` returns null unless
   another service in the same project can read the object with its own credentials.
2. Choose it in `createStorage` from a new variable in `storageEnv`, documented in
   `.env.example` and `docs/environment.md`. Callers don't change.

## Tests

`packages/nest-common/src/storage.test.ts` covers `GcsStorage` with a fake
`@google-cloud/storage` client (`GcsClientLike`, narrower than the real SDK so a test
can implement just what's called), and its signed URLs with the real client and a key
made up inside the test (signing is local, so offline); `packages/nest-common/test/storage.integration.test.ts`
runs `S3Storage` against RustFS (`bun run test:integration` starts it; there's no local
GCS to run an equivalent integration suite against). The upload flow is covered in
`apps/api/test/api.integration.test.ts`, the worker's `uploads` tests in
`apps/worker/test/worker.integration.test.ts`, and `apps/web/e2e/avatar.spec.ts` — all
against RustFS too, so a change that only `GcsStorage` makes needs its own unit test.

## Finish

1. The verify skill.
2. Ask the `reviewer` agent to review the change, and the `security-reviewer` agent: a
   new implementation brings its own credentials and sends data somewhere new. If you
   wrote a migration, the `migration-reviewer` agent too.
3. Update the seam's row in the README's "Scaling path" table if what's "Now" changed.
