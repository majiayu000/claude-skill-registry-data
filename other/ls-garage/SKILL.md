---
name: ls-garage
description: Operate the documented Garage v2.3.0 Admin API allowlist and S3 subset through an offline-first, JSON-only CLI.
---

# Garage

Use `scripts/garage.py` for one validated JSON operation at a time. Plans are
the default, validate a supplied configuration shape without resolving its
credentials, and never contact a service. `--apply` is the only network switch
and requires an explicit JSON configuration file.

```bash
python3 scripts/garage.py --tool s3.ListBuckets --args-json '{}'
python3 scripts/garage.py --tool admin.GetClusterHealth --args-json '{}' --apply --config garage.json
```

The runtime supports the documented S3 operations listed in
[OPERATION_MATRIX.md](OPERATION_MATRIX.md), path-style SigV4 endpoints, and
the pinned Garage Admin API v2.3.0 schema projection. Its original official
source has SHA-256 `07ffb2d0febbf386747eed0232b1a97931d323182f11e77537519620e6eb10d8`;
the projection records separate source provenance. This is schema-tested
compatibility, not qualification of every Garage deployment.
It never imports another provider's skill.

The pinned Admin API projection and upstream attribution are described in
[references/NOTICE.md](references/NOTICE.md). The projection and notice retain
their source-specific AGPL-3.0 provenance; this skill does not relabel those
upstream assets.

## Standalone runtime setup

Use Python 3.12 or newer. The thin entrypoint loads this skill's own package
under `scripts/lib/ls_garage`; configuration, validation, transport, storage,
transfers, and reporting have separate modules. This package-local boundary
lets an independently installed skill run without the LocalSetup distribution,
a source checkout, or the Backblaze skill.

Help, schemas, plans, and Admin operations use the standard library. S3 calls
require the audited, pinned SDK export supplied in `requirements-s3-sdk.txt`.
Create or select a caller-owned environment from the installed skill directory:

```bash
uv venv /path/to/garage-venv --python python3.12
uv pip install --python /path/to/garage-venv/bin/python --require-hashes \
  -r requirements-s3-sdk.txt
/path/to/garage-venv/bin/python scripts/garage.py --capabilities
```

The tool never installs packages automatically. A missing SDK returns
`dependency_missing` with exit 2; install the hashed export in the interpreter
you selected. Avoid modifying an unrelated application's environment.

## Safety contract

All input and output is JSON. Use `--schema request`, `--schema result`, and
`--capabilities` without credentials or network access. Every response is a
versioned envelope; transport headers, tokens, and secret keys are excluded
from ordinary output. Normal key IDs are returned when they identify a change.

`--allow-destructive` is required for deletes and multipart aborts.
`--allow-access-change` is required for bucket/key permissions and S3 website,
CORS, or lifecycle changes. `--allow-overwrite` is required for writes that
can replace an object: put, post, copy, multipart completion/high-level
uploads/resume, and presigned PUT/POST. Garage does not document conditional
no-clobber guarantees, so requests that require one are rejected locally.
`--allow-public` is required when a website is enabled because it can publish
bucket content.

The CLI does not implement versions, object lock, retention, legal holds, S3
ACLs/policies, provider-managed/default encryption, or recovery from a prior
version. SSE-C is supported only through explicit protected references; it is
not default server-side encryption.

## Configuration

Configuration has separate `s3` and `admin` sections. Credentials use exactly
one `{ "env": "NAME" }` or protected mode-0600 owned regular file reference
`{ "file": "/path", "field": "optionalJsonField" }`. HTTPS is mandatory.
An explicit `allow_loopback_http: true` permits only literal `127.0.0.1` or
`::1` HTTP endpoints for local tests. TLS verification remains enabled; an
optional `ca_bundle` supplies a private CA.

```json
{
  "s3": {
    "endpoint": "https://garage.example",
    "region": "garage",
    "access_key_id": {"env": "GARAGE_ACCESS_KEY"},
    "secret_access_key": {"file": "/secure/garage-secret"},
    "addressing_style": "path"
  },
  "admin": {
    "endpoint": "https://garage-admin.example",
    "token": {"file": "/secure/admin-token"}
  }
}
```

