---
name: ls-backblaze
description: Safely plan and execute Backblaze B2 S3-compatible storage operations and B2 native bucket, key, and notification administration.
metadata:
  version: "1.1"
compatibility: "Python 3.12+. S3 execution requires the separately installed, pinned s3-sdk dependency export; plans, help, schemas, and native B2 administration use only the standard library."
---

# Backblaze B2 storage

`scripts/backblaze.py` is a standalone JSON CLI. It deliberately contains its
own package under `scripts/lib/ls_backblaze`: an installed optional skill must
not depend on a LocalSetup checkout, LocalSetup wheel, or another skill.

Use `--tool`, and exactly one of `--args-json` or `--args-file` (`-` reads
stdin). Without `--apply`, every valid request returns a zero-network plan.
`--schema` and `--capabilities` are also offline. Requests never contain raw
credentials; apply-mode configuration refers to credentials by `{ "env":
"NAME" }` or `{ "file": "/protected/path" }`.

```bash
python3 scripts/backblaze.py --tool s3.ListObjectsV2 \
  --args-json '{"bucket":"example","prefix":"reports/"}'
python3 scripts/backblaze.py --tool native.ListBuckets --args-json '{}' \
  --config b2-config.json --apply
```

Install the caller-owned SDK environment from `requirements-s3-sdk.txt`; the
tool never installs packages. S3 credentials are explicit and SDK discovery,
metadata lookup, and shell credential processes are disabled. Native requests
require HTTPS, validate official B2 endpoints, do not follow redirects, and
use bounded safe-read retries. Mutations are sent once: a lost or malformed
response is reported as `unknown` with a read-only reconciliation operation.

Dangerous requests require `--allow-destructive`, access changes require
`--allow-access-change`, public ACLs require `--allow-public`, and replacement
uploads/copies require `--allow-overwrite`. The operation matrix documents
supported fields, capabilities, retry class, and intentionally unsupported
features. Object-name deletion creates a delete marker; permanent version
deletion requires `version_id` and the destructive flag.

Secrets returned by native key creation are delivered only to a newly reserved
0600 output file and are never included in JSON output. Presigned URLs are
sensitive result values. Multipart checkpoints are private 0600 files and
resume only after source and remote-part reconciliation.

## Install and configure

Create a caller-owned environment explicitly; the hashed requirements file is
exported from LocalSetup's authoritative `s3-sdk` lock group. It is identical to
the export in the Garage skill, but neither skill imports the other.

```bash
python3 -m venv /path/to/b2-venv
/path/to/b2-venv/bin/python -m pip install --require-hashes -r requirements-s3-sdk.txt
/path/to/b2-venv/bin/python scripts/backblaze.py --schema request
python3 scripts/backblaze.py --schema result
```

An example configuration contains references, never credential literals:

```json
{
  "s3": {
    "endpoint": "https://s3.us-west-004.backblazeb2.com",
    "region": "us-west-004",
    "access_key_id": {"env": "B2_S3_KEY_ID"},
    "secret_access_key": {"file": "/protected/b2-s3-key"}
  },
  "native": {
    "endpoint": "https://api.backblazeb2.com",
    "key_id": {"env": "B2_NATIVE_KEY_ID"},
    "application_key": {"file": "/protected/b2-native-key"}
  },
  "request_budget_seconds": 300
}
```

