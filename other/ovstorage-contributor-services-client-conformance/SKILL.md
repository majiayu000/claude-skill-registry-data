---
name: ovstorage-contributor-services-client-conformance
description: Use when checking the Storage API wire contract that ovstorage-plugin-services-client depends on.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, services, conformance]
tools: [Read, Bash]
compatibility: Requires the ovstorage-services conformance suite, Python and Poetry, and a local or deployed Storage API service. Deployment credentials are user-supplied.
---

# Services-client conformance check

The Omniverse Storage API ships its own pytest-bdd conformance
suite (Gherkin features, executed via the `run-conformance-tests` Poetry
script). In the root ovstorage repo, use it to check the wire contract that
`ovstorage-plugin-services-client/` depends on: after a vendor-sync, before
relying on a deployed Omniverse Storage Service endpoint, or when investigating whether a
services-client failure is caused by server/API drift.

This is not the service implementation or Kubernetes deployment runbook. For
service-stack deployment and operations, use the `ovstorage-services` routing
in a source checkout.

## When to run

- After a vendor-sync of `ovstorage-services/` (the canonical contracts
  or the suite itself may have moved).
- Against a deployed Omniverse Storage Service server before depending on it from the
  services-client plugin.
- Periodically against the reference filesystem implementation to
  smoke-test the suite itself.

## How to run

The suite is a black-box pytest run against a separately-running
Storage API service. It does NOT boot an in-process server — you
start one first, then point the suite at it.

```bash
cd ovstorage-services/apis/storage-api/conformance_tests

# One-time setup
python -m venv .poetry_venv
.poetry_venv/bin/pip install poetry
.poetry_venv/bin/poetry install
source .venv/bin/activate

# In a second terminal: start the reference Storage API service
local-filesystem-service filesystem --static-dir /tmp/storage
# Default endpoints: REST http://localhost:8011, gRPC localhost:50051

# Back in the first terminal: run the suite
run-conformance-tests
```

`run-conformance-tests` is a Poetry-script entrypoint installed by
`poetry install`. It wraps `pytest` and pre-loads the default
`storageapi_testdata_generator` plugin; any extra args pass through to
pytest, e.g. `run-conformance-tests -k stat -vv`.

To target a deployed server instead of the reference filesystem,
override the endpoints via environment variables before running:

- `TEST_STORAGE_API_REST_ENDPOINT` (default `http://localhost:8011`)
- `TEST_STORAGE_API_GRPC_ENDPOINT` (default `localhost:50051`)
- `TEST_STORAGE_API_RESOURCE_BASE` (default `file-storage://fileservice`)

The suite's own
[`README.md`](../../ovstorage-services/apis/storage-api/conformance_tests/README.md)
covers the alternative `boto3` test-data generator and the OpenAPI
schema-diff hooks.

## What it covers

The suite's Gherkin features live under
`conformance_tests/src/conformance_tests/features/`. The current
coverage areas are:

- `capabilities/` — `ListTopLevelAddresses` responses and capability
  discovery.
- `filefolder/` (v1alpha + v1beta) — folder creation, `ListStat`,
  delete-folder semantics.
- `fileobject/` (v1alpha + v1beta) — `Stat`, `ReadFromAddress`,
  `Write`, `Copy`, `Delete`, `FetchWriteTypeInfo`.
- `metadata/v1alpha` — `GetMetadata` / `UpdateMetadata`.
- `versioning/v1beta` — `EnumerateVersions`.

Watches (`EventConsumerService`) and ACL-specific behavior are NOT
covered by this suite today.

## Interpreting failures

A test failure either (a) flags a real plugin/server bug, or (b)
indicates the conformance suite has been updated and the
implementation under test hasn't caught up. The pytest output names
the scenario; read the matching `.feature` and step-definitions under
`conformance_tests/src/conformance_tests/features/` for the expected
behavior.

## Related reading

- Plugin user reference:
  [`docs/public/plugin-storage/plugin-services-client.md`](../../docs/public/plugin-storage/plugin-services-client.md)
- Plugin internals:
  [`ovstorage-services-client/ovstorage-plugin-services-client/README.md`](../../ovstorage-services-client/ovstorage-plugin-services-client/README.md)
- Suite's own configuration reference:
  [`ovstorage-services/apis/storage-api/conformance_tests/README.md`](../../ovstorage-services/apis/storage-api/conformance_tests/README.md)