The client uses one 300-second total budget, five-second connection timeout,
60-second read timeout, no redirects, at most three attempts for safe reads,
and no hidden SDK retry or mutation replay. A missing mutation response is
`unknown`; reconcile with the named read operation before taking further
action.

## Secret restoration and delivery

`admin.GetKeyInfo` always sends `showSecretKey=false`. A `CreateKey` response
is delivered only to the `secret_output` protected mode-0600 file supplied by
the request; ordinary JSON output contains no secret. If durable delivery
fails after creation, the result identifies the created key ID and requires
reconciliation. `admin.ImportKey` accepts only
`{"restore_existing":true,"restore_file":{"file":"..."}}`; the protected
export file must contain the existing key ID, secret, and name.

Unencrypted presigned GET/PUT URLs and POST forms are sensitive intended output.
All SSE-C presigns require an exclusive `secret_output` file. Encrypted GET/PUT
write `{url, headers}` there, so the recipient can supply every signed customer
header; encrypted POST writes `{url, fields}` including its policy. Normal JSON
returns only the protected path, sensitivity flag, and expiration. The encoded
POST policy also contains the customer key and must stay in that file.


## Update semantics

For Admin `UpdateBucket`, outer `null` values are rejected because Garage
treats them as unchanged. Use `corsRules: []` or `lifecycleRules: []` to
clear those settings. Clear both quotas with
`{"maxObjects":null,"maxSize":null}`. `websiteAccess:{"enabled":false}`
clears website settings. Permission changes must contain explicitly `true`
flags; false values are rejected because Garage silently ignores them.

SSE-C multipart applies the three customer headers to creation, every upload
part, list-parts, and completion. Garage's completion validation is conditional
in its tagged v2.3.0 implementation, but the client consistently sends the
configured headers.

## Transfers, results, and troubleshooting

`GetObject` requires a local `destination`; it streams into a temporary file
in that directory and publishes only after length and available checksum
verification. The default is no-clobber, including a concurrent new destination.
`overwrite:true` preserves the prior regular file in an exclusive
`.garage-backup` before atomic replacement. An existing backup or any destination
symlink is a local rejection. Keep that backup until the downloaded data is accepted.

`UploadFileMultipart` requires `source` and `checkpoint`; `part_size` defaults
to 5 MiB. Checkpoints bind provider, endpoint, region, credential identity,
bucket, key, source inode/stat/SHA-256, upload ID, encryption fingerprint, and
confirmed parts. `ResumeMultipartUpload` reconciles remote parts and source
identity before any new part. It refuses uncertain initialization or completion,
changed sources, and inconsistent parts; preserve the checkpoint and use
`ListParts`, `ListMultipartUploads`, or `HeadObject` before another action.
There is no automatic restart, abort, bucket emptying, or prior-version recovery.

Results report actual content length, available checksum evidence, and assurance.
Multipart ETags are not whole-file checksums. Garage results do not promise a
recoverable prior version. Batch deletion returns each failed member and distinguishes
partial success, total known failure, and incomplete/unknown responses.

Use `--args-file request.json` or `--args-file -` instead of `--args-json` when
reading a request file or stdin. Only one source is accepted; arguments are
bounded to 1 MiB. Unknown fields, unsupported lifecycle/website options, and
conditional no-clobber requirements reject locally. Object keys remain opaque.

| Exit | Meaning and next step |
| --- | --- |
| 0 | Local plan or confirmed success. |
| 2 | Invalid arguments/configuration, unsupported feature, or missing SDK; inspect the schema or configuration. |
| 3 | Missing operation authorization flag or unsafe local output; review the existing owner's scope and selected path. |
| 4 | Known service/read failure; inspect retryability and the configured endpoint/capabilities. |
| 5 | Partial or unknown mutation; perform the returned read-only reconciliation before any retry. |
| 130 | Interruption; preserve checkpoints and reconcile any mutation whose dispatch may have begun. |

Offline acceptance exercises SDK serialization, the pinned Admin schema, retries,
secret delivery, transfer recovery, and independent installed imports. Live
Backblaze/Garage provider qualification remains unperformed. To separately run
read-only live smoke checks with explicit authority and credentials, invoke
`scripts/garage_live_smoke.py --apply --config garage.json`; add `--bucket NAME`
for `HeadBucket` or `--admin-health` for the separately configured health endpoint.
This smoke script does not perform live mutation qualification.