Choose the S3 endpoint for your B2 account's region. This CLI currently requires
its configured endpoint and signing region to match. Backblaze's [regional
guide](https://www.backblaze.com/docs/en/cloud-storage-get-started-with-a-backblaze-integration)
and [AWS CLI presign example](https://www.backblaze.com/docs/cloud-storage-use-the-aws-cli-with-backblaze-b2)
show a `us-west-004` endpoint with a `us-east-1` signing scope in the latter,
so matching is a local CLI restriction, not a verified universal B2 requirement.
Live provider qualification has not been performed.
Only the section used by the operation is required. Protected files must be
owned by the caller, regular, mode `0600`, at most 64 KiB, and reached without
symlinks. Credential discovery, instance metadata and credential subprocesses
are not used. An optional `ca_bundle` names a trusted PEM bundle; verification
cannot be disabled. Only official HTTPS B2 API endpoints on port 443 are accepted,
including the API URL returned by account authorization.

Every invocation emits one JSON envelope with `schema_version`, `operation`,
`ok`, `outcome`, and either a typed `result` or sanitized `error`. Exit codes are
`0` for success/plan, `2` for input/configuration/unsupported operation/missing
SDK, `3` for a policy rejection, `4` for a known failure, `5` for a partial or
unknown outcome, and `130` for interruption. An interruption during a mutation
may leave its outcome unknown. Do not infer failure from a lost response.

## Transfers and recovery

Use `s3.PutObject` with a local `source` for a streamed single request, including
empty files. `s3.GetObject` requires a local `destination`; it streams into a
same-directory temporary file, verifies content length, and verifies a complete
provider SHA256 checksum when supplied. Composite checksums are reported without
claiming whole-file verification. ETags, particularly multipart ETags, are never
represented as whole-file hashes.

Download publication is exclusive by default. The request argument
`"overwrite": true` preserves an existing regular file in a private, same-directory
recovery directory and creates an independent byte copy at
`<destination>.backblaze-backup`; for a maximum-length basename, the backup uses a
bounded `.backblaze-backup-<16 hex>` name instead. The result always includes the
backup path. Set `"include_recovery_path": true` to also return the private recovery
directory; this field is opt-in so existing strict result-v1 consumers keep their
current result shape. Keep both paths until recovery is no longer needed. An
existing backup or a symlink causes rejection. Publication briefly leaves the
destination path absent and uses an exclusive create so a concurrent entry is
never overwritten. Writes through an already-open descriptor continue on the
displaced file in the recovery directory.
Detected source changes stop publication, but no portable local operation can
guarantee a coherent backup snapshot while a non-cooperating process writes the
file during copying. Keep or move both recovery artifacts explicitly before
another overwrite. Upload/copy/completion replacement authority is the CLI flag
`--allow-overwrite`, not a JSON request field. B2 retains prior versions subject
to lifecycle and retention settings; a delete marker does not erase historical
versions, and prior-version recovery is not guaranteed after permanent deletion.

For multipart uploads, choose `s3.UploadFileMultipart` with `source`, `bucket`,
`key`, and a new `checkpoint` path. This CLI accepts `part_size` from 5 MiB
through 5 GiB and reads request bodies at most 1 MiB at a time; the size range is
the local workflow's limit, not a claim about every B2 S3 multipart client. At
most 10,000 parts are allowed.
The checkpoint binds the provider, credential identity, destination, source
inode/timestamps/size/SHA256, upload ID, encryption fingerprint and confirmed
parts. The source must remain unchanged throughout upload.

`s3.ResumeMultipartUpload` accepts the same source/destination/checkpoint and,
when applicable, the same encryption reference. It first reconciles every
remote part with the checkpoint. A mismatch, unrecorded remote part, or a
checkpoint in `initializing`, `completing`, `completed`, or `source_changed`
state requires explicit read-only reconciliation. It never restarts, completes
again, or aborts automatically. Use `ListParts`, `ListMultipartUploads`, and
`HeadObject` to determine actual state before choosing a new action. A sidecar
`<checkpoint>.lock` prevents overlapping local writers. After a crash, verify
that the owner stopped and reconcile remote state before removing that lock.

SSE-C uses an explicitly referenced, base64-encoded 32-byte key:

```json
{"algorithm":"SSE-C","key":{"file":"/protected/sse-c-key"}}
```

The compatibility form `{"algorithm":"SSE-C","key_env":"B2_SSE_C"}` also
works. SSE-B2 uses `"AES256"` or `{"algorithm":"AES256"}`. Source and
destination copy encryption are separate fields. Keep customer keys outside
checkpoints; losing a customer key makes encrypted content unrecoverable.

## Native administration and troubleshooting

Native account authorization returns capability and scope information, with
the token redacted. Operations check required capabilities before mutation.
Bucket names are case-insensitive; native operations accept the documented
mixed-case names, while S3 requests require lowercase interoperable names.
Bucket creation fixes the name; updates require `if_revision_is` and at least
one explicitly selected field. Collections such as CORS, lifecycle and bucket
information replace their complete corresponding collection. Enabling Object
Lock is irreversible; default retention changes apply to future writes.

Backblaze documents [`defaultServerSideEncryption.mode: null`](https://www.backblaze.com/apidocs/b2-update-bucket)
as resetting the bucket default to SSE-B2/AES256 and
[`defaultRetention.mode: null`](https://www.backblaze.com/docs/cloud-storage-enable-object-lock-with-the-native-api)
as disabling default retention. This CLI's closed request schema still rejects
those null forms. Backblaze's [always-on encryption](https://www.backblaze.com/blog/backblaze-b2-to-encrypt-new-uploads-by-default/)
applies to new buckets, while existing buckets receive it gradually. Once enabled,
new writes receive SSE-B2 unless SSE-C is requested, and server-side encryption
cannot be disabled. S3
[`DeleteBucketEncryption`](https://www.backblaze.com/apidocs/s3-delete-bucket-encryption)
clears explicit bucket configuration; it does not disable effective encryption.
Neither account signup/billing nor a second native object-transfer stack is
included.

The provider supports S3 lifecycle Get/Put/Delete ([supported lifecycle
features](https://www.backblaze.com/apidocs/s3-put-lifecycle-configuration))
and bucket policy operations, but this CLI does not expose those S3 operations.
Lifecycle fields remain available through the native bucket operations. If S3
lifecycle APIs are used outside this CLI, manage rules through that API surface
only: Backblaze's [native update reference](https://www.backblaze.com/apidocs/b2-update-bucket)
warns that web-console or native lifecycle edits regenerate S3 rule IDs.
Bucket-policy operation availability is phased by Backblaze; check the
[IAM/STS API reference](https://www.backblaze.com/docs/cloud-storage-iam-sts-api).

Notification updates replace the complete rule set. `customHeaders` is a map
from header name to protected reference in this CLI and is serialized to the
native array of `{name,value}` pairs. There may be at most ten headers and the
resolved URL-encoded representation is limited to 2,048 bytes. HMAC references
must resolve to exactly 32 alphanumeric characters. Webhooks require HTTPS,
cannot target Backblaze or literal IP addresses, and rules for matching event
types cannot have overlapping object prefixes. Ignored provider fields such as
`isSuspended` and `suspensionReason` reject locally.
Event Notifications must first be enabled for the account through Backblaze
Support when access has not already been granted; see the [feature setup
guide](https://www.backblaze.com/docs/cloud-storage-event-notifications). A
bucket can have at most 25 rules ([reference](https://www.backblaze.com/docs/cloud-storage-event-notifications-reference-guide)).

Key creation reserves a new `secret_output` file before the remote create. If
creation succeeds but secret delivery fails, the result identifies the created
key and gives reconciliation instructions. It never recreates or automatically
revokes the key. `native.DeleteKey` is an explicit destructive operation.

Safe HTTP/SDK reads have at most three attempts per request with bounded exponential delay,
a capped `Retry-After`, five-second connection timeout, sixty-second read timeout,
and a shared request budget of at most 300 seconds. A native safe read may
refresh an expired token once within those attempts and the same budget. A native
invocation has a shared ceiling of nine sends: up to three for initial authorization,
three for the selected safe operation (including the expired-token attempt), and
three for its one refresh authorization. Standalone authorization has at most
three sends. A mutation is sent once and uses at most four sends including
authorization.
Mutations never retry automatically; gateway errors and lost responses may be
`unknown`. Listing operations expose continuation state; object-list helpers
accept `max_pages` and detect missing/repeated tokens. Other lists return one
provider page for an explicit next call.

Offline acceptance covers schemas, SDK serialization, native HTTP fixtures,
secret handling, transfers and independent materialization. Live Backblaze
qualification has not been performed. The opt-in live smoke helper is read-only
and requires explicit caller configuration and `--apply`; use a disposable test
account for any separate live mutation qualification.
